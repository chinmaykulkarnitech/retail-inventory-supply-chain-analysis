-- ============================================================================
-- SQL SCRIPT 03: STOCKOUT & AVAILABILITY ANALYSIS
-- Project: Retail Inventory & Supply Chain Performance Analysis
-- Database: SQLite / PostgreSQL Compatible
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 11: Stockout Events & Stockout Rate % by Category & Store
-- Formula: Stockout Rate % = (Stockout Observations / Total Observation Events) * 100
-- ----------------------------------------------------------------------------
SELECT 
    p.category,
    st.store_name,
    st.region,
    COUNT(i.inventory_date) AS total_observation_events,
    SUM(i.stockout_flag) AS stockout_events,
    ROUND((CAST(SUM(i.stockout_flag) AS FLOAT) / COUNT(i.inventory_date)) * 100.0, 2) AS stockout_rate_pct
FROM fact_inventory i
JOIN dim_product p ON i.product_id = p.product_id
JOIN dim_store st ON i.store_id = st.store_id
GROUP BY p.category, st.store_name, st.region
HAVING SUM(i.stockout_flag) > 0
ORDER BY stockout_rate_pct DESC;


-- ----------------------------------------------------------------------------
-- QUERY 12: Ranking Stockout-Prone SKUs across the Retail Network
-- Purpose: Identify top SKUs experiencing out-of-stock conditions using window ranking.
-- ----------------------------------------------------------------------------
WITH sku_stockouts AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        p.brand,
        SUM(i.stockout_flag) AS total_stockout_days,
        COUNT(i.inventory_date) AS total_obs_days,
        ROUND((CAST(SUM(i.stockout_flag) AS FLOAT) / COUNT(i.inventory_date)) * 100.0, 2) AS stockout_rate_pct
    FROM fact_inventory i
    JOIN dim_product p ON i.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category, p.brand
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY stockout_rate_pct DESC, total_stockout_days DESC) AS stockout_rank,
    product_id,
    product_name,
    category,
    brand,
    total_stockout_days,
    stockout_rate_pct,
    CASE 
        WHEN stockout_rate_pct >= 8.0 THEN 'CRITICAL RISK'
        WHEN stockout_rate_pct >= 4.0 THEN 'HIGH RISK'
        ELSE 'MODERATE RISK'
    END AS stockout_risk_level
FROM sku_stockouts
WHERE total_stockout_days > 0
LIMIT 15;


-- ----------------------------------------------------------------------------
-- QUERY 13: Estimated Lost Sales Opportunity from Stockouts
-- Methodology: 
--   Estimated Lost Revenue = Stockout Days * Average Daily Sales Revenue (when in stock)
-- ----------------------------------------------------------------------------
WITH avg_daily_sales AS (
    SELECT 
        product_id,
        store_id,
        SUM(sales_amount) / 365.0 AS avg_daily_sales_amount,
        SUM(quantity_sold) / 365.0 AS avg_daily_units
    FROM fact_sales
    GROUP BY product_id, store_id
),
stockout_summary AS (
    SELECT 
        product_id,
        store_id,
        SUM(stockout_flag) AS stockout_days
    FROM fact_inventory
    WHERE stockout_flag = 1
    GROUP BY product_id, store_id
)
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    st.store_name,
    ss.stockout_days,
    ROUND(ads.avg_daily_units, 2) AS est_daily_lost_units,
    ROUND(ads.avg_daily_sales_amount, 2) AS est_daily_lost_revenue,
    ROUND(ss.stockout_days * ads.avg_daily_sales_amount, 2) AS estimated_lost_sales_opportunity
FROM stockout_summary ss
JOIN avg_daily_sales ads ON ss.product_id = ads.product_id AND ss.store_id = ads.store_id
JOIN dim_product p ON ss.product_id = p.product_id
JOIN dim_store st ON ss.store_id = st.store_id
ORDER BY estimated_lost_sales_opportunity DESC;
