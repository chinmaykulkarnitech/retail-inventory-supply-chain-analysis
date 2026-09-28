import os
import random
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# Set random seeds for reproducibility
np.random.seed(42)
random.seed(42)

def generate_retail_dataset(base_dir):
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    
    print("Generating synthetic retail inventory & supply chain dataset...", flush=True)
    
    # ---------------------------------------------------------
    # 1. DIM SUPPLIER (10 Suppliers)
    # ---------------------------------------------------------
    suppliers_data = [
        {"supplier_id": "SUP-101", "supplier_name": "Apex Electronics Corp", "supplier_region": "East Asia", "supplier_type": "Manufacturer", "base_lead_time": 10, "base_fill_rate": 0.95},
        {"supplier_id": "SUP-102", "supplier_name": "Global Tech Logistics", "supplier_region": "North America", "supplier_type": "Distributor", "base_lead_time": 5, "base_fill_rate": 0.98},
        {"supplier_id": "SUP-103", "supplier_name": "Urban Style Apparel Inc", "supplier_region": "Southeast Asia", "supplier_type": "Manufacturer", "base_lead_time": 14, "base_fill_rate": 0.90},
        {"supplier_id": "SUP-104", "supplier_name": "Premier Garments Ltd", "supplier_region": "North America", "supplier_type": "Wholesaler", "base_lead_time": 4, "base_fill_rate": 0.96},
        {"supplier_id": "SUP-105", "supplier_name": "Culinary Home Goods", "supplier_region": "Europe", "supplier_type": "Manufacturer", "base_lead_time": 12, "base_fill_rate": 0.92},
        {"supplier_id": "SUP-106", "supplier_name": "Comfort Living Co", "supplier_region": "North America", "supplier_type": "Distributor", "base_lead_time": 6, "base_fill_rate": 0.97},
        {"supplier_id": "SUP-107", "supplier_name": "Vitality Wellness Labs", "supplier_region": "North America", "supplier_type": "Manufacturer", "base_lead_time": 5, "base_fill_rate": 0.94},
        {"supplier_id": "SUP-108", "supplier_name": "Pure Glow Cosmetics", "supplier_region": "Europe", "supplier_type": "Manufacturer", "base_lead_time": 8, "base_fill_rate": 0.93},
        {"supplier_id": "SUP-109", "supplier_name": "Organic Harvest Traders", "supplier_region": "South America", "supplier_type": "Importer", "base_lead_time": 11, "base_fill_rate": 0.91},
        {"supplier_id": "SUP-110", "supplier_name": "Pantry Direct Distribution", "supplier_region": "North America", "supplier_type": "Distributor", "base_lead_time": 3, "base_fill_rate": 0.99},
    ]
    df_suppliers = pd.DataFrame(suppliers_data)
    
    # ---------------------------------------------------------
    # 2. DIM STORE (8 Stores)
    # ---------------------------------------------------------
    stores_data = [
        {"store_id": "STR-101", "store_name": "Metro Center Store", "city": "New York", "state": "NY", "region": "Northeast", "store_type": "Flagship", "target_inventory_turnover": 8.0},
        {"store_id": "STR-102", "store_name": "Harbor Place Store", "city": "Boston", "state": "MA", "region": "Northeast", "store_type": "Supercenter", "target_inventory_turnover": 6.5},
        {"store_id": "STR-103", "store_name": "Sun Valley Plaza", "city": "Miami", "state": "FL", "region": "South", "store_type": "Express", "target_inventory_turnover": 7.0},
        {"store_id": "STR-104", "store_name": "Peachtree Mall Store", "city": "Atlanta", "state": "GA", "region": "South", "store_type": "Mall Store", "target_inventory_turnover": 5.5},
        {"store_id": "STR-105", "store_name": "Windy City Supercenter", "city": "Chicago", "state": "IL", "region": "Midwest", "store_type": "Supercenter", "target_inventory_turnover": 6.0},
        {"store_id": "STR-106", "store_name": "Lakeshore Express", "city": "Minneapolis", "state": "MN", "region": "Midwest", "store_type": "Express", "target_inventory_turnover": 7.5},
        {"store_id": "STR-107", "store_name": "Pacific Center Store", "city": "Los Angeles", "state": "CA", "region": "West", "store_type": "Flagship", "target_inventory_turnover": 8.5},
        {"store_id": "STR-108", "store_name": "Emerald City Supercenter", "city": "Seattle", "state": "WA", "region": "West", "store_type": "Supercenter", "target_inventory_turnover": 6.2},
    ]
    df_stores = pd.DataFrame(stores_data)
    
    # ---------------------------------------------------------
    # 3. DIM PRODUCT (50 SKUs)
    # ---------------------------------------------------------
    categories = {
        "Consumer Electronics": {
            "suppliers": ["SUP-101", "SUP-102"],
            "subcategories": ["Audio", "Mobile", "Computers", "Accessories"],
            "items": [
                ("Pro Wireless Noise-Canceling Earbuds", "Audio", "AudioTech", 45.0, 129.99),
                ("UltraSlim 15-inch Laptop", "Computers", "TechPro", 450.0, 899.99),
                ("4K UHD 27-inch Ergonomic Monitor", "Computers", "VisionMax", 160.0, 349.99),
                ("Smart Fitness Watch Series 5", "Mobile", "PulseGear", 65.0, 179.99),
                ("Portable Bluetooth Speaker 20W", "Audio", "AudioTech", 22.0, 59.99),
                ("Ergonomic Wireless Mouse", "Accessories", "TechPro", 12.0, 34.99),
                ("Mechanical RGB Gaming Keyboard", "Accessories", "TechPro", 35.0, 89.99),
                ("7-in-1 USB-C Multiport Hub", "Accessories", "TechPro", 18.0, 49.99),
                ("1TB Portable External SSD", "Computers", "VisionMax", 55.0, 119.99),
                ("HD Webcam 1080p with Mic", "Accessories", "VisionMax", 20.0, 49.99),
            ]
        },
        "Apparel": {
            "suppliers": ["SUP-103", "SUP-104"],
            "subcategories": ["Menswear", "Womenswear", "Footwear", "Accessories"],
            "items": [
                ("Classic Slim Fit Denim Jeans", "Menswear", "DenimCo", 18.0, 59.99),
                ("Premium Organic Cotton T-Shirt", "Menswear", "BasicsPlus", 5.0, 24.99),
                ("Fleece Zip-Up Hoodie", "Menswear", "BasicsPlus", 16.0, 49.99),
                ("Lightweight Performance Running Shoes", "Footwear", "StrideRight", 32.0, 99.99),
                ("Athletic Moisture-Wicking Shorts", "Menswear", "StrideRight", 10.0, 29.99),
                ("All-Weather Waterproof Rain Jacket", "Womenswear", "OutdoorGear", 38.0, 119.99),
                ("Merino Wool Thermal Socks (3-Pack)", "Accessories", "BasicsPlus", 7.0, 22.99),
                ("Genuine Leather Dress Belt", "Accessories", "DenimCo", 12.0, 34.99),
                ("Wrinkle-Free Formal Oxford Shirt", "Menswear", "DenimCo", 20.0, 54.99),
                ("Insulated Winter Parka Coat", "Womenswear", "OutdoorGear", 75.0, 199.99),
            ]
        },
        "Home & Kitchen": {
            "suppliers": ["SUP-105", "SUP-106"],
            "subcategories": ["Small Appliances", "Cookware", "Home Organization", "Bedding"],
            "items": [
                ("Digital Touchscreen Air Fryer 5.8Qt", "Small Appliances", "KitchenChef", 42.0, 109.99),
                ("Compact Espresso & Cappuccino Maker", "Small Appliances", "KitchenChef", 70.0, 189.99),
                ("10-Piece Non-Stick Cookware Set", "Cookware", "KitchenChef", 65.0, 159.99),
                ("High-Speed Countertop Blender 1200W", "Small Appliances", "KitchenChef", 35.0, 89.99),
                ("Smart Robot Vacuum Cleaner", "Small Appliances", "CleanHome", 110.0, 269.99),
                ("Ergonomic Memory Foam Bed Pillow", "Bedding", "ComfortRest", 15.0, 44.99),
                ("Double-Wall Stainless Water Bottle 32oz", "Cookware", "ComfortRest", 8.0, 24.99),
                ("Adjustable Dual-Motor Standing Desk", "Home Organization", "CleanHome", 180.0, 399.99),
                ("Japanese Steel 8-inch Chef Knife", "Cookware", "KitchenChef", 25.0, 69.99),
                ("Dimmable LED Architect Desk Lamp", "Home Organization", "CleanHome", 14.0, 39.99),
            ]
        },
        "Health & Beauty": {
            "suppliers": ["SUP-107", "SUP-108"],
            "subcategories": ["Personal Care", "Skincare", "Supplements", "Wellness"],
            "items": [
                ("Sonic Electric Toothbrush with 4 Heads", "Personal Care", "PureOral", 22.0, 64.99),
                ("Gentle Hydrating Facial Cleanser 8oz", "Skincare", "GlowLab", 6.0, 18.99),
                ("Broad Spectrum Sunscreen SPF 50", "Skincare", "GlowLab", 7.0, 21.99),
                ("Vitamin C Brightening Facial Serum", "Skincare", "GlowLab", 12.0, 34.99),
                ("Ionic Ceramic Hair Dryer 1875W", "Personal Care", "GlowLab", 24.0, 59.99),
                ("Grass-Fed Whey Protein Powder 2lbs", "Supplements", "NutriCore", 18.0, 42.99),
                ("Ultrasonic Essential Oil Diffuser", "Wellness", "PureOral", 11.0, 29.99),
                ("Deep Moisture Body Cream 16oz", "Skincare", "GlowLab", 8.0, 22.99),
                ("Precision Waterproof Beard Trimmer", "Personal Care", "PureOral", 19.0, 49.99),
                ("Non-Slip Extra Thick Yoga Mat 6mm", "Wellness", "NutriCore", 10.0, 29.99),
            ]
        },
        "Grocery & Pantry": {
            "suppliers": ["SUP-109", "SUP-110"],
            "subcategories": ["Beverages", "Oils & Condiments", "Snacks", "Pantry Staples"],
            "items": [
                ("Organic Single-Origin Coffee Beans 1lb", "Beverages", "ArtisanRoast", 6.0, 16.99),
                ("Cold-Pressed Extra Virgin Olive Oil 1L", "Oils & Condiments", "TuscanGold", 7.5, 19.99),
                ("Organic Japanese Matcha Green Tea", "Beverages", "ArtisanRoast", 9.0, 24.99),
                ("Raw Roasted Almonds & Cashews 16oz", "Snacks", "NatureSnack", 5.0, 13.99),
                ("70% Dark Artisanal Chocolate Bar (5-Pack)", "Snacks", "NatureSnack", 6.0, 17.99),
                ("Pure Wildflower Raw Honey 24oz", "Pantry Staples", "TuscanGold", 5.5, 14.99),
                ("Plant-Based High Protein Bars (12-Pack)", "Snacks", "NatureSnack", 11.0, 27.99),
                ("Unsweetened Organic Almond Milk 64oz", "Beverages", "ArtisanRoast", 1.8, 4.49),
                ("Whole Grain Rolled Oats 32oz", "Pantry Staples", "NatureSnack", 2.2, 5.99),
                ("Artisanal Italian Pasta Variety Pack 4-Pack", "Pantry Staples", "TuscanGold", 4.0, 11.99),
            ]
        }
    }
    
    products_list = []
    prod_idx = 1
    for cat, cat_info in categories.items():
        for item in cat_info["items"]:
            name, subcat, brand, cost, price = item
            sup_id = random.choice(cat_info["suppliers"])
            prod_id = f"PRD-{prod_idx:03d}"
            products_list.append({
                "product_id": prod_id,
                "product_name": name,
                "category": cat,
                "subcategory": subcat,
                "brand": brand,
                "supplier_id": sup_id,
                "unit_cost": round(cost, 2),
                "selling_price": round(price, 2)
            })
            prod_idx += 1
            
    df_products = pd.DataFrame(products_list)
    
    # ---------------------------------------------------------
    # 4. DIM DATE (Full Year 2025: 365 Days)
    # ---------------------------------------------------------
    start_date = datetime(2025, 1, 1)
    date_list = []
    for i in range(365):
        curr = start_date + timedelta(days=i)
        date_id = int(curr.strftime("%Y%m%d"))
        date_list.append({
            "date_id": date_id,
            "date": curr.strftime("%Y-%m-%d"),
            "day": curr.day,
            "month": curr.month,
            "month_name": curr.strftime("%B"),
            "quarter": (curr.month - 1) // 3 + 1,
            "year": curr.year,
            "week": curr.isocalendar()[1],
            "weekday": curr.isoweekday(),
            "weekday_name": curr.strftime("%A"),
            "is_weekend": 1 if curr.isoweekday() in [6, 7] else 0
        })
    df_date = pd.DataFrame(date_list)
    
    # ---------------------------------------------------------
    # 5. FACT SALES (~30,000 Transactions)
    # ---------------------------------------------------------
    print("Generating sales transactions...", flush=True)
    sales_records = []
    sale_id_counter = 100001
    
    prod_ids = df_products["product_id"].tolist()
    prod_dict = df_products.set_index("product_id").to_dict("index")
    store_ids = df_stores["store_id"].tolist()
    
    prod_weights = {}
    for pid in prod_ids:
        val = int(pid.split('-')[1])
        if val in [1, 4, 11, 14, 21, 25, 31, 34, 41, 44]:
            prod_weights[pid] = 3.5
        elif val in [9, 10, 19, 20, 29, 30, 39, 40, 49, 50]:
            prod_weights[pid] = 0.3
        else:
            prod_weights[pid] = 1.0
            
    total_w = sum(prod_weights.values())
    norm_pweights = [prod_weights[p]/total_w for p in prod_ids]
    
    for day_idx in range(365):
        curr_date = start_date + timedelta(days=day_idx)
        date_id = int(curr_date.strftime("%Y%m%d"))
        date_str = curr_date.strftime("%Y-%m-%d")
        month = curr_date.month
        is_weekend = curr_date.isoweekday() in [6, 7]
        
        season_mult = 1.0
        if month in [11, 12]:
            season_mult = 1.55
        elif month in [6, 7]:
            season_mult = 1.2
        elif month in [1, 2]:
            season_mult = 0.8
            
        if is_weekend:
            season_mult *= 1.3
            
        daily_tx_count = int(np.random.normal(80 * season_mult, 10))
        daily_tx_count = max(40, daily_tx_count)
        
        chosen_products = np.random.choice(prod_ids, size=daily_tx_count, p=norm_pweights)
        chosen_stores = np.random.choice(store_ids, size=daily_tx_count)
        
        for p_id, s_id in zip(chosen_products, chosen_stores):
            p_info = prod_dict[p_id]
            unit_cost = p_info["unit_cost"]
            unit_price = p_info["selling_price"]
            
            qty = np.random.choice([1, 2, 3, 4, 5], p=[0.60, 0.25, 0.10, 0.03, 0.02])
            discount = np.random.choice([0.0, 0.05, 0.10, 0.15], p=[0.70, 0.15, 0.10, 0.05])
            
            eff_price = round(unit_price * (1.0 - discount), 2)
            sales_amt = round(qty * eff_price, 2)
            cost_amt = round(qty * unit_cost, 2)
            profit_amt = round(sales_amt - cost_amt, 2)
            
            sales_records.append({
                "sale_id": f"SAL-{sale_id_counter}",
                "date_id": date_id,
                "date": date_str,
                "product_id": p_id,
                "store_id": s_id,
                "customer_id": f"CUST-{random.randint(1000, 9999)}",
                "quantity_sold": qty,
                "unit_price": unit_price,
                "discount": discount,
                "sales_amount": sales_amt,
                "cost_amount": cost_amt,
                "gross_profit": profit_amt
            })
            sale_id_counter += 1
            
    df_sales = pd.DataFrame(sales_records)
    
    # Fast map of sales sum by (store_id, product_id, date)
    sales_grouped = df_sales.groupby(["store_id", "product_id", "date"])["quantity_sold"].sum().to_dict()
    avg_sales_dict = (df_sales.groupby(["store_id", "product_id"])["quantity_sold"].sum() / 365.0).to_dict()
    
    # ---------------------------------------------------------
    # 6. FACT INVENTORY (Daily Store-Product Snapshot Log)
    # ---------------------------------------------------------
    print("Generating daily inventory snapshots...", flush=True)
    inv_records = []
    
    # Sample snapshot dates (every 3 days = 122 snapshots per store-product pair = ~48,800 rows)
    snapshot_days = [start_date + timedelta(days=d) for d in range(0, 365, 3)]
    
    for s_id in store_ids:
        for p_id in prod_ids:
            p_info = prod_dict[p_id]
            avg_daily_dmd = avg_sales_dict.get((s_id, p_id), 0.5)
            
            sup_id = p_info["supplier_id"]
            sup_info = next(s for s in suppliers_data if s["supplier_id"] == sup_id)
            lead_time = sup_info["base_lead_time"]
            
            safety_stock = int(np.ceil(1.65 * np.sqrt(lead_time) * (avg_daily_dmd * 0.5)))
            safety_stock = max(5, safety_stock)
            reorder_point = int(np.ceil(avg_daily_dmd * lead_time + safety_stock))
            
            val = int(p_id.split('-')[1])
            is_stockout_prone = val in [1, 4, 11, 14, 21]
            is_excess_prone = val in [9, 10, 19, 20, 29, 30]
            
            current_stock = reorder_point * 2 if not is_excess_prone else reorder_point * 6
            
            for dt in snapshot_days:
                date_str = dt.strftime("%Y-%m-%d")
                date_id = int(dt.strftime("%Y%m%d"))
                
                opening_stock = current_stock
                qty_sold = sales_grouped.get((s_id, p_id, date_str), 0)
                if qty_sold == 0:
                    qty_sold = int(np.random.poisson(avg_daily_dmd * 3))
                
                received_qty = 0
                if opening_stock < reorder_point:
                    if is_stockout_prone and random.random() < 0.4:
                        received_qty = 0
                    else:
                        received_qty = int(reorder_point * 1.5)
                        
                available_stock = opening_stock + received_qty
                actual_sold = min(available_stock, qty_sold)
                closing_stock = available_stock - actual_sold
                
                stockout_flag = 1 if closing_stock == 0 and qty_sold > actual_sold else 0
                excess_flag = 1 if closing_stock > (reorder_point * 3.5) else 0
                
                inv_records.append({
                    "inventory_date": date_str,
                    "date_id": date_id,
                    "product_id": p_id,
                    "store_id": s_id,
                    "opening_stock": opening_stock,
                    "received_quantity": received_qty,
                    "quantity_sold": actual_sold,
                    "closing_stock": closing_stock,
                    "safety_stock": safety_stock,
                    "reorder_point": reorder_point,
                    "stockout_flag": stockout_flag,
                    "excess_inventory_flag": excess_flag
                })
                
                current_stock = closing_stock
                
    df_inventory = pd.DataFrame(inv_records)
    
    # ---------------------------------------------------------
    # 7. FACT PURCHASE / SUPPLY (~2,200 Purchase Orders)
    # ---------------------------------------------------------
    print("Generating purchase orders...", flush=True)
    po_records = []
    po_id_counter = 50001
    
    for i in range(2200):
        order_dt = start_date + timedelta(days=random.randint(0, 330))
        p_id = random.choice(prod_ids)
        s_id = random.choice(store_ids)
        p_info = prod_dict[p_id]
        sup_id = p_info["supplier_id"]
        sup_info = next(s for s in suppliers_data if s["supplier_id"] == sup_id)
        
        base_lt = sup_info["base_lead_time"]
        base_fr = sup_info["base_fill_rate"]
        
        actual_lt = max(1, int(np.random.normal(base_lt, 2)))
        if random.random() < 0.15:
            actual_lt += random.randint(3, 7)
            
        exp_delivery_dt = order_dt + timedelta(days=base_lt)
        act_delivery_dt = order_dt + timedelta(days=actual_lt)
        
        qty_ordered = random.randint(50, 500)
        if random.random() < (1.0 - base_fr):
            qty_received = int(qty_ordered * random.uniform(0.70, 0.95))
        else:
            qty_received = qty_ordered
            
        po_records.append({
            "purchase_id": f"PO-{po_id_counter}",
            "date_id": int(order_dt.strftime("%Y%m%d")),
            "product_id": p_id,
            "store_id": s_id,
            "supplier_id": sup_id,
            "order_date": order_dt.strftime("%Y-%m-%d"),
            "expected_delivery_date": exp_delivery_dt.strftime("%Y-%m-%d"),
            "actual_delivery_date": act_delivery_dt.strftime("%Y-%m-%d"),
            "quantity_ordered": qty_ordered,
            "quantity_received": qty_received,
            "unit_cost": p_info["unit_cost"],
            "lead_time_days": actual_lt
        })
        po_id_counter += 1
        
    df_purchase = pd.DataFrame(po_records)
    
    # ---------------------------------------------------------
    # 8. INTRODUCE INTENTIONAL DATA QUALITY ISSUES IN RAW FILES
    # ---------------------------------------------------------
    print("Injecting intentional raw data quality edge-cases for auditing...", flush=True)
    df_sales_raw = df_sales.copy()
    
    duplicates = df_sales_raw.sample(15, random_state=42)
    df_sales_raw = pd.concat([df_sales_raw, duplicates], ignore_index=True)
    
    missing_store_idx = df_sales_raw.sample(12, random_state=101).index
    df_sales_raw.loc[missing_store_idx, "store_id"] = np.nan
    
    inc_date_idx = df_sales_raw.sample(8, random_state=202).index
    df_sales_raw.loc[inc_date_idx, "date"] = df_sales_raw.loc[inc_date_idx, "date"].str.replace("-", "/")
    
    invalid_idx = df_sales_raw.sample(4, random_state=303).index
    df_sales_raw.loc[invalid_idx[0], "quantity_sold"] = -2
    df_sales_raw.loc[invalid_idx[1], "unit_price"] = -49.99
    
    df_products_raw = df_products.copy()
    df_products_raw.loc[[5, 18, 35], "category"] = np.nan
    
    # Save CSVs
    df_sales_raw.to_csv(os.path.join(raw_dir, 'raw_sales.csv'), index=False)
    df_inventory.to_csv(os.path.join(raw_dir, 'raw_inventory.csv'), index=False)
    df_purchase.to_csv(os.path.join(raw_dir, 'raw_purchase_orders.csv'), index=False)
    df_products_raw.to_csv(os.path.join(raw_dir, 'raw_products.csv'), index=False)
    df_stores.to_csv(os.path.join(raw_dir, 'raw_stores.csv'), index=False)
    df_suppliers.to_csv(os.path.join(raw_dir, 'raw_suppliers.csv'), index=False)
    df_date.to_csv(os.path.join(raw_dir, 'raw_date.csv'), index=False)
    
    print("Raw synthetic dataset successfully generated and saved to data/raw/", flush=True)
    print(f"Sales Records: {len(df_sales_raw)}", flush=True)
    print(f"Inventory Snapshots: {len(df_inventory)}", flush=True)
    print(f"Purchase Orders: {len(df_purchase)}", flush=True)

if __name__ == "__main__":
    project_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    generate_retail_dataset(project_base)
