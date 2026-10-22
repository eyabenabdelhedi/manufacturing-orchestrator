from orchestrator.planner import backtracking_plan

memo_cache = {}      # dictionnaire global de cache
cache_stats = {
    "hits": 0,
    "misses": 0
}

    # Crée une clé unique basée sur les types d'actions + objectifs

def make_cache_key(actions, objectives):
    action_types = tuple(action["type"] for action in actions)
    objective_key = tuple(objectives)
    return action_types, objective_key


def dp_backtracking_plan(actions, objectives):
    key = make_cache_key(actions, objectives)

    if key in memo_cache:
        cache_stats["hits"] += 1
        return memo_cache[key]

    cache_stats["misses"] += 1
    plan = backtracking_plan(actions, objectives)
    memo_cache[key] = plan
    return plan


def get_cache_stats():
    total = cache_stats["hits"] + cache_stats["misses"]

    if total == 0:
        hit_ratio = 0
    else:
        hit_ratio = cache_stats["hits"] / total

    return {
        "hits": cache_stats["hits"],
        "misses": cache_stats["misses"],
        "hit_ratio": round(hit_ratio, 2),
        "cache_size": len(memo_cache)
    }