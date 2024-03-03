import cohere
from starlette.datastructures import State

from information_retrieval.utils.standard_logger import get_logger

logger = get_logger()


async def create_cohere_client(state: State) -> cohere.Client:
    logger.debug(f"Creating Cohere client...")
    cohere_api_key = state.env.get("COHERE_API_KEY")

    try:
        co: cohere.Client = cohere.Client(cohere_api_key)
    except Exception as e:
        logger.error(f"Failed to create Cohere client: {e}")
        raise e
    else:
        logger.debug("Cohere client created.")
        return co
