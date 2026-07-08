import re


def clean_resume_text(text: str) -> str:
    without_control_chars = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", " ", text)
    return re.sub(r"[ \t]+", " ", without_control_chars).strip()


def normalize_resume_text(text: str) -> str:
    normalized_lines = [line.strip() for line in text.splitlines() if line.strip()]
    normalized = "\n".join(normalized_lines)
    return normalized[:20000]
