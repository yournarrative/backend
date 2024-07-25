import cohere

from information_retrieval.core.logger import app_logger as logger


def create_cohere_client(api_key: str) -> cohere.Client:
    logger.debug("Creating Cohere client...")

    if not api_key:
        logger.error("API key not provided.")
        raise ValueError("API key not provided")

    try:
        co: cohere.Client = cohere.Client(api_key)
    except Exception as e:
        logger.error(f"Failed to create Cohere client: {e}")
        raise e
    else:
        logger.debug("Cohere client created.")
        return co
