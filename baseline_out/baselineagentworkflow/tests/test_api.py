import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from baselineagentworkflow.main import app

client = TestClient(app)


class TestProcessTaskEndpoint:
    """Tests for ProcessTask endpoint."""

    def test_processtask_success(self):
        """Test successful ProcessTask request."""
        request_data = {"test": "data"}
        response = client.post("/api/v1/process", json=request_data)
        assert response.status_code == 200

    def test_processtask_validation_error(self):
        """Test validation error handling."""
        response = client.post("/api/v1/process", json={})
        assert response.status_code == 422

