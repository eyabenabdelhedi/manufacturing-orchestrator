def get_failure_actions():
    return [
        {"type": "read_csv", "path": "data_synthetic/wrong_file.csv"},
        {"type": "compute_kpis"},
        {"type": "critic_check"},
        {"type": "generate_report"},
    ]


def get_failure_objectives():
    return ["read_csv", "compute_kpis", "critic_check", "generate_report"]