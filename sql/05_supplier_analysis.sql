-- ============================================================================
-- SQL SCRIPT 05: SUPPLIER & SUPPLY CHAIN PERFORMANCE ANALYSIS
-- Project: Retail Inventory & Supply Chain Performance Analysis
-- Database: SQLite / PostgreSQL Compatible
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 17: Supplier Performance Scorecard
-- Formula:
--   Fill Rate % = (Quantity Received / Quantity Ordered) * 100
--   On-Time Delivery Rate % = (Orders Delivered On-Time / Total Orders) * 100
-- ----------------------------------------------------------------------------
SELECT 
    sup.supplier_id,
    sup.supplier_name,
    sup.supplier_region,
    sup.supplier_type,
    COUNT(po.purchase_id) AS total_orders,
    SUM(po.quantity_ordered) AS total_units_ordered,
    SUM(po.quantity_received) AS total_units_received,
    ROUND((CAST(SUM(po.quantity_received) AS FLOAT) / SUM(po.quantity_ordered)) * 100.0, 2) AS supplier_fill_rate_pct,
    ROUND(
        (CAST(SUM(CASE WHEN po.actual_delivery_date <= po.expected_delivery_date THEN 1 ELSE 0 END) AS FLOAT) / COUNT(po.purchase_id)) * 100.0, 2
    ) AS on_time_delivery_rate_pct,
    ROUND(AVG(po.lead_time_days), 1) AS avg_actual_lead_time_days
FROM fact_purchase po
JOIN dim_supplier sup ON po.supplier_id = sup.supplier_id
GROUP BY sup.supplier_id, sup.supplier_name, sup.supplier_region, sup.supplier_type
ORDER BY supplier_fill_rate_pct ASC;


-- ----------------------------------------------------------------------------
-- QUERY 18: Supply Chain Delays & Bottleneck Exception Report
-- Purpose: Identify suppliers with severe lead time spikes and low fulfillment.
-- ----------------------------------------------------------------------------
SELECT 
    po.purchase_id,
    sup.supplier_name,
    p.product_name,
    st.store_name,
    po.order_date,
    po.expected_delivery_date,
    po.actual_delivery_date,
    po.lead_time_days,
    po.quantity_ordered,
    po.quantity_received,
    (po.quantity_ordered - po.quantity_received) AS shorted_units,
    CASE 
        WHEN po.actual_delivery_date > po.expected_delivery_date AND po.quantity_received < po.quantity_ordered THEN 'DELAYED & SHORTED'
        WHEN po.actual_delivery_date > po.expected_delivery_date THEN 'DELAYED'
        WHEN po.quantity_received < po.quantity_ordered THEN 'SHORTED'
        ELSE 'FULFILLED ON-TIME'
    END AS po_status
FROM fact_purchase po
JOIN dim_supplier sup ON po.supplier_id = sup.supplier_id
JOIN dim_product p ON po.product_id = p.product_id
JOIN dim_store st ON po.store_id = st.store_id
WHERE po.actual_delivery_date > po.expected_delivery_date 
   OR po.quantity_received < po.quantity_ordered
ORDER BY po.lead_time_days DESC
LIMIT 20;
