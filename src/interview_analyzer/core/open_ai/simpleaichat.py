import pydantic
from simpleaichat import AIChat
from starlette.datastructures import State

from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


class SimpleAIChatConnector:
    def __init__(self, api_key: str):
        self.ai = AIChat(
            api_key=api_key,
            console=False,
            save_messages=False,
            model="gpt-3.5-turbo",
            params={"temperature": 0.0}
        )

    def get_structured_response(self, system_prompt: str, output_model: pydantic.BaseModel) -> pydantic.BaseModel:
        try:
            response_structured = self.ai(
                "Please analyze this interview transcript.",
                output_schema=output_model,
                system=system_prompt,
            )
        except Exception as e:
            logger.error(f"Failed to get response from SimpleAIChatConnector: {e}")
            raise e

        try:
            output = output_model(**response_structured)
            return output
        except Exception as e:
            logger.error(f"Failed to parse response from OpenAI: {e}")
            raise e


def create_simple_ai_chat_connector(state: State) -> SimpleAIChatConnector:
    return SimpleAIChatConnector(api_key=state.env.get("OPENAI_API_KEY"))
