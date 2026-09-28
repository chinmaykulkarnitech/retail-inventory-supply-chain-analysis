-- ============================================================================
-- SQL SCRIPT 01: SALES PERFORMANCE ANALYSIS
-- Project: Retail Inventory & Supply Chain Performance Analysis
-- Database: SQLite / PostgreSQL Compatible
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1: Executive Sales Overview & Financial Totals
-- Purpose: Summarize revenue, unit volume, cost of goods sold, and gross profit margin.
-- ----------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT s.sale_id) AS total_transactions,
    SUM(s.quantity_sold) AS total_units_sold,
    ROUND(SUM(s.sales_amount), 2) AS total_sales_amount,
    ROUND(SUM(s.cost_amount), 2) AS total_cogs,
    ROUND(SUM(s.gross_profit), 2) AS total_gross_profit,
    ROUND((SUM(s.gross_profit) / SUM(s.sales_amount)) * 100.0, 2) AS gross_margin_pct
FROM fact_sales s;


-- ----------------------------------------------------------------------------
-- QUERY 2: Sales Breakdown by Product Category and Subcategory
-- Purpose: Evaluate category contribution to total sales volume and profit margins.
-- ----------------------------------------------------------------------------
SELECT 
    p.category,
    p.subcategory,
    COUNT(DISTINCT s.sale_id) AS transaction_count,
    SUM(s.quantity_sold) AS total_units_sold,
    ROUND(SUM(s.sales_amount), 2) AS category_sales_amount,
    ROUND(SUM(s.gross_profit), 2) AS category_gross_profit,
    ROUND((SUM(s.gross_profit) / SUM(s.sales_amount)) * 100.0, 2) AS gross_margin_pct,
    ROUND(
        (SUM(s.sales_amount) / SUM(SUM(s.sales_amount)) OVER ()) * 100.0, 2
    ) AS sales_contribution_pct
FROM fact_sales s
JOIN dim_product p ON s.product_id = p.product_id
GROUP BY p.category, p.subcategory
ORDER BY category_sales_amount DESC;


-- ----------------------------------------------------------------------------
-- QUERY 3: Sales Performance by Store Location & Store Type
-- Purpose: Identify top-performing stores and regions to guide inventory allocation.
-- ----------------------------------------------------------------------------
SELECT 
    st.store_id,
    st.store_name,
    st.city,
    st.state,
    st.region,
    st.store_type,
    SUM(s.quantity_sold) AS total_units_sold,
    ROUND(SUM(s.sales_amount), 2) AS store_sales_amount,
    ROUND(SUM(s.gross_profit), 2) AS store_gross_profit,
    ROUND((SUM(s.gross_profit) / SUM(s.sales_amount)) * 100.0, 2) AS gross_margin_pct
FROM fact_sales s
JOIN dim_store st ON s.store_id = st.store_id
GROUP BY st.store_id, st.store_name, st.city, st.state, st.region, st.store_type
ORDER BY store_sales_amount DESC;


-- ----------------------------------------------------------------------------
-- QUERY 4: Monthly Sales Trend & Month-over-Month (MoM) Growth Rate
-- Purpose: Analyze monthly revenue momentum and MoM growth rate using window function LAG().
-- ----------------------------------------------------------------------------
WITH monthly_summary AS (
    SELECT 
        d.year,
        d.month,
        d.month_name,
        SUM(s.quantity_sold) AS monthly_units,
        ROUND(SUM(s.sales_amount), 2) AS monthly_sales,
        ROUND(SUM(s.gross_profit), 2) AS monthly_profit
    FROM fact_sales s
    JOIN dim_date d ON s.date_id = d.date_id
    GROUP BY d.year, d.month, d.month_name
)
SELECT 
    year,
    month,
    month_name,
    monthly_units,
    monthly_sales,
    monthly_profit,
    LAG(monthly_sales) OVER (ORDER BY year, month) AS prev_month_sales,
    ROUND(
        ((monthly_sales - LAG(monthly_sales) OVER (ORDER BY year, month)) / 
        LAG(monthly_sales) OVER (ORDER BY year, month)) * 100.0, 2
    ) AS mom_growth_pct
FROM monthly_summary
ORDER BY year, month;


-- ----------------------------------------------------------------------------
-- QUERY 5: Top 10 Best-Selling Products by Revenue
-- Purpose: Highlight revenue drivers using window function DENSE_RANK().
-- ----------------------------------------------------------------------------
WITH product_sales AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        SUM(s.quantity_sold) AS units_sold,
        ROUND(SUM(s.sales_amount), 2) AS total_sales,
        ROUND(SUM(s.gross_profit), 2) AS total_profit
    FROM fact_sales s
    JOIN dim_product p ON s.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    DENSE_RANK() OVER (ORDER BY total_sales DESC) AS revenue_rank,
    product_id,
    product_name,
    category,
    units_sold,
    total_sales,
    total_profit
FROM product_sales
LIMIT 10;


-- ----------------------------------------------------------------------------
-- QUERY 6: Bottom 10 Slowest-Selling Products by Revenue
-- Purpose: Identify low-velocity products candidate for markdown or discontinuation.
-- ----------------------------------------------------------------------------
WITH product_sales AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        SUM(s.quantity_sold) AS units_sold,
        ROUND(SUM(s.sales_amount), 2) AS total_sales,
        ROUND(SUM(s.gross_profit), 2) AS total_profit
    FROM fact_sales s
    JOIN dim_product p ON s.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
)
SELECT 
    DENSE_RANK() OVER (ORDER BY total_sales ASC) AS bottom_rank,
    product_id,
    product_name,
    category,
    units_sold,
    total_sales,
    total_profit
FROM product_sales
LIMIT 10;


-- ----------------------------------------------------------------------------
-- QUERY 7: 7-Day Moving Average Sales per Store
-- Purpose: Smooth daily demand fluctuations for inventory reordering signals.
-- ----------------------------------------------------------------------------
WITH daily_store_sales AS (
    SELECT 
        s.store_id,
        s.date,
        SUM(s.sales_amount) AS daily_sales
    FROM fact_sales s
    GROUP BY s.store_id, s.date
)
SELECT 
    store_id,
    date,
    ROUND(daily_sales, 2) AS daily_sales,
    ROUND(
        AVG(daily_sales) OVER (
            PARTITION BY store_id 
            ORDER BY date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    ) AS rolling_7day_avg_sales
FROM daily_store_sales
ORDER BY store_id, date;
