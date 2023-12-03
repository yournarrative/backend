from typing import Dict, Any

import assemblyai as aai
import yaml
from starlette.datastructures import State

from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def init_app_state(state: State):
    state.config = load_config("resources/config.yaml")
    state.api_keys = load_config("resources/api-keys.yaml")
    aai.settings.api_key = state.api_keys["assemblyai"]
    state.transcriber = aai.Transcriber()


def load_config(path: str) -> Dict[str, Any]:
    logger.debug(f"Loading config from {path}...")
    with open(path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


async def cleanup_app_state(state: State):
    await state.transcriber.close()
