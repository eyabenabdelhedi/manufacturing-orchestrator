from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.dp_planner import dp_backtracking_plan, get_cache_stats


def test_dp_cache_hit():
    actions = get_scenario2_actions()
    objectives = get_scenario2_objectives()

    dp_backtracking_plan(actions, objectives)
    dp_backtracking_plan(actions, objectives)

    stats = get_cache_stats()

    assert stats["hits"] >= 1
    assert stats["cache_size"] >= 1