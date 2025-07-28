import logging
import sys

from app.core.config import settings


def setup_logging() -> None:
    """Setup logging configuration for the application."""

    # Create a custom formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Set log level based on environment
    if settings.ENVIRONMENT == "local":
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)

    # Configure specific loggers
    loggers_to_configure = [
        "uvicorn",
        "uvicorn.error",
        "uvicorn.access",
        "fastapi",
        # "sqlalchemy.engine",
        "alembic",
    ]

    for logger_name in loggers_to_configure:
        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)
        logger.addHandler(console_handler)
        logger.propagate = False

    # Create application logger
    app_logger = logging.getLogger("app")
    app_logger.setLevel(log_level)
    app_logger.addHandler(console_handler)
    app_logger.propagate = False

    # Log startup message
    app_logger.info(f"Logging configured for environment: {settings.ENVIRONMENT}")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance for the given name."""
    return logging.getLogger(f"app.{name}")
