import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

from interview_analyzer.api.api_v1.enrich.endpoint import enrich_transcript
from interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from interview_analyzer.api.api_v1.shared.model import SimpleTranscript
from interview_analyzer.api.api_v1.transcribe.endpoint import transcribe_speech
from interview_analyzer.app_lifespan_management import init_app_state, cleanup_app_state
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


@app.post("/api-v1/transcribe/audioToSimpleTranscript/", response_model=SimpleTranscript)
async def return_speech_to_text_single(file: UploadFile, request: Request):
    logger.debug(f"Received request to transcribe audio to text - {file.filename}")
    try:
        transcript: SimpleTranscript = await transcribe_speech(audio_file=file, state=request.app.state)
        return transcript
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


@app.post("/api-v1/enrich/simpleTranscriptToEnrichedTranscript/", response_model=EnrichedTranscript)
async def return_speech_to_text(transcript: SimpleTranscript, request: Request):
    logger.debug(f"Received request to transcribe simple transcript to text - {transcript.utterances[3]}")
    try:
        enriched_transcript: EnrichedTranscript = await enrich_transcript(transcript=transcript, state=request.app.state)
        return enriched_transcript
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


@app.post("/api-v1/enrich/audioToEnrichedTranscript/", response_model=EnrichedTranscript)
async def return_speech_to_text(file: UploadFile, request: Request):
    logger.debug(f"Received request to transcribe audio to text - {file.filename}")
    try:
        transcript: SimpleTranscript = await transcribe_speech(audio_file=file, state=request.app.state)
        logger.debug("HELLO 123")
        logger.debug(transcript)
        enriched_transcript: EnrichedTranscript = await enrich_transcript(transcript=transcript, state=request.app.state)
        return enriched_transcript
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


# @app.post("/api-v1/questionAnswerFeedback/", response_model=QuestionAnswerFeedback)
# async def return_question_answer_feedback(endpoint_input: QuestionAndAnswer, request: Request):
#     logger.debug(f"Received request to provide feedback on question and answer - {endpoint_input}")
#     try:
#         result: QuestionAnswerFeedback = await question_answer_feedback(
#             question=endpoint_input.question,
#             answer=endpoint_input.answer,
#             state=request.app.state
#         )
#         return result
#     except Exception as e:
#         logger.error(e)
#         return HTTPException(status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host=os.getenv("HOST"), port=int(os.getenv("PORT")))
