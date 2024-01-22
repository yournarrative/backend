from typing import List

from pydantic import BaseModel

from interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from interview_analyzer.api.api_v1.feedback.model import QuestionAndAnswerWithFeedback


class Interview(BaseModel):
    enriched_transcript: EnrichedTranscript
    analysis: List[QuestionAndAnswerWithFeedback]
