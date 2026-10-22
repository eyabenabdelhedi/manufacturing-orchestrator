from workflows.scenario1_failure import get_failure_actions, get_failure_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop


def test_agent_loop_failure_injection():
    actions = get_failure_actions()
    objectives = get_failure_objectives()

    plan = backtracking_plan(actions, objectives)
    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    assert result["success"] is False
    assert "error" in result