-- ============================================================================
-- SQL SCRIPT 02: INVENTORY PERFORMANCE & TURNOVER ANALYSIS
-- Project: Retail Inventory & Supply Chain Performance Analysis
-- Database: SQLite / PostgreSQL Compatible
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 8: Inventory Holding Summary & Value by Category
-- Purpose: Calculate average closing stock units, inventory valuation, and total holding cost.
-- ----------------------------------------------------------------------------
SELECT 
    p.category,
    COUNT(DISTINCT i.product_id) AS total_skus,
    ROUND(AVG(i.closing_stock), 1) AS avg_closing_units,
    ROUND(SUM(i.closing_stock * p.unit_cost) / COUNT(DISTINCT i.inventory_date), 2) AS avg_daily_inventory_value,
    ROUND(MAX(i.closing_stock * p.unit_cost), 2) AS peak_inventory_value
FROM fact_inventory i
JOIN dim_product p ON i.product_id = p.product_id
GROUP BY p.category
ORDER BY avg_daily_inventory_value DESC;


-- ----------------------------------------------------------------------------
-- QUERY 9: Category Inventory Turnover & Days of Inventory Outstanding (DIO)
-- Formula: 
--   Inventory Turnover = Annual COGS / Average Inventory Value
--   DIO = (Average Inventory Value / Annual COGS) * 365
-- ----------------------------------------------------------------------------
WITH category_cogs AS (
    SELECT 
        p.category,
        SUM(s.cost_amount) AS total_annual_cogs
    FROM fact_sales s
    JOIN dim_product p ON s.product_id = p.product_id
    GROUP BY p.category
),
category_inv AS (
    SELECT 
        p.category,
        SUM(i.closing_stock * p.unit_cost) / COUNT(DISTINCT i.inventory_date) AS avg_inv_value
    FROM fact_inventory i
    JOIN dim_product p ON i.product_id = p.product_id
    GROUP BY p.category
)
SELECT 
    c.category,
    ROUND(c.total_annual_cogs, 2) AS total_annual_cogs,
    ROUND(i.avg_inv_value, 2) AS avg_inventory_value,
    ROUND(c.total_annual_cogs / NULLIF(i.avg_inv_value, 0), 2) AS inventory_turnover_ratio,
    ROUND((i.avg_inv_value / NULLIF(c.total_annual_cogs, 0)) * 365.0, 1) AS days_of_inventory_outstanding
FROM category_cogs c
JOIN category_inv i ON c.category = i.category
ORDER BY inventory_turnover_ratio DESC;


-- ----------------------------------------------------------------------------
-- QUERY 10: Store-Level Inventory Distribution & Turnover Efficiency
-- Purpose: Compare inventory carrying efficiency across stores to detect operational imbalances.
-- ----------------------------------------------------------------------------
WITH store_cogs AS (
    SELECT 
        s.store_id,
        SUM(s.cost_amount) AS store_annual_cogs
    FROM fact_sales s
    GROUP BY s.store_id
),
store_inv AS (
    SELECT 
        i.store_id,
        SUM(i.closing_stock * p.unit_cost) / COUNT(DISTINCT i.inventory_date) AS store_avg_inv_value
    FROM fact_inventory i
    JOIN dim_product p ON i.product_id = p.product_id
    GROUP BY i.store_id
)
SELECT 
    st.store_id,
    st.store_name,
    st.city,
    st.region,
    st.store_type,
    ROUND(sc.store_annual_cogs, 2) AS annual_cogs,
    ROUND(si.store_avg_inv_value, 2) AS avg_inventory_value,
    ROUND(sc.store_annual_cogs / NULLIF(si.store_avg_inv_value, 0), 2) AS store_inventory_turnover,
    ROUND((si.store_avg_inv_value / NULLIF(sc.store_annual_cogs, 0)) * 365.0, 1) AS store_dio
FROM dim_store st
JOIN store_cogs sc ON st.store_id = sc.store_id
JOIN store_inv si ON st.store_id = si.store_id
ORDER BY store_inventory_turnover DESC;
