def is_action_feasible(action: dict, completed: set, context: dict) -> bool:
    action_type = action["type"]

    if action_type == "read_csv":
        return "read_csv" not in completed

    if action_type == "compute_kpis":
        return "read_csv" in completed and "compute_kpis" not in completed

    if action_type == "critic_check":
        return "compute_kpis" in completed and "critic_check" not in completed

    if action_type == "generate_report":
        return "critic_check" in completed and "generate_report" not in completed

    if action_type == "http_get_indicator":
        return "http_get_indicator" not in completed

    if action_type == "validate_indicator_json":
        return "http_get_indicator" in completed and "validate_indicator_json" not in completed

    if action_type == "transform_indicator_data":
        return "validate_indicator_json" in completed and "transform_indicator_data" not in completed

    if action_type == "generate_indicator_report":
        return "transform_indicator_data" in completed and "generate_indicator_report" not in completed

    return False


def prune_branch(completed: set, objectives: list) -> bool:
    valid_objectives = {
        "read_csv",
        "compute_kpis",
        "critic_check",
        "generate_report",
        "http_get_indicator",
        "validate_indicator_json",
        "transform_indicator_data",
        "generate_indicator_report",
    }

    for obj in objectives:
        if obj not in valid_objectives:
            return True

    return False


def backtracking_plan(actions, objectives, completed=None, path=None, context=None):
    if completed is None:
        completed = set()

    if path is None:
        path = []

    if context is None:
        context = {}

    if prune_branch(completed, objectives):
        return None

    if all(obj in completed for obj in objectives):
        return path

    for action in actions:
        action_type = action["type"]

        if action_type in completed:
            continue

        if not is_action_feasible(action, completed, context):
            continue

        new_completed = completed.copy()
        new_completed.add(action_type)

        new_path = path + [action]

        result = backtracking_plan(
            actions,
            objectives,
            completed=new_completed,
            path=new_path,
            context=context,
        )

        if result is not None:
            return result

    return None