import marvin
from starlette.datastructures import State

from information_retrieval.connectors.cohere.client import create_cohere_client
from information_retrieval.connectors.supabase.client import create_supabase_client
from information_retrieval.utils.files import load_config_from_env, load_env
from information_retrieval.utils.standard_logger import get_logger


logger = get_logger()


async def init_app_state(state: State):
    state.env = load_env()

    state.config = load_config_from_env(
        env=state.env.get("ENVIRONMENT"),
    )

    state.cohere_client = create_cohere_client(
        api_key=state.env.get("COHERE_API_KEY", ""),
    )

    state.supabase_client = create_supabase_client(
        url=state.env.get("SUPABASE_URL", ""), key=state.env.get("SUPABASE_KEY", ""),
    )

    init_marvin_api_key(api_key=state.env.get("OPENAI_API_KEY", ""))


def init_marvin_api_key(api_key: str):
    if not api_key:
        logger.error("Marvin OPENAI API key not provided.")
        raise ValueError("Marvin OPENAI API key not provided")

    marvin.settings.openai.api_key = api_key


def cleanup_app_state(state: State):
    pass
