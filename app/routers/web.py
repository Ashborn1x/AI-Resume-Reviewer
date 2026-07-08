from typing import Annotated

from fastapi import APIRouter, Depends, File, Request, UploadFile
from fastapi.responses import HTMLResponse

from app.core.templates import templates
from app.repositories.analysis_repository import AnalysisRepository
from app.routers.dependencies import (
    get_analysis_repository,
    get_resume_analysis_service,
    get_upload_service,
)
from app.services.resume_analysis_service import ResumeAnalysisService
from app.services.upload_service import UploadService

router = APIRouter(tags=["web"])


@router.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@router.post("/analyze", response_class=HTMLResponse)
async def analyze_resume(
    request: Request,
    upload_service: Annotated[UploadService, Depends(get_upload_service)],
    analysis_service: Annotated[ResumeAnalysisService, Depends(get_resume_analysis_service)],
    repository: Annotated[AnalysisRepository, Depends(get_analysis_repository)],
    file: UploadFile = File(...),
) -> HTMLResponse:
    upload = await upload_service.validate_and_store(file)
    analysis = await analysis_service.analyze(upload)
    record = repository.create(
        original_filename=upload.original_filename,
        stored_filename=upload.stored_filename,
        content_type=upload.content_type,
        file_size_bytes=upload.size_bytes,
        provider=analysis_service.provider_name,
        model_name=analysis_service.model_name,
        analysis=analysis,
    )
    return templates.TemplateResponse(
        request,
        "result.html",
        {
            "record": record,
            "analysis": analysis,
            "feedback_sections": [
                ("Summary", analysis.summary_feedback),
                ("Experience", analysis.experience_feedback),
                ("Projects", analysis.projects_feedback),
                ("Skills", analysis.skills_feedback),
                ("Education", analysis.education_feedback),
                ("Recruiter Feedback", analysis.recruiter_feedback),
            ],
            "item_groups": [
                ("Strengths", analysis.strengths),
                ("Weaknesses", analysis.weaknesses),
                ("Missing Skills", analysis.missing_skills),
            ],
        },
    )
