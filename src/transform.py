import pandas as pd
from datetime import datetime
from src.config import logger

def transform_jobs(raw_jobs: list) -> pd.DataFrame:
    """Cleans and normalizes raw JSON data fields into a strict schema dataframe."""
    logger.info("Starting structural data transformation engine...")
    if not raw_jobs:
        logger.warning("Empty input array passed to transformer. Skipping execution.")
        return pd.DataFrame()

    try:
        df = pd.DataFrame(raw_jobs)
        
        # Enforce target structural grid blueprint columns
        expected_cols = ['id', 'title', 'company', 'location', 'salary_min', 'salary_max', 'tags']
        for col in expected_cols:
            if col not in df.columns:
                df[col] = None

        df = df[expected_cols]

        # Standardize and clean string layers
        df['title'] = df['title'].fillna('Unknown Title').astype(str).str.strip()
        df['company'] = df['company'].fillna('Unknown Company').astype(str).str.strip()
        df['location'] = df['location'].fillna('Remote / Not Specified').astype(str).str.strip()
        
        # Coerce numeric bounds safely to remove NaN elements
        df['salary_min'] = pd.to_numeric(df['salary_min'], errors='coerce').fillna(0).astype(int)
        df['salary_max'] = pd.to_numeric(df['salary_max'], errors='coerce').fillna(0).astype(int)
        
        # Convert relational tag object structures to database text streams
        df['tags'] = df['tags'].apply(lambda x: ", ".join(x) if isinstance(x, list) else (str(x) if pd.notnull(x) else ''))

        # Track system processing metrics
        df['extracted_at'] = datetime.utcnow()

        logger.info(f"Data transformation completed. Resulting matrix layout metrics: {df.shape}")
        return df

    except Exception as e:
        logger.error(f"Transformation engine experienced a systemic breakdown: {e}", exc_info=True)
        raise e
