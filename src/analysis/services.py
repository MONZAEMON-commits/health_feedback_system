# analysis/services.py

import pandas as pd
from analysis.utils import load_opinion_csv
from conditions.models import Condition


def build_analysis_dataframes(csv_path: str) -> dict[str, pd.DataFrame]:
    """
    現行要件における最低限の分析のみを行う。
    ・体調：physical / mental の平均・中央値・日別傾向
    ・ご意見箱：タグ別件数のみ
    """

    # -----------------------------
    # 体調データ（DB）
    # -----------------------------
    condition_qs = Condition.objects.all().values(
        "date",
        "user_id",
        "physical",
        "mental",
    )
    condition_df = pd.DataFrame(list(condition_qs))

    if condition_df.empty:
        condition_stats = pd.DataFrame()
        condition_daily_trend = pd.DataFrame()
    else:
        condition_stats = pd.DataFrame({
            "metric": ["physical", "mental"],
            "mean": [
                condition_df["physical"].mean(),
                condition_df["mental"].mean(),
            ],
            "median": [
                condition_df["physical"].median(),
                condition_df["mental"].median(),
            ],
        })

        condition_daily_trend = (
            condition_df
            .groupby("date")[["physical", "mental"]]
            .mean()
            .reset_index()
            .sort_values("date")
        )

    # -----------------------------
    # ご意見箱（CSV）
    # -----------------------------
    opinion_df = load_opinion_csv(csv_path)

    if opinion_df.empty or "tag" not in opinion_df.columns:
        opinion_tag_stats = pd.DataFrame()
    else:
        opinion_tag_stats = (
            opinion_df
            .groupby("tag")
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
        )

    return {
        "condition_raw": condition_df,
        "opinion_raw": opinion_df,
        "condition_stats": condition_stats,
        "condition_daily_trend": condition_daily_trend,
        "opinion_tag_stats": opinion_tag_stats,
    }
