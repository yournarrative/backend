from starlette.datastructures import State

from information_retrieval.connectors.cohere.client import create_cohere_client
from information_retrieval.connectors.rds.database import create_database_access_layer
from information_retrieval.utils.files import create_temp_directory, load_config_from_env, load_env


async def init_app_state(state: State):
    # Load env variables
    state.env = load_env()

    # Load config
    state.config = load_config_from_env(env=state.env.get("ENVIRONMENT"))

    # Init RDS DB Access Layer
    state.database_access_layer = await create_database_access_layer(state)

    # Init Cohere connector
    state.cohere_client = await create_cohere_client(state)

    # Create temp location for audio files
    create_temp_directory()


async def cleanup_app_state(state: State):
    pass
