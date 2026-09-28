# Analytical Methodology & Mathematical Framework

**Project**: Retail Inventory & Supply Chain Performance Analysis  
**Author**: Data Analytics & Supply Chain Engineering Team  

---

## 1. Mathematical Formulas & Metric Definitions

### 1.1 Financial & Margin Metrics

$$\text{Gross Margin \%} = \left( \frac{\text{Total Sales Amount} - \text{Total Cost Amount}}{\text{Total Sales Amount}} \right) \times 100$$

$$\text{Average Order Value (AOV)} = \frac{\text{Total Net Sales Revenue}}{\text{Total Distinct Transactions}}$$

### 1.2 Inventory Efficiency Metrics

$$\text{Inventory Turnover Ratio} = \frac{\text{Annualized Cost of Goods Sold (COGS)}}{\text{Average Daily Inventory Valuation}}$$

$$\text{Days of Inventory Outstanding (DIO)} = \left( \frac{\text{Average Daily Inventory Valuation}}{\text{Annualized COGS}} \right) \times 365$$

$$\text{Sell-Through Rate \%} = \left( \frac{\text{Units Sold}}{\text{Opening Stock} + \text{Received Quantity}} \right) \times 100$$

### 1.3 Safety Stock & Reorder Point Formulas

We calculate **Safety Stock ($SS$)** using a 95% service level ($Z = 1.65$) accounting for daily demand variance ($\sigma_D$) and lead time variance ($\sigma_{LT}$):

$$SS = Z \times \sqrt{ (\overline{LT} \times \sigma_D^2) + (\overline{D}^2 \times \sigma_{LT}^2) }$$

Where:
- $\overline{LT}$ = Average supplier lead time in days
- $\overline{D}$ = Average daily unit demand
- $\sigma_D$ = Standard deviation of daily demand
- $\sigma_{LT}$ = Standard deviation of lead time days

**Reorder Point (ROP)** is calculated as:

$$\text{ROP} = (\overline{D} \times \overline{LT}) + SS$$

### 1.4 Stockout & Lost Opportunity Estimation

$$\text{Stockout Rate \%} = \left( \frac{\text{Total Days with Stockout Flag = 1}}{\text{Total Observation Snapshots}} \right) \times 100$$

$$\text{Estimated Lost Revenue Opportunity} = \sum (\text{Stockout Days} \times \text{Average Daily Sales Revenue})$$

### 1.5 Supply Chain SLA Metrics

$$\text{Supplier Fill Rate \%} = \left( \frac{\text{Total Units Received}}{\text{Total Units Ordered}} \right) \times 100$$

$$\text{On-Time Delivery Rate \%} = \left( \frac{\text{Purchase Orders Delivered on or before Expected Date}}{\text{Total Purchase Orders}} \right) \times 100$$

---

## 2. ABC Inventory Pareto Classification Rules

Products are segmented based on their cumulative percentage contribution to total annual COGS:
- **Class A (High Value)**: Products contributing to the top **70.0%** of total COGS.
- **Class B (Medium Value)**: Products contributing to the next **20.0%** (70.1% to 90.0%) of COGS.
- **Class C (Low Value)**: Products contributing to the final **10.0%** (90.1% to 100.0%) of COGS.

---

## 3. Risk Classification Rules for Action Center

1. **Replenishment Risk**:
   - `CRITICAL`: Stockout Rate $\ge 5.0\%$ OR Closing Stock $<$ Safety Stock.
   - `HIGH`: Closing Stock $<$ Reorder Point.
   - `NORMAL`: Closing Stock $\ge$ Reorder Point.

2. **Excess Inventory Risk**:
   - `CRITICAL EXCESS`: DIO $\ge 120$ Days AND Slow-Moving Flag = 1.
   - `HIGH EXCESS`: DIO $\ge 90$ Days.
   - `BALANCED`: DIO $< 90$ Days.
