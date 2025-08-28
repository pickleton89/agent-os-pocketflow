import pytest
from unittest.mock import AsyncMock, patch
from orderprocessor.nodes import OrderValidator, InventoryChecker, PaymentProcessor, ShippingCoordinator


class TestOrderValidator:
    """Tests for OrderValidator node."""

    @pytest.fixture
    def node(self):
        return OrderValidator()

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


class TestInventoryChecker:
    """Tests for InventoryChecker node."""

    @pytest.fixture
    def node(self):
        return InventoryChecker()

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


class TestPaymentProcessor:
    """Tests for PaymentProcessor node."""

    @pytest.fixture
    def node(self):
        return PaymentProcessor()

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


class TestShippingCoordinator:
    """Tests for ShippingCoordinator node."""

    @pytest.fixture
    def node(self):
        return ShippingCoordinator()

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

