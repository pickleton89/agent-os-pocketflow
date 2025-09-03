import pytest
from unittest.mock import AsyncMock, patch
from baselinetoolworkflow.nodes import RequestValidator, AuthHandler, ExternalConnector, DataTransformer, ResponseProcessor


class TestRequestValidator:
    """Tests for RequestValidator node."""

    @pytest.fixture
    def node(self):
        return RequestValidator()

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


class TestAuthHandler:
    """Tests for AuthHandler node."""

    @pytest.fixture
    def node(self):
        return AuthHandler()

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


class TestExternalConnector:
    """Tests for ExternalConnector node."""

    @pytest.fixture
    def node(self):
        return ExternalConnector()

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


class TestDataTransformer:
    """Tests for DataTransformer node."""

    @pytest.fixture
    def node(self):
        return DataTransformer()

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


class TestResponseProcessor:
    """Tests for ResponseProcessor node."""

    @pytest.fixture
    def node(self):
        return ResponseProcessor()

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

