from typing import List

from pydantic import BaseModel


class QuestionAndAnswer(BaseModel):
    question: str
    question_type: str
    answer: str


class Feedback(BaseModel):
    methodology: str


    positive_feedback: List[str]
    negative_feedback: List[str]


class QuestionAnswerFeedback(BaseModel):
    question: str
    answer: str
    feedback: List[Feedback]
