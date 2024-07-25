from starlette.datastructures import State

from legacy.interview_analyzer.api.api_v1.enrich.helpers import send_for_analysis
from legacy.interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from legacy.interview_analyzer.api.api_v1.transcribe.model import SimpleTranscript


async def enrich_transcript(transcript: SimpleTranscript, state: State) -> EnrichedTranscript:
    enriched_transcript: EnrichedTranscript = await send_for_analysis(transcript, state)
    return enriched_transcript
