import json
from datetime import datetime
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

def log_interaction(prompt, response):
    """
    Logs the prompt and response to logs/log.jsonl in JSONL format.
    Each line is a separate JSON object.
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "response": response
    }
    with open("logs/log.jsonl", "a") as log_file:
        json.dump(log_entry, log_file)
        log_file.write("\n")
