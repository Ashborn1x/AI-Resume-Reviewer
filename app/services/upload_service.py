import asyncio
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import Settings
from app.schemas.uploads import StoredUpload
from app.services.exceptions import UploadValidationError
from app.utils.files import get_safe_extension, sanitize_filename, validate_file_signature

logger = logging.getLogger(__name__)


class UploadService:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def validate_and_store(self, file: UploadFile) -> StoredUpload:
        if not file.filename:
            raise UploadValidationError("Please choose a resume file to upload.")

        original_filename = sanitize_filename(file.filename)
        extension = get_safe_extension(original_filename)
        if extension not in self._settings.allowed_upload_extensions:
            allowed = ", ".join(sorted(self._settings.allowed_upload_extensions))
            raise UploadValidationError(f"Unsupported file type. Allowed formats: {allowed}.")

        content = await file.read(self._settings.max_upload_size_bytes + 1)
        if len(content) > self._settings.max_upload_size_bytes:
            raise UploadValidationError(
                f"File is too large. Maximum size is {self._settings.max_upload_size_mb} MB."
            )
        if not content:
            raise UploadValidationError("The uploaded file is empty.")
        validate_file_signature(content, extension)

        upload_dir = Path(self._settings.upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)
        stored_filename = f"{uuid4().hex}.{extension}"
        stored_path = upload_dir / stored_filename
        await asyncio.to_thread(stored_path.write_bytes, content)

        logger.info(
            "resume_uploaded",
            extra={
                "original_filename": original_filename,
                "stored_filename": stored_filename,
                "content_type": file.content_type or "application/octet-stream",
                "size_bytes": len(content),
            },
        )
        return StoredUpload(
            original_filename=original_filename,
            stored_filename=stored_filename,
            path=stored_path,
            content_type=file.content_type or "application/octet-stream",
            size_bytes=len(content),
            extension=extension,
        )
