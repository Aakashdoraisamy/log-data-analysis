import shutil
import os
from datetime import datetime
from pathlib import Path
from scripts import config as cfg 

SRC = "/var/log/syslog"

date_str = datetime.now().strftime("%Y%m%d_%H%M%S")

# Destination file path inside data/raw_logs/
dst = os.path.abspath(os.path.join(cfg.RAW_LOG_DIR, f"syslog_{date_str}.log"))

Path(cfg.RAW_LOG_DIR).mkdir(parents=True, exist_ok=True)
shutil.copy(SRC, dst)
print(f"✅ Copied {SRC} -> {dst}")
