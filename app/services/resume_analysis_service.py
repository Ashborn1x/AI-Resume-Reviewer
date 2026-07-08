import logging
import time

from app.ai.features.resume_analyzer import ResumeAnalyzer
from app.parsers.parser_factory import ResumeParserFactory
from app.schemas.analysis import ResumeAnalysisResult
from app.schemas.uploads import StoredUpload
from app.services.exceptions import ParsingError
from app.utils.text import clean_resume_text, normalize_resume_text

logger = logging.getLogger(__name__)


class ResumeAnalysisService:
    def __init__(
        self,
        *,
        resume_analyzer: ResumeAnalyzer,
        parser_factory: ResumeParserFactory,
    ) -> None:
        self._resume_analyzer = resume_analyzer
        self._parser_factory = parser_factory

    @property
    def provider_name(self) -> str:
        return self._resume_analyzer.provider_name

    @property
    def model_name(self) -> str:
        return self._resume_analyzer.model_name

    async def analyze(self, upload: StoredUpload) -> ResumeAnalysisResult:
        started_at = time.perf_counter()
        parser = self._parser_factory.get_parser(upload.extension)
        raw_text = await parser.extract_text(upload.path)
        cleaned_text = clean_resume_text(raw_text)
        normalized_text = normalize_resume_text(cleaned_text)

        if len(normalized_text) < 100:
            raise ParsingError("The resume text could not be extracted clearly enough for analysis.")

        analysis = await self._resume_analyzer.analyze(normalized_text)

        duration_ms = round((time.perf_counter() - started_at) * 1000, 2)
        logger.info(
            "resume_analysis_completed",
            extra={
                "provider": self.provider_name,
                "model": self.model_name,
                "duration_ms": duration_ms,
                "text_length": len(normalized_text),
            },
        )
        return analysis
