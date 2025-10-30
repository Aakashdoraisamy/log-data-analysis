import os
import pandas as pd
import mysql.connector
from pathlib import Path
from scripts import config as cfg

csv_files = sorted(Path(cfg.PROCESSED_DIR).glob("clean_logs_*.csv"))
if not csv_files:
    print("❌ No processed files found.")
    raise SystemExit(1)

csv_path = csv_files[-1]
print(f"📂 Loading data from: {csv_path}")

df = pd.read_csv(csv_path)
try:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", cfg.DB_HOST),
        user=os.getenv("DB_USER", cfg.DB_USER),
        password=os.getenv("DB_PASS", cfg.DB_PASS),
        database=os.getenv("DB_NAME", cfg.DB_NAME)
    )
    cursor = conn.cursor()
    print("✅ Connected to MySQL database.")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    raise SystemExit(1)

create_table_sql = """
CREATE TABLE IF NOT EXISTS system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp VARCHAR(64),
    host VARCHAR(64),
    process VARCHAR(128),
    pid INT,
    level VARCHAR(16),
    message TEXT
)
"""
cursor.execute(create_table_sql)
conn.commit()

insert_sql = """
INSERT INTO system_logs (timestamp, host, process, pid, level, message)
VALUES (%s, %s, %s, %s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(insert_sql, (
        str(row.get("timestamp")),
        str(row.get("host")),
        str(row.get("process")),
        int(row.get("pid", 0)) if not pd.isna(row.get("pid")) else None,
        str(row.get("level")),
        str(row.get("message"))
    ))

conn.commit()
cursor.close()
conn.close()

print(f"✅ Inserted {len(df)} rows into MySQL table `system_logs` successfully.")
