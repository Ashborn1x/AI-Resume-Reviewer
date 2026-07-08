import json
import logging
import time
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from app.ai.base import AIProvider
from app.services.exceptions import AIResponseValidationError
from app.utils.json import extract_json_object

logger = logging.getLogger(__name__)
T = TypeVar("T", bound=BaseModel)


class AIService:
    def __init__(self, provider: AIProvider) -> None:
        self._provider = provider

    @property
    def provider_name(self) -> str:
        return self._provider.name

    @property
    def model_name(self) -> str:
        return self._provider.model_name

    async def generate_structured(self, *, prompt: str, response_model: type[T]) -> T:
        started_at = time.perf_counter()
        response_text = await self._provider.generate_json(prompt)
        latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.info(
            "ai_request_completed",
            extra={
                "provider": self.provider_name,
                "model": self.model_name,
                "latency_ms": latency_ms,
            },
        )

        try:
            payload = json.loads(response_text)
        except json.JSONDecodeError:
            payload = extract_json_object(response_text)

        try:
            return response_model.model_validate(payload)
        except ValidationError as exc:
            logger.warning(
                "ai_response_validation_failed",
                extra={"provider": self.provider_name, "model": self.model_name},
            )
            raise AIResponseValidationError("The AI returned malformed analysis data. Please try again.") from exc
