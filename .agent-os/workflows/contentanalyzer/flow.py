from pocketflow import Flow
from .nodes import DocumentRetrieverNode, ContextBuilderNode, LLMAnalyzerNode, ResponseFormatterNode
import logging

logger = logging.getLogger(__name__)


class ContentAnalyzerFlow(Flow):
    """
    Analyze content using document retrieval and LLM processing
    """

    def __init__(self):
        nodes = {
            "documentretrievernode": DocumentRetrieverNode(),
            "contextbuildernode": ContextBuilderNode(),
            "llmanalyzernode": LLMAnalyzerNode(),
            "responseformatternode": ResponseFormatterNode(),
        }

        edges = {
            "documentretrievernode": {"success": "contextbuildernode", "error": "error_handler"},
            "contextbuildernode": {"success": "llmanalyzernode", "error": "error_handler"},
            "llmanalyzernode": {"success": "responseformatternode", "error": "error_handler"},
            "responseformatternode": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

