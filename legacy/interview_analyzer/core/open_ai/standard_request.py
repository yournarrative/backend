from openai import OpenAI
from starlette.datastructures import State

from legacy.interview_analyzer.utils.logger import get_logger

logger = get_logger()


async def get_completion(prompt: str, state: State, model="gpt-4") -> str:
    messages = [{"role": "user", "content": prompt}]
    result = ""
    try:
        client = OpenAI(api_key=state.env.get("OPENAI_API_KEY"))
        response = client.chat.completions.create(model=model, messages=messages, temperature=0)
        result = response.choices[0].message.content
    except Exception as e:
        logger.error(f"Failed to get completion from OpenAI: {e}")
    finally:
        return result
