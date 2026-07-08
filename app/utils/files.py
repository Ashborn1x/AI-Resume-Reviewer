import re
from pathlib import Path

from app.services.exceptions import UploadValidationError


def sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    sanitized = re.sub(r"[^A-Za-z0-9._-]", "_", name).strip("._")
    return sanitized or "resume"


def get_safe_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def validate_file_signature(content: bytes, extension: str) -> None:
    if extension == "pdf" and not content.startswith(b"%PDF-"):
        raise UploadValidationError("The uploaded file does not appear to be a valid PDF.")
    if extension == "docx" and not content.startswith(b"PK"):
        raise UploadValidationError("The uploaded file does not appear to be a valid DOCX.")
    if extension == "txt" and b"\x00" in content[:1024]:
        raise UploadValidationError("The uploaded file does not appear to be a valid text file.")
