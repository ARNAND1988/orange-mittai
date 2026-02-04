import logging
import sys

LOG_FORMAT = (
    "%(asctime)s | "
    "%(levelname)s | "
    "%(name)s | "
    "%(message)s"
)

def setup_logging():
    """
    Global logging configuration
    """

    logging.basicConfig(
        level=logging.INFO,
        format=LOG_FORMAT,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ],
        force=True,  # 🔥 OVERRIDES uvicorn default logging
    )

    # Reduce noise from uvicorn internals
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.error").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)

    # SQLAlchemy (optional)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
