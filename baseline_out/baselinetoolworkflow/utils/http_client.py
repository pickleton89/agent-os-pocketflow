"""
Make HTTP requests to external APIs

BEST PRACTICE: Keep utility functions simple and transparent.
DO NOT: Hide complex reasoning or decision logic here.
Complex prompt construction belongs in nodes, not utilities.

UTILITY RESPONSIBILITIES:
- Simple I/O operations (file read/write, API calls)
- Data formatting and parsing
- External service interfaces

AVOID IN UTILITIES:
- Business logic or multi-step workflows
- Complex LLM reasoning or prompt construction
- State management (use SharedStore in nodes)
- Flow control or branching logic
"""

from typing import Any, Dict, List, Optional, Tuple, Union


async def http_client(
    url: str, method: Optional[str] = None, headers: Optional[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Make HTTP requests to external APIs

GUIDANCE: For API utilities, provide clean service interfaces.
- Focus on request/response handling
- Keep authentication and retry logic simple
- Avoid business logic or complex response processing
    """

    # Framework guidance: Keep this function focused and transparent
    # EXAMPLE: Simple async HTTP request
    # import httpx
    # async with httpx.AsyncClient() as client:
    #     response = await client.get(url)
    #     return response.json()
    # TODO: Implement http_client
    # 
    # FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow
    # framework provides templates and structure, but YOU implement the specific
    # business logic for your use case.
    #
    # Why? This ensures maximum flexibility and prevents vendor lock-in.
    # 
    # Next Steps:
    # 1. Review docs/design.md for your specific requirements
    # 2. Follow PocketFlow utility patterns: simple, focused functions
    # 3. See ~/.agent-os/standards/best-practices.md for patterns
    raise NotImplementedError("Utility function http_client not implemented")


if __name__ == "__main__":
    # Test http_client function
    import asyncio
    # asyncio.run(http_client())
    pass