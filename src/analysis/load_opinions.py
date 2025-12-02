from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR / 'php_opinion_box' / 'opinions' / 'opinion_box.csv'


def load_opinion_csv():
    if not CSV_PATH.exists():
        return None
    df = pd.read_csv(CSV_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    return df
