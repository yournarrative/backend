import json
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

from interview_analyzer.api.api_v1.feedback.endpoint import question_answer_feedback
from interview_analyzer.api.api_v1.feedback.model import QuestionAnswerFeedback, QuestionAndAnswer
from interview_analyzer.api.api_v1.speech_to_text.endpoint import LabelledTranscribedText, speech_to_text_multiple, \
    TranscribedText, speech_to_text_single
from interview_analyzer.app_lifespan_management import init_app_state, cleanup_app_state
from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_app_state(app.state)
    yield
    await cleanup_app_state(app.state)


app = FastAPI(title="Silver", lifespan=lifespan)

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


@app.post("/api-v1/audioToTextSingle/", response_model=TranscribedText)
async def return_speech_to_text_single(file: UploadFile, request: Request):
    logger.debug(f"Received request to transcribe audio to text - {file.filename}")
    try:
        result: TranscribedText = await speech_to_text_single(audio_file=file, state=request.app.state)
        return result
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


@app.post("/api-v1/audioToTextSingleWithPreviousFeedback/", response_model=QuestionAnswerFeedback)
async def return_speech_to_text_single(file: UploadFile = File(...), info: str = Form(...), request: Request = app.state):
    logger.debug(f"Received request to transcribe audio to text - {file.filename}")
    try:
        transcribed_answer: TranscribedText = await speech_to_text_single(audio_file=file, state=request.app.state)
        result: QuestionAnswerFeedback = await question_answer_feedback(
            question=json.loads(info)["question"],
            answer=transcribed_answer.utterances[0].text,
            state=request.app.state
        )
        return result
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


@app.post("/api-v1/audioToTextMultiple/", response_model=LabelledTranscribedText)
async def return_speech_to_text(file: UploadFile, request: Request):
    logger.debug(f"Received request to transcribe audio to text - {file.filename}")
    try:
        result: LabelledTranscribedText = await speech_to_text_multiple(audio_file=file, state=request.app.state)
        return result
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


@app.post("/api-v1/questionAnswerFeedback/", response_model=QuestionAnswerFeedback)
async def return_question_answer_feedback(endpoint_input: QuestionAndAnswer, request: Request):
    logger.debug(f"Received request to provide feedback on question and answer - {endpoint_input}")
    try:
        result: QuestionAnswerFeedback = await question_answer_feedback(
            question=endpoint_input.question,
            answer=endpoint_input.answer,
            state=request.app.state
        )
        return result
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 5000))
