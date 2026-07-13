from app.ai.base import AIProvider
from app.ai.providers.bedrock import BedrockProvider
from app.core.config import Settings


def create_ai_provider(settings: Settings) -> AIProvider:
    return BedrockProvider(
        region_name=settings.aws_region,
        model_name=settings.ai_model,
        timeout_seconds=settings.ai_timeout_seconds,
    )
