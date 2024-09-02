from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, Response, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

from information_retrieval.api.v1.models.activity import Activity
from information_retrieval.api.v1.models.files import (
    GetProfilePictureRequest,
    GetResumeRequest,
    ParseExistingResumeRequest,
    ParseExistingResumeResponse,
    UploadProfilePictureRequest,
    UploadResumeRequest,
)
from information_retrieval.api.v1.processing.ai.resume_to_activities import create_activities_from_resume_ai
from information_retrieval.api.v1.processing.extraction.pdf import extract_text_from_pdf
from information_retrieval.api.v1.processing.extraction.utils import is_accepted_file_type, normalize_image
from information_retrieval.connectors.supabase.crud import get_file_from_object_storage, upsert_file_to_object_storage
from information_retrieval.core.logger import app_logger as logger

router = APIRouter()


upload_resume_endpoint = "/v1/files/uploadResume/"


def parse_upload_resume_request_data(
    user_id: Annotated[str, Form(...)],
) -> UploadResumeRequest:
    return UploadResumeRequest(user_id=user_id)


@router.post(upload_resume_endpoint)
async def upload_resume(
    file: UploadFile = File(...),
    data: UploadResumeRequest = Depends(parse_upload_resume_request_data),
    request: Request = None,
) -> Response:
    logger.debug(f"New request to {upload_resume_endpoint} endpoint: {data}")

    if not is_accepted_file_type(file.content_type, request.app.state.settings.config.get("RESUME_ACCEPTED_FILETYPES")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    content: bytes = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        await upsert_file_to_object_storage(
            supabase=request.app.state.supabase_client,
            bucket_name=request.app.state.settings.config.get("DOCUMENTS_BUCKET"),
            user_id=data.user_id,
            file_content=content,
            file_name="resume.pdf",
            file_content_type=file.content_type,
        )
    except Exception as e:
        logger.error(f"Error uploading resume to file storage: {e}")
        raise HTTPException(status_code=500, detail="Error uploading PDF file")
    else:
        logger.debug(f"Resume uploaded for user {data.user_id} successfully")
        return Response(status_code=200)


get_resume_endpoint = "/v1/files/getResume/"


@router.post(get_resume_endpoint)
async def get_resume(
    data: GetResumeRequest,
    request: Request = None,
) -> StreamingResponse:
    logger.debug(f"New request to {extract_activities_from_resume_endpoint} endpoint for user {data.user_id}")

    try:
        content: bytes = await get_file_from_object_storage(
            supabase=request.app.state.supabase_client,
            user_id=data.user_id,
            file_name="resume.pdf",
            bucket_name=request.app.state.settings.config.get("DOCUMENTS_BUCKET"),
        )
        file_stream = BytesIO(content)
    except Exception as e:
        logger.error(f"Error fetching resume for user {data.user_id} from file storage: {e}")
        raise HTTPException(status_code=500, detail="Error fetching requested resume from file storage")
    return StreamingResponse(
        file_stream,
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=resume.pdf"},
    )


extract_activities_from_resume_endpoint = "/v1/files/extractActivitiesFromResume/"


@router.post(extract_activities_from_resume_endpoint)
async def extract_activities_from_resume(
    data: ParseExistingResumeRequest,
    request: Request = None,
) -> ParseExistingResumeResponse:
    logger.debug(f"New request to {extract_activities_from_resume_endpoint} endpoint for user {data.user_id}")

    try:
        content: bytes = await get_file_from_object_storage(
            supabase=request.app.state.supabase_client,
            user_id=data.user_id,
            file_name="resume.pdf",
            bucket_name=request.app.state.settings.config.get("DOCUMENTS_BUCKET"),
        )
    except Exception as e:
        logger.error(f"Error fetching resume for user {data.user_id} from file storage: {e}")
        raise HTTPException(status_code=500, detail="Error fetching requested resume from file storage")

    try:
        text = extract_text_from_pdf(BytesIO(content))
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        raise HTTPException(status_code=500, detail="Error extracting text from resume")

    try:
        activities: list[Activity] = create_activities_from_resume_ai(content=text)
    except Exception as e:
        logger.error(f"Error turning resume text into activities list: {e}")
        raise HTTPException(status_code=500, detail="Error extracting activities from resume")

    return ParseExistingResumeResponse(activities=activities)


upload_profile_picture_endpoint = "/v1/files/uploadProfilePicture/"


def parse_upload_profile_picture_request_data(
    user_id: Annotated[str, Form(...)],
) -> UploadProfilePictureRequest:
    return UploadProfilePictureRequest(user_id=user_id)


@router.post(upload_profile_picture_endpoint)
async def upload_profile_picture(
    file: UploadFile = File(...),
    data: UploadProfilePictureRequest = Depends(parse_upload_profile_picture_request_data),
    request: Request = None,
) -> Response:
    logger.debug(f"New request to {upload_profile_picture_endpoint} endpoint: {data}")

    # Validate file type (only allow images)
    if not is_accepted_file_type(file.content_type, request.app.state.settings.config.get("IMAGE_ACCEPTED_FILETYPES")):
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Read the file content
    content: bytes = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        # Open the image and normalize it
        image = Image.open(BytesIO(content))

        # Convert the image to RGB mode if it's in P mode
        if image.mode == "P":
            image = image.convert("RGB")

        normalized_image_io = normalize_image(image)
        normalized_image_content = normalized_image_io.getvalue()

        # Store the normalized image in Supabase
        await upsert_file_to_object_storage(
            supabase=request.app.state.supabase_client,
            bucket_name=request.app.state.settings.config.get("PROFILE_PICTURE_BUCKET"),
            user_id=data.user_id,
            file_content=normalized_image_content,
            file_name="profile_picture.jpeg",
            file_content_type=file.content_type,
        )
    except Exception as e:
        logger.error(f"Error uploading image to file storage: {e}")
        raise HTTPException(status_code=500, detail="Error uploading image file")
    else:
        logger.debug(f"Image uploaded for user {data.user_id} successfully")
        return Response(status_code=200, content="Image uploaded successfully")


get_profile_picture_endpoint = "/v1/files/getProfilePicture/"


@router.post(get_profile_picture_endpoint)
async def get_profile_picture(
    data: GetProfilePictureRequest,
    request: Request = None,
) -> StreamingResponse:
    logger.debug(f"New request to {get_profile_picture_endpoint} endpoint for user {data.user_id}")

    try:
        content: bytes = await get_file_from_object_storage(
            supabase=request.app.state.supabase_client,
            user_id=data.user_id,
            file_name="profile_picture.jpeg",
            bucket_name=request.app.state.settings.config.get("PROFILE_PICTURE_BUCKET"),
        )
        file_stream = BytesIO(content)
    except Exception as e:
        logger.error(f"Error fetching profile picture for user {data.user_id} from file storage: {e}")
        raise HTTPException(status_code=500, detail="Error fetching requested profile picture from file storage")
    return StreamingResponse(
        file_stream,
        media_type="image/jpeg",
        headers={"Content-Disposition": "attachment; filename=profile_picture.jpeg"},
    )
