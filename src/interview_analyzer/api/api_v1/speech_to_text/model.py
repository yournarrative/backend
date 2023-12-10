from enum import Enum
from typing import List

from pydantic import BaseModel


class SpeakerType(Enum):
    DEFAULT = "Default"
    INTERVIEWER = "Interviewer"
    INTERVIEWEE = "Interviewee"


class Utterance(BaseModel):
    speaker: str
    text: str


class TranscribedText(BaseModel):
    utterances: List[Utterance]


class LabelledUtterance(BaseModel):
    speaker: str
    text: str
    speaker_type: SpeakerType


class LabelledTranscribedText(BaseModel):
    labelled_utterances: List[LabelledUtterance]