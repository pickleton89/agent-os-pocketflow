from __future__ import annotations

from typing import Any, Dict, List


def generate_utility(utility: Dict[str, Any]) -> str:
    """Generate utility function from specification.

    Mirrors the legacy _generate_utility method to preserve parity.
    """
    utility_code: List[str] = [
        '"""',
        f"{utility['description']}",
        '"""',
        "",
        "from typing import Any, Optional",
        "",
        "",
    ]

    # Function signature
    params: List[str] = []
    for param in utility.get("parameters", []):
        if param.get("optional", False):
            params.append(f"{param['name']}: Optional[{param['type']}] = None")
        else:
            params.append(f"{param['name']}: {param['type']}")

    # Determine if utility should be async based on description or explicit flag
    is_async_utility = utility.get("async", False) or any(
        keyword in utility["description"].lower()
        for keyword in [
            "llm",
            "api",
            "database",
            "file",
            "network",
            "http",
            "fetch",
            "request",
        ]
    )

    func_def = (
        f"async def {utility['name']}("
        if is_async_utility
        else f"def {utility['name']}("
    )
    test_call = (
        f"    # asyncio.run({utility['name']}())"
        if is_async_utility
        else f"    # {utility['name']}()"
    )

    utility_code.extend(
        [
            func_def,
            f"    {', '.join(params)}",
            f") -> {utility.get('return_type', 'Any')}:",
            '    """',
            f"    {utility['description']}",
            '    """',
            f"    # TODO: Implement {utility['name']}",
            f'    raise NotImplementedError("Utility function {utility["name"]} not implemented")',
            "",
            "",
            'if __name__ == "__main__":',
            f"    # Test {utility['name']} function",
        ]
    )

    if is_async_utility:
        utility_code.extend(["    import asyncio", test_call, "    pass"])
    else:
        utility_code.extend([test_call, "    pass"])

    return "\n".join(utility_code)


def generate_fastapi_main(spec) -> str:
    """Generate FastAPI main application (legacy parity)."""
    main_code = [
        "from fastapi import FastAPI, HTTPException",
        "from fastapi.middleware.cors import CORSMiddleware",
        f"from .router import router as {spec.name.lower()}_router",
        "import logging",
        "",
        "logging.basicConfig(level=logging.INFO)",
        "",
        "app = FastAPI(",
        f'    title="{spec.name} API",',
        f'    description="{spec.description}",',
        '    version="1.0.0"',
        ")",
        "",
        "app.add_middleware(",
        "    CORSMiddleware,",
        '    allow_origins=["*"],',
        "    allow_credentials=True,",
        '    allow_methods=["*"],',
        '    allow_headers=["*"],',
        ")",
        "",
        f'app.include_router({spec.name.lower()}_router, prefix="/api/v1", tags=["{spec.name}"])',
        "",
        '@app.get("/health")',
        "async def health_check():",
        '    return {"status": "healthy"}',
    ]

    return "\n".join(main_code)


def generate_fastapi_router(spec) -> str:
    """Generate FastAPI router with endpoints (legacy parity)."""
    router_code = [
        "from fastapi import APIRouter, HTTPException",
        "from .schemas.models import *",
        f"from .flow import {spec.name}Flow",
        "from typing import Dict, Any",
        "import logging",
        "from datetime import datetime",
        "",
        "logger = logging.getLogger(__name__)",
        "router = APIRouter()",
        "",
    ]

    for endpoint in spec.api_endpoints:
        method = endpoint.get("method", "post").lower()
        path = endpoint.get("path", f"/{endpoint['name'].lower()}")
        endpoint_name = endpoint["name"]
        default_desc = f"Execute {endpoint_name} workflow"

        router_code.extend([
            f'@router.{method}("{path}", response_model={endpoint_name}Response)',
            f"async def {endpoint_name.lower()}_endpoint(request: {endpoint_name}Request):",
            '    """',
            f"    {endpoint.get('description', default_desc)}",
            '    """',
            "    # Initialize SharedStore",
            "    shared = {",
            '        "request_data": request.dict(),',
            '        "timestamp": datetime.utcnow().isoformat()',
            "    }",
            "",
            "    # Execute workflow - let PocketFlow handle retries and errors",
            f"    flow = {spec.name}Flow()",
            "    await flow.run_async(shared)",
            "",
            "    # Check for flow-level errors",
            '    if "error" in shared:',
            "        raise HTTPException(",
            "            status_code=422,",
            '            detail=shared.get("error_message", "Workflow execution failed")',
            "        )",
            "",
            "    # Return response",
            f'    return {endpoint["name"]}Response(**shared.get("result", {{}}))',
            "",
            "",
        ])

    return "\n".join(router_code)


# -----------------------------
# Phase 1: Extracted generators
# -----------------------------

def generate_pydantic_models(spec) -> str:
    """Generate Pydantic models from shared store schema (legacy parity)."""
    models: List[str] = [
        "from pydantic import BaseModel, Field, validator",
        "from typing import Dict, List, Optional, Any",
        "from datetime import datetime",
        "",
        "",
    ]

    # SharedStore model
    models.extend([
        "class SharedStoreModel(BaseModel):",
        '    """Pydantic model for SharedStore validation."""',
        "",
    ])

    for key, value_type in spec.shared_store_schema.items():
        models.append(f"    {key}: {value_type}")

    models.extend(["", ""])

    # API models (universal architecture)
    for endpoint in spec.api_endpoints:
        # Request model
        models.extend([
            f"class {endpoint['name']}Request(BaseModel):",
            f'    """Request model for {endpoint["name"]} endpoint."""',
            "",
        ])
        for field in endpoint.get("request_fields", []):
            models.append(f"    {field['name']}: {field['type']}")
        models.extend(["", ""])

        # Response model
        models.extend([
            f"class {endpoint['name']}Response(BaseModel):",
            f'    """Response model for {endpoint["name"]} endpoint."""',
            "",
        ])
        for field in endpoint.get("response_fields", []):
            models.append(f"    {field['name']}: {field['type']}")
        models.extend(["", ""])

    return "\n".join(models)


def _get_smart_node_defaults(node: Dict[str, Any], is_async: bool = False) -> Dict[str, str]:
    """Generate smart defaults based on node name and description (legacy parity)."""
    name = str(node.get("name", "")).lower()
    description = str(node.get("description", "")).lower()

    # Common patterns for different node types
    prep_examples = {
        "retriever": 'return shared.get("query", "")',
        "loader": 'return shared.get("file_path", "")',
        "analyzer": 'return shared.get("content", "")',
        "formatter": 'return shared.get("raw_data", "")',
        "validator": 'return shared.get("input_data", "")',
        "transformer": 'return shared.get("input_data", "")',
        "llm": 'prompt = f"Process this: {shared.get(\"content\", \"\")}"\n        return prompt',
        "embedding": 'return shared.get("text", "")',
        "search": 'return shared.get("query", "")',
        "filter": 'return shared.get("items", [])',
    }

    # Async exec examples
    exec_examples_async = {
        "retriever": 'search_results = await search_documents(prep_result)\n        return search_results',
        "loader": 'async with aiofiles.open(prep_result, "r") as f:\n            content = await f.read()\n        return content',
        "analyzer": 'analysis = await analyze_content(prep_result)\n        return analysis',
        "formatter": 'formatted_data = await format_response_async(prep_result)\n        return formatted_data',
        "validator": 'is_valid = await validate_input_async(prep_result)\n        return {"valid": is_valid, "data": prep_result}',
        "transformer": 'transformed = await transform_data_async(prep_result)\n        return transformed',
        "llm": 'response = await call_llm(prep_result)\n        return response',
        "embedding": 'embedding = await get_embedding(prep_result)\n        return embedding',
        "search": 'results = await search_vector_db(prep_result)\n        return results',
        "filter": 'filtered = await filter_async(prep_result)\n        return filtered',
    }

    # Sync exec examples
    exec_examples_sync = {
        "retriever": 'search_results = search_documents(prep_result)\n        return search_results',
        "loader": 'with open(prep_result, "r") as f:\n            content = f.read()\n        return content',
        "analyzer": 'analysis = analyze_content(prep_result)\n        return analysis',
        "formatter": 'formatted_data = format_response(prep_result)\n        return formatted_data',
        "validator": 'is_valid = validate_input(prep_result)\n        return {"valid": is_valid, "data": prep_result}',
        "transformer": 'transformed = transform_data(prep_result)\n        return transformed',
        "llm": 'response = call_llm_sync(prep_result)\n        return response',
        "embedding": 'embedding = get_embedding_sync(prep_result)\n        return embedding',
        "search": 'results = search_vector_db_sync(prep_result)\n        return results',
        "filter": 'filtered = [item for item in prep_result if meets_criteria(item)]\n        return filtered',
    }

    exec_examples = exec_examples_async if is_async else exec_examples_sync

    post_examples = {
        "retriever": 'shared["retrieved_docs"] = exec_result',
        "loader": 'shared["loaded_content"] = exec_result',
        "analyzer": 'shared["analysis_result"] = exec_result',
        "formatter": 'shared["formatted_output"] = exec_result',
        "validator": 'shared["validation_result"] = exec_result',
        "transformer": 'shared["transformed_data"] = exec_result',
        "llm": 'shared["llm_response"] = exec_result',
        "embedding": 'shared["embeddings"] = exec_result',
        "search": 'shared["search_results"] = exec_result',
        "filter": 'shared["filtered_data"] = exec_result',
    }

    for pattern in prep_examples.keys():
        if pattern in name or pattern in description:
            return {
                "prep": prep_examples[pattern],
                "exec": exec_examples[pattern],
                "post": post_examples[pattern],
            }

    # Default fallback
    return {
        "prep": 'return shared.get("input_data")',
        "exec": '# Implement your core logic here\n        return "success"',
        "post": 'shared["output_data"] = exec_result',
    }


def _get_enhanced_todos_for_node(node: Dict[str, Any]) -> List[str]:
    return list(node.get("enhanced_todos", []))


def _get_orchestrator_guidance_for_node(node: Dict[str, Any]) -> List[str]:
    return list(node.get("orchestrator_guidance", []))


def _get_framework_reminders_for_node(node: Dict[str, Any]) -> List[str]:
    return list(node.get("framework_reminders", []))


def generate_nodes(spec) -> str:
    """Generate PocketFlow nodes from specification (legacy parity)."""
    nodes_code: List[str] = [
        "from pocketflow import Node, AsyncNode, BatchNode",
        "from typing import Dict, Any",
        "import logging",
        "",
        "logger = logging.getLogger(__name__)",
        "",
        "",
    ]

    for node in spec.nodes:
        node_type = node.get("type", "Node")

        valid_node_types = {
            "Node",
            "AsyncNode",
            "BatchNode",
            "AsyncBatchNode",
            "AsyncParallelBatchNode",
        }
        if node_type not in valid_node_types:
            raise ValueError(
                f"Invalid node type '{node_type}' for node '{node['name']}'. "
                f"Valid types are: {', '.join(sorted(valid_node_types))}"
            )

        batch_comment = ""
        if node_type == "BatchNode":
            batch_comment = "\n    # NOTE: BatchNode used for processing multiple items in parallel"

        is_async_node = node_type in [
            "AsyncNode",
            "AsyncBatchNode",
            "AsyncParallelBatchNode",
        ]
        exec_method = "async def exec_async" if is_async_node else "def exec"
        exec_signature = f"    {exec_method}(self, prep_result: Any) -> str:"

        smart_defaults = _get_smart_node_defaults(node, is_async_node)
        enhanced_todos = _get_enhanced_todos_for_node(node)
        orchestrator_guidance = _get_orchestrator_guidance_for_node(node)
        framework_reminders = _get_framework_reminders_for_node(node)

        nodes_code.extend([
            f"class {node['name']}({node_type}):",
            '    """',
            f"    {node['description']}",
            f'    """{batch_comment}',
            "",
        ])

        # Framework reminders
        if framework_reminders:
            for reminder in framework_reminders:
                nodes_code.append(f"    {reminder}")
            nodes_code.append("")

        # Orchestrator guidance
        if orchestrator_guidance:
            for guidance in orchestrator_guidance:
                nodes_code.append(f"    {guidance}")
            nodes_code.append("")

        nodes_code.extend([
            "    def prep(self, shared: Dict[str, Any]) -> Any:",
            '        """Data preparation and validation."""',
            f'        logger.info(f"Preparing data for {node["name"]}")',
            "",
            "        # Enhanced TODO guidance from framework extensions:",
        ])

        # Enhanced TODOs for prep
        prep_todos = enhanced_todos[:2] if enhanced_todos else [
            "# TODO: Customize this prep logic based on your needs",
        ]
        for todo in prep_todos:
            nodes_code.append(f"        {todo}")

        nodes_code.extend([
            f"        {smart_defaults['prep']}",
            "",
            exec_signature,
            '        """Core processing logic."""',
            f'        logger.info(f"Executing {node["name"]}")',
            "",
            "        # Enhanced TODO guidance from framework extensions:",
        ])

        exec_todos = (
            enhanced_todos[2:4]
            if len(enhanced_todos) > 2
            else ["# TODO: Customize this exec logic based on your needs"]
        )
        for todo in exec_todos:
            nodes_code.append(f"        {todo}")

        nodes_code.extend([
            f"        {smart_defaults['exec']}",
            "",
            "    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None:",
            '        """Post-processing and result storage."""',
            f'        logger.info(f"Post-processing for {node["name"]}")',
            "",
            "        # Enhanced TODO guidance from framework extensions:",
        ])

        post_todos = (
            enhanced_todos[4:]
            if len(enhanced_todos) > 4
            else ["# TODO: Customize this post logic based on your needs"]
        )
        for todo in post_todos:
            nodes_code.append(f"        {todo}")

        nodes_code.extend([
            f"        {smart_defaults['post']}",
            "",
            "",
        ])

    return "\n".join(nodes_code)


def generate_flow(spec) -> str:
    """Generate PocketFlow flow assembly (legacy parity)."""
    flow_code: List[str] = [
        "from pocketflow import Flow",
        "from .nodes import " + ", ".join(node["name"] for node in spec.nodes),
        "import logging",
        "",
        "logger = logging.getLogger(__name__)",
        "",
        "",
    ]

    flow_code.extend([
        f"class {spec.name}Flow(Flow):",
        '    """',
        f"    {spec.description}",
        '    """',
        "",
        "    def __init__(self):",
        "        nodes = {",
    ])

    for node in spec.nodes:
        flow_code.append(f'            "{node["name"].lower()}": {node["name"]}(),')

    flow_code.extend([
        "        }",
        "",
        "        edges = {",
    ])

    for i, node in enumerate(spec.nodes):
        node_name = node["name"].lower()
        if i < len(spec.nodes) - 1:
            next_node = spec.nodes[i + 1]["name"].lower()
            flow_code.append(
                f'            "{node_name}": {{"success": "{next_node}", "error": "error_handler"}},'
            )
        else:
            flow_code.append(
                f'            "{node_name}": {{"success": None, "error": "error_handler"}},'
            )

    flow_code.extend([
        "        }",
        "",
        "        super().__init__(nodes=nodes, edges=edges)",
        "",
        "",
    ])

    return "\n".join(flow_code)
