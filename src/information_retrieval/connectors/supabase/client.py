from supabase import create_client, Client

from information_retrieval.utils.standard_logger import get_logger


logger = get_logger()


async def create_supabase_client(url: str, key: str) -> Client:
    logger.debug(f"Creating supabase connector for url: {url}")
    logger.debug(f"Creating supabase connector for key: {key}")
    try:
        client: Client = create_client(url, key)
    except Exception as e:
        logger.error(f"Error creating supabase connector, error: {e}")
        raise e
    else:
        logger.debug("Successfully created supabase connector.")
        return client
