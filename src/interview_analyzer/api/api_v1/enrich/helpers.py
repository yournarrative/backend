import json

from starlette.datastructures import State

from interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from interview_analyzer.api.api_v1.transcribe.model import SimpleTranscript
from interview_analyzer.core.open_ai.prompts.interview_analysis import interview_analysis_system_prompt
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def send_for_analysis(transcript: SimpleTranscript, state: State) -> EnrichedTranscript:
    system_prompt: str = interview_analysis_system_prompt
    instructions: str = f"Please analyze this interview transcript: {json.dumps(transcript.model_dump(mode='json')['utterances'])}"

    enriched_transcript: EnrichedTranscript = state.simple_ai_chat_connector.get_structured_response(
        system_prompt=system_prompt, instructions=instructions, output_model=EnrichedTranscript)
    return enriched_transcript
