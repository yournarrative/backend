from typing import Dict, Any
import os, os.path
import yaml

from information_retrieval.utils.standard_logger import get_logger

logger = get_logger()


def load_env() -> Dict[str, str]:
    logger.debug("Loading env variables...")
    env = dict(os.environ)
    logger.debug(f"Env variables loaded: {env}")
    return env


def load_config_from_env(env: str) -> Dict[str, Any]:
    logger.debug(f"Loading config from env: {env}...")
    env = env.replace('"', '')
    with open(f"resources/config/{env}/conf.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config
