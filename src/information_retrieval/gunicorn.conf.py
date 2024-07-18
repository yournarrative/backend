import multiprocessing
import os

bind = os.getenv("HOST") + ":" + os.getenv("PORT")
if os.environ.get("ENVIRONMENT") == "local":
    workers = 1
else:
    workers = 2
    # workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
reload = True
reload_engine = "auto"
timeout = 30
