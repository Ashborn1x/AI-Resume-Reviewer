from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.ai.ai_service import AIService
from app.ai.features.resume_analyzer import ResumeAnalyzer
from app.ai.provider_factory import create_ai_provider
from app.core.config import Settings, get_settings
from app.core.database import get_db_session
from app.parsers.parser_factory import ResumeParserFactory
from app.prompts.prompt_manager import PromptManager
from app.repositories.analysis_repository import AnalysisRepository
from app.services.resume_analysis_service import ResumeAnalysisService
from app.services.upload_service import UploadService

SettingsDep = Annotated[Settings, Depends(get_settings)]
DbSessionDep = Annotated[Session, Depends(get_db_session)]


def get_upload_service(settings: SettingsDep) -> UploadService:
    return UploadService(settings)


def get_prompt_manager(settings: SettingsDep) -> PromptManager:
    return PromptManager(settings)


def get_ai_service(settings: SettingsDep) -> AIService:
    return AIService(create_ai_provider(settings))


def get_parser_factory() -> ResumeParserFactory:
    return ResumeParserFactory()


def get_resume_analyzer(
    ai_service: Annotated[AIService, Depends(get_ai_service)],
    prompt_manager: Annotated[PromptManager, Depends(get_prompt_manager)],
) -> ResumeAnalyzer:
    return ResumeAnalyzer(ai_service=ai_service, prompt_manager=prompt_manager)


def get_resume_analysis_service(
    resume_analyzer: Annotated[ResumeAnalyzer, Depends(get_resume_analyzer)],
    parser_factory: Annotated[ResumeParserFactory, Depends(get_parser_factory)],
) -> ResumeAnalysisService:
    return ResumeAnalysisService(
        resume_analyzer=resume_analyzer,
        parser_factory=parser_factory,
    )


def get_analysis_repository(db: DbSessionDep) -> AnalysisRepository:
    return AnalysisRepository(db)
