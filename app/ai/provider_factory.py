from app.ai.base import AIProvider
from app.ai.providers.ollama import OllamaProvider
from app.core.config import Settings
from app.services.exceptions import AIProviderError


def create_ai_provider(settings: Settings) -> AIProvider:
    provider_name = settings.ai_provider.lower()
    if provider_name == "ollama":
        return OllamaProvider(
            base_url=settings.ollama_base_url,
            model_name=settings.ai_model,
            timeout_seconds=settings.ai_timeout_seconds,
        )
    raise AIProviderError(f"Unsupported AI provider configured: {settings.ai_provider}.")
