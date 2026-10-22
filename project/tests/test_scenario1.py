from orchestrator.critic import critic_check


def test_critic_check_success():
    kpis = {
        "total_quantity": 450,
        "avg_lead_time": 6.0,
        "quantity_by_product": {"A": 250, "B": 200}
    }

    result = critic_check(kpis)
    assert result["approved"] is True


def test_critic_check_missing_key():
    kpis = {
        "total_quantity": 450,
        "avg_lead_time": 6.0
    }

    result = critic_check(kpis)
    assert result["approved"] is False