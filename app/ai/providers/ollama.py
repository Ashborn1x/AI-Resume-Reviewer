import logging

import httpx

from app.ai.base import AIProvider
from app.services.exceptions import AIProviderError

logger = logging.getLogger(__name__)


class OllamaProvider(AIProvider):
    def __init__(self, *, base_url: str, model_name: str, timeout_seconds: int) -> None:
        self._base_url = base_url.rstrip("/")
        self._model_name = model_name
        self._timeout_seconds = timeout_seconds

    @property
    def name(self) -> str:
        return "ollama"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def generate_json(self, prompt: str) -> str:
        payload = {
            "model": self._model_name,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.1,
            },
        }
        try:
            async with httpx.AsyncClient(timeout=self._timeout_seconds) as client:
                response = await client.post(f"{self._base_url}/api/generate", json=payload)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            logger.warning("ollama_request_failed", extra={"model": self._model_name})
            raise AIProviderError("Could not reach the local Ollama provider. Check that Ollama is running.") from exc

        data = response.json()
        generated = data.get("response")
        if not isinstance(generated, str) or not generated.strip():
            raise AIProviderError("The local AI provider returned an empty response.")
        return generated
