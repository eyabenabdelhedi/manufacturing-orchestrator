from orchestrator.metrics import compare_bt_vs_dp, compute_task_success_metrics


def test_bt_vs_dp_comparison_structure():
    result = compare_bt_vs_dp()

    for scenario in ["scenario1", "scenario2"]:
        assert scenario in result
        assert "backtracking_only" in result[scenario]
        assert "backtracking_with_dp" in result[scenario]
        assert "speedup_factor" in result[scenario]

        bt = result[scenario]["backtracking_only"]
        dp = result[scenario]["backtracking_with_dp"]

        assert bt["avg_ms"] >= 0
        assert dp["avg_ms"] >= 0
        assert dp["cache_hits"] >= 1
        assert dp["hit_ratio"] > 0
        assert dp["cache_size"] >= 1


def test_dp_is_not_slower_than_bt_after_warmup():
    result = compare_bt_vs_dp()

    for scenario in ["scenario1", "scenario2"]:
        bt_avg = result[scenario]["backtracking_only"]["avg_ms"]
        dp_avg = result[scenario]["backtracking_with_dp"]["avg_ms"]

        assert dp_avg <= bt_avg * 1.2


def test_task_success_metrics():
    metrics = compute_task_success_metrics()

    assert metrics["total_runs"] >= 7
    assert metrics["task_success_rate_percent"] > 0
    assert metrics["failure_handling_rate_percent"] == 100.0