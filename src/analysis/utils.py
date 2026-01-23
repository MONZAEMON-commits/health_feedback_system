import os
import pandas as pd


def load_opinion_csv(csv_path: str) -> pd.DataFrame:
    """
    ご意見箱CSVを読み込む。
    CSV が存在しない場合は、空の DataFrame を返す。
    """

    if not os.path.exists(csv_path):
        # CSVがまだ存在しない（意見未投稿）
        return pd.DataFrame(
            columns=["timestamp", "employee_id", "mode", "content", "tag"]
        )

    return pd.read_csv(csv_path)

def count_by_tag(df):
    """
    ご意見箱データをタグ別に件数集計する。
    空DataFrameの場合は空のdictを返す。
    """
    
    if df.empty:
        return {}

    return df["tag"].value_counts().to_dict()
