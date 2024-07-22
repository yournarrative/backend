import multiprocessing
import os

from information_retrieval.utils.standard_logger import get_logger

logger = get_logger()

bind = os.getenv("HOST") + ":" + os.getenv("PORT")
if os.environ.get("ENVIRONMENT") == "local":
    workers = 1
else:
    workers = multiprocessing.cpu_count() * 2 + 1
logger.debug(f"Number of gunicorn workers: {workers}")
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
reload_engine = "auto"
timeout = 600
