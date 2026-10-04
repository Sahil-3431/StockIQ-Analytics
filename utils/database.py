import sqlite3
from pathlib import Path

import pandas as pd


# ============================================================
# DATABASE PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DB_PATH = PROJECT_ROOT / "stock_market.db"


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """
    return sqlite3.connect(DB_PATH)


# ============================================================
# EXECUTE SELECT QUERY
# ============================================================

def run_query(query: str) -> pd.DataFrame:
    """
    Execute a SELECT query and return the result as DataFrame.
    """

    connection = get_connection()

    try:
        return pd.read_sql_query(query, connection)

    finally:
        connection.close()


# ============================================================
# GET ALL STOCK DATA
# ============================================================

def get_all_data() -> pd.DataFrame:
    """
    Load complete stock market dataset.
    """

    query = """
        SELECT *
        FROM stock_market_data
        ORDER BY trade_date, company
    """

    return run_query(query)


# ============================================================
# GET COMPANIES
# ============================================================

def get_companies() -> list:
    """
    Return sorted list of companies.
    """

    query = """
        SELECT DISTINCT company
        FROM stock_market_data
        ORDER BY company
    """

    df = run_query(query)

    return df["company"].tolist()


# ============================================================
# GET DATE RANGE
# ============================================================

def get_date_range():
    """
    Return minimum and maximum trading dates.
    """

    query = """
        SELECT
            MIN(trade_date) AS start_date,
            MAX(trade_date) AS end_date
        FROM stock_market_data
    """

    df = run_query(query)

    return df.iloc[0]["start_date"], df.iloc[0]["end_date"]


# ============================================================
# GET COMPANY DATA
# ============================================================

def get_company_data(company: str) -> pd.DataFrame:
    """
    Return stock data for a selected company.
    """

    query = """
        SELECT *
        FROM stock_market_data
        WHERE company = ?
        ORDER BY trade_date
    """

    connection = get_connection()

    try:
        return pd.read_sql_query(
            query,
            connection,
            params=(company,)
        )

    finally:
        connection.close()


# ============================================================
# DATABASE HEALTH CHECK
# ============================================================

def database_health_check() -> dict:
    """
    Return basic database information.
    """

    query = """
        SELECT
            COUNT(*) AS total_records,
            COUNT(DISTINCT company) AS total_companies,
            MIN(trade_date) AS start_date,
            MAX(trade_date) AS end_date
        FROM stock_market_data
    """

    df = run_query(query)

    row = df.iloc[0]

    return {
        "total_records": int(row["total_records"]),
        "total_companies": int(row["total_companies"]),
        "start_date": row["start_date"],
        "end_date": row["end_date"],
    }