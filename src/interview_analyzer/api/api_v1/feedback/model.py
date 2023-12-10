from typing import List

from pydantic import BaseModel


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
