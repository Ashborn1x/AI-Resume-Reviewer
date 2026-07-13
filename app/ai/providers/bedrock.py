import asyncio
import logging
from typing import Any

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

from app.ai.base import AIProvider
from app.services.exceptions import AIProviderError

logger = logging.getLogger(__name__)


class BedrockProvider(AIProvider):
    def __init__(self, *, region_name: str, model_name: str, timeout_seconds: int) -> None:
        self._model_name = model_name
        self._client = boto3.client(
            "bedrock-runtime",
            region_name=region_name,
            config=Config(
                connect_timeout=timeout_seconds,
                read_timeout=timeout_seconds,
                retries={"max_attempts": 3, "mode": "standard"},
            ),
        )

    @property
    def name(self) -> str:
        return "aws-bedrock"

    @property
    def model_name(self) -> str:
        return self._model_name

    async def generate_json(self, prompt: str) -> str:
        try:
            response = await asyncio.to_thread(
                self._client.converse,
                modelId=self._model_name,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"temperature": 0.1},
            )
        except (BotoCoreError, ClientError) as exc:
            logger.warning("bedrock_request_failed", extra={"model": self._model_name})
            raise AIProviderError(
                "The AWS Bedrock request failed. Verify AWS credentials, region, model access, and network connectivity."
            ) from exc

        generated = self._extract_text(response)
        if not generated:
            raise AIProviderError("AWS Bedrock returned an empty response.")
        return generated

    @staticmethod
    def _extract_text(response: dict[str, Any]) -> str:
        content = response.get("output", {}).get("message", {}).get("content", [])
        return "".join(
            block["text"] for block in content if isinstance(block, dict) and isinstance(block.get("text"), str)
        ).strip()
