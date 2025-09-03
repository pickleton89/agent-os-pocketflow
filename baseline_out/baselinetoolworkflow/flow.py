from pocketflow import Flow
from .nodes import RequestValidator, AuthHandler, ExternalConnector, DataTransformer, ResponseProcessor
import logging

logger = logging.getLogger(__name__)


class BaselineTOOLWorkflowFlow(Flow):
    """
    Baseline generation snapshot for TOOL pattern
    """

    def __init__(self):
        # TODO: Customize node instances and their configurations
        nodes = {
            "requestvalidator": RequestValidator(),
            "authhandler": AuthHandler(),
            "externalconnector": ExternalConnector(),
            "datatransformer": DataTransformer(),
            "responseprocessor": ResponseProcessor(),
        }

        # TODO: Customize workflow connections and error handling
        edges = {
            "requestvalidator": {"success": "authhandler", "error": "error_handler"},
            "authhandler": {"success": "externalconnector", "error": "error_handler"},
            "externalconnector": {"success": "datatransformer", "error": "error_handler"},
            "datatransformer": {"success": "responseprocessor", "error": "error_handler"},
            "responseprocessor": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

