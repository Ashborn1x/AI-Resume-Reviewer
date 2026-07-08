import asyncio
from pathlib import Path

from app.parsers.base import ResumeParser
from app.services.exceptions import ParsingError


class TxtResumeParser(ResumeParser):
    async def extract_text(self, path: Path) -> str:
        return await asyncio.to_thread(self._extract, path)

    def _extract(self, path: Path) -> str:
        try:
            return path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            raise ParsingError("Could not read the TXT resume.") from exc
