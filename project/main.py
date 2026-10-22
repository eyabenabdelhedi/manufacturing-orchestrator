from workflows.scenario1 import get_scenario1_actions, get_scenario1_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop
from orchestrator.run_manager import log_event, start_run


def main():
    run_id = start_run()
    print(f"Run ID: {run_id}")

    csv_path = "data_synthetic/manufacturing_orders.csv"

    actions = get_scenario1_actions(csv_path)
    objectives = get_scenario1_objectives()

    log_event("run_started", {"scenario": "scenario1", "csv_path": csv_path})

    plan = backtracking_plan(actions, objectives)

    if plan is None:
        print("Planning failed: no valid plan found")
        log_event("planning_failed", {"reason": "no_valid_plan"})
        return

    print("\nPlan found:")
    for step in plan:
        print(step)

    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    print("\n--- OUTPUT ---")

    if result["success"]:
        context = result["context"]

        print("\nCSV loaded successfully")
        print(context["df"])

        print("\nKPIs:")
        print(context["kpis"])

        print("\nCritic result:")
        print(context["critic_result"])

        print("\nReport result:")
        print(context["report"])

        log_event(
            "run_finished",
            {
                "success": True,
                "steps_executed": result.get("steps_executed", 0),
                "kpis": context.get("kpis"),
                "critic_result": context.get("critic_result"),
                "report": context.get("report"),
            },
        )
    else:
        print("\nRun failed:")
        print(result["error"])

        log_event(
            "run_finished",
            {
                "success": False,
                "error": result["error"],
            },
        )


if __name__ == "__main__":
    main()