from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, HTTPException, UploadFile, Response, BackgroundTasks
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

from interview_analyzer.api.api_v1.convert.endpoint import convert_audio_filetype
from interview_analyzer.api.api_v1.email.endpoint import send_email
from interview_analyzer.api.api_v1.enrich.endpoint import enrich_transcript
from interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from interview_analyzer.api.api_v1.feedback.endpoint import question_answer_feedback
from interview_analyzer.api.api_v1.feedback.model import QuestionAndAnswerWithFeedback
from interview_analyzer.api.api_v1.interview.model import Interview
from interview_analyzer.api.api_v1.transcribe.model import SimpleTranscript
from interview_analyzer.api.api_v1.transcribe.endpoint import transcribe_upload_file_speech_to_text, \
    transcribe_bytes_file_speech_to_text
from interview_analyzer.app_lifespan_management import init_app_state, cleanup_app_state
from interview_analyzer.connectors.rds import crud
from interview_analyzer.connectors.s3.crud import read_file_from_s3, upload_file_to_s3
from interview_analyzer.connectors.s3.schema import ProcessS3Request
from interview_analyzer.utils.files import cleanup_temp_file
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_app_state(app.state)
    yield
    await cleanup_app_state(app.state)


app = FastAPI(title="Ghosted", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def health_check():
    return "I'm healthy, yo!"


# @app.post("/api-v1/transcribe/audioToSimpleTranscript/", response_model=SimpleTranscript)
# async def return_speech_to_text_single(file: UploadFile, request: Request):
#     logger.debug(f"Received request to transcribe audio to text - {file.filename}")
#     try:
#         transcript: SimpleTranscript = await transcribe_upload_file_speech_to_text(audio_file=file, state=request.app.state)
#         return transcript
#     except Exception as e:
#         logger.error(e)
#         return HTTPException(status_code=500)
#
#
# @app.post("/api-v1/enrich/audioToEnrichedTranscript/", response_model=EnrichedTranscript)
# async def return_speech_to_text(file: UploadFile, request: Request):
#     logger.debug(f"Received request to transcribe audio to text - {file.filename}")
#     try:
#         transcript: SimpleTranscript = await transcribe_upload_file_speech_to_text(
#             audio_file=file, state=request.app.state
#         )
#         enriched_transcript: EnrichedTranscript = await enrich_transcript(transcript=transcript, state=request.app.state)
#         return enriched_transcript
#     except Exception as e:
#         logger.error(e)
#         return HTTPException(status_code=500)


async def _convert_audio_file_type(data: ProcessS3Request, request: Request):
    try:
        audio_file_bytes = read_file_from_s3(request.app.state.s3_connector, data.bucket, data.key)
        output_filepath: str = await convert_audio_filetype(
            file_bytes=audio_file_bytes, filename=data.key, output_filetype="mp3",
        )
        upload_filepath = "/".join(data.key.split("/")[0:-1]) + '/' + output_filepath.split("/")[-1]
        upload_file_to_s3(
            s3=request.app.state.s3_connector,
            local_filepath=output_filepath,
            upload_key=upload_filepath,
            bucket_name=data.bucket,
        )
        cleanup_temp_file(output_filepath)
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


@app.post("/api-v1/convert/convertAudio/")
async def convert_audio_file_type(data: ProcessS3Request, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(_convert_audio_file_type, data, request)
    return Response(status_code=200)


async def _process_s3_file_into_rds(data: ProcessS3Request, request: Request):
    try:
        audio_file = read_file_from_s3(request.app.state.s3_connector, data.bucket, data.key)
        transcript: SimpleTranscript = transcribe_bytes_file_speech_to_text(
            audio_file=audio_file,
            filename=data.key,
            state=request.app.state,
        )
        enriched_transcript: EnrichedTranscript = await enrich_transcript(
            transcript=transcript,
            state=request.app.state,
        )
        analysis: List[QuestionAndAnswerWithFeedback] = await question_answer_feedback(
            enriched_transcript=enriched_transcript,
            state=request.app.state,
        )
        interview = Interview(enriched_transcript=enriched_transcript, analysis=analysis)
        interview_uuid = await crud.get_interview_id_from_rds_using_s3_path(
            async_session=request.app.state.database_access_layer.async_session,
            s3_bucket=data.bucket,
            s3_key=data.key
        )
        await crud.update_interview_with_interview_object(
            async_session=request.app.state.database_access_layer.async_session,
            interview_uuid=interview_uuid,
            interview=interview,
        )
        if data.send_email_when_finished:
            email_address: str = await crud.get_email_from_rds_using_interview_uuid(
                async_session=request.app.state.database_access_layer.async_session,
                interview_uuid=interview_uuid
            )
            await send_email(
                interview=interview,
                email_to=email_address,
                state=request.app.state
            )
        return Response(status_code=200)
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


# Entrypoint for the S3 triggered Lambda function
@app.post("/api-v1/process/audioFileToDatabaseUpdate/")
async def process_s3_file_into_rds(data: ProcessS3Request, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(_process_s3_file_into_rds, data, request)
    return Response(status_code=200)


if __name__ == "__main__":
    uvicorn.run(app)
