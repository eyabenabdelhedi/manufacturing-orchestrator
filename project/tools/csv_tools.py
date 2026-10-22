import pandas as pd
from tools.safety import validate_csv_path


def read_csv_file(path):
    safety_check = validate_csv_path(path)
    if not safety_check["ok"]:
        return {"error": safety_check["error"]}

    try:
        df = pd.read_csv(path)
        return df
    except Exception as e:
        return {"error": str(e)}