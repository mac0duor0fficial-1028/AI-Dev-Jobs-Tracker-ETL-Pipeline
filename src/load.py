import psycopg2
from psycopg2 import extras
import pandas as pd
from src.config import DB_CONFIG, logger

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS ai_dev_jobs (
    job_id VARCHAR(100) PRIMARY KEY,
    title VARCHAR(255),
    company VARCHAR(255),
    location VARCHAR(255),
    salary_min INT,
    salary_max INT,
    tags TEXT,
    extracted_at TIMESTAMP
);
"""

UPSERT_QUERY = """
INSERT INTO ai_dev_jobs (job_id, title, company, location, salary_min, salary_max, tags, extracted_at)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (job_id) DO UPDATE SET
    title = EXCLUDED.title,
    company = EXCLUDED.company,
    location = EXCLUDED.location,
    salary_min = EXCLUDED.salary_min,
    salary_max = EXCLUDED.salary_max,
    tags = EXCLUDED.tags,
    extracted_at = EXCLUDED.extracted_at;
"""

def load_jobs_to_postgres(df: pd.DataFrame):
    """Saves the cleaned DataFrame into the PostgreSQL cluster using transactional batch upserts."""
    logger.info("Initializing relational loading sequences...")
    if df.empty:
        logger.warning("Empty dataset mapped to database executor. Ingestion bypassed.")
        return

    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Ensure schema table presence
        cursor.execute(CREATE_TABLE_QUERY)
        
        # Compile records as database parameters
        data_tuples = [tuple(row) for row in df.to_numpy()]
        
        # Batch execute parameters via fast binary data packaging
        extras.execute_batch(cursor, UPSERT_QUERY, data_tuples)
        conn.commit()
        
        logger.info(f"Loading complete. Successfully committed {len(df)} entries.")
        cursor.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        logger.critical(f"Database insertion failed. Triggering recovery rollback. Error: {error}", exc_info=True)
        if conn:
            conn.rollback()
        raise error
            
    finally:
        if conn is not None:
            conn.close()
            logger.info("Database connection successfully safely recycled.")
