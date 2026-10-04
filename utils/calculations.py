import pandas as pd
import numpy as np


# ============================================================
# COMPANY PERFORMANCE
# ============================================================

def calculate_company_performance(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame()

    result = (
        df.groupby("company")
        .agg(
            avg_close_price=("close_price", "mean"),
            highest_close_price=("close_price", "max"),
            lowest_close_price=("close_price", "min"),
            avg_daily_return=("daily_return_percentage", "mean"),
            avg_delivery=("delivery_percentage", "mean"),
            avg_turnover=("turnover_crore", "mean"),
            total_turnover=("turnover_crore", "sum"),
            total_trades=("no_of_trades", "sum"),
        )
        .reset_index()
    )

    return result


# ============================================================
# PERIOD RETURN
# ============================================================

def calculate_period_return(df: pd.DataFrame) -> float:

    if df.empty:
        return 0.0

    df = df.sort_values("trade_date")

    first_price = df.iloc[0]["close_price"]
    last_price = df.iloc[-1]["close_price"]

    if first_price == 0:
        return 0.0

    return ((last_price - first_price) / first_price) * 100


# ============================================================
# POSITIVE DAY PERCENTAGE
# ============================================================

def calculate_positive_day_percentage(df: pd.DataFrame) -> float:

    if df.empty:
        return 0.0

    positive_days = (
        df["daily_return_percentage"] > 0
    ).sum()

    total_days = len(df)

    if total_days == 0:
        return 0.0

    return (positive_days / total_days) * 100


# ============================================================
# VOLATILITY
# ============================================================

def calculate_volatility(df: pd.DataFrame) -> float:

    if df.empty:
        return 0.0

    return df["daily_return_percentage"].std()


# ============================================================
# AVERAGE PRICE RANGE
# ============================================================

def calculate_average_range(df: pd.DataFrame) -> float:

    if df.empty:
        return 0.0

    return df["price_range"].mean()


# ============================================================
# MONTHLY DATA
# ============================================================

def calculate_monthly_data(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame()

    data = df.copy()

    data["trade_date"] = pd.to_datetime(
        data["trade_date"]
    )

    data["month"] = (
        data["trade_date"]
        .dt.to_period("M")
        .astype(str)
    )

    result = (
        data.groupby(
            ["month", "company"],
            as_index=False
        )
        .agg(
            avg_close=("close_price", "mean"),
            total_turnover=("turnover_crore", "sum"),
            total_trades=("no_of_trades", "sum"),
            avg_delivery=("delivery_percentage", "mean"),
        )
    )

    return result


# ============================================================
# YEARLY DATA
# ============================================================

def calculate_yearly_data(df: pd.DataFrame) -> pd.DataFrame:

    if df.empty:
        return pd.DataFrame()

    data = df.copy()

    data["trade_date"] = pd.to_datetime(
        data["trade_date"]
    )

    data["year"] = data["trade_date"].dt.year

    result = (
        data.groupby(
            ["year", "company"],
            as_index=False
        )
        .agg(
            avg_close=("close_price", "mean"),
            total_turnover=("turnover_crore", "sum"),
            avg_return=("daily_return_percentage", "mean"),
            avg_delivery=("delivery_percentage", "mean"),
            total_trades=("no_of_trades", "sum"),
        )
    )

    return result


# ============================================================
# TOP COMPANY
# ============================================================

def get_top_company(
    performance_df: pd.DataFrame,
    metric: str
):

    if performance_df.empty:
        return None

    if metric not in performance_df.columns:
        return None

    row = performance_df.loc[
        performance_df[metric].idxmax()
    ]

    return row["company"]


# ============================================================
# SUMMARY STATISTICS
# ============================================================

def get_summary_statistics(df: pd.DataFrame) -> dict:

    if df.empty:
        return {
            "total_records": 0,
            "total_companies": 0,
            "total_turnover": 0,
            "avg_close": 0,
            "positive_days": 0,
        }

    positive_days = (
        df["daily_return_percentage"] > 0
    ).sum()

    return {
        "total_records": len(df),

        "total_companies": df["company"].nunique(),

        "total_turnover": df["turnover_crore"].sum(),

        "avg_close": df["close_price"].mean(),

        "positive_days": positive_days,
    }