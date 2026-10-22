import os

ALLOWED_BASE_DIR = os.path.abspath("data_synthetic")
ALLOWED_EXTENSION = ".csv"


def is_safe_path(path: str) -> bool:
    abs_path = os.path.abspath(path)
    return abs_path.startswith(ALLOWED_BASE_DIR)


def is_csv_file(path: str) -> bool:
    return path.lower().endswith(ALLOWED_EXTENSION)


def validate_csv_path(path: str):
    if not is_csv_file(path):
        return {"ok": False, "error": "Only CSV files are allowed."}

    if not is_safe_path(path):
        return {"ok": False, "error": "Path is outside allowed directory."}

    if not os.path.exists(path):
        return {"ok": False, "error": "File does not exist."}

    return {"ok": True}