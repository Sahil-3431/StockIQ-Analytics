import os
import pandas as pd

# ============================================================
# PATH CONFIGURATION
# ============================================================

RAW_DIR = os.path.join("data", "raw")
CLEANED_DIR = os.path.join("data", "cleaned")
os.makedirs(CLEANED_DIR, exist_ok=True)

# ============================================================
# SOURCE FILES
# ============================================================

FILES = {
    "Bajaj Auto": "Bajaj Auto.csv",
    "Eicher Motors": "Eicher Motors.csv",
    "Hero Motocorp": "Hero Motocorp.csv",
    "Infosys": "Infosys.csv",
    "TCS": "TCS.csv",
    "TVS Motors": "TVS Motors.csv",
}

# ============================================================
# ACTUAL DATASET COLUMNS
# ============================================================

EXPECTED_COLUMNS = [
    "Date",
    "Open Price",
    "High Price",
    "Low Price",
    "Close Price",
    "WAP",
    "No.of Shares",
    "No. of Trades",
    "Total Turnover (Rs.)",
    "Deliverable Quantity",
    "% Deli. Qty to Traded Qty",
    "Spread High-Low",
    "Spread Close-Open",
]

# ============================================================
# CLEAN SINGLE COMPANY DATASET
# ============================================================

def clean_dataset(company_name, filename):
    print("\n" + "=" * 75)
    print(f"Cleaning: {company_name}")
    print("=" * 75)
    input_path = os.path.join(RAW_DIR, filename)

    # --------------------------------------------------------
    # Check file
    # --------------------------------------------------------

    if not os.path.exists(input_path):
        print(f"❌ File not found: {input_path}")
        return None

    # --------------------------------------------------------
    # Read CSV
    # --------------------------------------------------------

    df = pd.read_csv(input_path)
    print(f"Original rows: {len(df)}")
    print(f"Original columns: {len(df.columns)}")

    # --------------------------------------------------------
    # Clean column names
    # --------------------------------------------------------

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    # --------------------------------------------------------
    # Validate columns
    # --------------------------------------------------------

    missing_columns = [
        column
        for column in EXPECTED_COLUMNS
        if column not in df.columns
    ]
    if missing_columns:
        print("❌ Missing columns:")
        print(missing_columns)
        print("\nActual columns found:")
        print(list(df.columns))
        return None

    # --------------------------------------------------------
    # Keep required columns
    # --------------------------------------------------------

    df = df[EXPECTED_COLUMNS].copy()

    # ========================================================
    # DUPLICATE CHECK
    # ========================================================

    duplicate_count = df.duplicated().sum()
    print(f"Duplicate rows found: {duplicate_count}")
    if duplicate_count > 0:
        df = df.drop_duplicates().copy()
        print(f"Duplicates removed: {duplicate_count}")
    else:
        print("Duplicates removed: 0")

    # ========================================================
    # DATE CLEANING
    # ========================================================

    df["Date"] = pd.to_datetime(df["Date"],errors="coerce")
    invalid_dates = df["Date"].isna().sum()
    if invalid_dates > 0:
        print(f"Invalid dates removed: {invalid_dates}")
        df = df.dropna(subset=["Date"]).copy()
    else:
        print("Invalid dates removed: 0")

    # ========================================================
    # NUMERIC COLUMNS
    # ========================================================

    numeric_columns = [
        "Open Price",
        "High Price",
        "Low Price",
        "Close Price",
        "WAP",
        "No.of Shares",
        "No. of Trades",
        "Total Turnover (Rs.)",
        "Deliverable Quantity",
        "% Deli. Qty to Traded Qty",
        "Spread High-Low",
        "Spread Close-Open",
    ]
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column],errors="coerce")

    # ========================================================
    # MISSING VALUE ANALYSIS
    # ========================================================

    print("\nMissing values before cleaning:")
    missing_before = (
        df.isna()
        .sum()
        .sort_values(ascending=False)
    )
    print(missing_before[missing_before > 0])

    # ========================================================
    # NUMERIC MISSING VALUE TREATMENT
    # ========================================================

    df[numeric_columns] = (
        df[numeric_columns]
        .interpolate(method="linear")
        .ffill()
        .bfill()
    )

    # ========================================================
    # SORT BY DATE
    # ========================================================

    df = (
        df.sort_values("Date")
        .reset_index(drop=True)
    )

    # ========================================================
    # COMPANY COLUMN
    # ========================================================

    df["Company"] = company_name

    # ========================================================
    # CALCULATED ANALYTICS COLUMNS
    # ========================================================

    # Daily return
    df["Daily Return %"] = (
        df["Close Price"]
        .pct_change()
        * 100
    )

    # Price range
    df["Price Range"] = (
        df["High Price"]
        - df["Low Price"]
    )

    # Intraday return
    df["Intraday Return %"] = (
        (
            df["Close Price"]
            - df["Open Price"]
        )
        / df["Open Price"]
    ) * 100

    # Turnover in Crores
    df["Turnover Crore"] = (
        df["Total Turnover (Rs.)"]
        / 10_000_000
    )

    # Volume in Lakhs
    df["Volume Lakh"] = (
        df["No.of Shares"]
        / 100_000
    )

    # ========================================================
    # FIRST DAILY RETURN
    # ========================================================

    df["Daily Return %"] = (
        df["Daily Return %"]
        .replace([float("inf"), -float("inf")],0)
        .fillna(0)
    )

    # ========================================================
    # INTRADAY RETURN
    # ========================================================

    df["Intraday Return %"] = (
        df["Intraday Return %"]
        .replace([float("inf"), -float("inf")],0)
        .fillna(0)
    )

    # ========================================================
    # DATA VALIDATION
    # ========================================================

    invalid_ohlc = (
        (df["High Price"] < df["Open Price"])
        |
        (df["High Price"] < df["Close Price"])
        |
        (df["High Price"] < df["Low Price"])
        |
        (df["Low Price"] > df["Open Price"])
        |
        (df["Low Price"] > df["Close Price"])
    ).sum()
    print(f"\nInvalid OHLC records: {invalid_ohlc}")

    # --------------------------------------------------------
    # Negative value check
    # --------------------------------------------------------

    negative_price_rows = (
        (
            df[
                [
                    "Open Price",
                    "High Price",
                    "Low Price",
                    "Close Price",
                    "WAP",
                ]
            ] < 0
        )
        .any(axis=1)
        .sum()
    )
    print(
        f"Negative price records: "
        f"{negative_price_rows}"
    )

    # --------------------------------------------------------
    # Remaining missing values
    # --------------------------------------------------------

    missing_after = df.isna().sum().sum()
    print(
        f"Total missing values after cleaning: "
        f"{missing_after}"
    )

    # ========================================================
    # SAVE CLEANED COMPANY DATASET
    # ========================================================

    safe_name = company_name.replace(" ","_")
    output_path = os.path.join(CLEANED_DIR,f"{safe_name}.csv")
    df.to_csv(output_path,index=False)
    print(f"\n✅ Cleaned file saved:")
    print(output_path)
    print(f"Final rows: {len(df)}")
    print(f"Final columns: {len(df.columns)}")
    return df


# ============================================================
# MAIN PROCESS
# ============================================================

def main():
    all_data = []

    # --------------------------------------------------------
    # Process all companies
    # --------------------------------------------------------

    for company_name, filename in FILES.items():
        df = clean_dataset(company_name,filename)
        if df is not None:
            all_data.append(df)

    # --------------------------------------------------------
    # Check processing
    # --------------------------------------------------------

    if not all_data:
        print("\n❌ No datasets were processed.")
        return

    # ========================================================
    # COMBINE ALL COMPANIES
    # ========================================================

    combined_df = pd.concat(all_data,ignore_index=True)

    # ========================================================
    # SORT COMBINED DATA
    # ========================================================

    combined_df = (
        combined_df
        .sort_values(["Company", "Date"])
        .reset_index(drop=True)
    )

    # ========================================================
    # SAVE COMBINED DATASET
    # ========================================================

    combined_path = os.path.join(CLEANED_DIR,"stock_market_combined.csv")
    combined_df.to_csv(combined_path,index=False)

    # ========================================================
    # FINAL REPORT
    # ========================================================

    print("\n")
    print("=" * 75)
    print("FINAL DATA CLEANING REPORT")
    print("=" * 75)
    print(
        f"Total companies: "
        f"{combined_df['Company'].nunique()}"
    )
    print(
        f"Total records: "
        f"{len(combined_df)}"
    )
    print(
        f"Total columns: "
        f"{len(combined_df.columns)}"
    )
    print("\nRecords by company:")
    print(
        combined_df["Company"]
        .value_counts()
        .sort_index()
    )
    print("\nDate range:")
    print(
        f"{combined_df['Date'].min().date()}"
        f" → "
        f"{combined_df['Date'].max().date()}"
    )
    print("\nRemaining missing values:")
    remaining_missing = (
        combined_df
        .isna()
        .sum()
    )
    remaining_missing = (
        remaining_missing[remaining_missing > 0]
        .sort_values(ascending=False)
    )
    if len(remaining_missing) == 0:
        print("✅ No missing values")
    else:
        print(remaining_missing)
    print("\nCompany-wise date range:")
    company_dates = (
        combined_df
        .groupby("Company")["Date"]
        .agg(
            ["min", "max", "count"]
        )
    )
    print(company_dates)
    print("\n" + "=" * 75)
    print("✅ CLEANING COMPLETED SUCCESSFULLY")
    print("=" * 75)
    print(f"\nCombined dataset:")
    print(combined_path)

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()