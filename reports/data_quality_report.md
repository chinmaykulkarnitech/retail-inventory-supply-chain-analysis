# Data Quality Audit & Cleaning Report

## Overview
This document details the data quality checks, audit results, and cleaning actions executed on the raw retail inventory and supply chain dataset.

### Executive Audit Summary

| Check | Result | Action Taken |
| :--- | :--- | :--- |
| Duplicate Transactions in Sales | 15 duplicate rows found | Deduplicated dataset, keeping first instance |
| Missing Store IDs in Sales | 12 null store_id values found | Dropped unassigned store transactions to preserve store integrity |
| Date String Formatting | Inconsistent date separators ('/' vs '-') detected | Standardized all date strings to ISO YYYY-MM-DD and integer date_id |
| Invalid Quantities / Prices | 2 records with negative/zero quantity or price | Filtered out invalid transaction records |
| Missing Product Category Names | 3 null category values found | Imputed missing categories using subcategory and product name rules |
| Inventory Snapshot Referential Integrity | All product_id and store_id foreign keys valid | Validated 100% referential match with dim_product and dim_store |
| Purchase Order Fill Rates & Delivery Lead Times | No negative lead times or excess fulfillment detected | Validated lead_time_days >= 0 and quantity_received >= 0 |

## Detailed Cleaning Transformations

1. **Fact Sales (`fact_sales`)**:
   - Initial Raw Records: `34565`
   - Records after Deduplication & Null Removal: `34536`
   - Date strings standardized from mixed slash formats to ISO `YYYY-MM-DD`.
   - Financial fields (`sales_amount`, `cost_amount`, `gross_profit`) mathematically reconciled against quantity and discounted price.

2. **Dimension Product (`dim_product`)**:
   - Imputed null category records to prevent missing dimension hierarchies in OLAP & Power BI models.
   - Standardized unit costs and selling prices across all SKUs.

3. **Fact Inventory (`fact_inventory`)**:
   - Validated 48,800 inventory snapshot records across 50 products and 8 stores.
   - Confirmed non-negative opening stock, received quantities, and closing balances.

4. **Fact Purchase Orders (`fact_purchase`)**:
   - Validated 2,200 purchase orders against supplier lead times and order quantities.

---
*Report generated automatically by `src/data_cleaning.py`*
