import pytest
import pandas as pd
from src.transform import transform_jobs

def test_transform_jobs_handles_valid_data():
    # Arrange: Mock API output payload data structures
    mock_raw_data = [
        {
            "id": "job_01",
            "title": "  ML Engineer II ",
            "company": "Samsara",
            "location": "Chicago, IL",
            "salary_min": "137000",
            "salary_max": 231000,
            "tags": ["llm", "agents"]
        }
    ]
    
    # Act: Process structures via core engine mapping rules
    result_df = transform_jobs(mock_raw_data)
    
    # Assert: Validate exact structural execution mapping states
    assert not result_df.empty
    assert result_df.loc[0, 'title'] == "ML Engineer II"  # Trimming spaces
    assert result_df.loc[0, 'salary_min'] == 137000      # Parsing string value to int
    assert result_df.loc[0, 'tags'] == "llm, agents"      # Flattening layout list

def test_transform_jobs_handles_empty_input():
    result_df = transform_jobs([])
    assert isinstance(result_df, pd.DataFrame)
    assert result_df.empty

def test_transform_jobs_fills_missing_fields():
    mock_broken_data = [{"id": "job_02"}]
    result_df = transform_jobs(mock_broken_data)
    
    assert result_df.loc[0, 'title'] == "Unknown Title"
    assert result_df.loc[0, 'company'] == "Unknown Company"
    assert result_df.loc[0, 'salary_min'] == 0
