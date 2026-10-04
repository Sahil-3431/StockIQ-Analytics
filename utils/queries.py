# ============================================================
# SQL QUERY LIBRARY
# ============================================================

SQL_QUERIES = {

    # --------------------------------------------------------
    # BASIC DATA EXPLORATION
    # --------------------------------------------------------

    "Q01 - Total Records": """
        SELECT COUNT(*) AS total_records
        FROM stock_market_data;
    """,

    "Q02 - Total Companies": """
        SELECT COUNT(DISTINCT company) AS total_companies
        FROM stock_market_data;
    """,

    "Q03 - List Companies": """
        SELECT DISTINCT company
        FROM stock_market_data
        ORDER BY company;
    """,

    "Q04 - Trading Date Range": """
        SELECT
            MIN(trade_date) AS start_date,
            MAX(trade_date) AS end_date
        FROM stock_market_data;
    """,

    "Q05 - Records Per Company": """
        SELECT
            company,
            COUNT(*) AS total_records
        FROM stock_market_data
        GROUP BY company
        ORDER BY total_records DESC;
    """,

    # --------------------------------------------------------
    # PRICE ANALYSIS
    # --------------------------------------------------------

    "Q06 - Average Closing Price": """
        SELECT
            company,
            ROUND(AVG(close_price), 2) AS avg_close_price
        FROM stock_market_data
        GROUP BY company
        ORDER BY avg_close_price DESC;
    """,

    "Q07 - Highest Closing Price": """
        SELECT
            company,
            ROUND(MAX(close_price), 2) AS highest_close_price
        FROM stock_market_data
        GROUP BY company
        ORDER BY highest_close_price DESC;
    """,

    "Q08 - Lowest Closing Price": """
        SELECT
            company,
            ROUND(MIN(close_price), 2) AS lowest_close_price
        FROM stock_market_data
        GROUP BY company
        ORDER BY lowest_close_price DESC;
    """,

    "Q09 - Top Closing Price Days": """
        SELECT
            company,
            trade_date,
            close_price
        FROM stock_market_data
        ORDER BY close_price DESC
        LIMIT 10;
    """,

    "Q10 - Average Price Range": """
        SELECT
            company,
            ROUND(AVG(price_range), 2) AS avg_price_range
        FROM stock_market_data
        GROUP BY company
        ORDER BY avg_price_range DESC;
    """,

    # --------------------------------------------------------
    # RETURN ANALYSIS
    # --------------------------------------------------------

    "Q11 - Average Daily Return": """
        SELECT
            company,
            ROUND(AVG(daily_return_percentage), 4)
                AS avg_daily_return
        FROM stock_market_data
        GROUP BY company
        ORDER BY avg_daily_return DESC;
    """,

    "Q12 - Maximum Daily Return": """
        SELECT
            company,
            ROUND(MAX(daily_return_percentage), 2)
                AS max_daily_return
        FROM stock_market_data
        GROUP BY company
        ORDER BY max_daily_return DESC;
    """,

    "Q13 - Minimum Daily Return": """
        SELECT
            company,
            ROUND(MIN(daily_return_percentage), 2)
                AS min_daily_return
        FROM stock_market_data
        GROUP BY company
        ORDER BY min_daily_return;
    """,

    "Q14 - Positive Trading Days": """
        SELECT
            company,
            COUNT(*) AS positive_days
        FROM stock_market_data
        WHERE daily_return_percentage > 0
        GROUP BY company
        ORDER BY positive_days DESC;
    """,

    "Q15 - Negative Trading Days": """
        SELECT
            company,
            COUNT(*) AS negative_days
        FROM stock_market_data
        WHERE daily_return_percentage < 0
        GROUP BY company
        ORDER BY negative_days DESC;
    """,

    # --------------------------------------------------------
    # TRADING ACTIVITY
    # --------------------------------------------------------

    "Q16 - Total Turnover": """
        SELECT
            company,
            ROUND(
                SUM(total_turnover) / 10000000.0,
                2
            ) AS total_turnover_crore
        FROM stock_market_data
        GROUP BY company
        ORDER BY total_turnover_crore DESC;
    """,

    "Q17 - Average Turnover": """
        SELECT
            company,
            ROUND(AVG(turnover_crore), 2)
                AS avg_turnover_crore
        FROM stock_market_data
        GROUP BY company
        ORDER BY avg_turnover_crore DESC;
    """,

    "Q18 - Total Trades": """
        SELECT
            company,
            SUM(no_of_trades) AS total_trades
        FROM stock_market_data
        GROUP BY company
        ORDER BY total_trades DESC;
    """,

    "Q19 - Average Daily Trades": """
        SELECT
            company,
            ROUND(AVG(no_of_trades), 0)
                AS avg_daily_trades
        FROM stock_market_data
        GROUP BY company
        ORDER BY avg_daily_trades DESC;
    """,

    "Q20 - Highest Turnover Days": """
        SELECT
            company,
            trade_date,
            ROUND(turnover_crore, 2)
                AS turnover_crore
        FROM stock_market_data
        ORDER BY turnover_crore DESC
        LIMIT 10;
    """,

    # --------------------------------------------------------
    # VOLUME & DELIVERY
    # --------------------------------------------------------

    "Q21 - Average Trading Volume": """
        SELECT
            company,
            ROUND(AVG(volume_lakh), 2)
                AS avg_volume_lakh
        FROM stock_market_data
        GROUP BY company
        ORDER BY avg_volume_lakh DESC;
    """,

    "Q22 - Total Trading Volume": """
        SELECT
            company,
            ROUND(SUM(volume_lakh), 2)
                AS total_volume_lakh
        FROM stock_market_data
        GROUP BY company
        ORDER BY total_volume_lakh DESC;
    """,

    "Q23 - Average Delivery Percentage": """
        SELECT
            company,
            ROUND(AVG(delivery_percentage), 2)
                AS avg_delivery_percentage
        FROM stock_market_data
        GROUP BY company
        ORDER BY avg_delivery_percentage DESC;
    """,

    "Q24 - Highest Delivery Days": """
        SELECT
            company,
            trade_date,
            ROUND(delivery_percentage, 2)
                AS delivery_percentage
        FROM stock_market_data
        ORDER BY delivery_percentage DESC
        LIMIT 10;
    """,

    "Q25 - Delivery Above 50 Percent": """
        SELECT
            company,
            ROUND(AVG(delivery_percentage), 2)
                AS avg_delivery_percentage
        FROM stock_market_data
        GROUP BY company
        HAVING AVG(delivery_percentage) > 50
        ORDER BY avg_delivery_percentage DESC;
    """,

    # --------------------------------------------------------
    # YEARLY ANALYSIS
    # --------------------------------------------------------

    "Q26 - Yearly Average Closing Price": """
        SELECT
            company,
            strftime('%Y', trade_date) AS year,
            ROUND(AVG(close_price), 2)
                AS avg_close_price
        FROM stock_market_data
        GROUP BY company, year
        ORDER BY company, year;
    """,

    "Q27 - Yearly Turnover": """
        SELECT
            company,
            strftime('%Y', trade_date) AS year,
            ROUND(
                SUM(total_turnover) / 10000000.0,
                2
            ) AS turnover_crore
        FROM stock_market_data
        GROUP BY company, year
        ORDER BY year, turnover_crore DESC;
    """,

    "Q28 - Yearly Trading Days": """
        SELECT
            company,
            strftime('%Y', trade_date) AS year,
            COUNT(*) AS trading_days
        FROM stock_market_data
        GROUP BY company, year
        ORDER BY company, year;
    """,

    "Q29 - Yearly Average Return": """
        SELECT
            company,
            strftime('%Y', trade_date) AS year,
            ROUND(
                AVG(daily_return_percentage),
                4
            ) AS avg_daily_return
        FROM stock_market_data
        GROUP BY company, year
        ORDER BY company, year;
    """,

    "Q30 - Company Performance Summary": """
        SELECT
            company,

            ROUND(AVG(close_price), 2)
                AS avg_close_price,

            ROUND(MIN(close_price), 2)
                AS lowest_close_price,

            ROUND(MAX(close_price), 2)
                AS highest_close_price,

            ROUND(AVG(daily_return_percentage), 4)
                AS avg_daily_return,

            ROUND(AVG(delivery_percentage), 2)
                AS avg_delivery_percentage,

            ROUND(
                SUM(total_turnover) / 10000000.0,
                2
            ) AS total_turnover_crore,

            SUM(no_of_trades) AS total_trades

        FROM stock_market_data

        GROUP BY company

        ORDER BY total_turnover_crore DESC;
    """
}


# ============================================================
# QUERY CATEGORIES
# ============================================================

QUERY_CATEGORIES = {
    "Basic Data Exploration": [
        "Q01 - Total Records",
        "Q02 - Total Companies",
        "Q03 - List Companies",
        "Q04 - Trading Date Range",
        "Q05 - Records Per Company",
    ],

    "Price Analysis": [
        "Q06 - Average Closing Price",
        "Q07 - Highest Closing Price",
        "Q08 - Lowest Closing Price",
        "Q09 - Top Closing Price Days",
        "Q10 - Average Price Range",
    ],

    "Return Analysis": [
        "Q11 - Average Daily Return",
        "Q12 - Maximum Daily Return",
        "Q13 - Minimum Daily Return",
        "Q14 - Positive Trading Days",
        "Q15 - Negative Trading Days",
    ],

    "Trading Activity": [
        "Q16 - Total Turnover",
        "Q17 - Average Turnover",
        "Q18 - Total Trades",
        "Q19 - Average Daily Trades",
        "Q20 - Highest Turnover Days",
    ],

    "Volume & Delivery": [
        "Q21 - Average Trading Volume",
        "Q22 - Total Trading Volume",
        "Q23 - Average Delivery Percentage",
        "Q24 - Highest Delivery Days",
        "Q25 - Delivery Above 50 Percent",
    ],

    "Yearly Analysis": [
        "Q26 - Yearly Average Closing Price",
        "Q27 - Yearly Turnover",
        "Q28 - Yearly Trading Days",
        "Q29 - Yearly Average Return",
        "Q30 - Company Performance Summary",
    ],
}


def get_query(query_name: str) -> str:
    """
    Return SQL query by name.
    """

    return SQL_QUERIES.get(query_name, "")


def get_all_query_names() -> list:
    """
    Return all available query names.
    """

    return list(SQL_QUERIES.keys())


def get_categories() -> list:
    """
    Return all query categories.
    """

    return list(QUERY_CATEGORIES.keys())