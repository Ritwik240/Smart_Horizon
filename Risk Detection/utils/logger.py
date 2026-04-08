# utils/logger.py

import logging
import sys

def get_logger(name: str):
    """
    Returns a configured logger with console output.
    Ensures multiple handlers are not added if called multiple times.
    """
    logger = logging.getLogger(name)
    
    # Avoid adding multiple handlers if logger already has one
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        # Console handler
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(logging.INFO)

        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        ch.setFormatter(formatter)

        logger.addHandler(ch)

        # Optional: Prevent propagation to root logger to avoid duplicate logs
        logger.propagate = False

    return logger