from enum import Enum

from interview_analyzer.utils.ai_assistants.assistant_instructions import star_method_instructions
from interview_analyzer.utils.ai_assistants.assistant_manager import AssistantManager


class AssistantType(Enum):
    STAR = "star"


class AssistantManagerFactory:
    @classmethod
    def provide_assistant(cls, assistant_type: AssistantType = AssistantType.STAR) -> AssistantManager:
        assistant = cls._provide_assistant_(assistant_type)
        return assistant

    @classmethod
    def _provide_assistant_(cls, assistant_type: AssistantType):
        if assistant_type.value == AssistantType.STAR.value:
            return AssistantManager(name="Interview STAR Assistant", instructions=star_method_instructions)
        # Second type of assistant
        # elif assistant_type.value == AssistantType.STAR.value:
        #     return AssistantManager(name="Interview STAR Assistant", instructions=star_method_instructions)
        else:
            raise ValueError(assistant_type)
