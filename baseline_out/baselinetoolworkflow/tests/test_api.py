import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from baselinetoolworkflow.main import app

client = TestClient(app)


class TestExecuteToolEndpoint:
    """Tests for ExecuteTool endpoint."""

    def test_executetool_success(self):
        """Test successful ExecuteTool request."""
        request_data = {"test": "data"}
        response = client.post("/api/v1/execute", json=request_data)
        assert response.status_code == 200

    def test_executetool_validation_error(self):
        """Test validation error handling."""
        response = client.post("/api/v1/execute", json={})
        assert response.status_code == 422

