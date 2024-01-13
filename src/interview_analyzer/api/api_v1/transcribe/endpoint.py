from fastapi import UploadFile
from starlette.datastructures import State

from interview_analyzer.api.api_v1.transcribe.helpers import send_to_assembly_ai
from interview_analyzer.api.api_v1.shared.model import SimpleTranscript
from interview_analyzer.utils.files import write_to_temp_file, cleanup_temp_file
from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


async def transcribe_speech(audio_file: UploadFile, state: State) -> SimpleTranscript:
    audio_file_path = write_to_temp_file(audio_file)
    simple_transcript = await send_to_assembly_ai(audio_file_path, state)
    cleanup_temp_file(audio_file_path)
    return simple_transcript
