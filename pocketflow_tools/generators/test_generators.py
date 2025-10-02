from __future__ import annotations

from typing import List


def generate_node_tests(spec) -> str:
    """Generate tests for nodes (legacy parity)."""
    workflow_name = spec.name.lower().replace(" ", "")
    parts: List[str] = [
        "import pytest",
        "from unittest.mock import AsyncMock, patch",
        f"from {workflow_name}.nodes import "
        + ", ".join(node["name"] for node in spec.nodes),
        "",
        "",
    ]

    for node in spec.nodes:
        parts.extend(
            [
                f"class Test{node['name']}:",
                f'    """Tests for {node["name"]} node."""',
                "",
                "    @pytest.fixture",
                "    def node(self):",
                f"        return {node['name']}()",
                "",
                "    @pytest.fixture",
                "    def shared_store(self):",
                '        return {"input_data": "test_data"}',
                "",
                "    def test_prep(self, node, shared_store):",
                '        """Test prep method."""',
                "        result = node.prep(shared_store)",
                '        assert result == "test_data"',
                "",
                "    @pytest.mark.asyncio",
                "    async def test_exec_async(self, node):",
                '        """Test exec_async method."""',
                '        result = await node.exec_async("test_data")',
                '        assert result == "success"',
                "",
                "    def test_post(self, node, shared_store):",
                '        """Test post method."""',
                '        node.post(shared_store, "prep_result", "exec_result")',
                '        assert "output_data" in shared_store',
                "",
                "",
            ]
        )

    return "\n".join(parts)


def generate_flow_tests(spec) -> str:
    """Generate tests for flow (legacy parity)."""
    workflow_name = spec.name.lower().replace(" ", "")
    parts: List[str] = [
        "import pytest",
        "from unittest.mock import AsyncMock, patch",
        f"from {workflow_name}.flow import {spec.name}Flow",
        "",
        "",
        f"class Test{spec.name}Flow:",
        f'    """Tests for {spec.name}Flow."""',
        "",
        "    @pytest.fixture",
        "    def flow(self):",
        f"        return {spec.name}Flow()",
        "",
        "    @pytest.fixture",
        "    def shared_store(self):",
        '        return {"input_data": "test_data"}',
        "",
        "    @pytest.mark.asyncio",
        "    async def test_flow_execution(self, flow, shared_store):",
        '        """Test complete flow execution."""',
        "        await flow.run_async(shared_store)",
        '        assert "output_data" in shared_store',
        "",
        "    @pytest.mark.asyncio",
        "    async def test_flow_error_handling(self, flow, shared_store):",
        '        """Test flow error handling."""',
        "        # Test with invalid input",
        '        shared_store["input_data"] = None',
        "        with pytest.raises(Exception):",
        "            await flow.run_async(shared_store)",
        "",
    ]

    return "\n".join(parts)


def generate_api_tests(spec) -> str:
    """Generate tests for FastAPI endpoints (legacy parity)."""
    workflow_name = spec.name.lower().replace(" ", "")
    parts: List[str] = [
        "import pytest",
        "from fastapi.testclient import TestClient",
        "from unittest.mock import AsyncMock, patch",
        f"from {workflow_name}.main import app",
        "",
        "client = TestClient(app)",
        "",
        "",
    ]

    for endpoint in spec.api_endpoints:
        method = endpoint.get("method", "post").upper()
        path = endpoint.get("path", f"/{endpoint['name'].lower()}")

        parts.extend(
            [
                f"class Test{endpoint['name']}Endpoint:",
                f'    """Tests for {endpoint["name"]} endpoint."""',
                "",
                f"    def test_{endpoint['name'].lower()}_success(self):",
                f'        """Test successful {endpoint["name"]} request."""',
                '        request_data = {"test": "data"}',
                f'        response = client.{method.lower()}("/api/v1{path}", json=request_data)',
                "        assert response.status_code == 200",
                "",
                f"    def test_{endpoint['name'].lower()}_validation_error(self):",
                '        """Test validation error handling."""',
                f'        response = client.{method.lower()}("/api/v1{path}", json={{}})',
                "        assert response.status_code == 422",
                "",
                "",
            ]
        )

    return "\n".join(parts)
