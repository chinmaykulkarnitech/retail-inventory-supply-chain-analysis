-- ============================================================================
-- SQL SCRIPT 06: ADVANCED INVENTORY ANALYTICS & MANAGEMENT ACTION CENTER
-- Project: Retail Inventory & Supply Chain Performance Analysis
-- Database: SQLite / PostgreSQL Compatible
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 19: Multi-Factor Composite Inventory Risk Score
-- Formula: 
--   Risk Score = (Stockout Rate % * 0.40) + (DIO Quartile * 0.30) + (100 - Fill Rate % * 0.30)
-- ----------------------------------------------------------------------------
WITH product_stockouts AS (
    SELECT 
        product_id,
        ROUND((CAST(SUM(stockout_flag) AS FLOAT) / COUNT(inventory_date)) * 100.0, 2) AS stockout_rate_pct
    FROM fact_inventory
    GROUP BY product_id
),
product_dio AS (
    SELECT 
        p.product_id,
        ROUND((AVG(i.closing_stock * p.unit_cost) / NULLIF(SUM(s.cost_amount), 0)) * 365.0, 1) AS dio
    FROM dim_product p
    JOIN fact_inventory i ON p.product_id = i.product_id
    LEFT JOIN fact_sales s ON p.product_id = s.product_id
    GROUP BY p.product_id
),
product_supplier_fr AS (
    SELECT 
        po.product_id,
        ROUND((CAST(SUM(po.quantity_received) AS FLOAT) / SUM(po.quantity_ordered)) * 100.0, 2) AS fill_rate_pct
    FROM fact_purchase po
    GROUP BY po.product_id
)
SELECT 
    p.product_id,
    p.product_name,
    p.category,
    COALESCE(ps.stockout_rate_pct, 0.0) AS stockout_rate_pct,
    COALESCE(pd.dio, 0.0) AS days_of_inventory,
    COALESCE(psf.fill_rate_pct, 100.0) AS supplier_fill_rate_pct,
    ROUND(
        (COALESCE(ps.stockout_rate_pct, 0.0) * 0.45) + 
        (CASE WHEN pd.dio > 90 THEN 30.0 WHEN pd.dio > 60 THEN 15.0 ELSE 0.0 END) + 
        ((100.0 - COALESCE(psf.fill_rate_pct, 100.0)) * 0.25), 2
    ) AS composite_risk_score,
    CASE 
        WHEN (COALESCE(ps.stockout_rate_pct, 0.0) * 0.45) + (CASE WHEN pd.dio > 90 THEN 30.0 ELSE 0.0 END) >= 20.0 THEN 'ACTION REQUIRED: REPLENISH OR MARKDOWN'
        ELSE 'STABLE'
    END AS action_recommendation
FROM dim_product p
LEFT JOIN product_stockouts ps ON p.product_id = ps.product_id
LEFT JOIN product_dio pd ON p.product_id = pd.product_id
LEFT JOIN product_supplier_fr psf ON p.product_id = psf.product_id
ORDER BY composite_risk_score DESC;


-- ----------------------------------------------------------------------------
-- QUERY 20: Store Inventory Efficiency Matrix (Sales Share vs Inventory Share)
-- Purpose: Benchmark store capital allocation efficiency.
-- ----------------------------------------------------------------------------
WITH store_sales_summary AS (
    SELECT 
        s.store_id,
        SUM(s.sales_amount) AS store_sales
    FROM fact_sales s
    GROUP BY s.store_id
),
store_inv_summary AS (
    SELECT 
        i.store_id,
        AVG(i.closing_stock * p.unit_cost) AS store_avg_inv
    FROM fact_inventory i
    JOIN dim_product p ON i.product_id = p.product_id
    GROUP BY i.store_id
),
network_totals AS (
    SELECT 
        (SELECT SUM(sales_amount) FROM fact_sales) AS total_network_sales,
        (SELECT SUM(i.closing_stock * p.unit_cost)/COUNT(DISTINCT i.inventory_date) FROM fact_inventory i JOIN dim_product p ON i.product_id = p.product_id) AS total_network_inv
)
SELECT 
    st.store_id,
    st.store_name,
    st.region,
    st.store_type,
    ROUND((sss.store_sales / nt.total_network_sales) * 100.0, 2) AS sales_share_pct,
    ROUND((sis.store_avg_inv / nt.total_network_inv) * 100.0, 2) AS inventory_share_pct,
    ROUND(
        ((sss.store_sales / nt.total_network_sales) * 100.0) - ((sis.store_avg_inv / nt.total_network_inv) * 100.0), 2
    ) AS efficiency_spread_pct,
    CASE 
        WHEN ((sss.store_sales / nt.total_network_sales) * 100.0) > ((sis.store_avg_inv / nt.total_network_inv) * 100.0) THEN 'HIGH EFFICIENCY (LEAN)'
        ELSE 'LOW EFFICIENCY (OVER-STOCKED)'
    END AS efficiency_rating
FROM dim_store st
JOIN store_sales_summary sss ON st.store_id = sss.store_id
JOIN store_inv_summary sis ON st.store_id = sis.store_id
CROSS JOIN network_totals nt
ORDER BY efficiency_spread_pct DESC;
