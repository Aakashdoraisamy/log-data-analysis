# scripts/00_config.py
# Put non-sensitive defaults here. For credentials use environment variables or .env in development.
import os

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "Aakash@0310") 
DB_NAME = os.getenv("DB_NAME", "log_analysis")

RAW_LOG_DIR = os.path.join(os.path.dirname(__file__), "../data/raw_logs")
RAW_LOG_DIR = os.path.join(os.path.dirname(__file__), "../data/raw_logs")

PROCESSED_DIR = os.path.join(os.path.dirname(__file__), "../data/clean_logs")
