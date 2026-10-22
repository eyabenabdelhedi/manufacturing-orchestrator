from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop
from orchestrator.run_manager import log_event, start_run


def main():
    run_id = start_run()
    print(f"Run ID: {run_id}")

    actions = get_scenario2_actions()
    objectives = get_scenario2_objectives()

    log_event("scenario2_run_started", {"scenario": "scenario2"})

    plan = backtracking_plan(actions, objectives)

    if plan is None:
        print("Planning failed")
        log_event("planning_failed", {"reason": "no_valid_plan"})
        return

    print("\nPlan found:")
    for step in plan:
        print(step)

    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    print("\n--- SCENARIO 2 OUTPUT ---")
    print(result)

    log_event("scenario2_run_finished", {"success": result["success"]})


if __name__ == "__main__":
    main()