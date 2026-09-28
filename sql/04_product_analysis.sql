-- ============================================================================
-- SQL SCRIPT 04: PRODUCT SEGMENTATION & ABC ANALYSIS
-- Project: Retail Inventory & Supply Chain Performance Analysis
-- Database: SQLite / PostgreSQL Compatible
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 14: ABC Inventory Classification (Pareto 70/20/10 Analysis)
-- Methodology:
--   Class A: Top products contributing up to 70% of total annual COGS value.
--   Class B: Products contributing the next 20% (70% to 90%).
--   Class C: Bottom products contributing the remaining 10% (90% to 100%).
-- ----------------------------------------------------------------------------
WITH product_cogs AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        ROUND(SUM(s.cost_amount), 2) AS total_cogs,
        ROUND(SUM(s.sales_amount), 2) AS total_sales
    FROM fact_sales s
    JOIN dim_product p ON s.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category
),
cogs_pareto AS (
    SELECT 
        product_id,
        product_name,
        category,
        total_cogs,
        total_sales,
        SUM(total_cogs) OVER (ORDER BY total_cogs DESC) AS cum_cogs,
        SUM(total_cogs) OVER () AS grand_total_cogs
    FROM product_cogs
)
SELECT 
    product_id,
    product_name,
    category,
    total_cogs,
    total_sales,
    ROUND((cum_cogs / grand_total_cogs) * 100.0, 2) AS cumulative_cogs_pct,
    CASE 
        WHEN (cum_cogs / grand_total_cogs) <= 0.70 THEN 'Class A (High Value)'
        WHEN (cum_cogs / grand_total_cogs) <= 0.90 THEN 'Class B (Medium Value)'
        ELSE 'Class C (Low Value)'
    END AS abc_classification
FROM cogs_pareto
ORDER BY total_cogs DESC;


-- ----------------------------------------------------------------------------
-- QUERY 15: Identification of Slow-Moving Products
-- Criteria: Products with Days of Inventory (DIO) > 90 days and low annual units sold.
-- ----------------------------------------------------------------------------
WITH prod_perf AS (
    SELECT 
        p.product_id,
        p.product_name,
        p.category,
        p.unit_cost,
        SUM(s.quantity_sold) AS units_sold,
        SUM(s.cost_amount) AS total_cogs
    FROM fact_sales s
    JOIN dim_product p ON s.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category, p.unit_cost
),
prod_inv_val AS (
    SELECT 
        i.product_id,
        AVG(i.closing_stock) AS avg_stock_units,
        AVG(i.closing_stock * p.unit_cost) AS avg_inv_value
    FROM fact_inventory i
    JOIN dim_product p ON i.product_id = p.product_id
    GROUP BY i.product_id
)
SELECT 
    pp.product_id,
    pp.product_name,
    pp.category,
    pp.units_sold,
    ROUND(piv.avg_stock_units, 1) AS avg_stock_units,
    ROUND(piv.avg_inv_value, 2) AS avg_inventory_value,
    ROUND((piv.avg_inv_value / NULLIF(pp.total_cogs, 0)) * 365.0, 1) AS days_of_inventory
FROM prod_perf pp
JOIN prod_inv_val piv ON pp.product_id = piv.product_id
WHERE (piv.avg_inv_value / NULLIF(pp.total_cogs, 0)) * 365.0 > 90.0
ORDER BY days_of_inventory DESC;


-- ----------------------------------------------------------------------------
-- QUERY 16: Excess Inventory Risk Classification & Capital Tied Up
-- Purpose: Flag products where closing stock far exceeds safety stock & reorder requirements.
-- ----------------------------------------------------------------------------
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    ROUND(AVG(i.closing_stock), 1) AS avg_closing_stock,
    ROUND(AVG(i.reorder_point), 1) AS avg_reorder_point,
    ROUND(AVG(i.closing_stock * p.unit_cost), 2) AS total_inventory_value,
    SUM(i.excess_inventory_flag) AS excess_snapshot_count,
    CASE 
        WHEN AVG(i.closing_stock) > AVG(i.reorder_point) * 3.5 THEN 'CRITICAL EXCESS'
        WHEN AVG(i.closing_stock) > AVG(i.reorder_point) * 2.0 THEN 'HIGH EXCESS'
        ELSE 'BALANCED'
    END AS excess_risk_status
FROM fact_inventory i
JOIN dim_product p ON i.product_id = p.product_id
GROUP BY p.product_id, p.product_name, p.category
HAVING AVG(i.closing_stock) > AVG(i.reorder_point) * 2.0
ORDER BY total_inventory_value DESC;
