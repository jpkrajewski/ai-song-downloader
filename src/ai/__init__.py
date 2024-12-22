from ai_song_downloader.src.ai.providers.base import Provider
from ai_song_downloader.src.ai.providers.cohere import CohereProvider
from ai_song_downloader.src.config import config

PROVIDERS = {"cohere": CohereProvider}


def get_provider() -> Provider:
    return PROVIDERS[config.AI_PROVIDER_TYPE](
        config.AI_PROVIDER_API_KEY, config.AI_PROVIDER_PROMPT_TEMPATE
    )
