import json

from app.services.exceptions import AIResponseValidationError


def extract_json_object(text: str) -> dict[str, object]:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise AIResponseValidationError("The AI response did not contain valid JSON.")

    try:
        payload = json.loads(text[start : end + 1])
    except json.JSONDecodeError as exc:
        raise AIResponseValidationError("The AI response contained malformed JSON.") from exc

    if not isinstance(payload, dict):
        raise AIResponseValidationError("The AI response must be a JSON object.")
    return payload
