"""
Search vector database for similar embeddings

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


async def vector_search(
    query_embedding: List[float], top_k: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    Search vector database for similar embeddings

GUIDANCE: Keep this utility simple and focused.
- Perform one clear operation
- Avoid hidden complexity or side effects
- Let nodes coordinate multiple utility calls
    """

    # Framework guidance: Keep this function focused and transparent
    # IMPLEMENTATION GUIDANCE:
    # - Keep the logic simple and focused on one task
    # - Use clear variable names and minimal complexity
    # - Let exceptions bubble up for retry handling
    # TODO: Implement vector_search
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
    raise NotImplementedError("Utility function vector_search not implemented")


if __name__ == "__main__":
    # Test vector_search function
    import asyncio
    # asyncio.run(vector_search())
    pass