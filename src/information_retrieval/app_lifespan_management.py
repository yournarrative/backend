import marvin
from starlette.datastructures import State

from information_retrieval.connectors.cohere.client import create_cohere_client
from information_retrieval.connectors.supabase.client import create_supabase_client
from information_retrieval.utils.files import load_config_from_env, load_env


async def init_app_state(state: State):
    # Load env variables
    state.env = load_env()

    import subprocess

    def ping_google():
        try:
            # Ping Google's DNS server
            output = subprocess.check_output(["ping", "-c", "4", "8.8.8.8"], universal_newlines=True)
            return output
        except subprocess.CalledProcessError as e:
            return f"Ping failed with error: {e}"

    result = ping_google()
    print(result)
    # Load config
    state.config = load_config_from_env(env=state.env.get("ENVIRONMENT"))

    # Init RDS DB Access Layer
    state.supabase_client = await create_supabase_client(state.env.get("SUPABASE_URL"),
                                                         state.env.get("SUPABASE_KEY"),)

    # Init Cohere connector
    state.cohere_client = await create_cohere_client(state)

    init_marvin_api_key(state)


def init_marvin_api_key(state: State):
    marvin.settings.openai.api_key = state.env.get("OPENAI_API_KEY")


async def cleanup_app_state(state: State):
    pass
