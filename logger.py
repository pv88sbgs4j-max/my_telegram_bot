import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    root = logging.getLogger()
    if root.handlers:
        return 
    
    formatter = logging.Formatter( "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    if not os.environ.get("RAILWAY_ENVIRONMENT"):
        os.makedirs("logs", exist_ok=True)
        file_handler = RotatingFileHandler(
            "logs/bot.log",
            maxBytes=10_000_000,  
            backupCount=5,
            encoding="utf-8"
            )   
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    root.setLevel(logging.DEBUG)