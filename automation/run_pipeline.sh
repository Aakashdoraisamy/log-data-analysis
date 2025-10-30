#!/bin/bash
# automation/run_pipeline.sh
cd /home/aakash/log_data_analysis || exit 1
source venv/bin/activate

# run steps
python3 scripts/01_extract_logs.py
python3 scripts/02_transform_logs.py
python3 scripts/03_load_to_db.py
python3 scripts/04_analyze_data.py
