"""
Split text into semantic chunks

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


def chunk_text(
    text: str, chunk_size: Optional[int] = None
) -> List[str]:
    """
    Split text into semantic chunks

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
    # TODO: Implement chunk_text
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
    raise NotImplementedError("Utility function chunk_text not implemented")


if __name__ == "__main__":
    # Test chunk_text function
    # chunk_text()
    pass