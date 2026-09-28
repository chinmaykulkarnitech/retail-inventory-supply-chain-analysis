# Executive Business Insights Report

**Project**: Retail Inventory & Supply Chain Performance Analysis  
**Target Audience**: Chief Operations Officer (COO), VP of Supply Chain, Category Managers  

---

## Executive Summary

An end-to-end operational analysis of **34,565 transaction records**, **48,800 inventory snapshots**, and **2,200 purchase orders** across 8 stores and 50 product SKUs revealed critical operational bottlenecks. Revenue for the 12-month period totaled **$5,271,228** with a strong gross profit margin of **59.8%**. However, sub-optimal inventory management is tying up capital in slow-moving SKUs while high-demand items suffer from stockout-induced lost sales opportunities.

---

## 1. High Stockout Frequency in Fast-Moving Consumer Electronics & Apparel

### Finding
Popular fast-moving SKUs in **Consumer Electronics** and **Apparel** frequently experience stockouts, resulting in unfulfilled customer demand and lost revenue.

### Evidence
- **Pro Wireless Noise-Canceling Earbuds (PRD-001)** experienced a **8.2% stockout rate** (30 stockout days across store locations).
- **Classic Slim Fit Denim Jeans (PRD-011)** recorded a **6.5% stockout rate**.
- Cross-analyzing daily demand against inventory snapshots indicates an estimated **$42,850 in lost revenue opportunities** directly linked to out-of-stock events for top-performing items.

### Business Impact
Unfulfilled demand directly impairs top-line growth, degrades customer retention, and forces consumers to purchase from competitors.

### Recommended Action
1. **Recalibrate Reorder Points**: Increase safety stock levels for Class A fast-movers by **25%** to absorb demand spikes.
2. **Implement Automated PO Triggers**: Configure automated purchase order generation whenever inventory dips below the updated Reorder Point ($ROP$).

---

## 2. Capital Tied Up in Slow-Moving Home & Kitchen Inventory

### Finding
Excess inventory is heavily concentrated in the **Home & Kitchen** category, where sales velocity is low relative to closing stock balances.

### Evidence
- **Adjustable Dual-Motor Standing Desk (PRD-028)** carries a Days of Inventory Outstanding (**DIO**) of **145.2 days** (target DIO is 45–60 days).
- **10-Piece Non-Stick Cookware Set (PRD-023)** carries **112.0 days** of inventory.
- Over **$310,000 in working capital** is currently locked in SKUs with DIO exceeding 90 days.

### Business Impact
Carrying excess inventory inflates warehouse storage costs, increases capital holding expense, and heightens the risk of inventory obsolescence or damage.

### Recommended Action
1. **Targeted Promotional Markdowns**: Execute a **15% to 20% promotional discount** on SKUs with DIO > 120 days to accelerate sell-through.
2. **Freeze Replenishment Orders**: Temporarily pause purchase orders for Class C slow-movers until closing stock drops below 1.5x Reorder Point.

---

## 3. Supplier Lead Time Variances & Fulfillment Shortages

### Finding
Supplier delivery delays and partial order fulfillment directly trigger retail store stockouts.

### Evidence
- **Urban Style Apparel Inc (SUP-103)** achieved an On-Time Delivery Rate of only **88.5%** with an average lead time of **16.2 days** (against a contractual SLA of 14 days).
- **Organic Harvest Traders (SUP-109)** recorded a Supplier Fill Rate of **89.2%**, shorting ordered units by over **10%** across multiple purchase orders.

### Business Impact
Unpredictable supplier delivery times undermine store replenishment schedules, forcing stores into stockout situations even when purchase orders were issued on time.

### Recommended Action
1. **Vendor SLA Review**: Institute formal quarterly supplier scorecards with financial penalties for late deliveries exceeding 3 business days.
2. **Lead Time Buffer Adjustment**: Dynamically adjust lead-time parameters in safety stock calculations for SUP-103 and SUP-109 to account for actual 16-day delivery realities.

---

## 4. Store-Level Inventory Allocation Imbalance

### Finding
Significant variance exists in inventory turnover efficiency across retail store locations.

### Evidence
- **Pacific Center Flagship (STR-107)** achieves an inventory turnover of **8.5x**, operating lean and efficiently.
- **Peachtree Mall Store (STR-104)** achieves an inventory turnover of only **5.2x**, holding 38% more inventory relative to its sales revenue contribution than STR-107.

### Business Impact
Regional over-stocking at underperforming stores restricts inventory availability at high-velocity urban stores.

### Recommended Action
1. **Inter-Store Inventory Transfers**: Re-balance stock by transferring excess inventory from STR-104 (Atlanta) to high-velocity store STR-103 (Miami) before issuing new vendor purchase orders.
