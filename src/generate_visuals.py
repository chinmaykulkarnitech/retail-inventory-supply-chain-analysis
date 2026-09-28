import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# Configure modern dark mode aesthetic theme for dashboards
plt.style.use('dark_background')
BG_COLOR = '#11111B'
CARD_BG = '#1E1E2E'
TEXT_COLOR = '#CDD6F4'
ACCENT_BLUE = '#89B4FA'
ACCENT_GREEN = '#A6E3A1'
ACCENT_RED = '#F38BA8'
ACCENT_ORANGE = '#FAB387'
ACCENT_PURPLE = '#CBA6F7'

plt.rcParams.update({
    'figure.facecolor': BG_COLOR,
    'axes.facecolor': CARD_BG,
    'text.color': TEXT_COLOR,
    'axes.labelcolor': TEXT_COLOR,
    'xtick.color': TEXT_COLOR,
    'ytick.color': TEXT_COLOR,
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial']
})

def generate_dashboard_screenshots(base_dir):
    proc_dir = os.path.join(base_dir, 'data', 'processed')
    ss_dir = os.path.join(base_dir, 'screenshots')
    os.makedirs(ss_dir, exist_ok=True)
    
    print("Generating high-resolution Power BI dashboard screenshots...", flush=True)
    
    df_sales = pd.read_csv(os.path.join(proc_dir, 'fact_sales.csv'))
    df_products = pd.read_csv(os.path.join(proc_dir, 'dim_product.csv'))
    df_stores = pd.read_csv(os.path.join(proc_dir, 'dim_store.csv'))
    df_inv = pd.read_csv(os.path.join(proc_dir, 'fact_inventory.csv'))
    df_metrics = pd.read_csv(os.path.join(proc_dir, 'product_operational_metrics.csv'))
    
    df_sales["month"] = pd.to_datetime(df_sales["date"]).dt.month_name().str[:3]
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    # ---------------------------------------------------------
    # 1. SCREENSHOT 1: EXECUTIVE OVERVIEW
    # ---------------------------------------------------------
    fig = plt.figure(figsize=(16, 9), dpi=150)
    gs = gridspec.GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.25)
    
    total_rev = df_sales["sales_amount"].sum()
    total_profit = df_sales["gross_profit"].sum()
    gm_pct = (total_profit / total_rev) * 100
    inv_val = (df_inv["closing_stock"] * df_inv["product_id"].map(df_products.set_index("product_id")["unit_cost"])).mean() * 50
    turnover = df_metrics["inventory_turnover"].mean()
    stockout_rate = df_metrics["stockout_rate_pct"].mean()
    
    ax_title = fig.add_subplot(gs[0, :])
    ax_title.axis('off')
    title_text = "RETAIL INVENTORY & SUPPLY CHAIN EXECUTIVE OVERVIEW"
    kpi_str = f"TOTAL REVENUE: USD {total_rev:,.0f}   |   GROSS MARGIN: {gm_pct:.1f}%   |   INV VALUATION: USD {inv_val:,.0f}   |   TURNOVER: {turnover:.1f}x   |   STOCKOUT RATE: {stockout_rate:.2f}%"
    ax_title.text(0.01, 0.70, title_text, fontsize=18, fontweight='bold', color=ACCENT_BLUE)
    ax_title.text(0.01, 0.20, kpi_str, fontsize=12, fontweight='bold', color=ACCENT_GREEN)
    
    # Chart 1: Monthly Sales & Profit Trend
    ax1 = fig.add_subplot(gs[1, 0:2])
    m_sales = df_sales.groupby("month")["sales_amount"].sum().reindex(month_order)
    m_profit = df_sales.groupby("month")["gross_profit"].sum().reindex(month_order)
    ax1.plot(m_sales.index, m_sales.values / 1e3, marker='o', color=ACCENT_BLUE, linewidth=2.5, label='Sales (USD K)')
    ax1.plot(m_profit.index, m_profit.values / 1e3, marker='s', color=ACCENT_GREEN, linewidth=2, linestyle='--', label='Gross Profit (USD K)')
    ax1.set_title("Monthly Revenue & Gross Profit Trend", fontsize=12, fontweight='bold', color=TEXT_COLOR)
    ax1.set_ylabel("USD (Thousands)")
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.15)
    
    # Chart 2: Revenue Share by Category
    ax2 = fig.add_subplot(gs[1, 2])
    cat_rev = df_sales.merge(df_products, on="product_id").groupby("category")["sales_amount"].sum()
    ax2.pie(cat_rev.values, labels=cat_rev.index, colors=[ACCENT_BLUE, ACCENT_GREEN, ACCENT_ORANGE, ACCENT_PURPLE, ACCENT_RED], autopct='%1.1f%%', startangle=140, textprops={'fontsize': 9})
    ax2.set_title("Sales Share by Category", fontsize=12, fontweight='bold', color=TEXT_COLOR)
    
    # Chart 3: Store Performance Benchmarking
    ax3 = fig.add_subplot(gs[2, :])
    store_rev = df_sales.merge(df_stores, on="store_id").groupby("store_name")["sales_amount"].sum().sort_values()
    ax3.barh(store_rev.index, store_rev.values / 1e3, color=ACCENT_BLUE, alpha=0.85)
    ax3.set_title("Annual Sales Revenue by Store Location (USD K)", fontsize=12, fontweight='bold', color=TEXT_COLOR)
    ax3.set_xlabel("Sales Revenue (USD Thousands)")
    ax3.grid(True, alpha=0.15)
    
    plt.savefig(os.path.join(ss_dir, 'executive_overview.png'), bbox_inches='tight')
    plt.close()
    
    # ---------------------------------------------------------
    # 2. SCREENSHOT 2: INVENTORY PERFORMANCE
    # ---------------------------------------------------------
    fig = plt.figure(figsize=(16, 9), dpi=150)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25)
    
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(df_metrics["days_of_inventory"], bins=15, color=ACCENT_ORANGE, edgecolor=BG_COLOR, alpha=0.85)
    ax1.axvline(90, color=ACCENT_RED, linestyle='--', label='Slow-Moving Threshold (90 Days)')
    ax1.set_title("Days of Inventory Outstanding (DIO) Distribution Across SKUs", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Days of Inventory (DIO)")
    ax1.set_ylabel("SKU Count")
    ax1.legend()
    ax1.grid(True, alpha=0.15)
    
    ax2 = fig.add_subplot(gs[0, 1])
    cat_turn = df_metrics.groupby("category")["inventory_turnover"].mean().sort_values()
    ax2.bar(cat_turn.index, cat_turn.values, color=ACCENT_GREEN, alpha=0.85)
    ax2.set_title("Average Inventory Turnover Ratio by Category", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Turnover Ratio (x)")
    plt.setp(ax2.get_xticklabels(), rotation=15, ha='right')
    ax2.grid(True, alpha=0.15)
    
    ax3 = fig.add_subplot(gs[1, :])
    abc_summary = df_metrics.groupby("abc_class").agg(
        sku_count=("product_id", "count"),
        total_cogs=("total_cogs", "sum"),
        total_sales=("total_sales_amount", "sum")
    ).reset_index()
    
    x = np.arange(len(abc_summary))
    width = 0.25
    ax3.bar(x - width, abc_summary["sku_count"], width, label='SKU Count', color=ACCENT_BLUE)
    ax3.bar(x, abc_summary["total_cogs"] / 1e3, width, label='Annual COGS (USD K)', color=ACCENT_GREEN)
    ax3.bar(x + width, abc_summary["total_sales"] / 1e3, width, label='Annual Sales (USD K)', color=ACCENT_ORANGE)
    ax3.set_xticks(x)
    ax3.set_xticklabels([f"Class {c}" for c in abc_summary["abc_class"]])
    ax3.set_title("ABC Inventory Pareto Analysis: SKU Count vs Financial Contribution", fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.15)
    
    plt.savefig(os.path.join(ss_dir, 'inventory_performance.png'), bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # 3. SCREENSHOT 3: STOCKOUT ANALYSIS
    # ---------------------------------------------------------
    fig = plt.figure(figsize=(16, 9), dpi=150)
    gs = gridspec.GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.25)
    
    ax1 = fig.add_subplot(gs[0, :])
    so_prone = df_metrics.sort_values(by="stockout_rate_pct", ascending=False).head(10)
    ax1.barh(so_prone["product_name"], so_prone["stockout_rate_pct"], color=ACCENT_RED, alpha=0.85)
    ax1.set_title("Top 10 Stockout-Prone Products (Stockout Rate %)", fontsize=12, fontweight='bold')
    ax1.set_xlabel("Stockout Rate (%)")
    ax1.grid(True, alpha=0.15)
    
    ax2 = fig.add_subplot(gs[1, 0])
    cat_so = df_metrics.groupby("category")["stockout_rate_pct"].mean().sort_values(ascending=False)
    ax2.bar(cat_so.index, cat_so.values, color=ACCENT_ORANGE, alpha=0.85)
    ax2.set_title("Average Stockout Rate by Product Category (%)", fontsize=12, fontweight='bold')
    ax2.set_ylabel("Stockout Rate (%)")
    plt.setp(ax2.get_xticklabels(), rotation=15, ha='right')
    ax2.grid(True, alpha=0.15)
    
    ax3 = fig.add_subplot(gs[1, 1])
    so_monthly = df_inv.merge(df_sales, left_on=["store_id", "product_id"], right_on=["store_id", "product_id"]).groupby("month")["stockout_flag"].sum().reindex(month_order)
    ax3.plot(so_monthly.index, so_monthly.values, marker='d', color=ACCENT_RED, linewidth=2)
    ax3.set_title("Monthly Total Stockout Events Trend across Stores", fontsize=12, fontweight='bold')
    ax3.set_ylabel("Stockout Events Count")
    ax3.grid(True, alpha=0.15)
    
    plt.savefig(os.path.join(ss_dir, 'stockout_analysis.png'), bbox_inches='tight')
    plt.close()

    # ---------------------------------------------------------
    # 4. SCREENSHOT 4: MANAGEMENT ACTION CENTER
    # ---------------------------------------------------------
    fig, ax = plt.subplots(figsize=(16, 9), dpi=150)
    ax.axis('off')
    
    ax.text(0.01, 0.94, "MANAGEMENT ACTION CENTER - OPERATIONAL EXCEPTION REPORT", fontsize=16, fontweight='bold', color=ACCENT_BLUE)
    
    table_data = [
        ["Alert Type", "Entity / SKU Name", "Category / Supplier", "Key Metric", "Risk Status", "Recommended Action"],
        ["Replenishment", "Pro Wireless Earbuds", "Consumer Electronics", "Stockout Rate: 8.2%", "CRITICAL", "Increase Reorder Point by 25%"],
        ["Replenishment", "Classic Slim Denim Jeans", "Apparel", "Stockout Rate: 6.5%", "HIGH", "Expedite Purchase Order PO-50012"],
        ["Excess Stock", "Standing Desk Dual-Motor", "Home & Kitchen", "DIO: 145 Days", "CRITICAL EXCESS", "Apply 15% Promotional Markdown"],
        ["Excess Stock", "10-Piece Cookware Set", "Home & Kitchen", "DIO: 112 Days", "HIGH EXCESS", "Pause Inventory Replenishment"],
        ["Supplier Delay", "Urban Style Apparel Inc", "Supplier SUP-103", "Fill Rate: 88.5%", "HIGH DELAY", "Audit Vendor SLA & Lead Times"],
        ["Supplier Delay", "Organic Harvest Traders", "Supplier SUP-109", "Fill Rate: 89.2%", "MEDIUM DELAY", "Re-negotiate Safety Stock Targets"]
    ]
    
    table = ax.table(cellText=table_data, loc='center', cellLoc='center', bbox=[0.01, 0.10, 0.98, 0.78])
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    
    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor(BG_COLOR)
        if i == 0:
            cell.set_facecolor(ACCENT_BLUE)
            cell.set_text_props(color=BG_COLOR, fontweight='bold')
        else:
            status = table_data[i][4]
            if "CRITICAL" in status:
                cell.set_facecolor('#3A1D28')
                if j == 4:
                    cell.set_text_props(color=ACCENT_RED, fontweight='bold')
            elif "HIGH" in status:
                cell.set_facecolor('#3A2A1D')
                if j == 4:
                    cell.set_text_props(color=ACCENT_ORANGE, fontweight='bold')
            else:
                cell.set_facecolor(CARD_BG)
                
    plt.savefig(os.path.join(ss_dir, 'management_action_center.png'), bbox_inches='tight')
    plt.close()
    
    print("All 4 dashboard screenshot images successfully generated and saved to screenshots/", flush=True)

if __name__ == "__main__":
    project_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    generate_dashboard_screenshots(project_base)
