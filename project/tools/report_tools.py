import json


def generate_json_report(kpis, output_path="logs/report.json"):
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(kpis, f, indent=4)
        return {"success": True, "path": output_path}
    except Exception as e:
        return {"error": str(e)}
def generate_indicator_report(indicator_summary, output_path="logs/scenario2_report.json"):
    import json

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(indicator_summary, f, indent=4)
        return {"success": True, "path": output_path}
    except Exception as e:
        return {"error": str(e)}