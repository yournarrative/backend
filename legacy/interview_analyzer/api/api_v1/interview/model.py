from typing import List

from pydantic import BaseModel

from legacy.interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from legacy.interview_analyzer.api.api_v1.feedback.model import QuestionAndAnswerWithFeedback


class Interview(BaseModel):
    enriched_transcript: EnrichedTranscript
    analysis: List[QuestionAndAnswerWithFeedback]
