from starlette.datastructures import State

from interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from interview_analyzer.api.api_v1.transcribe.model import SimpleTranscript
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def send_for_analysis(transcript: SimpleTranscript, state: State) -> EnrichedTranscript:
    system_prompt = f"""
    You are the world's greatest interview coach. I will give you a transcript of 
    Here is an interview transcript. Analyze it. You will be given $500 if you can 
    correctly analyze all aspects of this interview as requested:

    {transcript.model_dump(mode="json")['utterances']}
    """

    enriched_transcript: EnrichedTranscript = state.simple_ai_chat_connector.get_structured_response(
        system_prompt=system_prompt, output_model=EnrichedTranscript)
    return enriched_transcript
