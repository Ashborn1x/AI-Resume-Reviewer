from app.utils.text import clean_resume_text, normalize_resume_text


def test_clean_resume_text_removes_control_characters() -> None:
    assert clean_resume_text("Hello\x00   World") == "Hello World"


def test_normalize_resume_text_removes_blank_lines() -> None:
    assert normalize_resume_text(" A \n\n B ") == "A\nB"
