from supabase import Client, create_client

from information_retrieval.core.logger import app_logger as logger


def create_supabase_client(url: str, key: str) -> Client:
    logger.debug(f"Creating supabase connector for url: {url}")

    if not url or not key:
        logger.error("URL or key not provided.")
        raise ValueError("Supabase URL or key not provided")

    try:
        client: Client = create_client(url.strip('"'), key.strip('"'))
    except Exception as e:
        logger.error(f"Error creating supabase connector, error: {e}")
        raise e
    else:
        logger.debug("Successfully created supabase connector.")
        return client
