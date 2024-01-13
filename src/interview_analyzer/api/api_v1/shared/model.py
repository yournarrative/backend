from enum import Enum
from typing import List

from pydantic import BaseModel


class SpeakerType(Enum):
    DEFAULT = "Default"
    INTERVIEWER = "Interviewer"
    INTERVIEWEE = "Interviewee"


class SimpleUtterance(BaseModel):
    speaker: str
    text: str


class SimpleTranscript(BaseModel):
    utterances: List[SimpleUtterance]
