from typing import List

from pydantic import BaseModel
from simpleaichat.utils import fd


class Feedback(BaseModel):
    """Feedback on a question and answer with a specific method_name, such as STAR or technical feedback"""

    method_name: str = fd(
        description="The name of the feedback method."
    )
    feedback_explanation: str = fd(
        description="The feedback explanation to be read by the interviewee of how well they answered the question."
    )
    score: int = fd(
        description="The score given to this interview based on the associated feedback method.",
        min_value=0,
        max_value=5,
    )


class STARFeedback(Feedback):
    """Feedback based on the "STAR" method for answering behavioral interview questions"""
    method_name: str = "STAR"


class QuestionAndAnswerWithoutFeedback(BaseModel):
    question: str
    question_number: int
    question_type: str
    answer: str


class QuestionAndAnswerWithFeedback(BaseModel):
    question: str
    question_number: int
    question_type: str
    answer: str
    feedback: List[Feedback]
