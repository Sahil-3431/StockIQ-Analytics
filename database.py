import os
import sqlite3
import pandas as pd

# ============================================================
# PATHS
# ============================================================

CLEANED_DIR = os.path.join("data","cleaned")
DATABASE_PATH = "stock_market.db"

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    connection = sqlite3.connect(
        DATABASE_PATH,
        check_same_thread=False
    )
    return connection


# ============================================================
# CREATE DATABASE TABLE
# ============================================================

def create_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS stock_market_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            trade_date DATE NOT NULL,
            open_price REAL,
            high_price REAL,
            low_price REAL,
            close_price REAL,
            wap REAL,
            no_of_shares INTEGER,
            no_of_trades INTEGER,
            total_turnover REAL,
            deliverable_quantity REAL,
            delivery_percentage REAL,
            spread_high_low REAL,
            spread_close_open REAL,
            daily_return_percentage REAL,
            price_range REAL,
            intraday_return_percentage REAL,
            turnover_crore REAL,
            volume_lakh REAL
        )
        """
    )
    connection.commit()


# ============================================================
# CREATE INDEXES
# ============================================================

def create_indexes(connection):
    cursor = connection.cursor()
    indexes = [

        """
        CREATE INDEX IF NOT EXISTS
        idx_company
        ON stock_market_data(company)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_trade_date
        ON stock_market_data(trade_date)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_company_date
        ON stock_market_data(company, trade_date)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_turnover
        ON stock_market_data(total_turnover)
        """,

        """
        CREATE INDEX IF NOT EXISTS
        idx_close_price
        ON stock_market_data(close_price)
        """
    ]

    for query in indexes:
        cursor.execute(query)
    connection.commit()

# ============================================================
# LOAD CLEANED DATA
# ============================================================

def load_cleaned_data():

    combined_file = os.path.join(
        CLEANED_DIR,
        "stock_market_combined.csv"
    )

    if not os.path.exists(combined_file):
        raise FileNotFoundError(
            f"Cleaned dataset not found: {combined_file}\n"
            "Please run data_cleaning.py first."
        )
    df = pd.read_csv(combined_file)
    return df

# ============================================================
# PREPARE DATA FOR DATABASE
# ============================================================

def prepare_data(df):
    database_df = pd.DataFrame({
        "company":df["Company"],
        "trade_date":pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d"),
        "open_price":df["Open Price"],
        "high_price":df["High Price"],
        "low_price":df["Low Price"],
        "close_price":df["Close Price"],
        "wap":df["WAP"],
        "no_of_shares":df["No.of Shares"],
        "no_of_trades":df["No. of Trades"],
        "total_turnover":df["Total Turnover (Rs.)"],
        "deliverable_quantity":df["Deliverable Quantity"],
        "delivery_percentage":df["% Deli. Qty to Traded Qty"],
        "spread_high_low":df["Spread High-Low"],
        "spread_close_open":df["Spread Close-Open"],
        "daily_return_percentage":df["Daily Return %"],
        "price_range":df["Price Range"],
        "intraday_return_percentage":df["Intraday Return %"],
        "turnover_crore":df["Turnover Crore"],
        "volume_lakh":df["Volume Lakh"],
    })
    return database_df

# ============================================================
# INSERT DATA
# ============================================================

def insert_data(connection, df):
    cursor = connection.cursor()

    # --------------------------------------------------------
    # Clear existing data
    # --------------------------------------------------------

    cursor.execute("DELETE FROM stock_market_data")

    # Reset auto increment
    cursor.execute(
        """
        DELETE FROM sqlite_sequence
        WHERE name = 'stock_market_data'
        """
    )
    connection.commit()

    # --------------------------------------------------------
    # Insert data
    # --------------------------------------------------------

    df.to_sql("stock_market_data",connection,if_exists="append",index=False)
    connection.commit()

# ============================================================
# DATABASE VALIDATION
# ============================================================

def validate_database(connection):
    cursor = connection.cursor()

    # --------------------------------------------------------
    # Total rows
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM stock_market_data
        """
    )
    total_rows = cursor.fetchone()[0]

    # --------------------------------------------------------
    # Total companies
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT COUNT(DISTINCT company)
        FROM stock_market_data
        """
    )
    total_companies = cursor.fetchone()[0]

    # --------------------------------------------------------
    # Date range
    # --------------------------------------------------------

    cursor.execute(
        """
        SELECT
            MIN(trade_date),
            MAX(trade_date)
        FROM stock_market_data
        """
    )
    min_date, max_date = cursor.fetchone()

    # --------------------------------------------------------
    # Company-wise records
    # --------------------------------------------------------

    company_counts = pd.read_sql_query(
        """
        SELECT
            company,
            COUNT(*) AS records
        FROM stock_market_data
        GROUP BY company
        ORDER BY company
        """,
        connection
    )

    # --------------------------------------------------------
    # Missing values
    # --------------------------------------------------------

    missing_check = pd.read_sql_query(
        """
        SELECT
            COUNT(*) AS total_rows,
            SUM(
                CASE
                    WHEN company IS NULL
                    THEN 1
                    ELSE 0
                END
            ) AS missing_company,

            SUM(
                CASE
                    WHEN trade_date IS NULL
                    THEN 1
                    ELSE 0
                END
            ) AS missing_date,

            SUM(
                CASE
                    WHEN close_price IS NULL
                    THEN 1
                    ELSE 0
                END
            ) AS missing_close_price

        FROM stock_market_data
        """,
        connection
    )

    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------

    print("\n")
    print("=" * 75)
    print("DATABASE VALIDATION")
    print("=" * 75)
    print(f"Database: {DATABASE_PATH}")
    print(f"Total records: {total_rows}")
    print(f"Total companies: {total_companies}")
    print(f"Date range: {min_date} → {max_date}")
    print("\nRecords by company:")
    print(company_counts.to_string(index=False))
    print("\nMissing value check:")
    print(missing_check.to_string(index=False))
    print("=" * 75)

# ============================================================
# MAIN DATABASE BUILD
# ============================================================

def build_database():
    print("\n")
    print("=" * 75)
    print("BUILDING STOCK MARKET DATABASE")
    print("=" * 75)

    # --------------------------------------------------------
    # Load cleaned dataset
    # --------------------------------------------------------

    print("\n 1. Loading cleaned dataset...")
    df = load_cleaned_data()
    print(f"Loaded records: {len(df)}")

    # --------------------------------------------------------
    # Prepare database dataframe
    # --------------------------------------------------------

    print("\n 2. Preparing database columns...")
    database_df = prepare_data(df)
    print(
        f"Prepared records: "
        f"{len(database_df)}"
    )

    # --------------------------------------------------------
    # Create connection
    # --------------------------------------------------------

    print("\n 3. Creating SQLite database...")
    connection = get_connection()

    # --------------------------------------------------------
    # Create table
    # --------------------------------------------------------

    print("4. Creating stock_market_data table...")
    create_table(connection)

    # --------------------------------------------------------
    # Insert data
    # --------------------------------------------------------

    print("5. Inserting cleaned data...")
    insert_data(connection,database_df)

    # --------------------------------------------------------
    # Create indexes
    # --------------------------------------------------------

    print("6. Creating database indexes...")
    create_indexes(connection)

    # --------------------------------------------------------
    # Validate
    # --------------------------------------------------------

    print("7. Validating database...")
    validate_database(connection)

    # --------------------------------------------------------
    # Close connection
    # --------------------------------------------------------

    connection.close()
    print("\n")
    print("=" * 75)
    print("✅ DATABASE CREATED SUCCESSFULLY")
    print("=" * 75)
    print(f"\nDatabase file:")
    print(os.path.abspath(DATABASE_PATH))

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    build_database()