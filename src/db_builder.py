import os
import sqlite3
import pandas as pd

def build_database(base_dir):
    proc_dir = os.path.join(base_dir, 'data', 'processed')
    db_path = os.path.join(base_dir, 'data', 'retail_inventory.db')
    
    if os.path.exists(db_path):
        os.remove(db_path)
        
    print(f"Building relational SQLite database at {db_path}...", flush=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # Read processed CSV files
    df_date = pd.read_csv(os.path.join(proc_dir, 'dim_date.csv'))
    df_products = pd.read_csv(os.path.join(proc_dir, 'dim_product.csv'))
    df_stores = pd.read_csv(os.path.join(proc_dir, 'dim_store.csv'))
    df_suppliers = pd.read_csv(os.path.join(proc_dir, 'dim_supplier.csv'))
    df_sales = pd.read_csv(os.path.join(proc_dir, 'fact_sales.csv'))
    df_inventory = pd.read_csv(os.path.join(proc_dir, 'fact_inventory.csv'))
    df_purchase = pd.read_csv(os.path.join(proc_dir, 'fact_purchase.csv'))
    
    # Write tables to SQLite database
    df_date.to_sql('dim_date', conn, if_exists='replace', index=False)
    df_products.to_sql('dim_product', conn, if_exists='replace', index=False)
    df_stores.to_sql('dim_store', conn, if_exists='replace', index=False)
    df_suppliers.to_sql('dim_supplier', conn, if_exists='replace', index=False)
    df_sales.to_sql('fact_sales', conn, if_exists='replace', index=False)
    df_inventory.to_sql('fact_inventory', conn, if_exists='replace', index=False)
    df_purchase.to_sql('fact_purchase', conn, if_exists='replace', index=False)
    
    # Create indexes for optimal analytical query performance
    print("Creating database indexes...", flush=True)
    indexes = [
        "CREATE INDEX idx_sales_date ON fact_sales(date_id);",
        "CREATE INDEX idx_sales_prod ON fact_sales(product_id);",
        "CREATE INDEX idx_sales_store ON fact_sales(store_id);",
        "CREATE INDEX idx_inv_date ON fact_inventory(date_id);",
        "CREATE INDEX idx_inv_prod_store ON fact_inventory(product_id, store_id);",
        "CREATE INDEX idx_purchase_supplier ON fact_purchase(supplier_id);",
        "CREATE INDEX idx_purchase_prod ON fact_purchase(product_id);",
        "CREATE INDEX idx_prod_cat ON dim_product(category);"
    ]
    for idx_sql in indexes:
        cursor.execute(idx_sql)
        
    conn.commit()
    conn.close()
    print("SQLite Database successfully created and indexed!", flush=True)

if __name__ == "__main__":
    project_base = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    build_database(project_base)
