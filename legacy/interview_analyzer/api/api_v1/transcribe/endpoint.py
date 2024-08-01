from fastapi import UploadFile
from starlette.datastructures import State

from legacy.interview_analyzer.api.api_v1.transcribe.helpers import send_to_assembly_ai
from legacy.interview_analyzer.api.api_v1.transcribe.model import SimpleTranscript
from legacy.interview_analyzer.utils.files import (
    cleanup_temp_file,
    write_bytes_file_to_temp_file,
    write_upload_file_to_temp_file,
)
from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


async def transcribe_upload_file_speech_to_text(audio_file: UploadFile, state: State) -> SimpleTranscript:
    audio_file_path = write_upload_file_to_temp_file(audio_file)
    simple_transcript = send_to_assembly_ai(audio_file_path, state)
    cleanup_temp_file(audio_file_path)
    return simple_transcript


def transcribe_bytes_file_speech_to_text(audio_file: bytes, filename: str, state: State) -> SimpleTranscript:
    audio_file_path = write_bytes_file_to_temp_file(audio_file, filename)
    simple_transcript = send_to_assembly_ai(audio_file_path, state)
    cleanup_temp_file(audio_file_path)
    return simple_transcript
