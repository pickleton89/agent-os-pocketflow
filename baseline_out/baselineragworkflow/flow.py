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

