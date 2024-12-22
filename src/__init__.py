import logging
import os

# Define a logs directory
LOG_DIR = os.path.join(os.path.dirname(__file__), "../logs")
os.makedirs(LOG_DIR, exist_ok=True)  # Ensure the logs directory exists

# Define the log file path
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Set up basic logging configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filemode="a",  # Append to the log file
)

# Example logger
logger = logging.getLogger(__name__)
logger.debug("Logger initialized.")
