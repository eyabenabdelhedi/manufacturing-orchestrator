from concurrent.futures import ThreadPoolExecutor
from workflows.scenario2 import get_scenario2_actions, get_scenario2_objectives
from orchestrator.planner import backtracking_plan
from orchestrator.loop import run_agent_loop


def run_one_scenario2():
    actions = get_scenario2_actions()
    objectives = get_scenario2_objectives()

    plan = backtracking_plan(actions, objectives)
    result = run_agent_loop(plan, max_steps=10, max_retries=2)

    return result["success"]


def test_parallel_runs_no_crash():
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(lambda _: run_one_scenario2(), range(3)))

    assert all(results)