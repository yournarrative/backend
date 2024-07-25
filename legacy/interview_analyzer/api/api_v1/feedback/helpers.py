import json
from typing import List, Tuple

from starlette.datastructures import State

from legacy.interview_analyzer.api.api_v1.enrich.model import EnrichedTranscript, LabelledUtterance
from legacy.interview_analyzer.api.api_v1.feedback.model import Feedback, QuestionAndAnswerWithoutFeedback, STARFeedback
from legacy.interview_analyzer.core.open_ai.prompts.star_method import star_method_system_prompt
from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


def organize_questions_and_answers(enriched_transcript: EnrichedTranscript) -> List[QuestionAndAnswerWithoutFeedback]:
    reorganized_data: List[QuestionAndAnswerWithoutFeedback] = []
    i = 0
    while i < len(enriched_transcript.utterances):
        cur: LabelledUtterance = enriched_transcript.utterances[i]

        if cur.speaker_type.lower() == "interviewer" and cur.speech_type.lower() == "question":
            i, answer = collect_answer(i, cur.question_number, enriched_transcript.utterances)
            q = QuestionAndAnswerWithoutFeedback(
                question=cur.text,
                question_number=cur.question_number,
                question_type=cur.question_type,
                answer=answer,
            )
            reorganized_data.append(q)
        else:
            i += 1
    logger.debug(f"Reorganized data: {reorganized_data}")
    return reorganized_data


def collect_answer(i: int, question_number: int, utterances: List[LabelledUtterance]) -> Tuple[int, str]:
    answer_list: List[str] = []
    while i < len(utterances):
        cur: LabelledUtterance = utterances[i]
        if (
            cur.speaker_type.lower() == "interviewee"
            and cur.question_number == question_number
            and (cur.speech_type.lower() == "answer" or cur.speech_type.lower() == "continuation")
        ):
            answer_list.append(cur.text)
        i += 1
        if cur.question_number > question_number:
            i -= 1
            break
    return i, " ".join(answer_list).strip()


def get_feedback(q: QuestionAndAnswerWithoutFeedback, state: State) -> List[Feedback]:
    """Function to get all associated feedback methods based on the type category of question"""

    feedback_list: List[Feedback] = []

    if q.question_type.lower() == "behavioral":
        logger.debug(f"Giving feedback for behavioral question: {q.question}")

        star_feedback: STARFeedback = state.simple_ai_chat_connector.get_structured_response(
            system_prompt=star_method_system_prompt,
            instructions=f"Give STAR method feedback for this question: {json.dumps(q.model_dump(mode='json'))}",
            output_model=STARFeedback,
        )

        feedback_list.append(star_feedback)  # Add to this as we get new kinds of questions
    else:
        pass  # Fill in with other types of questions and their associated feedback methods

    return feedback_list
