import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
import psycopg2
from src.load import load_jobs_to_postgres

@pytest.fixture
def sample_dataframe():
    """Provides a valid, clean sample DataFrame matching our transform schema blueprint."""
    return pd.DataFrame([{
        'job_id': 'job_99',
        'title': 'Data Architect',
        'company': 'Enterprise AI',
        'location': 'Remote',
        'salary_min': 150000,
        'salary_max': 200000,
        'tags': 'airflow, postgres',
        'extracted_at': pd.Timestamp('2026-11-02 00:00:00')
    }])

def test_load_jobs_to_postgres_skips_empty_dataframe():
    """Verifies that an empty dataset is bypassed before establishing database connections."""
    with patch('src.load.psycopg2.connect') as mock_connect:
        empty_df = pd.DataFrame()
        
        load_jobs_to_postgres(empty_df)
        
        # Database connection engine shouldn't be initialized
        mock_connect.assert_not_called()

def test_load_jobs_to_postgres_success(sample_dataframe):
    """Verifies database execution path, tracking initialization queries and batch processes."""
    with patch('src.load.psycopg2.connect') as mock_connect:
        # Mock connection hierarchy steps
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        with patch('src.load.extras.execute_batch') as mock_execute_batch:
            # Act: Run loader operation module
            load_jobs_to_postgres(sample_dataframe)
            
            # Assert: Trace transactions executions safely
            mock_cursor.execute.assert_called_once()  # Verification of CREATE TABLE QUERY presence
            mock_execute_batch.assert_called_once()   # Target verification for extras batch utility triggers
            mock_conn.commit().assert_called_once()
            mock_conn.close().assert_called_once()

def test_load_jobs_to_postgres_rollback_on_database_error(sample_dataframe):
    """Verifies transaction rollback and recovery protocols run safely during query breaks."""
    with patch('src.load.psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        
        with patch('src.load.extras.execute_batch') as mock_execute_batch:
            # Force batch script compilation to simulate transactional database error states
            mock_execute_batch.side_effect = psycopg2.DatabaseError("Deadlock detected or connection drop")
            
            # Assert: Ensure operational errors cascade up cleanly so orchestration workflows pick them up
            with pytest.raises(psycopg2.DatabaseError):
                load_jobs_to_postgres(sample_dataframe)
                
            # Verify system safety protocols ran during tracking failures
            mock_conn.rollback.assert_called_once()
            mock_conn.close().assert_called_once()
