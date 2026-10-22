from tools.safety import validate_csv_path


def test_validate_csv_path_success():
    result = validate_csv_path("data_synthetic/manufacturing_orders.csv")
    assert result["ok"] is True


def test_validate_csv_path_block_non_csv():
    result = validate_csv_path("data_synthetic/manufacturing_orders.txt")
    assert result["ok"] is False


def test_validate_csv_path_block_outside_folder():
    result = validate_csv_path("../secret.csv")
    assert result["ok"] is False