import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from baselineragworkflow.main import app

client = TestClient(app)


class TestSearchQueryEndpoint:
    """Tests for SearchQuery endpoint."""

    def test_searchquery_success(self):
        """Test successful SearchQuery request."""
        request_data = {"test": "data"}
        response = client.post("/api/v1/search", json=request_data)
        assert response.status_code == 200

    def test_searchquery_validation_error(self):
        """Test validation error handling."""
        response = client.post("/api/v1/search", json={})
        assert response.status_code == 422

