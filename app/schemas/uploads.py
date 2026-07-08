from pathlib import Path

from pydantic import BaseModel


class StoredUpload(BaseModel):
    original_filename: str
    stored_filename: str
    path: Path
    content_type: str
    size_bytes: int
    extension: str
