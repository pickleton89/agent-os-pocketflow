from pocketflow import Flow
from .nodes import DocumentLoader, TextChunker, EmbeddingGenerator, QueryProcessor, Retriever, ContextFormatter, ResponseGenerator
import logging

logger = logging.getLogger(__name__)


class BaselineRAGWorkflowFlow(Flow):
    """
    Baseline generation snapshot for RAG pattern
    """

    def __init__(self):
        # TODO: Customize node instances and their configurations
        # 
        # FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Configure node parameters based on your domain needs
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        nodes = {
            "documentloader": DocumentLoader(),
            "textchunker": TextChunker(),
            "embeddinggenerator": EmbeddingGenerator(),
            "queryprocessor": QueryProcessor(),
            "retriever": Retriever(),
            "contextformatter": ContextFormatter(),
            "responsegenerator": ResponseGenerator(),
        }

        # TODO: Customize workflow connections and error handling
        # 
        # FRAMEWORK GUIDANCE: This TODO is intentional. The Agent OS + PocketFlow
        # framework provides templates and structure, but YOU implement the specific
        # business logic for your use case.
        #
        # Why? This ensures maximum flexibility and prevents vendor lock-in.
        # 
        # Next Steps:
        # 1. Review docs/design.md for your specific requirements
        # 2. Follow PocketFlow flow lifecycle: init() → run_async() → cleanup()
        # 3. See ~/.agent-os/standards/best-practices.md for patterns
        edges = {
            "documentloader": {"success": "textchunker", "error": "error_handler"},
            "textchunker": {"success": "embeddinggenerator", "error": "error_handler"},
            "embeddinggenerator": {"success": "queryprocessor", "error": "error_handler"},
            "queryprocessor": {"success": "retriever", "error": "error_handler"},
            "retriever": {"success": "contextformatter", "error": "error_handler"},
            "contextformatter": {"success": "responsegenerator", "error": "error_handler"},
            "responsegenerator": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

