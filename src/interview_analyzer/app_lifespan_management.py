import os
from dotenv import load_dotenv, find_dotenv

from starlette.datastructures import State

from interview_analyzer.core.assembly_ai.transcriber import create_assembly_ai_transcriber
from interview_analyzer.core.open_ai.simpleaichat import create_simple_ai_chat_connector
from interview_analyzer.data.rds.database import create_database_access_layer
from interview_analyzer.data.s3.connector import create_s3_connector
from interview_analyzer.core.open_ai.assistants.assistant_manager_factory import initialize_ai_assistants
from interview_analyzer.utils.files import create_temp_directory, load_config_from_env


async def init_app_state(state: State):
    # Load env variables
    load_dotenv(find_dotenv())
    state.env = os.environ

    # Load config
    state.config = load_config_from_env(env=state.env.get("ENVIRONMENT"))

    # Set API Keys
    state.transcriber = create_assembly_ai_transcriber(state)

    # Init OpenAI AI Assistants
    state.assistants = initialize_ai_assistants()

    # Init SimpleAI Data Wrapper
    state.simple_ai_chat_connector = create_simple_ai_chat_connector(state)

    # Init RDS DB Access Layer
    state.database_access_layer = await create_database_access_layer(state)

    # Init S3 Connector
    state.s3_connector = await create_s3_connector(state)

    # Create temp location for audio files
    create_temp_directory()


async def cleanup_app_state(state: State):
    # await state.transcriber.close()
    pass
