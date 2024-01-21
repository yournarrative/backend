from starlette.datastructures import State

from interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from interview_analyzer.api.api_v1.transcribe.model import SimpleTranscript
from interview_analyzer.api.api_v1.enrich.helpers import send_for_analysis


async def enrich_transcript(transcript: SimpleTranscript, state: State) -> EnrichedTranscript:
    enriched_transcript: EnrichedTranscript = await send_for_analysis(transcript, state)
    return enriched_transcript
