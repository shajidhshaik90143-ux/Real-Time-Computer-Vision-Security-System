import logging
from pathlib import Path


def create_logger(log_directory):

    log_directory = Path(log_directory)

    log_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    log_file = log_directory / "security.log"

    logger = logging.getLogger(
        "security_system"
    )

    logger.setLevel(
        logging.INFO
    )

    if not logger.handlers:

        handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s"
        )

        handler.setFormatter(
            formatter
        )

        logger.addHandler(
            handler
        )

    return logger