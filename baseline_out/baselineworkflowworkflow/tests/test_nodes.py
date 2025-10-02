import pytest
from unittest.mock import AsyncMock, patch
from baselineworkflowworkflow.nodes import InputValidator, BusinessLogicProcessor, OutputFormatter


class TestInputValidator:
    """Tests for InputValidator node."""

    @pytest.fixture
    def node(self):
        return InputValidator()

    @pytest.fixture
    def shared_store(self):
        return {"input_data": "test_data"}

    def test_prep(self, node, shared_store):
        """Test prep method."""
        result = node.prep(shared_store)
        assert result == "test_data"

    @pytest.mark.asyncio
    async def test_exec_async(self, node):
        """Test exec_async method."""
        result = await node.exec_async("test_data")
        assert result == "success"

    def test_post(self, node, shared_store):
        """Test post method."""
        node.post(shared_store, "prep_result", "exec_result")
        assert "output_data" in shared_store


class TestBusinessLogicProcessor:
    """Tests for BusinessLogicProcessor node."""

    @pytest.fixture
    def node(self):
        return BusinessLogicProcessor()

    @pytest.fixture
    def shared_store(self):
        return {"input_data": "test_data"}

    def test_prep(self, node, shared_store):
        """Test prep method."""
        result = node.prep(shared_store)
        assert result == "test_data"

    @pytest.mark.asyncio
    async def test_exec_async(self, node):
        """Test exec_async method."""
        result = await node.exec_async("test_data")
        assert result == "success"

    def test_post(self, node, shared_store):
        """Test post method."""
        node.post(shared_store, "prep_result", "exec_result")
        assert "output_data" in shared_store


class TestOutputFormatter:
    """Tests for OutputFormatter node."""

    @pytest.fixture
    def node(self):
        return OutputFormatter()

    @pytest.fixture
    def shared_store(self):
        return {"input_data": "test_data"}

    def test_prep(self, node, shared_store):
        """Test prep method."""
        result = node.prep(shared_store)
        assert result == "test_data"

    @pytest.mark.asyncio
    async def test_exec_async(self, node):
        """Test exec_async method."""
        result = await node.exec_async("test_data")
        assert result == "success"

    def test_post(self, node, shared_store):
        """Test post method."""
        node.post(shared_store, "prep_result", "exec_result")
        assert "output_data" in shared_store

