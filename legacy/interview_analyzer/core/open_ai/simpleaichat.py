import pydantic
from simpleaichat import AIChat
from starlette.datastructures import State

from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


class SimpleAIChatConnector:
    def __init__(self, api_key: str):
        self.ai = AIChat(
            api_key=api_key,
            console=False,
            save_messages=False,
            model="gpt-4-turbo-preview",
            params={"temperature": 0.0},
        )

    def get_structured_response(
        self, system_prompt: str, instructions: str, output_model: pydantic.BaseModel
    ) -> pydantic.BaseModel:
        try:
            print(instructions[-100:])
            structured_response = self.ai(
                instructions,
                output_schema=output_model,
                system=system_prompt,
            )
            print("STRUCTURED RESPONSE:::")
            print(structured_response)
        except Exception as e:
            logger.error(f"Failed to get response from SimpleAIChatConnector: {e}")
            raise e

        try:
            output = output_model(**structured_response)
            return output
        except Exception as e:
            logger.error(f"Failed to parse response from OpenAI: {e}")
            raise e


def create_simple_ai_chat_connector(state: State) -> SimpleAIChatConnector:
    return SimpleAIChatConnector(api_key=state.env.get("OPENAI_API_KEY"))
