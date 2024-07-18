from supabase import create_client, Client

from information_retrieval.utils.standard_logger import get_logger


logger = get_logger()


def create_supabase_client(url: str, key: str) -> Client:
    logger.debug(f"Creating supabase connector for url: {url}")
    logger.debug(f"Creating supabase connector for key: {key}")

    import re
    if not re.match(r"^(https?)://.+", url):
        print('NO MATCH')
    else:
        print('MATCH')

    try:
        client: Client = create_client(url.strip(), key.strip())
    except Exception as e:
        logger.error(f"Error creating supabase connector, error: {e}")
        raise e
    else:
        logger.debug("Successfully created supabase connector.")
        return client


def init_supabase():
    # Fetch the Supabase URL and API key from environment variables
    url: str = os.getenv("SUPABASE_URL")
    key: str = os.getenv("SUPABASE_KEY")

    if not url or not key:
        print("Supabase URL or API key is not set in environment variables.")
        return None

    try:
        supabase: Client = create_client(url, key)
        print("Successfully connected to Supabase.")
        return supabase
    except Exception as e:
        print(f"Error connecting to Supabase: {e}")
        return None