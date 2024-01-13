from typing import List

from pydantic import BaseModel

from interview_analyzer.api.api_v1.shared.model import SpeakerType


class LabelledUtterance(BaseModel):
    speaker: str
    text: str
    speaker_type: SpeakerType


class EnrichedTranscript(BaseModel):
    utterances: List[LabelledUtterance]
