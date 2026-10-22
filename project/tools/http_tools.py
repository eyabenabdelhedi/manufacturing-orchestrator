import time
import json
import os

ALLOWED_ENDPOINTS = {
    "mock://tunisia/manufacturing_indicators",
    "mock://tunisia/manufacturing_indicators_backup",
}

ENDPOINT_DATA_FILES = {
    "mock://tunisia/manufacturing_indicators":
        "data_synthetic/manufacturing_indicators.json",
    "mock://tunisia/manufacturing_indicators_backup":
        "data_synthetic/manufacturing_indicators.json",
}


def http_get_indicator(endpoint, failure_mode=None):
    if endpoint not in ALLOWED_ENDPOINTS:
        return {"error": "Endpoint not allowed"}

    if failure_mode == "timeout":
        time.sleep(1)
        return {"error": "Request timeout"}

    if failure_mode == "429":
        return {"error": "HTTP 429 rate limit"}

    if failure_mode == "bad_json":
        return {
            "country": "Tunisia",
            "sector": "manufacturing",
            "indicator": "manufacturing_value_added_index"
        }

    if failure_mode == "transform_error":
        return {
            "country": "Tunisia",
            "sector": "manufacturing",
            "indicator": "manufacturing_value_added_index",
            "series": [
                {"year": 2021, "value": 0},
                {"year": 2022, "value": 101.2}
            ]
        }

    data_file = ENDPOINT_DATA_FILES[endpoint]
    try:
        with open(data_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"error": f"Data file not found: {data_file}"}
    except json.JSONDecodeError as e:
        return {"error": f"Invalid JSON in data file: {str(e)}"}
