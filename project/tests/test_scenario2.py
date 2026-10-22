from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop


def test_scenario2_success():
    actions = get_scenario2_actions()
    objectives = get_scenario2_objectives()

    plan = backtracking_plan(actions, objectives)
    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    assert result["success"] is True
    assert "indicator_summary" in result["context"]
    assert "indicator_report" in result["context"]


def test_scenario2_failure_429():
    actions = get_scenario2_actions(failure_mode="429")
    objectives = get_scenario2_objectives()

    plan = backtracking_plan(actions, objectives)
    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    assert result["success"] is False
    assert "HTTP 429" in result["error"]