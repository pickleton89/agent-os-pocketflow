"""
Apply LLM-based reasoning to analyze problems

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


async def llm_reasoning(
    context: str, task: str
) -> str:
    """
    Apply LLM-based reasoning to analyze problems

GUIDANCE: For LLM utilities, keep prompts simple and transparent.
- Pass prompts as clear parameters, don't construct them internally
- Avoid complex reasoning chains or decision logic
- Let nodes handle prompt construction and result processing
    """

    # Framework guidance: Keep this function focused and transparent
    # EXAMPLE: Simple async LLM call pattern
    # from openai import AsyncOpenAI
    # client = AsyncOpenAI()
    # response = await client.chat.completions.create(
    #     model='gpt-4',
    #     messages=[{'role': 'user', 'content': prompt}]
    # )
    # return response.choices[0].message.content
    # TODO: Implement llm_reasoning
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
    raise NotImplementedError("Utility function llm_reasoning not implemented")


if __name__ == "__main__":
    # Test llm_reasoning function
    import asyncio
    # asyncio.run(llm_reasoning())
    pass