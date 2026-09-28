import os
import pandas as pd
import numpy as np

def run_feature_engineering(base_dir):
    proc_dir = os.path.join(base_dir, 'data', 'processed')
    
    df_sales = pd.read_csv(os.path.join(proc_dir, 'fact_sales.csv'))
    df_inventory = pd.read_csv(os.path.join(proc_dir, 'fact_inventory.csv'))
    df_purchase = pd.read_csv(os.path.join(proc_dir, 'fact_purchase.csv'))
    df_products = pd.read_csv(os.path.join(proc_dir, 'dim_product.csv'))
    df_stores = pd.read_csv(os.path.join(proc_dir, 'dim_store.csv'))
    df_suppliers = pd.read_csv(os.path.join(proc_dir, 'dim_supplier.csv'))
    
    print("Computing Operational Inventory & Supply Chain Features...", flush=True)
    
    # ---------------------------------------------------------
    # 1. PRODUCT LEVEL INVENTORY & SALES METRICS
    # ---------------------------------------------------------
    # Merge unit cost
    df_inv_prod = df_inventory.merge(df_products[["product_id", "product_name", "category", "subcategory", "unit_cost", "selling_price"]], on="product_id", how="left")
    df_inv_prod["inventory_value"] = (df_inv_prod["closing_stock"] * df_inv_prod["unit_cost"]).round(2)
    
    # Aggregate sales by product
    prod_sales = df_sales.groupby("product_id").agg(
        total_units_sold=("quantity_sold", "sum"),
        total_sales_amount=("sales_amount", "sum"),
        total_cogs=("cost_amount", "sum"),
        total_gross_profit=("gross_profit", "sum"),
        active_sales_days=("date_id", "nunique")
    ).reset_index()
    
    # Aggregate inventory by product
    prod_inv = df_inv_prod.groupby("product_id").agg(
        avg_closing_stock=("closing_stock", "mean"),
        avg_inventory_value=("inventory_value", "mean"),
        total_stockout_events=("stockout_flag", "sum"),
        total_obs_days=("inventory_date", "nunique"),
        total_received_units=("received_quantity", "sum"),
        total_opening_units=("opening_stock", "mean")
    ).reset_index()
    
    # Merge Product Metrics
    prod_metrics = df_products.merge(prod_sales, on="product_id", how="left").merge(prod_inv, on="product_id", how="left")
    prod_metrics.fillna({
        "total_units_sold": 0, "total_sales_amount": 0.0, "total_cogs": 0.0, "total_gross_profit": 0.0,
        "avg_closing_stock": 0.0, "avg_inventory_value": 0.0, "total_stockout_events": 0
    }, inplace=True)
    
    # Feature Calculations
    prod_metrics["gross_margin_pct"] = np.where(prod_metrics["total_sales_amount"] > 0, (prod_metrics["total_gross_profit"] / prod_metrics["total_sales_amount"]) * 100.0, 0.0).round(2)
    prod_metrics["avg_daily_demand"] = (prod_metrics["total_units_sold"] / 365.0).round(2)
    prod_metrics["inventory_turnover"] = np.where(prod_metrics["avg_inventory_value"] > 0, prod_metrics["total_cogs"] / prod_metrics["avg_inventory_value"], 0.0).round(2)
    prod_metrics["days_of_inventory"] = np.where(prod_metrics["total_cogs"] > 0, (prod_metrics["avg_inventory_value"] / prod_metrics["total_cogs"]) * 365.0, 999.0).round(1)
    prod_metrics["stockout_rate_pct"] = ((prod_metrics["total_stockout_events"] / (prod_metrics["total_obs_days"] * 8.0)) * 100.0).round(2) # 8 stores
    prod_metrics["sell_through_rate_pct"] = np.where((prod_metrics["total_opening_units"] + prod_metrics["total_received_units"]) > 0, (prod_metrics["total_units_sold"] / (prod_metrics["total_opening_units"] + prod_metrics["total_received_units"])) * 100.0, 0.0).round(2)
    
    # ---------------------------------------------------------
    # 2. ABC INVENTORY ANALYSIS (PARETO)
    # ---------------------------------------------------------
    prod_metrics.sort_values(by="total_cogs", ascending=False, inplace=True)
    prod_metrics["cum_cogs"] = prod_metrics["total_cogs"].cumsum()
    total_cogs_sum = prod_metrics["total_cogs"].sum()
    prod_metrics["cum_cogs_pct"] = (prod_metrics["cum_cogs"] / total_cogs_sum) * 100.0
    
    def assign_abc(pct):
        if pct <= 70.0:
            return 'A'
        elif pct <= 90.0:
            return 'B'
        else:
            return 'C'
            
    prod_metrics["abc_class"] = prod_metrics["cum_cogs_pct"].apply(assign_abc)
    
    # ---------------------------------------------------------
    # 3. SEGMENTATION & RISK FLAGS
    # ---------------------------------------------------------
    # Fast Mover vs Slow Mover based on Sales Velocity 75th/25th percentiles
    p75_sales = prod_metrics["total_units_sold"].quantile(0.75)
    p25_sales = prod_metrics["total_units_sold"].quantile(0.25)
    
    prod_metrics["fast_moving_flag"] = np.where(prod_metrics["total_units_sold"] >= p75_sales, 1, 0)
    prod_metrics["slow_moving_flag"] = np.where(prod_metrics["total_units_sold"] <= p25_sales, 1, 0)
    prod_metrics["excess_inventory_flag"] = np.where((prod_metrics["days_of_inventory"] > 120) & (prod_metrics["slow_moving_flag"] == 1), 1, 0)
    prod_metrics["stockout_prone_flag"] = np.where(prod_metrics["stockout_rate_pct"] > 5.0, 1, 0)
    
    # ---------------------------------------------------------
    # 4. SUPPLIER PERFORMANCE METRICS
    # ---------------------------------------------------------
    sup_metrics = df_purchase.groupby("supplier_id").agg(
        total_po_count=("purchase_id", "nunique"),
        total_ordered_units=("quantity_ordered", "sum"),
        total_received_units=("quantity_received", "sum"),
        avg_actual_lead_time=("lead_time_days", "mean")
    ).reset_index()
    
    # On-time delivery check
    df_purchase["is_on_time"] = np.where(df_purchase["actual_delivery_date"] <= df_purchase["expected_delivery_date"], 1, 0)
    sup_on_time = df_purchase.groupby("supplier_id")["is_on_time"].mean().reset_index()
    sup_on_time["on_time_delivery_rate_pct"] = (sup_on_time["is_on_time"] * 100.0).round(2)
    
    sup_metrics = sup_metrics.merge(sup_on_time[["supplier_id", "on_time_delivery_rate_pct"]], on="supplier_id", how="left")
    sup_metrics["fill_rate_pct"] = ((sup_metrics["total_received_units"] / sup_metrics["total_ordered_units"]) * 100.0).round(2)
    sup_metrics["avg_actual_lead_time"] = sup_metrics["avg_actual_lead_time"].round(1)
    
    # Merge with dim_supplier
    df_suppliers_summary = df_suppliers.merge(sup_metrics, on="supplier_id", how="left")
    
    # ---------------------------------------------------------
    # SAVE DERIVED METRICS
    # ---------------------------------------------------------
    prod_metrics.to_csv(os.path.join(proc_dir, 'product_operational_metrics.csv'), index=False)
    df_suppliers_summary.to_csv(os.path.join(proc_dir, 'supplier_operational_metrics.csv'), index=False)
    
    print("Derived Operational Metrics successfully generated!", flush=True)

if __name__ == "__main__":
    project_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    run_feature_engineering(project_base)
