import sqlite3
import glob

def test_sql():
    conn = sqlite3.connect('data/retail_inventory.db')
    sql_files = sorted(glob.glob('sql/*.sql'))
    
    for f in sql_files:
        print(f"\n==================================================")
        print(f"Executing File: {f}")
        print(f"==================================================")
        with open(f, 'r') as fp:
            sql_text = fp.read()
            
        # Split statements by semicolon while ignoring comments
        raw_statements = sql_text.split(';')
        stmt_idx = 1
        for stmt in raw_statements:
            # Clean lines starting with --
            lines = [line for line in stmt.split('\n') if not line.strip().startswith('--')]
            clean_stmt = ' '.join(lines).strip()
            if clean_stmt:
                try:
                    cur = conn.cursor()
                    cur.execute(clean_stmt)
                    rows = cur.fetchall()
                    cols = [d[0] for d in cur.description] if cur.description else []
                    print(f"Query #{stmt_idx} Success: Returned {len(rows)} rows | Columns: {cols[:4]}")
                    stmt_idx += 1
                except Exception as e:
                    print(f"Query #{stmt_idx} Error: {e}")
                    print(f"Failing Statement:\n{clean_stmt}\n")

if __name__ == "__main__":
    test_sql()
