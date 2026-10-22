import json
import os
import re
import uuid
import threading
import contextvars
from datetime import datetime

LOG_FILE = "logs/run_log.jsonl"

_current_run_id = contextvars.ContextVar("run_id", default=None)
_log_lock = threading.Lock()


def start_run(run_id=None):
    if run_id is None:
        run_id = str(uuid.uuid4())
    _current_run_id.set(run_id)
    return run_id


def get_run_id():
    run_id = _current_run_id.get()
    if run_id is None:
        run_id = start_run()
    return run_id


def redact_value(value):
    if isinstance(value, str):
        value = re.sub(r"C:\\Users\\[^\\]+", "<USER_PATH>", value)
        return value

    if isinstance(value, dict):
        redacted = {}
        for key, val in value.items():
            if key.lower() in {"token", "api_key", "secret", "password"}:
                redacted[key] = "***REDACTED***"
            else:
                redacted[key] = redact_value(val)
        return redacted

    if isinstance(value, list):
        return [redact_value(item) for item in value]

    return value


def log_event(event_type, details, log_path=LOG_FILE):
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    event = {
        "timestamp": datetime.utcnow().isoformat(),
        "run_id": get_run_id(),
        "event_type": event_type,
        "details": redact_value(details),
    }

    with _log_lock:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, default=str) + "\n")