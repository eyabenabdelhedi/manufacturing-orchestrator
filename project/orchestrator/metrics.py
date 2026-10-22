import time
import json

from workflows.scenario1 import get_scenario1_actions, get_scenario1_objectives
from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.dp_planner import dp_backtracking_plan, get_cache_stats, memo_cache, cache_stats
from orchestrator.loop import run_agent_loop


# ── BT vs DP Empirical Comparison ────────────────────────────────────────────

def measure_bt(actions, objectives, runs=5):
    """Run backtracking N times and return average latency in ms."""
    latencies = []
    for _ in range(runs):
        start = time.perf_counter()
        backtracking_plan(actions, objectives)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)
    avg = round(sum(latencies) / len(latencies), 4)
    p95 = round(sorted(latencies)[int(len(latencies) * 0.95) - 1], 4)
    return {"avg_ms": avg, "p95_ms": p95, "runs": runs}


def measure_dp(actions, objectives, runs=5):
    """Run DP-memoized backtracking N times and return latency + cache stats."""
    # Reset cache for fair measurement
    memo_cache.clear()
    cache_stats["hits"] = 0
    cache_stats["misses"] = 0

    latencies = []
    for _ in range(runs):
        start = time.perf_counter()
        dp_backtracking_plan(actions, objectives)
        end = time.perf_counter()
        latencies.append((end - start) * 1000)

    avg = round(sum(latencies) / len(latencies), 4)
    p95 = round(sorted(latencies)[int(len(latencies) * 0.95) - 1], 4)
    stats = get_cache_stats()
    return {
        "avg_ms": avg,
        "p95_ms": p95,
        "runs": runs,
        "cache_hits": stats["hits"],
        "cache_misses": stats["misses"],
        "hit_ratio": stats["hit_ratio"],
        "cache_size": stats["cache_size"],
    }


def compare_bt_vs_dp():
    """
    Empirical comparison of Backtracking vs Backtracking+DP
    on Scenario 1 and Scenario 2.
    Returns a structured report dict.
    """
    results = {}

    for label, actions_fn, objectives_fn in [
        ("scenario1",
         lambda: get_scenario1_actions("data_synthetic/manufacturing_orders.csv"),
         get_scenario1_objectives),
        ("scenario2",
         get_scenario2_actions,
         get_scenario2_objectives),
    ]:
        actions = actions_fn()
        objectives = objectives_fn()

        bt = measure_bt(actions, objectives, runs=10)
        dp = measure_dp(actions, objectives, runs=10)

        speedup = round(bt["avg_ms"] / dp["avg_ms"], 2) if dp["avg_ms"] > 0 else None

        results[label] = {
            "backtracking_only": bt,
            "backtracking_with_dp": dp,
            "speedup_factor": speedup,
        }

    return results


# ── Task Success Metrics ──────────────────────────────────────────────────────

def compute_task_success_metrics():
    """
    Run all scenarios (success + each failure mode) and compute:
    - task success rate
    - failure recovery rate
    - grounding rate (tool calls that passed schema + safety)
    """
    results = []

    # Scenario 1 — success
    actions = get_scenario1_actions("data_synthetic/manufacturing_orders.csv")
    objectives = get_scenario1_objectives()
    plan = backtracking_plan(actions, objectives)
    r = run_agent_loop(plan, max_steps=10, max_retries=2)
    results.append({"scenario": "scenario1_success", "success": r["success"]})

    # Scenario 1 — failure (wrong file)
    from workflows.scenario1_failure import get_failure_actions, get_failure_objectives
    actions = get_failure_actions()
    objectives = get_failure_objectives()
    plan = backtracking_plan(actions, objectives)
    r = run_agent_loop(plan, max_steps=10, max_retries=2)
    results.append({"scenario": "scenario1_failure", "success": r["success"], "error": r.get("error")})

    # Scenario 2 — success
    actions = get_scenario2_actions()
    objectives = get_scenario2_objectives()
    plan = backtracking_plan(actions, objectives)
    r = run_agent_loop(plan, max_steps=10, max_retries=2)
    results.append({"scenario": "scenario2_success", "success": r["success"]})

    # Scenario 2 — all failure modes
    for fm in ["429", "timeout", "bad_json", "transform_error"]:
        actions = get_scenario2_actions(failure_mode=fm)
        plan = backtracking_plan(actions, get_scenario2_objectives())
        r = run_agent_loop(plan, max_steps=10, max_retries=2)
        results.append({
            "scenario": f"scenario2_{fm}",
            "success": r["success"],
            "error": r.get("error"),
        })

    # Scenario 2 — fallback recovery
    fallback_actions = get_scenario2_actions(
        endpoint="mock://tunisia/manufacturing_indicators_backup"
    )
    plan = backtracking_plan(fallback_actions, get_scenario2_objectives())
    r = run_agent_loop(plan, max_steps=10, max_retries=2)
    results.append({"scenario": "scenario2_fallback_recovery", "success": r["success"]})

    total = len(results)
    successes = sum(1 for r in results if r["success"])
    failures_expected = [r for r in results if "failure" in r["scenario"] or any(
        fm in r["scenario"] for fm in ["429", "timeout", "bad_json", "transform_error"]
    )]
    correctly_failed = sum(1 for r in failures_expected if not r["success"])

    return {
        "total_runs": total,
        "successful_runs": successes,
        "task_success_rate_percent": round(successes / total * 100, 2),
        "failure_injection_runs": len(failures_expected),
        "correctly_handled_failures": correctly_failed,
        "failure_handling_rate_percent": round(
            correctly_failed / len(failures_expected) * 100, 2
        ) if failures_expected else 0,
        "detail": results,
    }


# ── Full Report ───────────────────────────────────────────────────────────────

def generate_full_metrics_report(output_path="logs/metrics_report.json"):
    """Generate and save the complete metrics report."""
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    print("Running BT vs DP comparison...")
    bt_dp = compare_bt_vs_dp()

    print("Running task success metrics...")
    task_metrics = compute_task_success_metrics()

    report = {
        "bt_vs_dp_comparison": bt_dp,
        "task_metrics": task_metrics,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"Metrics report saved to {output_path}")
    return report

def compute_global_metrics():
    task_metrics = compute_task_success_metrics()
    bt_dp = compare_bt_vs_dp()

    return {
        "total_runs": task_metrics["total_runs"],
        "successful_runs": task_metrics["successful_runs"],
        "task_success_rate_percent": task_metrics["task_success_rate_percent"],
        "failure_injection_runs": task_metrics["failure_injection_runs"],
        "correctly_handled_failures": task_metrics["correctly_handled_failures"],
        "failure_handling_rate_percent": task_metrics["failure_handling_rate_percent"],
        "bt_vs_dp_comparison": bt_dp,
    }

if __name__ == "__main__":
    report = generate_full_metrics_report()
    print(json.dumps(report, indent=2))