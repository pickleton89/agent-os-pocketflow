from pocketflow import Node, AsyncNode, BatchNode
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class RequestValidator(Node):
    """
    Validate incoming API requests
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
        logger.info(f"Preparing data for RequestValidator")

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
        return shared.get("input_data", "")

    def exec(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing RequestValidator")

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
        is_valid = validate_input(prep_result)
        return {"valid": is_valid, "data": prep_result}

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for RequestValidator")

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
        shared["validation_result"] = exec_result
        return "success" if exec_result.get("valid", True) else "validation_failed"


class AuthHandler(AsyncNode):
    """
    Handle authentication and authorization
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
        logger.info(f"Preparing data for AuthHandler")

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
        logger.info(f"Executing AuthHandler")

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
        logger.info(f"Post-processing for AuthHandler")

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


class ExternalConnector(AsyncNode):
    """
    Connect to external APIs and services
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
        logger.info(f"Preparing data for ExternalConnector")

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
        logger.info(f"Executing ExternalConnector")

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
        logger.info(f"Post-processing for ExternalConnector")

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


class DataTransformer(Node):
    """
    Transform data between formats
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
        logger.info(f"Preparing data for DataTransformer")

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
        return shared.get("input_data", "")

    def exec(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing DataTransformer")

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
        transformed = transform_data(prep_result)
        return transformed

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for DataTransformer")

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
        shared["transformed_data"] = exec_result
        return "success"


class ResponseProcessor(Node):
    """
    Process and format API responses
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
        logger.info(f"Preparing data for ResponseProcessor")

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
        logger.info(f"Executing ResponseProcessor")

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
        logger.info(f"Post-processing for ResponseProcessor")

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

