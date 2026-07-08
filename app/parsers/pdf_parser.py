import asyncio
from pathlib import Path

from pypdf import PdfReader

from app.parsers.base import ResumeParser
from app.services.exceptions import ParsingError


class PdfResumeParser(ResumeParser):
    async def extract_text(self, path: Path) -> str:
        return await asyncio.to_thread(self._extract, path)

    def _extract(self, path: Path) -> str:
        try:
            reader = PdfReader(path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            raise ParsingError("Could not extract text from the PDF resume.") from exc
