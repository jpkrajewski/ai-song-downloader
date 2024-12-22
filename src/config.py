import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass
class Config:
    AI_PROVIDER_TYPE: str = "cohere"
    AI_PROVIDER_API_KEY: str = ""
    AI_PROVIDER_PROMPT_TEMPATE: str = "Please provide a list of 50 songs that are good for DJ mixing and remixing, similar to the style or vibe of the following prompt: {}. The list should contain song titles only, with one song per line. Do not include any numbering or additional information—just the song titles separated by a newline character (\n)"
    YTDLP_MIN_VIEWS: int = 50_000


def load_config():
    load_dotenv()
    return Config(
        AI_PROVIDER_TYPE=os.getenv("AI_PROVIDER_TYPE", Config.AI_PROVIDER_TYPE),
        AI_PROVIDER_API_KEY=os.getenv(
            "AI_PROVIDER_API_KEY", Config.AI_PROVIDER_API_KEY
        ),
        AI_PROVIDER_PROMPT_TEMPATE=os.getenv(
            "AI_PROVIDER_PROMPT_TEMPATE", Config.AI_PROVIDER_PROMPT_TEMPATE
        ),
        YTDLP_MIN_VIEWS=os.getenv("YTDLP_MIN_VIEWS", Config.YTDLP_MIN_VIEWS),
    )


config = load_config()
