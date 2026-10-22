from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop


def test_recovery_with_fallback():
    objectives = get_scenario2_objectives()

    failing_actions = get_scenario2_actions(failure_mode="429")
    failing_plan = backtracking_plan(failing_actions, objectives)
    failing_result = run_agent_loop(failing_plan, max_steps=10, max_retries=2)

    assert failing_result["success"] is False

    fallback_actions = get_scenario2_actions(
        endpoint="mock://tunisia/manufacturing_indicators_backup"
    )
    fallback_plan = backtracking_plan(fallback_actions, objectives)
    fallback_result = run_agent_loop(fallback_plan, max_steps=10, max_retries=2)

    assert fallback_result["success"] is True