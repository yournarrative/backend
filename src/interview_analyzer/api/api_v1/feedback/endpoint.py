from starlette.datastructures import State

from interview_analyzer.api.api_v1.feedback.helpers import get_interview_feedback, format_suggestions
from interview_analyzer.api.api_v1.feedback.model import Feedback, QuestionAnswerFeedback


async def question_answer_feedback(question: str, answer: str, state: State) -> QuestionAnswerFeedback:
    suggestion_response = await get_interview_feedback(
        interview_question=question,
        answer=answer,
        state=state
    )
    feedback: Feedback = format_suggestions(suggestion_response)
    return QuestionAnswerFeedback(
        question=question,
        answer=answer,
        feedback=feedback
    )
