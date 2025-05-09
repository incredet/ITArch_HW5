import logging
import os

def setup_logging(log_file: str = 'logs/app.log') -> logging.Logger:
    """
    Configure root logger to output INFO+ logs to a file and console.
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    file_fmt = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_fmt)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_fmt)
    logger.addHandler(console_handler)

    return logger