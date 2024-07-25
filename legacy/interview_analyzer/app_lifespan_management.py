from starlette.datastructures import State

from legacy.interview_analyzer.connectors.email.tie_server import create_tie_server
from legacy.interview_analyzer.connectors.rds.database import create_database_access_layer
from legacy.interview_analyzer.connectors.s3.connector import create_s3_connector
from legacy.interview_analyzer.core.assembly_ai.transcriber import create_assembly_ai_transcriber
from legacy.interview_analyzer.core.open_ai.assistants.assistant_manager_factory import initialize_ai_assistants
from legacy.interview_analyzer.core.open_ai.simpleaichat import create_simple_ai_chat_connector
from legacy.interview_analyzer.utils.files import create_temp_directory, load_config_from_env, load_env


async def init_app_state(state: State):
    # Load env variables
    state.env = load_env()

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

    # Init SMTP email connector
    state.TIE_server = await create_tie_server(state)

    # Create temp location for audio files
    create_temp_directory()


async def cleanup_app_state(state: State):
    # Close the SMTP server connection
    state.TIE_server.quit()
