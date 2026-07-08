import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.templates import templates
from app.schemas.errors import ErrorResponse
from app.services.exceptions import ResumeAnalyzerError

logger = logging.getLogger(__name__)


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(ResumeAnalyzerError)
    async def resume_analyzer_exception_handler(
        request: Request,
        exc: ResumeAnalyzerError,
    ) -> HTMLResponse | JSONResponse:
        logger.warning("application_error", extra={"error_code": exc.code, "path": request.url.path})
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorResponse(message=exc.message, code=exc.code).model_dump(),
            )
        return templates.TemplateResponse(
            request,
            "error.html",
            {"message": exc.message, "status_code": exc.status_code},
            status_code=exc.status_code,
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> HTMLResponse | JSONResponse:
        logger.warning("request_validation_error", extra={"path": request.url.path})
        message = "The submitted data is invalid. Please review your input and try again."
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=ErrorResponse(message=message, code="validation_error").model_dump(),
            )
        return templates.TemplateResponse(
            request,
            "error.html",
            {"message": message, "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException,
    ) -> HTMLResponse | JSONResponse:
        message = str(exc.detail) if exc.detail else "The requested resource could not be processed."
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=exc.status_code,
                content=ErrorResponse(message=message, code="http_error").model_dump(),
            )
        return templates.TemplateResponse(
            request,
            "error.html",
            {"message": message, "status_code": exc.status_code},
            status_code=exc.status_code,
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request,
        exc: Exception,
    ) -> HTMLResponse | JSONResponse:
        logger.exception("unhandled_error", extra={"path": request.url.path})
        message = "Something went wrong while processing your request."
        if request.url.path.startswith("/api"):
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=ErrorResponse(message=message, code="internal_error").model_dump(),
            )
        return templates.TemplateResponse(
            request,
            "error.html",
            {"message": message, "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
