import requests
from src.config import API_URL, API_TIMEOUT, logger

def extract_jobs() -> list:
    """Fetches raw JSON tracking arrays from the platform REST API endpoint."""
    logger.info("Starting ingestion extraction phase...")
    try:
        response = requests.get(API_URL, params={"limit": 50}, timeout=API_TIMEOUT)
        response.raise_for_status()
        
        data = response.json()
        jobs = data.get("jobs", data) if isinstance(data, dict) else data
        
        logger.info(f"Successfully extracted {len(jobs)} raw tracking records.")
        return jobs
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Extraction failed due to network runtime errors: {e}", exc_info=True)
        raise e
