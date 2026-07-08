import pytest

from app.services.exceptions import UploadValidationError
from app.utils.files import get_safe_extension, sanitize_filename, validate_file_signature


def test_sanitize_filename_removes_path_and_unsafe_characters() -> None:
    assert sanitize_filename("../bad resume!.pdf") == "bad_resume_.pdf"


def test_get_safe_extension_normalizes_extension() -> None:
    assert get_safe_extension("resume.PDF") == "pdf"


def test_validate_file_signature_rejects_invalid_pdf() -> None:
    with pytest.raises(UploadValidationError):
        validate_file_signature(b"not a pdf", "pdf")
