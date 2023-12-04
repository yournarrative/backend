from enum import Enum
from typing import List

from fastapi import UploadFile
from pydantic import BaseModel
from starlette.datastructures import State

from interview_analyzer.api.api_v1.speech_to_text.helpers import cleanup_temp_file, write_to_temp_file, \
    identify_and_assign_personas, transcribe_audio_to_text_multiple_speakers, \
    transcribe_audio_to_text_single_speaker
from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


class SpeakerType(Enum):
    DEFAULT = "Default"
    INTERVIEWER = "Interviewer"
    INTERVIEWEE = "Interviewee"


# SINGLE SPEAKER

class Utterance(BaseModel):
    speaker: str
    text: str


class TranscribedText(BaseModel):
    utterances: List[Utterance]


async def speech_to_text_single(audio_file: UploadFile, state: State) -> TranscribedText:
    audio_file_path = write_to_temp_file(audio_file)
    transcribed_text = await transcribe_audio_to_text_single_speaker(audio_file_path, state)
    cleanup_temp_file(audio_file_path)
    return transcribed_text


# MULTIPLE SPEAKERS

class LabelledUtterance(BaseModel):
    speaker: str
    text: str
    speaker_type: SpeakerType


class LabelledTranscribedText(BaseModel):
    labelled_utterances: List[LabelledUtterance]


async def speech_to_text_multiple(audio_file: UploadFile, state: State) -> LabelledTranscribedText:
    audio_file_path = write_to_temp_file(audio_file)
    transcribed_text = await transcribe_audio_to_text_multiple_speakers(audio_file_path, state)
    cleanup_temp_file(audio_file_path)
    labelled_transcribed_text = identify_and_assign_personas(transcribed_text)
    return labelled_transcribed_text
