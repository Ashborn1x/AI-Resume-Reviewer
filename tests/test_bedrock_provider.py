from unittest.mock import Mock

import pytest

from app.ai.providers.bedrock import BedrockProvider
from app.services.exceptions import AIProviderError


@pytest.mark.asyncio
async def test_generate_json_returns_bedrock_text(mocker: Mock) -> None:
    client = Mock()
    client.converse.return_value = {
        "output": {"message": {"content": [{"text": '{"score": 85}'}, {"text": "\n"}]}}
    }
    mocker.patch("app.ai.providers.bedrock.boto3.client", return_value=client)
    provider = BedrockProvider(region_name="us-east-1", model_name="test-model", timeout_seconds=10)

    result = await provider.generate_json("Review this resume")

    assert result == '{"score": 85}'
    client.converse.assert_called_once_with(
        modelId="test-model",
        messages=[{"role": "user", "content": [{"text": "Review this resume"}]}],
        inferenceConfig={"temperature": 0.1},
    )


def test_extract_text_rejects_empty_bedrock_output() -> None:
    assert BedrockProvider._extract_text({"output": {"message": {"content": []}}}) == ""


def test_extract_error_details_reads_bedrock_client_error() -> None:
    exc = Mock()
    exc.response = {"Error": {"Code": "ValidationException", "Message": "Operation not allowed"}}

    assert BedrockProvider._extract_error_details(exc) == ("ValidationException", "Operation not allowed")


@pytest.mark.asyncio
async def test_generate_json_rejects_empty_bedrock_output(mocker: Mock) -> None:
    client = Mock()
    client.converse.return_value = {"output": {"message": {"content": []}}}
    mocker.patch("app.ai.providers.bedrock.boto3.client", return_value=client)
    provider = BedrockProvider(region_name="us-east-1", model_name="test-model", timeout_seconds=10)

    with pytest.raises(AIProviderError, match="empty response"):
        await provider.generate_json("Review this resume")
