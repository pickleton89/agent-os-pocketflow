from pocketflow import Flow
from .nodes import InputValidator, BusinessLogicProcessor, OutputFormatter
import logging

logger = logging.getLogger(__name__)


class BaselineWORKFLOWWorkflowFlow(Flow):
    """
    Baseline generation snapshot for WORKFLOW pattern
    """

    def __init__(self):
        # TODO: Customize node instances and their configurations
        nodes = {
            "inputvalidator": InputValidator(),
            "businesslogicprocessor": BusinessLogicProcessor(),
            "outputformatter": OutputFormatter(),
        }

        # TODO: Customize workflow connections and error handling
        edges = {
            "inputvalidator": {"success": "businesslogicprocessor", "error": "error_handler"},
            "businesslogicprocessor": {"success": "outputformatter", "error": "error_handler"},
            "outputformatter": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

