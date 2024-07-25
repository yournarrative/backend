from typing import List

from starlette.datastructures import State

from legacy.interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript
from legacy.interview_analyzer.api.api_v1.feedback.helpers import get_feedback, organize_questions_and_answers
from legacy.interview_analyzer.api.api_v1.feedback.model import (
    Feedback,
    QuestionAndAnswerWithFeedback,
    QuestionAndAnswerWithoutFeedback,
)
from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


async def question_answer_feedback(
    enriched_transcript: EnrichedTranscript,
    state: State,
) -> List[QuestionAndAnswerWithFeedback]:
    # Reformat questions with all associated answer utterances to analyze each question fully at once
    organized_qna_without_feedback: List[QuestionAndAnswerWithoutFeedback] = organize_questions_and_answers(
        enriched_transcript=enriched_transcript
    )

    # Get feedback on each individual question and associated one at a time
    qna_with_feedback_list: List[QuestionAndAnswerWithFeedback] = []
    for q in organized_qna_without_feedback:
        feedback: List[Feedback] = get_feedback(q, state)
        qna_with_feedback = QuestionAndAnswerWithFeedback(
            question=q.question,
            question_number=q.question_number,
            question_type=q.question_type,
            answer=q.answer,
            feedback=feedback,
        )
        qna_with_feedback_list.append(qna_with_feedback)

    return qna_with_feedback_list
