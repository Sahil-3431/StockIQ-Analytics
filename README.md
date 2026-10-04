# 📊 SQL - Stock Market Analysis

A professional end-to-end stock market analytics project built using **Python, SQL, SQLite, Pandas, Plotly, and Streamlit**.

The project analyzes historical stock market data of six major companies and provides interactive dashboards, SQL-based analytics, trading activity analysis, performance comparison, and business insights.

---

## 🚀 Live Application

🔗 Streamlit App:  
[https://stockiq-analytics.streamlit.app/]

---

## 💻 GitHub Repository

🔗 GitHub Repository:  
[https://github.com/Sahil-3431/StockIQ-Analytics]

---

## 📌 Project Overview

This project focuses on analyzing historical stock market data from:

- Bajaj Auto
- Eicher Motors
- Hero Motocorp
- Infosys
- TCS
- TVS Motors

The dataset contains daily trading information including:

- Open Price
- High Price
- Low Price
- Close Price
- WAP
- Number of Shares
- Number of Trades
- Total Turnover
- Deliverable Quantity
- Delivery Percentage
- Spread High-Low
- Spread Close-Open

Additional analytical metrics were created during data preparation.

---

## 🎯 Project Objectives

The main objectives of this project are:

- Analyze historical stock price movements
- Compare company performance
- Analyze daily returns and volatility
- Study trading activity
- Analyze turnover and trading volume
- Analyze delivery percentage
- Identify positive and negative trading days
- Perform SQL-based stock market analysis
- Generate actionable business insights
- Build an interactive analytics dashboard

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Data processing and application development |
| Pandas | Data cleaning and analysis |
| NumPy | Numerical calculations |
| SQLite | Database management |
| SQL | Analytical queries |
| Plotly | Interactive visualizations |
| Streamlit | Interactive dashboard |
| GitHub | Version control and project hosting |

---

## 📂 Project Structure

```text
SQL-Stock-Market-Analysis/
│
├── data/
│   ├── raw/
│   │   ├── Bajaj Auto.csv
│   │   ├── Eicher Motors.csv
│   │   ├── Hero Motocorp.csv
│   │   ├── Infosys.csv
│   │   ├── TCS.csv
│   │   └── TVS Motors.csv
│   │
│   └── cleaned/
│       ├── Bajaj_Auto_cleaned.csv
│       ├── Eicher_Motors_cleaned.csv
│       ├── Hero_Motocorp_cleaned.csv
│       ├── Infosys_cleaned.csv
│       ├── TCS_cleaned.csv
│       ├── TVS_Motors_cleaned.csv
│       └── stock_market_combined.csv
│
├── sql/
│   ├── schema.sql
│   └── queries.sql
│
├── utils/
│   ├── __init__.py
│   ├── database.py
│   ├── queries.py
│   ├── calculations.py
│   └── theme.py
│
├── app.py
├── data_cleaning.py
├── database.py
├── requirements.txt
└── stock_market.db