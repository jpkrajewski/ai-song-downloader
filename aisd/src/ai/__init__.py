from aisd.src.ai.providers.base import Provider
from aisd.src.ai.providers.cohere import CohereProvider
from aisd.src.config import config

PROVIDERS = {"cohere": CohereProvider}


def get_provider() -> Provider:
    return PROVIDERS[config.AI_PROVIDER_TYPE](
        config.AI_PROVIDER_API_KEY, config.AI_PROVIDER_PROMPT_TEMPATE
    )
