from enum import Enum
from typing import Dict

from legacy.interview_analyzer.core.open_ai.assistants.assistant_instructions import star_method_instructions
from legacy.interview_analyzer.core.open_ai.assistants.assistant_manager import AssistantManager
from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


class AssistantType(Enum):
    STAR = "star"


class AssistantManagerFactory:
    @classmethod
    def provide_assistant(cls, assistant_type: AssistantType = AssistantType.STAR) -> AssistantManager:
        assistant = cls._provide_assistant_(assistant_type)
        return assistant

    @classmethod
    def _provide_assistant_(cls, assistant_type: AssistantType):
        if assistant_type == AssistantType.STAR:
            return AssistantManager(name="Interview STAR Feedback Assistant", instructions=star_method_instructions)
        else:
            raise ValueError(assistant_type)


def initialize_ai_assistants() -> Dict[str, AssistantManager]:
    logger.debug("Initializing AI Assistants...")
    assistants = {a.value: AssistantManagerFactory.provide_assistant(a) for a in AssistantType}
    logger.debug("AI Assistants initialized.")
    return assistants
