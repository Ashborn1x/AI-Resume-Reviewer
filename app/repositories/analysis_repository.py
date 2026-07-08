from sqlalchemy.orm import Session

from app.models.analysis import AnalysisResult
from app.schemas.analysis import ResumeAnalysisResult


class AnalysisRepository:
    def __init__(self, db: Session) -> None:
        self._db = db

    def create(
        self,
        *,
        original_filename: str,
        stored_filename: str,
        content_type: str,
        file_size_bytes: int,
        provider: str,
        model_name: str,
        analysis: ResumeAnalysisResult,
    ) -> AnalysisResult:
        record = AnalysisResult(
            original_filename=original_filename,
            stored_filename=stored_filename,
            content_type=content_type,
            file_size_bytes=file_size_bytes,
            provider=provider,
            model_name=model_name,
            overall_score=analysis.overall_score,
            ats_score=analysis.ats_score,
            profession=analysis.profession,
            result_json=analysis.model_dump_json(),
        )
        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record
