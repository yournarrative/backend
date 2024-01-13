from starlette.datastructures import State

from interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from interview_analyzer.api.api_v1.shared.model import SimpleTranscript
from interview_analyzer.api.api_v1.enrich.helpers import identify_and_assign_personas


async def enrich_transcript(transcript: SimpleTranscript, state: State) -> EnrichedTranscript:
    enriched_transcript: EnrichedTranscript = await identify_and_assign_personas(transcript, state)
    return enriched_transcript
