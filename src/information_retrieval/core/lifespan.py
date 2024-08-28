import marvin
from fastapi import FastAPI

from information_retrieval.connectors.supabase.client import create_supabase_client
from information_retrieval.core.config import settings
from information_retrieval.core.logger import app_logger as logger


async def init_app_state(app: FastAPI):
    app.state.settings = settings

    # app.state.cohere_client = create_cohere_client(
    #     api_key=app.state.settings.env_vars.get("COHERE_API_KEY", ""),
    # )

    app.state.supabase_client = create_supabase_client(
        url=app.state.settings.env_vars.get("SUPABASE_URL", ""),
        key=app.state.settings.env_vars.get("SUPABASE_KEY", ""),
    )

    init_marvin_api_key(api_key=app.state.settings.env_vars.get("OPENAI_API_KEY", ""))


def init_marvin_api_key(api_key: str):
    if not api_key:
        e = ValueError("Marvin OPENAI API key not provided")
        logger.error(e)
        raise e

    marvin.settings.openai.api_key = api_key


async def cleanup_app_state(app: FastAPI):
    pass
