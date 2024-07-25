import os
from typing import Any

import yaml

from information_retrieval.core.logger import app_logger as logger


class Settings:
    def __init__(self):
        logger.debug("Loading settings...")
        self.env_vars = self.load_env()
        self.config = self.load_config_from_env(env=self.env_vars.get("ENVIRONMENT"))
        logger.debug("Settings loaded.")

    @staticmethod
    def load_env() -> dict[str, str]:
        logger.debug("Loading env variables...")
        env = dict(os.environ)
        logger.debug("Env variables loaded.")
        return env

    @staticmethod
    def load_config_from_env(env: str) -> dict[str, Any]:
        logger.debug(f"Loading config from env: {env}")
        env = env.replace('"', "")
        with open(f"resources/config/{env}/conf.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)
        logger.debug(f"Config loaded: {config}")
        return config


settings = Settings()
