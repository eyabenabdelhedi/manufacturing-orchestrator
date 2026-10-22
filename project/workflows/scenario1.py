def get_scenario1_actions(csv_path="data_synthetic/manufacturing_orders.csv"):
    return [
        {"type": "read_csv", "path": csv_path},
        {"type": "compute_kpis"},
        {"type": "critic_check"},
        {"type": "generate_report"},
    ]


def get_scenario1_objectives():
    return ["read_csv", "compute_kpis", "critic_check", "generate_report"]