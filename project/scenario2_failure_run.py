import sys
from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop
from orchestrator.run_manager import log_event, start_run


def main():
    failure_mode = sys.argv[1] if len(sys.argv) > 1 else "429"

    run_id = start_run()
    print(f"Run ID: {run_id}")

    actions = get_scenario2_actions(failure_mode=failure_mode)
    objectives = get_scenario2_objectives()

    log_event(
        "scenario2_failure_started",
        {"scenario": "scenario2_failure", "failure_mode": failure_mode},
    )

    plan = backtracking_plan(actions, objectives)
    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    print("\n--- SCENARIO 2 FAILURE OUTPUT ---")
    print(result)

    log_event("scenario2_failure_finished", result)


if __name__ == "__main__":
    main()