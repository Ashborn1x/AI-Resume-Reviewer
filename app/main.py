from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from app.core.config import get_settings
from app.core.exception_handlers import register_exception_handlers
from app.core.logging import configure_logging
from app.middleware.request_logging import RequestLoggingMiddleware
from app.routers import health, web


def create_app() -> FastAPI:
    base_dir = Path(__file__).resolve().parent.parent
    settings = get_settings()
    configure_logging(settings.log_level)

    app = FastAPI(
        title=settings.app_name,
        debug=settings.app_debug,
    )
    app.mount("/static", StaticFiles(directory=str(base_dir / "static")), name="static")
    app.add_middleware(RequestLoggingMiddleware)
    app.include_router(web.router)
    app.include_router(health.router)
    register_exception_handlers(app)
    return app


app = create_app()
