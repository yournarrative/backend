import marvin
from fastapi import FastAPI

from information_retrieval.config import settings
from information_retrieval.connectors.cohere.client import create_cohere_client
from information_retrieval.connectors.supabase.client import create_supabase_client
from information_retrieval.utils.standard_logger import app_logger as logger


# TODO: figure out proper dependency injection for this
async def init_app_state(app: FastAPI):
    app.state.settings = settings

    app.state.cohere_client = create_cohere_client(
        api_key=app.state.settings.env_vars.get("COHERE_API_KEY", ""),
    )

    app.state.supabase_client = create_supabase_client(
        url=app.state.settings.env_vars.get("SUPABASE_URL", ""),
        key=app.state.settings.env_vars.get("SUPABASE_KEY", ""),
    )

    init_marvin_api_key(api_key=app.state.settings.env_vars.get("OPENAI_API_KEY", ""))


def init_marvin_api_key(api_key: str):
    if not api_key:
        logger.error("Marvin OPENAI API key not provided.")
        raise ValueError("Marvin OPENAI API key not provided")

    marvin.settings.openai.api_key = api_key


def cleanup_app_state(app: FastAPI):
    pass
