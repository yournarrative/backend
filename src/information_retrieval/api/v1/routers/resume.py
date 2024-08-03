from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile

from information_retrieval.api.v1.models.activity import Activity
from information_retrieval.api.v1.models.resume import (
    ParseResumeAndReturnActivitiesRequest,
    ParseResumeAndReturnActivitiesResponse,
)
from information_retrieval.api.v1.processing.ai.resume_to_activities import create_activities_from_resume_ai
from information_retrieval.api.v1.processing.extraction.pdf import extract_text_from_pdf
from information_retrieval.core.logger import app_logger as logger

router = APIRouter()


parse_resume_and_return_activities_endpoint = "/v1/resumes/uploadResumeAndReturnActivities/"


def parse_upload_resume_request_data(
    user_id: Annotated[str, Form(...)],
) -> ParseResumeAndReturnActivitiesRequest:
    return ParseResumeAndReturnActivitiesRequest(user_id=user_id)


@router.post(parse_resume_and_return_activities_endpoint)
async def parse_resume_and_return_activities(
    file: UploadFile = File(...),
    data: ParseResumeAndReturnActivitiesRequest = Depends(parse_upload_resume_request_data),
    request: Request = None,
) -> ParseResumeAndReturnActivitiesResponse:
    logger.debug(f"New request to {parse_resume_and_return_activities_endpoint} endpoint: {data}")

    # Validate file type
    # TODO: Add "application/vnd.openxmlformats-officedocument.wordprocessingml.document" later
    if file.content_type not in ["application/pdf"]:
        raise HTTPException(status_code=400, detail="Invalid file type")

    content: bytes = await file.read()

    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        text = extract_text_from_pdf(BytesIO(content))
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        raise HTTPException(status_code=500, detail="Error processing PDF file")

    activities = []

    try:
        activities: list[Activity] = create_activities_from_resume_ai(content=text)
    except Exception as e:
        logger.error(f"Error turning resume text into activities list: {e}")
        raise HTTPException(status_code=500, detail="Error processing PDF file")

    return ParseResumeAndReturnActivitiesResponse(activities=activities)
