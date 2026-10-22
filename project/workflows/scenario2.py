def get_scenario2_actions(failure_mode=None, endpoint="mock://tunisia/manufacturing_indicators"):
    return [
        {
            "type": "http_get_indicator",
            "endpoint": endpoint,
            "failure_mode": failure_mode,
        },
        {"type": "validate_indicator_json"},
        {"type": "transform_indicator_data"},
        {"type": "generate_indicator_report"},
    ]


def get_scenario2_objectives():
    return [
        "http_get_indicator",
        "validate_indicator_json",
        "transform_indicator_data",
        "generate_indicator_report",
    ]