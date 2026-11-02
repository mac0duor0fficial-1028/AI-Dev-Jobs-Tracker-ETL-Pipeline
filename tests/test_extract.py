import pytest
from unittest.mock import patch, MagicMock
import requests
from src.extract import extract_jobs

def test_extract_jobs_success():
    """Verifies that extract_jobs successfully returns data when the API responds with 200 OK."""
    # Arrange: Mock api return schema structures
    mock_payload = {
        "jobs": [
            {"id": "job_01", "title": "AI Engineer"},
            {"id": "job_02", "title": "ML Platform Engineer"}
        ]
    }
    
    with patch('src.extract.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_payload
        mock_get.return_value = mock_response
        
        # Act: Execute extraction module execution steps
        result = extract_jobs()
        
        # Assert: Verify properties match up accurately
        assert len(result) == 2
        assert result[0]['title'] == "AI Engineer"
        mock_get.assert_called_once()

def test_extract_jobs_handles_flat_array():
    """Verifies extract_jobs functions properly even if the endpoint outputs a flat array instead of a dictionary."""
    mock_payload = [{"id": "job_03", "title": "Data Scientist"}]
    
    with patch('src.extract.requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_payload
        mock_get.return_value = mock_response
        
        result = extract_jobs()
        
        assert len(result) == 1
        assert result[0]['id'] == "job_03"

def test_extract_jobs_raises_exception_on_http_error():
    """Verifies that network degradation or client HTTP errors bubble up out of the module safely."""
    with patch('src.extract.requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.HTTPError("404 Client Error: Not Found")
        
        # Assert that the function raises the HTTPError when called
        with pytest.raises(requests.exceptions.RequestException):
            extract_jobs()
