from typing import List

from pydantic import BaseModel
from starlette.datastructures import State

from interview_analyzer.utils.llm import get_completion

LEADING_POSITIVE_FEEDBACK_TITLE: str = "Things done well"
LEADING_NEGATIVE_FEEDBACK_TITLE: str = "Things to improve upon"
NUM_SUGGESTIONS: int = 5


class QuestionAndAnswer(BaseModel):
    question: str
    answer: str


class Feedback(BaseModel):
    positive_feedback: List[str]
    negative_feedback: List[str]


class QuestionAnswerFeedback(BaseModel):
    question: str
    answer: str
    feedback: Feedback


async def question_answer_feedback(question: str, answer: str, state: State) -> QuestionAnswerFeedback:
    suggestion_response = await get_interview_feedback(
        interview_question=question,
        answer=answer,
        state=state
    )
    feedback: Feedback = format_suggestions(suggestion_response)
    return QuestionAnswerFeedback(
        question=question,
        answer=answer,
        feedback=feedback
    )


async def get_interview_feedback(interview_question: str, answer: str, state: State):

    prompt = "Given the following interview question: " + \
             "\n" + interview_question + \
             "\n" + "And the following answer: " + \
             "\n" + answer + \
             "\n" + f"Suggest a list of {NUM_SUGGESTIONS} things the answer did well, leading with the title: '{LEADING_POSITIVE_FEEDBACK_TITLE}'" + \
             "\n" + f"and {NUM_SUGGESTIONS} things the answer improve upon leading with the title: '{LEADING_NEGATIVE_FEEDBACK_TITLE}'."
    response = await get_completion(prompt, state)
    return response


def format_suggestions(suggestion_response: str) -> Feedback:
    positive_feedback = []
    negative_feedback = []
    for i, line in enumerate(suggestion_response.split("\n")):
        if LEADING_POSITIVE_FEEDBACK_TITLE in line:
            positive_feedback.extend([l for l in suggestion_response.split("\n")[i+1:i+NUM_SUGGESTIONS+1]])
        elif LEADING_NEGATIVE_FEEDBACK_TITLE in line:
            negative_feedback.extend([l for l in suggestion_response.split("\n")[i+1:i+NUM_SUGGESTIONS+1]])
    return Feedback(positive_feedback=positive_feedback, negative_feedback=negative_feedback)
