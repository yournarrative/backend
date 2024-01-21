from typing import List

from pydantic import BaseModel
from simpleaichat.utils import fd


class LabelledUtterance(BaseModel):
    """A labelled utterance from an interview transcript"""

    position: int = fd(
        description="The order in which the utterance was spoken. This should be a monotonically "
                    "increasing integer starting with 0."
    )
    speaker: str = fd(
        description="Which speaker is the \"interviewer\" and which speaker is the \"interviewee\"."
                    " Label these as \"Interviewer\" and \"Interviewee\" respectively."
    )
    text: str = fd(
        description="The text of the utterance."
    )
    speech_type: str = fd(
        description="Which utterances are questions and which utterances are answers, and which utterances are "
                    "continuations of the current question/answer, and which utterances are irrelevant to the "
                    "interview entirely (such as a greeting, brief personal introduction, miscellaneous remark, or off "
                    "topic discussion). Label these as \"Question\", \"Answer\", \"Continuation\", "
                    "and \"Irrelevant\" respectively."
    )
    speaker_type: str = fd(
        description="When a new question is identified, determine if it is a \"Behavioral\" question or "
                    "a \"Technical\" question. Label these as \"Behavioral\" and \"Technical\" respectively. "
                    "If it is not a new question, return the label \"None\" for the question type."
    )
    question_number: int = fd(
        description="This is a monotonically increasing integer that represents the number of the question that "
                    "is being asked. This number should be incremented each time a new question is identified. "
                    "If it is not a new question, assign the number of the previous question. If it is a new "
                    "question, return the number of the new question."
    )


class EnrichedTranscript(BaseModel):
    """An enriched transcript that contains details and analysis about an interview"""

    utterances: List[LabelledUtterance] = fd(description="A list of labelled utterances from an interview transcript")
