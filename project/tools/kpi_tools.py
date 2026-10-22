def compute_kpis(df):
    try:
        total_quantity = df["quantity"].sum()
        avg_lead_time = df["lead_time_days"].mean()

        by_product = df.groupby("product")["quantity"].sum().to_dict()

        return {
            "total_quantity": int(total_quantity),
            "avg_lead_time": float(avg_lead_time),
            "quantity_by_product": by_product
        }

    except Exception as e:
        return {"error": str(e)}