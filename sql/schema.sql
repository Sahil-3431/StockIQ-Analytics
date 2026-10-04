-- ============================================================
-- SQL - STOCK MARKET ANALYSIS
-- Database Schema
-- ============================================================

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
);

-- ============================================================
-- INDEXES
-- ============================================================

CREATE INDEX IF NOT EXISTS idx_company
ON stock_market_data(company);

CREATE INDEX IF NOT EXISTS idx_trade_date
ON stock_market_data(trade_date);

CREATE INDEX IF NOT EXISTS idx_company_date
ON stock_market_data(company, trade_date);

CREATE INDEX IF NOT EXISTS idx_close_price
ON stock_market_data(close_price);

CREATE INDEX IF NOT EXISTS idx_turnover
ON stock_market_data(total_turnover);