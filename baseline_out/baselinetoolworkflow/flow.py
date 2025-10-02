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
            "requestvalidator": RequestValidator(),
            "authhandler": AuthHandler(),
            "externalconnector": ExternalConnector(),
            "datatransformer": DataTransformer(),
            "responseprocessor": ResponseProcessor(),
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
            "requestvalidator": {"success": "authhandler", "error": "error_handler"},
            "authhandler": {"success": "externalconnector", "error": "error_handler"},
            "externalconnector": {"success": "datatransformer", "error": "error_handler"},
            "datatransformer": {"success": "responseprocessor", "error": "error_handler"},
            "responseprocessor": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

