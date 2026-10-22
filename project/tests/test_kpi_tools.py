from tools.csv_tools import read_csv_file
from tools.kpi_tools import compute_kpis


def test_compute_kpis():
    df = read_csv_file("data_synthetic/manufacturing_orders.csv")
    kpis = compute_kpis(df)

    assert kpis["total_quantity"] == 450
    assert kpis["avg_lead_time"] == 6.0
    assert kpis["quantity_by_product"]["A"] == 250
    assert kpis["quantity_by_product"]["B"] == 200