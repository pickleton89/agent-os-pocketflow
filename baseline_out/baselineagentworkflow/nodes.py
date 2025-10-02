from pocketflow import Node, AsyncNode, BatchNode
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class TaskAnalyzer(AsyncNode):
    """
    Analyze incoming tasks and requirements
    """

    def prep(self, shared: Dict[str, Any]) -> Any:
        """
        Data preparation and validation.
        
        BEST PRACTICE: Only read from shared store here.
        DO NOT: Perform computation or external calls.
        DO NOT: Access databases, APIs, or call LLMs.
        
        This method should be fast, synchronous, and focused on
        extracting the exact data needed for exec().
        """
        logger.info(f"Preparing data for TaskAnalyzer")

        # Framework guidance: Read only what exec() needs from shared store
        # TODO: Extract the exact data exec() needs from shared store
        # TODO: Consider input validation if needed (but keep it lightweight)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        return shared.get("content", "")

    async def exec_async(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing TaskAnalyzer")

        # Framework guidance: Process prep_result, avoid shared store access
        # TODO: Implement the core processing logic using only prep_result
        # TODO: Return the processed result (avoid side effects here)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        analysis = await analyze_content(prep_result)
        return analysis

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for TaskAnalyzer")

        # Framework guidance: Store exec_result in shared store, return flow signal
        # TODO: Store exec_result in shared store with appropriate key
        # TODO: Return flow signal for branching ('success', 'error', specific state)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        shared["analysis_result"] = exec_result
        return "success"


class ReasoningEngine(AsyncNode):
    """
    Apply reasoning and decision-making logic
    """

    def prep(self, shared: Dict[str, Any]) -> Any:
        """
        Data preparation and validation.
        
        BEST PRACTICE: Only read from shared store here.
        DO NOT: Perform computation or external calls.
        DO NOT: Access databases, APIs, or call LLMs.
        
        This method should be fast, synchronous, and focused on
        extracting the exact data needed for exec().
        """
        logger.info(f"Preparing data for ReasoningEngine")

        # Framework guidance: Read only what exec() needs from shared store
        # TODO: Extract the exact data exec() needs from shared store
        # TODO: Consider input validation if needed (but keep it lightweight)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        return shared.get("input_data")

    async def exec_async(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing ReasoningEngine")

        # Framework guidance: Process prep_result, avoid shared store access
        # TODO: Implement the core processing logic using only prep_result
        # TODO: Return the processed result (avoid side effects here)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        # Implement your core logic here
        return "success"

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for ReasoningEngine")

        # Framework guidance: Store exec_result in shared store, return flow signal
        # TODO: Store exec_result in shared store with appropriate key
        # TODO: Return flow signal for branching ('success', 'error', specific state)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        shared["output_data"] = exec_result
        return "success"


class ActionPlanner(AsyncNode):
    """
    Plan sequence of actions to accomplish task
    """

    def prep(self, shared: Dict[str, Any]) -> Any:
        """
        Data preparation and validation.
        
        BEST PRACTICE: Only read from shared store here.
        DO NOT: Perform computation or external calls.
        DO NOT: Access databases, APIs, or call LLMs.
        
        This method should be fast, synchronous, and focused on
        extracting the exact data needed for exec().
        """
        logger.info(f"Preparing data for ActionPlanner")

        # Framework guidance: Read only what exec() needs from shared store
        # TODO: Extract the exact data exec() needs from shared store
        # TODO: Consider input validation if needed (but keep it lightweight)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        return shared.get("input_data")

    async def exec_async(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing ActionPlanner")

        # Framework guidance: Process prep_result, avoid shared store access
        # TODO: Implement the core processing logic using only prep_result
        # TODO: Return the processed result (avoid side effects here)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        # Implement your core logic here
        return "success"

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for ActionPlanner")

        # Framework guidance: Store exec_result in shared store, return flow signal
        # TODO: Store exec_result in shared store with appropriate key
        # TODO: Return flow signal for branching ('success', 'error', specific state)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        shared["output_data"] = exec_result
        return "success"


class ActionExecutor(AsyncNode):
    """
    Execute planned actions and tools
    """

    def prep(self, shared: Dict[str, Any]) -> Any:
        """
        Data preparation and validation.
        
        BEST PRACTICE: Only read from shared store here.
        DO NOT: Perform computation or external calls.
        DO NOT: Access databases, APIs, or call LLMs.
        
        This method should be fast, synchronous, and focused on
        extracting the exact data needed for exec().
        """
        logger.info(f"Preparing data for ActionExecutor")

        # Framework guidance: Read only what exec() needs from shared store
        # TODO: Extract the exact data exec() needs from shared store
        # TODO: Consider input validation if needed (but keep it lightweight)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        return shared.get("input_data")

    async def exec_async(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing ActionExecutor")

        # Framework guidance: Process prep_result, avoid shared store access
        # TODO: Implement the core processing logic using only prep_result
        # TODO: Return the processed result (avoid side effects here)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        # Implement your core logic here
        return "success"

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for ActionExecutor")

        # Framework guidance: Store exec_result in shared store, return flow signal
        # TODO: Store exec_result in shared store with appropriate key
        # TODO: Return flow signal for branching ('success', 'error', specific state)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        shared["output_data"] = exec_result
        return "success"


class ResultEvaluator(Node):
    """
    Evaluate results and determine next steps
    """

    def prep(self, shared: Dict[str, Any]) -> Any:
        """
        Data preparation and validation.
        
        BEST PRACTICE: Only read from shared store here.
        DO NOT: Perform computation or external calls.
        DO NOT: Access databases, APIs, or call LLMs.
        
        This method should be fast, synchronous, and focused on
        extracting the exact data needed for exec().
        """
        logger.info(f"Preparing data for ResultEvaluator")

        # Framework guidance: Read only what exec() needs from shared store
        # TODO: Extract the exact data exec() needs from shared store
        # TODO: Consider input validation if needed (but keep it lightweight)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        return shared.get("input_data")

    def exec(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing ResultEvaluator")

        # Framework guidance: Process prep_result, avoid shared store access
        # TODO: Implement the core processing logic using only prep_result
        # TODO: Return the processed result (avoid side effects here)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        # Implement your core logic here
        return "success"

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for ResultEvaluator")

        # Framework guidance: Store exec_result in shared store, return flow signal
        # TODO: Store exec_result in shared store with appropriate key
        # TODO: Return flow signal for branching ('success', 'error', specific state)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        shared["output_data"] = exec_result
        return "success"


class MemoryUpdater(Node):
    """
    Update agent memory with new information
    """

    def prep(self, shared: Dict[str, Any]) -> Any:
        """
        Data preparation and validation.
        
        BEST PRACTICE: Only read from shared store here.
        DO NOT: Perform computation or external calls.
        DO NOT: Access databases, APIs, or call LLMs.
        
        This method should be fast, synchronous, and focused on
        extracting the exact data needed for exec().
        """
        logger.info(f"Preparing data for MemoryUpdater")

        # Framework guidance: Read only what exec() needs from shared store
        # TODO: Extract the exact data exec() needs from shared store
        # TODO: Consider input validation if needed (but keep it lightweight)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        return shared.get("input_data")

    def exec(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing MemoryUpdater")

        # Framework guidance: Process prep_result, avoid shared store access
        # TODO: Implement the core processing logic using only prep_result
        # TODO: Return the processed result (avoid side effects here)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        # Implement your core logic here
        return "success"

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for MemoryUpdater")

        # Framework guidance: Store exec_result in shared store, return flow signal
        # TODO: Store exec_result in shared store with appropriate key
        # TODO: Return flow signal for branching ('success', 'error', specific state)
        # 
        # FRAMEWORK GUIDANCE: These TODOs are intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow node lifecycle: prep() → exec() → post()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        shared["output_data"] = exec_result
        return "success"

