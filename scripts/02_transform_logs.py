import os
import re
import pandas as pd
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DIR = os.path.join(BASE_DIR, "../data/raw_logs")
CLEAN_DIR = os.path.join(BASE_DIR, "../data/clean_logs")

os.makedirs(CLEAN_DIR, exist_ok=True)

raw_files = sorted([f for f in os.listdir(RAW_DIR) if f.startswith("syslog_")], reverse=True)
if not raw_files:
    print("❌ No raw log files found.")
    exit()

latest_file = os.path.join(RAW_DIR, raw_files[0])
print(f"📂 Processing: {latest_file}")

pattern = re.compile(
    r'(?P<timestamp>\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d+\+\d{2}:\d{2})\s+'
    r'(?P<host>\S+)\s+'
    r'(?P<process>[^\[]+)\[(?P<pid>\d+)\]:\s+'
    r'(?:#033\[\d+m)?(?P<level>[A-Z]+)(?:#033\[0m)?\s+'
    r'(?P<message>.*)'
)

# Parse log lines
data = []
with open(latest_file, "r", encoding="utf-8") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            data.append(match.groupdict())

if not data:
    print("⚠️ No parseable log lines found.")
    exit()

df = pd.DataFrame(data)

df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
clean_file = os.path.join(CLEAN_DIR, f"clean_logs_{timestamp_str}.csv")
df.to_csv(clean_file, index=False)

print(f"✅ Cleaned log data saved to: {clean_file}")
print(df.head())
