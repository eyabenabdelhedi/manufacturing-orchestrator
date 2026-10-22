from tools.csv_tools import read_csv_file


def test_read_csv_file_success():
    result = read_csv_file("data_synthetic/manufacturing_orders.csv")
    assert not isinstance(result, dict)
    assert len(result) == 3
    assert "quantity" in result.columns