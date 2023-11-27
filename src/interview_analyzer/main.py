import os

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
import uvicorn

from interview_analyzer.api.api_v1.feedback.endpoint import QuestionAnswerFeedback, QuestionAndAnswer, \
    question_answer_feedback
from interview_analyzer.api.api_v1.speech_to_text.endpoint import TranscribedTextSingle, AudioInput, \
    speech_to_text_single, TranscribedTextMultiple, speech_to_text_multiple
from interview_analyzer.pre_startup import init_app_state
from interview_analyzer.utils.standard_logger import get_logger

app = FastAPI(title="Silver")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = get_logger()

@app.on_event("startup")
async def startup():
    await init_app_state(app.state)


@app.get("/")
async def health_check():
    return "I'm healthy, yo!"


@app.post("/audioToTextSingle/", response_model=TranscribedTextSingle)
async def return_speech_to_text_single(endpoint_input: AudioInput, request: Request):
    logger.debug(f"Received request to transcribe audio to text - {endpoint_input.audio_bytes}")
    try:
        result: TranscribedTextSingle = await speech_to_text_single(audio_input=endpoint_input, state=request.app.state)
        return result
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)
    # except DataValidationError:
    #     return HTTPException(status_code=400)
    # except InternalProcessingError:
    #     return HTTPException(status_code=500)


@app.post("/audioToTextMultiple/", response_model=TranscribedTextMultiple)
async def return_speech_to_text_multiple(endpoint_input: AudioInput, request: Request):
    logger.debug(f"Received request to transcribe audio to text - {AudioInput}")
    try:
        result: TranscribedTextSingle = await speech_to_text_multiple(audio_input=endpoint_input, state=request.app.state)
        return result
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


@app.post("/questionAnswerFeedback/", response_model=QuestionAnswerFeedback)
async def return_question_answer_feedback(endpoint_input: QuestionAndAnswer, request: Request):
    logger.debug(f"Received request to provide feedback on question and answer - {QuestionAndAnswer}")
    try:
        result: QuestionAnswerFeedback = await question_answer_feedback(
            endpoint_input=endpoint_input,
            state=request.app.state
        )
        return result
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("PORT", 5000))

