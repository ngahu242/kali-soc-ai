import datetime
import os

LOG_FILE = "logs/soc_ai.log"


def log(event, level="INFO"):
    os.makedirs("logs", exist_ok=True)

    timestamp = datetime.datetime.now().isoformat()

    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{level}] {event}\n")