import logging
import sys
from datetime import datetime


def get_logger(name="Framework"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Formatting: Timestamp | Level | Message
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        # Console Handler
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.addHandler(sh)

        # File Handler for CI Artifacts
        fh = logging.FileHandler(f"test-results/execution.log")
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger