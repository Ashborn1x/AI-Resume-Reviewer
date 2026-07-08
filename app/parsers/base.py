from abc import ABC, abstractmethod
from pathlib import Path


class ResumeParser(ABC):
    @abstractmethod
    async def extract_text(self, path: Path) -> str:
        raise NotImplementedError
