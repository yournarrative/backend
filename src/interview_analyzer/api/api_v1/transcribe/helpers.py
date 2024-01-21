from typing import List

import assemblyai as aai
from starlette.datastructures import State

from interview_analyzer.api.api_v1.transcribe.model import SimpleUtterance, SimpleTranscript
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def send_to_assembly_ai(audio_file_path: str, state: State) -> SimpleTranscript:
    try:
        transcript = state.transcriber.transcribe(audio_file_path, config=aai.TranscriptionConfig(speaker_labels=True))
    except Exception as e:
        logger.error(f"Failed to transcribe audio from file {audio_file_path}: {e}")
        raise e
    else:
        utterances: List[SimpleUtterance] = []
        for u in transcript.utterances:
            utterances.append(SimpleUtterance(speaker=u.speaker, text=u.text))
        return SimpleTranscript(utterances=utterances)
