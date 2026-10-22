from workflows.scenario1 import get_scenario1_actions, get_scenario1_objectives
from orchestrator.planner import backtracking_plan


def test_backtracking_plan_found():
    actions = get_scenario1_actions("data_synthetic/manufacturing_orders.csv")
    objectives = get_scenario1_objectives()

    plan = backtracking_plan(actions, objectives)

    assert plan is not None
    assert len(plan) == 4
    assert plan[0]["type"] == "read_csv"
    assert plan[1]["type"] == "compute_kpis"
    assert plan[2]["type"] == "critic_check"
    assert plan[3]["type"] == "generate_report"