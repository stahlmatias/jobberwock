import logging
import os

def setup_logger():
    os.makedirs("logs", exist_ok=True)

    log_format = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    log_level = logging.INFO

    logger = logging.getLogger()
    logger.setLevel(log_level)

    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter(log_format))
    logger.addHandler(ch)

    fh = logging.FileHandler("logs/jobberwocky.log", mode="a", encoding="utf-8")
    fh.setFormatter(logging.Formatter(log_format))
    logger.addHandler(fh)