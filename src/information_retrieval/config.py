from information_retrieval.utils.file_io import load_config_from_env, load_env
from information_retrieval.utils.standard_logger import app_logger as logger


class Settings:
    def __init__(self):
        logger.debug("Loading settings...")
        self.env_vars = load_env()
        self.config = load_config_from_env(env=self.env_vars.get("ENVIRONMENT"))
        logger.debug("Settings loaded.")


settings = Settings()
