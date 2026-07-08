from app.ai.ai_service import AIService
from app.prompts.prompt_manager import PromptManager
from app.schemas.analysis import ResumeAnalysisResult
from app.services.exceptions import AIResponseValidationError


class ResumeAnalyzer:
    def __init__(self, *, ai_service: AIService, prompt_manager: PromptManager) -> None:
        self._ai_service = ai_service
        self._prompt_manager = prompt_manager

    @property
    def provider_name(self) -> str:
        return self._ai_service.provider_name

    @property
    def model_name(self) -> str:
        return self._ai_service.model_name

    async def analyze(self, resume_text: str) -> ResumeAnalysisResult:
        prompt = self._prompt_manager.render(
            "resume_analysis",
            resume_text=resume_text,
        )
        analysis = await self._ai_service.generate_structured(
            prompt=prompt,
            response_model=ResumeAnalysisResult,
        )
        if not isinstance(analysis, ResumeAnalysisResult):
            raise AIResponseValidationError("The AI response did not match the expected resume analysis schema.")
        return analysis
