from typing import List

from pydantic import BaseModel


class SimpleUtterance(BaseModel):
    speaker: str
    text: str


class SimpleTranscript(BaseModel):
    utterances: List[SimpleUtterance]
