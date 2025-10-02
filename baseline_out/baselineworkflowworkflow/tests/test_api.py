import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
from baselineworkflowworkflow.main import app

client = TestClient(app)


class TestProcessWorkflowEndpoint:
    """Tests for ProcessWorkflow endpoint."""

    def test_processworkflow_success(self):
        """Test successful ProcessWorkflow request."""
        request_data = {"test": "data"}
        response = client.post("/api/v1/process", json=request_data)
        assert response.status_code == 200

    def test_processworkflow_validation_error(self):
        """Test validation error handling."""
        response = client.post("/api/v1/process", json={})
        assert response.status_code == 422

