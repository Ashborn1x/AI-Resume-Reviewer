from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest

from app.schemas.uploads import StoredUpload
from app.services.exceptions import AIProviderError
from app.services.resume_analysis_service import ResumeAnalysisService


@pytest.mark.asyncio
async def test_resume_analysis_service_raises_when_ai_fails() -> None:
    analyzer = Mock()
    analyzer.provider_name = "aws-bedrock"
    analyzer.model_name = "anthropic.claude-3-5-haiku-20241022-v1:0"
    analyzer.analyze = AsyncMock(side_effect=AIProviderError("Operation not allowed"))

    parser = Mock()
    parser.extract_text = AsyncMock(
        return_value=(
            "Summary\n"
            "Experienced backend engineer building APIs and internal tools with Python, FastAPI, SQL, and AWS.\n"
            "Experience\n"
            "Led delivery of multiple services.\n"
            "Skills\n"
            "Python, FastAPI, SQL, AWS, Docker\n"
            "Education\n"
            "BS Computer Science\n"
        )
    )

    parser_factory = Mock()
    parser_factory.get_parser.return_value = parser

    service = ResumeAnalysisService(resume_analyzer=analyzer, parser_factory=parser_factory)
    upload = StoredUpload(
        original_filename="resume.pdf",
        stored_filename="resume.pdf",
        path=Path("resume.pdf"),
        content_type="application/pdf",
        size_bytes=1234,
        extension="pdf",
    )

    with pytest.raises(AIProviderError, match="Operation not allowed"):
        await service.analyze(upload)

    analyzer.analyze.assert_awaited_once()
    parser.extract_text.assert_awaited_once()
