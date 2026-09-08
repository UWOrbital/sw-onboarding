import logging

from fastapi import FastAPI
from loguru import logger

from app.api.routes.commands import commands_router
from app.api.routes.main_commands import main_commands_router
from app.config.env_settings.cors_config import add_cors_middleware


def setup_routes(app: FastAPI) -> None:
    """Adds the routes to the app"""
    base_prefix = "/api"

    app.include_router(commands_router, prefix=f"{base_prefix}/commands")
    app.include_router(main_commands_router, prefix=f"{base_prefix}/main-commands")


def setup_middlewares(app: FastAPI) -> None:
    """Adds the middlewares to the app"""
    add_cors_middleware(app)


def setup_logging() -> None:
    """Sets all logs from SQLAlchemy to the custom logger level VERBOSE"""
    verbose_level = 15  # DEBUG=10,  INFO=20
    logger.level("VERBOSE", no=verbose_level, color="<blue>")

    class SQLAlchemyHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            logger.log("VERBOSE", record.getMessage())

    sqlalchemy_logger = logging.getLogger("sqlalchemy.engine")
    sqlalchemy_logger.setLevel(verbose_level)
    sqlalchemy_logger.addHandler(SQLAlchemyHandler())
    sqlalchemy_logger.propagate = False
