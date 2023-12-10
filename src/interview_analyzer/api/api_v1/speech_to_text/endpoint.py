from fastapi import UploadFile
from starlette.datastructures import State

from interview_analyzer.api.api_v1.speech_to_text.helpers import cleanup_temp_file, write_to_temp_file, \
    identify_and_assign_personas, transcribe_audio_to_text_multiple_speakers, \
    transcribe_audio_to_text_single_speaker
from interview_analyzer.api.api_v1.speech_to_text.model import TranscribedText, LabelledTranscribedText
from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


async def speech_to_text_single(audio_file: UploadFile, state: State) -> TranscribedText:
    audio_file_path = write_to_temp_file(audio_file)
    transcribed_text = await transcribe_audio_to_text_single_speaker(audio_file_path, state)
    cleanup_temp_file(audio_file_path)
    return transcribed_text


async def speech_to_text_multiple(audio_file: UploadFile, state: State) -> LabelledTranscribedText:
    audio_file_path = write_to_temp_file(audio_file)
    transcribed_text = await transcribe_audio_to_text_multiple_speakers(audio_file_path, state)
    cleanup_temp_file(audio_file_path)
    labelled_transcribed_text = await identify_and_assign_personas(transcribed_text, state)
    return labelled_transcribed_text
