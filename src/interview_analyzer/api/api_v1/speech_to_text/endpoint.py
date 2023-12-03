from enum import Enum
from typing import List

import assemblyai as aai
from fastapi import UploadFile
from pydantic import BaseModel
from starlette.datastructures import State

from interview_analyzer.api.api_v1.speech_to_text.helpers import cleanup_temp_file, write_to_temp_file
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


class Utterance(BaseModel):
    speaker: str
    text: str


class TranscribedText(BaseModel):
    utterances: List[Utterance]


class SpeakerType(Enum):
    INTERVIEWER = "Interviewer"
    INTERVIEWEE = "Interviewee"


class LabelledUtterance(BaseModel):
    speaker: SpeakerType
    text: str


class LabelledTranscribedText(BaseModel):
    labelled_utterances: List[LabelledUtterance]


async def speech_to_text(audio_file: UploadFile, state: State) -> LabelledTranscribedText:
    # Write autio_input bytes to file
    audio_file_path = write_to_temp_file(audio_file)
    transcribed_text = await transcribe_audio_to_text(audio_file_path, state)
    cleanup_temp_file(audio_file_path)
    labelled_transcribed_text = identify_interviewer_and_interviewee(transcribed_text)
    return labelled_transcribed_text


async def transcribe_audio_to_text(audio_file_path: str, state: State):
    utterances: List[Utterance] = []
    try:
        transcript = state.transcriber.transcribe(
            audio_file_path,
            config=aai.TranscriptionConfig(
                speaker_labels=True,
            ),
        )
    except Exception as e:
        logger.error(f"Failed to transcribe audio from file {audio_file_path}: {e}")
    else:
        for u in transcript.utterances:
            utterances.append(Utterance(speaker=u.speaker, text=u.text))
    finally:
        print(utterances)
        return TranscribedText(utterances=utterances)


def identify_interviewer_and_interviewee(transcribed_text: TranscribedText):
    # TODO: Actually figure out who is who here
    labelled_utterances: List[LabelledUtterance] = []
    for utterance in transcribed_text.utterances:
        if utterance.speaker == "A":
            speaker = SpeakerType.INTERVIEWER
        elif utterance.speaker == "B":
            speaker = SpeakerType.INTERVIEWEE
        else:
            raise ValueError(f"Speaker label {utterance.speaker} is not recognized")
        labelled_utterances.append(LabelledUtterance(speaker=speaker, text=utterance.text))

    return LabelledTranscribedText(labelled_utterances=labelled_utterances)
