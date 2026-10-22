import time
from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.dp_planner import dp_backtracking_plan, get_cache_stats

def measure(func, actions, objectives):
    start = time.perf_counter()
    func(actions, objectives)
    return time.perf_counter() - start

def main():
    actions = get_scenario2_actions()
    objectives = get_scenario2_objectives()

    bt = measure(backtracking_plan, actions, objectives)
    dp1 = measure(dp_backtracking_plan, actions, objectives)
    dp2 = measure(dp_backtracking_plan, actions, objectives)

    print("Backtracking:", bt)
    print("DP first:", dp1)
    print("DP cached:", dp2)
    print("Cache stats:", get_cache_stats())

if __name__ == "__main__":
    main()