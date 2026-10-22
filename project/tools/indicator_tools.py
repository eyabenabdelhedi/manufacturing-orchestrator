def validate_indicator_json(data):
    required_keys = ["country", "sector", "indicator", "series"]

    for key in required_keys:
        if key not in data:
            return {"ok": False, "error": f"Missing key: {key}"}

    if data["country"] != "Tunisia":
        return {"ok": False, "error": "Country must be Tunisia"}

    if not isinstance(data["series"], list) or len(data["series"]) == 0:
        return {"ok": False, "error": "Series must be a non-empty list"}

    for item in data["series"]:
        if "year" not in item or "value" not in item:
            return {"ok": False, "error": "Each series item must contain year and value"}

    return {"ok": True}


def transform_indicator_data(data):
    series = data["series"]

    first = series[0]["value"]
    last = series[-1]["value"]

    if first == 0:
        return {"error": "Transformation error: baseline value cannot be zero"}

    growth = ((last - first) / first) * 100

    return {
        "country": data["country"],
        "sector": data["sector"],
        "indicator": data["indicator"],
        "latest_year": series[-1]["year"],
        "latest_value": last,
        "growth_percent": round(growth, 2),
        "chart_ready_series": series,
    }