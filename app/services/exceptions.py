from fastapi import status


class ResumeAnalyzerError(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str = "application_error",
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status_code = status_code


class UploadValidationError(ResumeAnalyzerError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="upload_validation_error", status_code=status.HTTP_400_BAD_REQUEST)


class ParsingError(ResumeAnalyzerError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="parsing_error", status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)


class AIProviderError(ResumeAnalyzerError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="ai_provider_error", status_code=status.HTTP_502_BAD_GATEWAY)


class AIResponseValidationError(ResumeAnalyzerError):
    def __init__(self, message: str) -> None:
        super().__init__(message, code="ai_response_validation_error", status_code=status.HTTP_502_BAD_GATEWAY)
