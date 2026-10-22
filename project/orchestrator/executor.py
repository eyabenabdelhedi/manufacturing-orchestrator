from tools.csv_tools import read_csv_file
from tools.kpi_tools import compute_kpis
from tools.report_tools import generate_json_report, generate_indicator_report
from tools.http_tools import http_get_indicator
from tools.indicator_tools import validate_indicator_json, transform_indicator_data
from orchestrator.critic import critic_check


def execute_action(action: dict, context: dict):
    action_type = action["type"]

    if action_type == "read_csv":
        path = action["path"]
        result = read_csv_file(path)

        if isinstance(result, dict) and "error" in result:
            return {"ok": False, "error": result["error"]}

        context["df"] = result
        return {"ok": True, "result": f"CSV loaded: {len(result)} rows"}

    if action_type == "compute_kpis":
        if "df" not in context:
            return {"ok": False, "error": "Missing dataframe in context"}

        kpis = compute_kpis(context["df"])

        if "error" in kpis:
            return {"ok": False, "error": kpis["error"]}

        context["kpis"] = kpis
        return {"ok": True, "result": kpis}

    if action_type == "critic_check":
        if "kpis" not in context:
            return {"ok": False, "error": "Missing KPIs in context"}

        critic_result = critic_check(context["kpis"])
        context["critic_result"] = critic_result

        return {"ok": critic_result["approved"], "result": critic_result}

    if action_type == "generate_report":
        if "kpis" not in context:
            return {"ok": False, "error": "Missing KPIs in context"}

        report = generate_json_report(context["kpis"])

        if "error" in report:
            return {"ok": False, "error": report["error"]}

        context["report"] = report
        return {"ok": True, "result": report}

    if action_type == "http_get_indicator":
        endpoint = action["endpoint"]
        failure_mode = action.get("failure_mode")

        result = http_get_indicator(endpoint, failure_mode)

        if "error" in result:
            return {"ok": False, "error": result["error"]}

        context["indicator_data"] = result
        return {"ok": True, "result": result}

    if action_type == "validate_indicator_json":
        if "indicator_data" not in context:
            return {"ok": False, "error": "Missing indicator data in context"}

        validation = validate_indicator_json(context["indicator_data"])

        if not validation["ok"]:
            return {"ok": False, "error": validation["error"]}

        context["indicator_validation"] = validation
        return {"ok": True, "result": validation}

    if action_type == "transform_indicator_data":
        if "indicator_data" not in context:
            return {"ok": False, "error": "Missing indicator data in context"}

        summary = transform_indicator_data(context["indicator_data"])

        if "error" in summary:
            return {"ok": False, "error": summary["error"]}

        context["indicator_summary"] = summary
        return {"ok": True, "result": summary}

    if action_type == "generate_indicator_report":
        if "indicator_summary" not in context:
            return {"ok": False, "error": "Missing indicator summary in context"}

        report = generate_indicator_report(context["indicator_summary"])

        if "error" in report:
            return {"ok": False, "error": report["error"]}

        context["indicator_report"] = report
        return {"ok": True, "result": report}

    return {"ok": False, "error": f"Unknown action type: {action_type}"}