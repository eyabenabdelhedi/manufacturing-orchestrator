from workflows.scenario1 import get_scenario1_actions, get_scenario1_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop
from orchestrator.run_manager import log_event, start_run


def main():
    run_id = start_run()
    print(f"Run ID: {run_id}")

    csv_path = "data_synthetic/wrong_file.csv"

    actions = get_scenario1_actions(csv_path)
    objectives = get_scenario1_objectives()

    log_event("failure_run_started", {"scenario": "scenario1_failure"})

    plan = backtracking_plan(actions, objectives)

    if plan is None:
        print("Planning failed")
        log_event("planning_failed", {"reason": "no_valid_plan"})
        return

    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    print("\n--- FAILURE OUTPUT ---")

    if not result["success"]:
        print(result)

        log_event(
            "failure_run_finished",
            {
                "success": False,
                "error": result["error"],
                "context": result.get("context", {}),
            },
        )
    else:
        print("Unexpected success (should fail)")

        log_event(
            "failure_run_finished",
            {
                "success": True,
                "warning": "failure scenario did not fail as expected",
            },
        )


if __name__ == "__main__":
    main()