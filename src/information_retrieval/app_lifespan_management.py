import marvin
from starlette.datastructures import State

from information_retrieval.connectors.cohere.client import create_cohere_client
from information_retrieval.connectors.supabase.client import create_supabase_client
from information_retrieval.utils.files import load_config_from_env, load_env


async def init_app_state(state: State):
    # Load env variables
    state.env = load_env()

    # Load config
    state.config = load_config_from_env(
        env=state.env.get("ENVIRONMENT"),
    )

    state.cohere_client = create_cohere_client(
        state=state,
    )

    state.supabase_client = create_supabase_client(
        url=state.env.get("SUPABASE_URL"), key=state.env.get("SUPABASE_KEY"),
    )

    init_marvin_api_key(state)


def init_marvin_api_key(state: State):
    marvin.settings.openai.api_key = state.env.get("OPENAI_API_KEY")


async def cleanup_app_state(state: State):
    pass
