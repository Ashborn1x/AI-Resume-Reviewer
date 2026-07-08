from pathlib import Path

from app.core.config import Settings
from app.services.exceptions import ResumeAnalyzerError


class PromptManager:
    def __init__(self, settings: Settings) -> None:
        self._prompt_dir = Path(settings.prompt_dir)

    def load(self, name: str) -> str:
        safe_name = Path(name).stem
        prompt_path = self._prompt_dir / f"{safe_name}.md"
        if not prompt_path.exists():
            raise ResumeAnalyzerError(f"Prompt not found: {safe_name}.", code="prompt_not_found")
        return prompt_path.read_text(encoding="utf-8")

    def render(self, name: str, **context: str) -> str:
        prompt = self.load(name)
        for key, value in context.items():
            prompt = prompt.replace(f"{{{{ {key} }}}}", value)
        return prompt
