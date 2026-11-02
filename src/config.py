import os
import logging

# API Specifications
API_URL = os.getenv("API_URL", "https://aidevboard.com")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 15))

# Database Engine Setup
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "your_database_name"),
    "user": os.getenv("DB_USER", "your_username"),
    "password": os.getenv("DB_PASSWORD", "your_password"),
    "port": int(os.getenv("DB_PORT", 5432))
}

# Standardized Airflow-compatible structured logger
logger = logging.getLogger("airflow.task")
