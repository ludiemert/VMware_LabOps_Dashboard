"""
JSON Lines logger for VMware LabOps.

Each event is written as ONE line of JSON at the end of a log file.
Later we can read this file to build reports, alerts and dashboard tables.
"""

# json converts Python dictionaries into JSON text.
import json

# datetime gives us the current date and time.
# timezone lets us store the time in UTC (a universal standard).
from datetime import datetime, timezone

# Path builds file paths that work on Windows, Linux and macOS.
from pathlib import Path

# __file__ is this file (src/logger.py).
# .resolve() makes the path absolute, .parent goes up one folder:
#   src/logger.py -> src -> project root.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# All health-check events go into this file (it is created automatically).
LOG_FILE = PROJECT_ROOT / "logs" / "health_checks.jsonl"


def write_log_event(event_type: str, status: str, details: dict) -> None:
    """Add one event as a new line at the end of the log file."""

    # Create the "logs" folder if it does not exist yet.
    # parents=True creates missing parent folders; exist_ok=True avoids
    # an error when the folder already exists.
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # The event is a normal Python dictionary.
    event = {
        # isoformat() writes the date like 2026-11-13T17:30:05+00:00.
        "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "event_type": event_type,  # what happened, e.g. "health_check"
        "status": status,  # how it went, e.g. "ok" or "error"
        "details": details,  # extra data (metrics or the error message)
    }

    # "a" means append: add at the end without erasing older events.
    with LOG_FILE.open("a", encoding="utf-8") as log_file:
        # json.dumps turns the dictionary into one line of JSON text.
        # "\n" ends the line, so the next event starts on a new line.
        log_file.write(json.dumps(event) + "\n")
