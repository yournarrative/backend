from typing import Dict, Any

import whisper
import yaml
from whisper.model import Whisper

from starlette.datastructures import State


async def init_app_state(state: State):
    state.whisper_model = await load_whisper_model()
    state.app_config = load_config("resources/config.yaml")


async def load_whisper_model() -> Whisper:
    print("Loading Whisper model...")
    model: Whisper = whisper.load_model("base")
    return model


def load_config(path: str) -> Dict[str, Any]:
    print(f"Loading config from {path}...")
    with open(path, "r") as config_file:
        config = yaml.safe_load(config_file)
    return config