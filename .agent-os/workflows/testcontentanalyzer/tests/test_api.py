import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from testcontentanalyzer.main import app

client = TestClient(app)


class TestAnalyzeContentEndpoint:
    """Tests for AnalyzeContent endpoint."""

    def test_analyzecontent_success(self):
        """Test successful AnalyzeContent request."""
        request_data = {"test": "data"}
        response = client.post("/api/v1/analyze", json=request_data)
        assert response.status_code == 200

    def test_analyzecontent_validation_error(self):
        """Test validation error handling."""
        response = client.post("/api/v1/analyze", json={})
        assert response.status_code == 422

