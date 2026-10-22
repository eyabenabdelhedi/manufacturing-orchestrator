import os
import json
import tkinter as tk
from tkinter import ttk

from workflows.scenario1 import get_scenario1_actions, get_scenario1_objectives
from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop
from orchestrator.run_manager import start_run, log_event
from orchestrator.dp_planner import dp_backtracking_plan, get_cache_stats


LOG_FILE = "logs/run_log.jsonl"


def read_log_events():
    if not os.path.exists(LOG_FILE):
        return []

    events = []
    with open(LOG_FILE, "r", encoding="utf-8") as file:
        for line in file:
            try:
                events.append(json.loads(line))
            except Exception:
                pass

    return events


def read_recent_logs(limit=10):
    events = read_log_events()[-limit:]

    if not events:
        return "No logs available."

    lines = []
    for event in events:
        timestamp = event.get("timestamp")
        run_id = event.get("run_id")
        event_type = event.get("event_type")
        lines.append(f"{timestamp} | {run_id} | {event_type}")

    return "\n".join(lines)


def format_plan(plan):
    if not plan:
        return "No plan available."

    lines = []
    for index, action in enumerate(plan, start=1):
        lines.append(f"{index}. {action['type']}")

    return "\n".join(lines)


def format_result(result):
    if not result:
        return "No result available."

    if not result["success"]:
        return json.dumps(
            {
                "status": "failed",
                "error": result.get("error"),
                "context": result.get("context", {}),
            },
            indent=2,
            default=str,
        )

    context = result["context"]
    output = {"status": "success"}

    if "kpis" in context:
        output["kpis"] = context["kpis"]

    if "critic_result" in context:
        output["critic"] = context["critic_result"]

    if "report" in context:
        output["report"] = context["report"]

    if "indicator_summary" in context:
        output["indicator_summary"] = context["indicator_summary"]

    if "indicator_report" in context:
        output["indicator_report"] = context["indicator_report"]

    return json.dumps(output, indent=2, default=str)


def build_timeline(plan, result):
    if not plan:
        return "No timeline available."

    lines = []

    for index, action in enumerate(plan, start=1):
        tool = action["type"]

        lines.append(f"Step {index}: {tool}")
        lines.append("Plan: tool selected")
        lines.append("Act: tool executed")
        lines.append("Observe: result stored")

        if tool in {"critic_check", "validate_indicator_json"}:
            lines.append("Critique: output validated")
        else:
            lines.append("Critique: constraints checked")

        lines.append("")

    if result:
        if result["success"]:
            lines.append("Final status: success")
        else:
            lines.append("Final status: failed")
            lines.append(f"Reason: {result.get('error')}")

    return "\n".join(lines)


def build_tool_inspector(plan, result):
    if not plan:
        return "No tool calls available."

    context = result.get("context", {}) if result else {}
    lines = []

    for index, action in enumerate(plan, start=1):
        tool = action["type"]

        lines.append(f"Tool call {index}")
        lines.append(f"Tool: {tool}")
        lines.append("Input:")
        lines.append(json.dumps(action, indent=2, default=str))

        lines.append("Validation: checked")

        if tool == "read_csv":
            summary = "CSV loaded" if "df" in context else "No output"
        elif tool == "compute_kpis":
            summary = context.get("kpis", "No output")
        elif tool == "critic_check":
            summary = context.get("critic_result", "No output")
        elif tool == "generate_report":
            summary = context.get("report", "No output")
        elif tool == "http_get_indicator":
            summary = context.get("indicator_data", "No output")
        elif tool == "validate_indicator_json":
            summary = context.get("indicator_validation", "No output")
        elif tool == "transform_indicator_data":
            summary = context.get("indicator_summary", "No output")
        elif tool == "generate_indicator_report":
            summary = context.get("indicator_report", "No output")
        else:
            summary = "No output"

        lines.append("Output:")
        lines.append(json.dumps(summary, indent=2, default=str))
        lines.append("")

    return "\n".join(lines)


def compute_metrics():
    events = read_log_events()

    finished_events = [
        event for event in events
        if event.get("event_type") in {
            "run_finished",
            "failure_run_finished",
            "scenario2_run_finished",
            "scenario2_failure_finished",
            "scenario2_recovery_finished",
            "gui_run_finished",
        }
    ]

    total = len(finished_events)
    success = 0
    failed = 0
    recovered = 0

    for event in finished_events:
        details = event.get("details", {})

        if details.get("success") is True:
            success += 1

        if details.get("success") is False:
            failed += 1

        if event.get("event_type") == "scenario2_recovery_finished" and details.get("success") is True:
            recovered += 1

    success_rate = round((success / total) * 100, 2) if total else 0

    failures = [
        event for event in events
        if event.get("event_type") in {"step_failed", "retry_failed"}
    ]

    recovery_rate = round((recovered / len(failures)) * 100, 2) if failures else 0

    return {
        "total_finished_runs": total,
        "successful_runs": success,
        "failed_runs": failed,
        "success_rate_percent": success_rate,
        "recovery_events": recovered,
        "recovery_rate_percent": recovery_rate,
        "dp_cache": get_cache_stats(),
    }


def update_safety_panel(failure_mode, result):
    lines = [
        "Safety and policy",
        "",
        "Allowed local folder: data_synthetic/",
        "Allowed endpoints:",
        "- mock://tunisia/manufacturing_indicators",
        "- mock://tunisia/manufacturing_indicators_backup",
        "",
        "Max steps: 10",
        "Max retries per step: 2",
        "Redaction: enabled for sensitive fields",
        "",
    ]

    if failure_mode:
        lines.append(f"Failure injection: {failure_mode}")
    else:
        lines.append("Failure injection: none")

    if result["success"]:
        lines.append("Policy result: execution completed")
    else:
        lines.append("Policy result: execution stopped safely")
        lines.append(f"Reason: {result.get('error')}")

    safety_text.delete("1.0", tk.END)
    safety_text.insert(tk.END, "\n".join(lines))


def refresh_logs():
    logs_text.delete("1.0", tk.END)
    logs_text.insert(tk.END, read_recent_logs())


def refresh_metrics():
    metrics_text.delete("1.0", tk.END)
    metrics_text.insert(tk.END, json.dumps(compute_metrics(), indent=2))


def run_selected_scenario():
    scenario = scenario_var.get()
    failure_mode = failure_var.get()

    if failure_mode == "none":
        failure_mode = None

    run_id = start_run()
    run_id_var.set(run_id)

    if scenario == "Scenario 1":
        actions = get_scenario1_actions("data_synthetic/manufacturing_orders.csv")
        objectives = get_scenario1_objectives()
        log_event("gui_run_started", {"scenario": "scenario1"})
    else:
        actions = get_scenario2_actions(failure_mode=failure_mode)
        objectives = get_scenario2_objectives()
        log_event("gui_run_started", {"scenario": "scenario2", "failure_mode": failure_mode})

    plan = backtracking_plan(actions, objectives)
    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, format_result(result))

    plan_text.delete("1.0", tk.END)
    plan_text.insert(tk.END, format_plan(plan))

    timeline_text.delete("1.0", tk.END)
    timeline_text.insert(tk.END, build_timeline(plan, result))

    inspector_text.delete("1.0", tk.END)
    inspector_text.insert(tk.END, build_tool_inspector(plan, result))

    update_safety_panel(failure_mode, result)
    refresh_logs()
    refresh_metrics()

    log_event("gui_run_finished", {"success": result["success"]})


def run_dp_demo():
    actions = get_scenario2_actions()
    objectives = get_scenario2_objectives()

    dp_backtracking_plan(actions, objectives)
    dp_backtracking_plan(actions, objectives)

    refresh_metrics()


app = tk.Tk()
app.title("Manufacturing Orchestrator")
app.geometry("1000x700")

title = tk.Label(app, text="Manufacturing Orchestrator", font=("Arial", 16, "bold"))
title.pack(pady=10)

top_frame = tk.Frame(app)
top_frame.pack(pady=5)

scenario_var = tk.StringVar(value="Scenario 1")
failure_var = tk.StringVar(value="none")
run_id_var = tk.StringVar(value="No run yet")

tk.Label(top_frame, text="Scenario:").grid(row=0, column=0, padx=5)

scenario_box = ttk.Combobox(
    top_frame,
    textvariable=scenario_var,
    values=["Scenario 1", "Scenario 2"],
    state="readonly",
    width=18,
)
scenario_box.grid(row=0, column=1, padx=5)

tk.Label(top_frame, text="Failure mode:").grid(row=0, column=2, padx=5)

failure_box = ttk.Combobox(
    top_frame,
    textvariable=failure_var,
    values=["none", "429", "timeout", "bad_json", "transform_error"],
    state="readonly",
    width=18,
)
failure_box.grid(row=0, column=3, padx=5)

tk.Button(top_frame, text="Run", command=run_selected_scenario, width=14).grid(
    row=0, column=4, padx=5
)

tk.Button(top_frame, text="DP Demo", command=run_dp_demo, width=14).grid(
    row=0, column=5, padx=5
)

tk.Label(app, textvariable=run_id_var, font=("Arial", 9)).pack(pady=3)

notebook = ttk.Notebook(app)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

result_frame = tk.Frame(notebook)
timeline_frame = tk.Frame(notebook)
plan_frame = tk.Frame(notebook)
inspector_frame = tk.Frame(notebook)
safety_frame = tk.Frame(notebook)
logs_frame = tk.Frame(notebook)
metrics_frame = tk.Frame(notebook)

notebook.add(result_frame, text="Results")
notebook.add(timeline_frame, text="Timeline")
notebook.add(plan_frame, text="Plan")
notebook.add(inspector_frame, text="Tool Inspector")
notebook.add(safety_frame, text="Safety")
notebook.add(logs_frame, text="Logs")
notebook.add(metrics_frame, text="Metrics")

result_text = tk.Text(result_frame, wrap="word")
timeline_text = tk.Text(timeline_frame, wrap="word")
plan_text = tk.Text(plan_frame, wrap="word")
inspector_text = tk.Text(inspector_frame, wrap="word")
safety_text = tk.Text(safety_frame, wrap="word")
logs_text = tk.Text(logs_frame, wrap="word")
metrics_text = tk.Text(metrics_frame, wrap="word")

for widget in [
    result_text,
    timeline_text,
    plan_text,
    inspector_text,
    safety_text,
    logs_text,
    metrics_text,
]:
    widget.pack(expand=True, fill="both")

refresh_logs()
refresh_metrics()

app.mainloop()