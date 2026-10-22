def critic_check(kpis):
    required_keys = ["total_quantity", "avg_lead_time", "quantity_by_product"]

    for key in required_keys:
        if key not in kpis:
            return {"approved": False, "error": f"Missing key: {key}"}

    if kpis["total_quantity"] <= 0:
        return {"approved": False, "error": "Total quantity must be > 0"}

    if kpis["avg_lead_time"] <= 0:
        return {"approved": False, "error": "Average lead time must be > 0"}

    if not isinstance(kpis["quantity_by_product"], dict):
        return {"approved": False, "error": "quantity_by_product must be a dictionary"}

    return {"approved": True, "message": "Report approved by Critic"}