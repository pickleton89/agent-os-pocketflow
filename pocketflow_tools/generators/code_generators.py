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

