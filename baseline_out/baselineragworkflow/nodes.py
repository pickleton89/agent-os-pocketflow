from pocketflow import Node, AsyncNode, BatchNode
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DocumentLoader(Node):
    """
    Load and preprocess documents for indexing
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
        logger.info(f"Preparing data for DocumentLoader")

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
        return shared.get("file_path", "")

    def exec(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing DocumentLoader")

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
        with open(prep_result, "r") as f:
            content = f.read()
        return content

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for DocumentLoader")

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
        shared["loaded_content"] = exec_result
        return "success"


class TextChunker(Node):
    """
    Split documents into manageable chunks
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
        logger.info(f"Preparing data for TextChunker")

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
        logger.info(f"Executing TextChunker")

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
        logger.info(f"Post-processing for TextChunker")

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


class EmbeddingGenerator(AsyncNode):
    """
    Generate embeddings for text chunks
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
        logger.info(f"Preparing data for EmbeddingGenerator")

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
        return shared.get("text", "")

    async def exec_async(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing EmbeddingGenerator")

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
        embedding = await get_embedding(prep_result)
        return embedding

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for EmbeddingGenerator")

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
        shared["embeddings"] = exec_result
        return "success"


class QueryProcessor(Node):
    """
    Process and analyze incoming queries
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
        logger.info(f"Preparing data for QueryProcessor")

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
        logger.info(f"Executing QueryProcessor")

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
        logger.info(f"Post-processing for QueryProcessor")

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


class Retriever(AsyncNode):
    """
    Retrieve relevant documents based on query
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
        logger.info(f"Preparing data for Retriever")

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
        return shared.get("query", "")

    async def exec_async(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing Retriever")

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
        search_results = await search_documents(prep_result)
        return search_results

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for Retriever")

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
        shared["retrieved_docs"] = exec_result
        return "success"


class ContextFormatter(Node):
    """
    Format retrieved context for response generation
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
        logger.info(f"Preparing data for ContextFormatter")

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
        return shared.get("raw_data", "")

    def exec(self, prep_result: Any) -> str:
        """
        Core processing logic.
        
        BEST PRACTICE: Use only prep_result as input.
        DO NOT: Access shared store directly.
        DO NOT: Use try/except for flow control.
        
        Let exceptions bubble up for PocketFlow retry handling.
        Use return values and post() for business logic branching.
        """
        logger.info(f"Executing ContextFormatter")

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
        formatted_data = format_response(prep_result)
        return formatted_data

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> Optional[str]:
        """
        Post-processing and result storage.
        
        BEST PRACTICE: Store results in shared store and return flow signals.
        DO NOT: Perform heavy computation here.
        DO NOT: Call external APIs or services.
        
        Use return values to signal flow branching (e.g., "success", "retry", "error").
        Keep this method fast and focused on data storage and routing.
        """
        logger.info(f"Post-processing for ContextFormatter")

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
        shared["formatted_output"] = exec_result
        return "success"


class ResponseGenerator(AsyncNode):
    """
    Generate response using retrieved context
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
        logger.info(f"Preparing data for ResponseGenerator")

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
        logger.info(f"Executing ResponseGenerator")

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
        logger.info(f"Post-processing for ResponseGenerator")

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

