import pytest
from unittest.mock import AsyncMock, patch
from baselinetoolworkflow.flow import BaselineTOOLWorkflowFlow


class TestBaselineTOOLWorkflowFlow:
    """Tests for BaselineTOOLWorkflowFlow."""

    @pytest.fixture
    def flow(self):
        return BaselineTOOLWorkflowFlow()

    @pytest.fixture
    def shared_store(self):
        return {"input_data": "test_data"}

    @pytest.mark.asyncio
    async def test_flow_execution(self, flow, shared_store):
        """Test complete flow execution."""
        await flow.run_async(shared_store)
        assert "output_data" in shared_store

    @pytest.mark.asyncio
    async def test_flow_error_handling(self, flow, shared_store):
        """Test flow error handling."""
        # Test with invalid input
        shared_store["input_data"] = None
        with pytest.raises(Exception):
            await flow.run_async(shared_store)
