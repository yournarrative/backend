import os
from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv

import assemblyai as aai
import yaml
from starlette.datastructures import State

# from interview_analyzer.data.database import DatabaseAccessLayer
from interview_analyzer.utils.ai_assistants.assistant_manager import AssistantManager
from interview_analyzer.utils.ai_assistants.assistant_manager_factory import AssistantType, AssistantManagerFactory
from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


async def init_app_state(state: State):
    # Load env variables
    load_dotenv(find_dotenv())
    state.env = os.environ

    # Load config
    state.config = load_config("resources/config.yaml")

    # Set API Keys
    aai.settings.api_key = state.env.get("ASSEMBLYAI_API_KEY")
    state.transcriber = aai.Transcriber()

    # Init OpenAI AI Assistants
    state.assistants = initialize_ai_assistants()

    # Init DB Access Layer
    # state.database_access_layer = await create_database_access_layer(state)

    # Create temp location for audio files
    create_temp_directory()


def create_temp_directory():
    if not os.path.exists(os.getcwd() + "/tmp"):
        os.mkdir(os.getcwd() + "/tmp", mode=0o777)


def initialize_ai_assistants() -> Dict[str, AssistantManager]:
    logger.debug("Initializing AI Assistants...")
    assistants = {a.name: AssistantManagerFactory.provide_assistant(a) for a in AssistantType}
    logger.debug("AI Assistants initialized.")
    return assistants


# async def create_database_access_layer(state: State) -> DatabaseAccessLayer:
#     return DatabaseAccessLayer(
#         host=state.env.get("DB_HOST"),
#         port=state.env.get("DB_PORT"),
#         name=state.env.get("DB_NAME"),
#         user=state.env.get("DB_USER"),
#         password=state.env.get("DB_PASSWORD"),
#         protocol=state.env.get("DB_PROTOCOL"),
#     )


def load_config(path: str) -> Dict[str, Any]:
    logger.debug(f"Loading config from {path}...")
    with open(path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


async def cleanup_app_state(state: State):
    # await state.transcriber.close()
    pass
