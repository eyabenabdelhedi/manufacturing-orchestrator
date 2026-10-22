from workflows.scenario1 import get_scenario1_actions, get_scenario1_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop


def test_agent_loop_success():
    actions = get_scenario1_actions("data_synthetic/manufacturing_orders.csv")
    objectives = get_scenario1_objectives()

    plan = backtracking_plan(actions, objectives)
    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    assert result["success"] is True
    assert "kpis" in result["context"]
    assert "critic_result" in result["context"]