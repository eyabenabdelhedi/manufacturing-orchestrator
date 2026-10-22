import time
from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.dp_planner import dp_backtracking_plan, get_cache_stats


def main():
    actions = get_scenario2_actions()
    objectives = get_scenario2_objectives()

    start_bt = time.perf_counter()
    backtracking_plan(actions, objectives)
    bt_time = time.perf_counter() - start_bt

    start_dp_1 = time.perf_counter()
    dp_backtracking_plan(actions, objectives)
    dp_first_time = time.perf_counter() - start_dp_1

    start_dp_2 = time.perf_counter()
    dp_backtracking_plan(actions, objectives)
    dp_cached_time = time.perf_counter() - start_dp_2

    print("Backtracking latency:")
    print(round(bt_time, 6))

    print("\nDP first run latency:")
    print(round(dp_first_time, 6))

    print("\nDP cached run latency:")
    print(round(dp_cached_time, 6))

    print("\nDP Cache Stats:")
    print(get_cache_stats())


if __name__ == "__main__":
    main()