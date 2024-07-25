import json

from starlette.datastructures import State

from legacy.interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from legacy.interview_analyzer.api.api_v1.transcribe.model import SimpleTranscript
from legacy.interview_analyzer.core.open_ai.prompts.interview_analysis import interview_analysis_system_prompt
from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


async def send_for_analysis(transcript: SimpleTranscript, state: State) -> EnrichedTranscript:
    system_prompt: str = interview_analysis_system_prompt
    instructions: str = (
        f"Please analyze this interview transcript: {json.dumps(transcript.model_dump(mode='json')['utterances'])}"
    )

    # 13 min interview char length: 19033
    enriched_transcript: EnrichedTranscript = state.simple_ai_chat_connector.get_structured_response(
        system_prompt=system_prompt, instructions=instructions, output_model=EnrichedTranscript
    )
    return enriched_transcript
