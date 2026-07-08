import asyncio
from pathlib import Path

from docx import Document

from app.parsers.base import ResumeParser
from app.services.exceptions import ParsingError


class DocxResumeParser(ResumeParser):
    async def extract_text(self, path: Path) -> str:
        return await asyncio.to_thread(self._extract, path)

    def _extract(self, path: Path) -> str:
        try:
            document = Document(path)
            return "\n".join(paragraph.text for paragraph in document.paragraphs if paragraph.text.strip())
        except Exception as exc:
            raise ParsingError("Could not extract text from the DOCX resume.") from exc
