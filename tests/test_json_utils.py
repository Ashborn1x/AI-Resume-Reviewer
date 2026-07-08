import pytest

from app.services.exceptions import AIResponseValidationError
from app.utils.json import extract_json_object


def test_extract_json_object_from_wrapped_text() -> None:
    payload = extract_json_object('prefix {"overall_score": 90} suffix')

    assert payload == {"overall_score": 90}


def test_extract_json_object_rejects_missing_json() -> None:
    with pytest.raises(AIResponseValidationError):
        extract_json_object("not json")
