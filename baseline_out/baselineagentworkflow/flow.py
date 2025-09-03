from pocketflow import Flow
from .nodes import TaskAnalyzer, ReasoningEngine, ActionPlanner, ActionExecutor, ResultEvaluator, MemoryUpdater
import logging

logger = logging.getLogger(__name__)


class BaselineAGENTWorkflowFlow(Flow):
    """
    Baseline generation snapshot for AGENT pattern
    """

    def __init__(self):
        # TODO: Customize node instances and their configurations
        nodes = {
            "taskanalyzer": TaskAnalyzer(),
            "reasoningengine": ReasoningEngine(),
            "actionplanner": ActionPlanner(),
            "actionexecutor": ActionExecutor(),
            "resultevaluator": ResultEvaluator(),
            "memoryupdater": MemoryUpdater(),
        }

        # TODO: Customize workflow connections and error handling
        edges = {
            "taskanalyzer": {"success": "reasoningengine", "error": "error_handler"},
            "reasoningengine": {"success": "actionplanner", "error": "error_handler"},
            "actionplanner": {"success": "actionexecutor", "error": "error_handler"},
            "actionexecutor": {"success": "resultevaluator", "error": "error_handler"},
            "resultevaluator": {"success": "memoryupdater", "error": "error_handler"},
            "memoryupdater": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

