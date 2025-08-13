import pytest
from unittest.mock import AsyncMock, patch
from ..nodes import DocumentRetrieverNode, ContextBuilderNode, LLMAnalyzerNode, ResponseFormatterNode


class TestDocumentRetrieverNode:
    """Tests for DocumentRetrieverNode node."""

    @pytest.fixture
    def node(self):
        return DocumentRetrieverNode()

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


class TestContextBuilderNode:
    """Tests for ContextBuilderNode node."""

    @pytest.fixture
    def node(self):
        return ContextBuilderNode()

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


class TestLLMAnalyzerNode:
    """Tests for LLMAnalyzerNode node."""

    @pytest.fixture
    def node(self):
        return LLMAnalyzerNode()

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


class TestResponseFormatterNode:
    """Tests for ResponseFormatterNode node."""

    @pytest.fixture
    def node(self):
        return ResponseFormatterNode()

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

