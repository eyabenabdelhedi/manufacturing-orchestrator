from orchestrator.executor import execute_action
from orchestrator.run_manager import log_event


def run_agent_loop(plan, context=None, max_steps=10, max_retries=2):
    if context is None:
        context = {}

    retries = 0
    step_count = 0

    for action in plan:
        if step_count >= max_steps:
            log_event("loop_stopped", {"reason": "max_steps_reached", "max_steps": max_steps})
            return {
                "success": False,
                "error": "Max steps reached",
                "context": context,
            }

        step_count += 1
        log_event("step_started", {"step": step_count, "action": action})

        result = execute_action(action, context)

        if result["ok"]:
            log_event("step_success", {"step": step_count, "action": action, "result": result["result"]})
            retries = 0
            continue

        log_event("step_failed", {"step": step_count, "action": action, "error": result["error"]})

        if retries < max_retries:
            retries += 1
            log_event("retrying_step", {"step": step_count, "retry": retries})
            retry_result = execute_action(action, context)

            if retry_result["ok"]:
                log_event("retry_success", {"step": step_count, "action": action, "result": retry_result["result"]})
                retries = 0
                continue

            log_event("retry_failed", {"step": step_count, "action": action, "error": retry_result["error"]})

        return {
            "success": False,
            "error": result["error"],
            "context": context,
        }

    return {
        "success": True,
        "context": context,
        "steps_executed": step_count,
    }