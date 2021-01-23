import os
import time
from loguru import logger

from .config import BASE_DIR

log_path = os.path.join(BASE_DIR, 'log')

if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_run = os.path.join(log_path, f"FastAPI_run_{time.strftime('%Y-%m-%d')}.log")
format = "{time: YYYY-MM-DD HH:mm:ss } | {level} {name} {line}: {message}"
logger.add(log_path_run, format=format, enqueue=True, rotation="50 MB", retention="10 days", level="INFO")