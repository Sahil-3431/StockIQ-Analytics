-- ============================================================
-- SQL - STOCK MARKET ANALYSIS
-- 30 PROFESSIONAL SQL QUERIES
-- ============================================================


-- ============================================================
-- CATEGORY 1: BASIC DATA EXPLORATION
-- ============================================================


-- Q01. Total number of records
SELECT COUNT(*) AS total_records
FROM stock_market_data;


-- Q02. Total number of companies
SELECT COUNT(DISTINCT company) AS total_companies
FROM stock_market_data;


-- Q03. List all companies
SELECT DISTINCT company
FROM stock_market_data
ORDER BY company;


-- Q04. Minimum and maximum trading date
SELECT
    MIN(trade_date) AS start_date,
    MAX(trade_date) AS end_date
FROM stock_market_data;


-- Q05. Records available for each company
SELECT
    company,
    COUNT(*) AS total_records
FROM stock_market_data
GROUP BY company
ORDER BY total_records DESC;



-- ============================================================
-- CATEGORY 2: PRICE ANALYSIS
-- ============================================================


-- Q06. Average closing price by company
SELECT
    company,
    ROUND(AVG(close_price), 2) AS avg_close_price
FROM stock_market_data
GROUP BY company
ORDER BY avg_close_price DESC;


-- Q07. Highest closing price for each company
SELECT
    company,
    ROUND(MAX(close_price), 2) AS highest_close_price
FROM stock_market_data
GROUP BY company
ORDER BY highest_close_price DESC;


-- Q08. Lowest closing price for each company
SELECT
    company,
    ROUND(MIN(close_price), 2) AS lowest_close_price
FROM stock_market_data
GROUP BY company
ORDER BY lowest_close_price DESC;


-- Q09. Highest trading day by closing price
SELECT
    company,
    trade_date,
    close_price
FROM stock_market_data
ORDER BY close_price DESC
LIMIT 10;


-- Q10. Average daily price range by company
SELECT
    company,
    ROUND(AVG(price_range), 2) AS avg_price_range
FROM stock_market_data
GROUP BY company
ORDER BY avg_price_range DESC;



-- ============================================================
-- CATEGORY 3: RETURN ANALYSIS
-- ============================================================


-- Q11. Average daily return by company
SELECT
    company,
    ROUND(AVG(daily_return_percentage), 4) AS avg_daily_return
FROM stock_market_data
GROUP BY company
ORDER BY avg_daily_return DESC;


-- Q12. Maximum daily return by company
SELECT
    company,
    ROUND(MAX(daily_return_percentage), 2) AS max_daily_return
FROM stock_market_data
GROUP BY company
ORDER BY max_daily_return DESC;


-- Q13. Minimum daily return by company
SELECT
    company,
    ROUND(MIN(daily_return_percentage), 2) AS min_daily_return
FROM stock_market_data
GROUP BY company
ORDER BY min_daily_return;


-- Q14. Number of positive trading days
SELECT
    company,
    COUNT(*) AS positive_days
FROM stock_market_data
WHERE daily_return_percentage > 0
GROUP BY company
ORDER BY positive_days DESC;


-- Q15. Number of negative trading days
SELECT
    company,
    COUNT(*) AS negative_days
FROM stock_market_data
WHERE daily_return_percentage < 0
GROUP BY company
ORDER BY negative_days DESC;



-- ============================================================
-- CATEGORY 4: TRADING ACTIVITY
-- ============================================================


-- Q16. Total turnover by company
SELECT
    company,
    ROUND(SUM(total_turnover) / 10000000.0, 2)
        AS total_turnover_crore
FROM stock_market_data
GROUP BY company
ORDER BY total_turnover_crore DESC;


-- Q17. Average turnover by company
SELECT
    company,
    ROUND(AVG(turnover_crore), 2) AS avg_turnover_crore
FROM stock_market_data
GROUP BY company
ORDER BY avg_turnover_crore DESC;


-- Q18. Total number of trades by company
SELECT
    company,
    SUM(no_of_trades) AS total_trades
FROM stock_market_data
GROUP BY company
ORDER BY total_trades DESC;


-- Q19. Average number of trades per day
SELECT
    company,
    ROUND(AVG(no_of_trades), 0) AS avg_daily_trades
FROM stock_market_data
GROUP BY company
ORDER BY avg_daily_trades DESC;


-- Q20. Highest turnover trading days
SELECT
    company,
    trade_date,
    ROUND(turnover_crore, 2) AS turnover_crore
FROM stock_market_data
ORDER BY turnover_crore DESC
LIMIT 10;



-- ============================================================
-- CATEGORY 5: VOLUME & DELIVERY ANALYSIS
-- ============================================================


-- Q21. Average traded volume by company
SELECT
    company,
    ROUND(AVG(volume_lakh), 2) AS avg_volume_lakh
FROM stock_market_data
GROUP BY company
ORDER BY avg_volume_lakh DESC;


-- Q22. Total traded volume by company
SELECT
    company,
    ROUND(SUM(volume_lakh), 2) AS total_volume_lakh
FROM stock_market_data
GROUP BY company
ORDER BY total_volume_lakh DESC;


-- Q23. Average delivery percentage
SELECT
    company,
    ROUND(AVG(delivery_percentage), 2) AS avg_delivery_percentage
FROM stock_market_data
GROUP BY company
ORDER BY avg_delivery_percentage DESC;


-- Q24. Highest delivery percentage trading days
SELECT
    company,
    trade_date,
    ROUND(delivery_percentage, 2) AS delivery_percentage
FROM stock_market_data
ORDER BY delivery_percentage DESC
LIMIT 10;


-- Q25. Companies with average delivery percentage above 50%
SELECT
    company,
    ROUND(AVG(delivery_percentage), 2)
        AS avg_delivery_percentage
FROM stock_market_data
GROUP BY company
HAVING AVG(delivery_percentage) > 50
ORDER BY avg_delivery_percentage DESC;



-- ============================================================
-- CATEGORY 6: YEARLY ANALYSIS
-- ============================================================


-- Q26. Yearly average closing price
SELECT
    company,
    strftime('%Y', trade_date) AS year,
    ROUND(AVG(close_price), 2) AS avg_close_price
FROM stock_market_data
GROUP BY company, year
ORDER BY company, year;


-- Q27. Yearly total turnover
SELECT
    company,
    strftime('%Y', trade_date) AS year,
    ROUND(SUM(total_turnover) / 10000000.0, 2)
        AS turnover_crore
FROM stock_market_data
GROUP BY company, year
ORDER BY year, turnover_crore DESC;


-- Q28. Yearly number of trading days
SELECT
    company,
    strftime('%Y', trade_date) AS year,
    COUNT(*) AS trading_days
FROM stock_market_data
GROUP BY company, year
ORDER BY company, year;


-- Q29. Yearly average daily return
SELECT
    company,
    strftime('%Y', trade_date) AS year,
    ROUND(AVG(daily_return_percentage), 4)
        AS avg_daily_return
FROM stock_market_data
GROUP BY company, year
ORDER BY company, year;


-- Q30. Overall company performance summary
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

    ROUND(SUM(total_turnover) / 10000000.0, 2)
        AS total_turnover_crore,

    SUM(no_of_trades)
        AS total_trades

FROM stock_market_data
GROUP BY company
ORDER BY total_turnover_crore DESC;