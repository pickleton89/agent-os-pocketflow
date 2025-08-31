import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from contentanalyzer.main import app

client = TestClient(app)


class TestAnalyzeEndpoint:
    """Tests for Analyze endpoint."""

    def test_analyze_success(self):
        """Test successful Analyze request."""
        request_data = {"test": "data"}
        response = client.post("/api/v1/analyze", json=request_data)
        assert response.status_code == 200

    def test_analyze_validation_error(self):
        """Test validation error handling."""
        response = client.post("/api/v1/analyze", json={})
        assert response.status_code == 422

