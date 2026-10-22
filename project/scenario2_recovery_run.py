from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop
from orchestrator.run_manager import log_event, start_run


def run_plan(actions, objectives):
    plan = backtracking_plan(actions, objectives)
    return run_agent_loop(plan, max_steps=10, max_retries=2)


def main():
    run_id = start_run()
    print(f"Run ID: {run_id}")

    objectives = get_scenario2_objectives()

    log_event("scenario2_recovery_started", {"scenario": "scenario2_recovery"})

    failing_actions = get_scenario2_actions(failure_mode="429")
    first_result = run_plan(failing_actions, objectives)

    print("\nFirst attempt:")
    print(first_result)

    if not first_result["success"]:
        log_event("fallback_triggered", {"reason": first_result["error"]})

        fallback_actions = get_scenario2_actions(
            failure_mode=None,
            endpoint="mock://tunisia/manufacturing_indicators_backup",
        )

        fallback_result = run_plan(fallback_actions, objectives)

        print("\nFallback attempt:")
        print(fallback_result)

        log_event("scenario2_recovery_finished", fallback_result)
    else:
        log_event("scenario2_recovery_finished", first_result)


if __name__ == "__main__":
    main()