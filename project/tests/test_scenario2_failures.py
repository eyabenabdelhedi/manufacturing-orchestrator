import pytest
from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop


@pytest.mark.parametrize(
    "failure_mode",
    ["429", "timeout", "bad_json", "transform_error"],
)
def test_scenario2_failure_modes(failure_mode):
    actions = get_scenario2_actions(failure_mode=failure_mode)
    objectives = get_scenario2_objectives()

    plan = backtracking_plan(actions, objectives)
    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    assert result["success"] is False
    assert "error" in result