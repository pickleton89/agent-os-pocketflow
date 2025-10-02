import pytest
from unittest.mock import AsyncMock, patch
from baselineragworkflow.nodes import DocumentLoader, TextChunker, EmbeddingGenerator, QueryProcessor, Retriever, ContextFormatter, ResponseGenerator


class TestDocumentLoader:
    """Tests for DocumentLoader node."""

    @pytest.fixture
    def node(self):
        return DocumentLoader()

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


class TestTextChunker:
    """Tests for TextChunker node."""

    @pytest.fixture
    def node(self):
        return TextChunker()

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


class TestEmbeddingGenerator:
    """Tests for EmbeddingGenerator node."""

    @pytest.fixture
    def node(self):
        return EmbeddingGenerator()

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


class TestQueryProcessor:
    """Tests for QueryProcessor node."""

    @pytest.fixture
    def node(self):
        return QueryProcessor()

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


class TestRetriever:
    """Tests for Retriever node."""

    @pytest.fixture
    def node(self):
        return Retriever()

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


class TestContextFormatter:
    """Tests for ContextFormatter node."""

    @pytest.fixture
    def node(self):
        return ContextFormatter()

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


class TestResponseGenerator:
    """Tests for ResponseGenerator node."""

    @pytest.fixture
    def node(self):
        return ResponseGenerator()

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

