"""
logger.py – Structured JSON logging for MiniVault API.
Provides:
- A custom JSONFormatter to log prompt-response pairs in JSONL format
- Rotating file handler to manage logs in logs/log.jsonl
"""
import logging
from logging.handlers import RotatingFileHandler
import json
from pathlib import Path
from datetime import datetime
import sys
import os

class JSONFormatter(logging.Formatter):
    """Custom formatter for structured JSON logs"""
    def format(self, record):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
        }
        
        if hasattr(record, 'prompt'):
            log_entry['prompt'] = record.prompt
        if hasattr(record, 'response'):
            log_entry['response'] = record.response
        
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry)

def configure_logger():
    """Configure the global logger with error handling"""
    try:
        # Ensure logs directory exists
        logs_dir = Path("logs")
        logs_dir.mkdir(exist_ok=True, mode=0o755)
        
        logger = logging.getLogger("logs")
        logger.setLevel(logging.INFO)
        
        # Rotating file handler (10MB x 5 backups)
        file_handler = RotatingFileHandler(
            filename=logs_dir/"log.jsonl",
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(JSONFormatter())
        
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger
        
    except Exception as e:
        print(f"CRITICAL: Failed to configure logging - {str(e)}", file=sys.stderr)
        sys.exit(1)

logger = configure_logger()

def log_interaction(prompt: str, response: str):
    """Log API interactions"""
    try:
        logger.info("API Interaction", extra={'prompt': prompt, 'response': response})

    except Exception as e:
        logger.error("Failed to log interaction", exc_info=True, extra={'error': str(e), 'prompt': prompt[:100]})
