import logging
import os
from logging.handlers import TimedRotatingFileHandler
import time


def init_app(app):
    log_directory = os.path.join(os.getcwd(), 'storage/logs')

    # Log to file
    today = time.strftime('%Y%m%d')
    log_file_path = os.path.join(log_directory, f"app-{today}.log")

    # Create log handler and set log level
    handler = TimedRotatingFileHandler(log_file_path, when='midnight', interval=1, backupCount=30)
    handler.setLevel(logging.INFO)

    # Create log format
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    # Add handler to Flask application logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)