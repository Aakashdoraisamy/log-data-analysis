# scripts/04_analyze_data.py
import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import logging

# ----------------------------
# Setup logging
# ----------------------------
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=os.path.join("logs", "analyze_data.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

try:
    # ----------------------------
    # Database connection
    # ----------------------------
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASS", ""),
        database=os.getenv("DB_NAME", "log_analysis")
    )

    logging.info("✅ Connected to MySQL database.")

    # ----------------------------
    # Query top processes
    # ----------------------------
    query = """
    SELECT process, COUNT(*) AS cnt 
    FROM system_logs 
    GROUP BY process 
    ORDER BY cnt DESC 
    LIMIT 10;
    """
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        logging.warning("⚠️ No data found in table `system_logs`.")
        print("No data found in table `system_logs`.")
    else:
        print(df.to_string(index=False))
        logging.info(f"✅ Retrieved {len(df)} records for analysis.")

        # ----------------------------
        # Save results
        # ----------------------------
        reports_dir = os.path.join(os.getcwd(), "reports")
        os.makedirs(reports_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_path = os.path.join(reports_dir, f"top_processes_{timestamp}.csv")
        img_path = os.path.join(reports_dir, f"top_processes_{timestamp}.png")

        df.to_csv(csv_path, index=False)

        # ----------------------------
        # Plot results
        # ----------------------------
        plt.figure(figsize=(8, 6))
        plt.barh(df['process'][::-1], df['cnt'][::-1])
        plt.xlabel('Count')
        plt.ylabel('Process')
        plt.title('Top 10 Processes by Log Count')
        plt.tight_layout()
        plt.savefig(img_path)
        plt.close()

        logging.info(f"✅ Report saved: {csv_path}")
        logging.info(f"✅ Chart saved: {img_path}")
        print(f"Saved analysis report → {csv_path}")
        print(f"Saved plot image → {img_path}")

except mysql.connector.Error as err:
    logging.error(f"❌ MySQL Error: {err}")
    print(f"MySQL Error: {err}")

except Exception as e:
    logging.error(f"❌ Unexpected error: {e}")
    print(f"Unexpected error: {e}")
