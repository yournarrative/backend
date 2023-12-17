import os
from typing import Dict, Any
from dotenv import load_dotenv, find_dotenv

import assemblyai as aai
import yaml
from starlette.datastructures import State

from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def init_app_state(state: State):
    load_dotenv(find_dotenv())
    state.config = load_config("resources/config.yaml")
    state.env = os.environ
    aai.settings.api_key = state.env.get("ASSEMBLYAI_API_KEY")
    state.transcriber = aai.Transcriber()


def load_config(path: str) -> Dict[str, Any]:
    logger.debug(f"Loading config from {path}...")
    with open(path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


async def cleanup_app_state(state: State):
    await state.transcriber.close()
