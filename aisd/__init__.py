# Load logging configuration from logging.conf
import logging
import logging.config
import os
from importlib.metadata import version
from pathlib import Path
from typing import Final

LOGGING_CONF_DIR: Final[str] = str(Path(__file__).parents[0] / "logging.conf")

if os.getenv("AI_SD_DEBUG") is not None:
    logging.config.fileConfig(
        LOGGING_CONF_DIR,
        disable_existing_loggers=False,
    )
    logger = logging.getLogger(__name__)
    logger.debug(f"Logging configuration loaded. Version: {version(__package__)}")
