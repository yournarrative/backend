import assemblyai as aai
from assemblyai import Transcriber
from starlette.datastructures import State

from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


def create_assembly_ai_transcriber(state: State) -> Transcriber:
    logger.debug("Creating AssemblyAI transcriber...")
    aai.settings.api_key = state.env.get("ASSEMBLYAI_API_KEY")

    try:
        transcriber = aai.Transcriber()
    except Exception as e:
        logger.error(f"Failed to create AssemblyAI transcriber: {e}")
        raise e
    else:
        logger.debug("AssemblyAI transcriber created.")
        return transcriber
