from pocketflow import Flow
from .nodes import ValidateTask, ProcessTask, FormatResponse
import logging

logger = logging.getLogger(__name__)


class TaskManagerFlow(Flow):
    """
    Simple CRUD application for managing tasks
    """

    def __init__(self):
        nodes = {
            "validatetask": ValidateTask(),
            "processtask": ProcessTask(),
            "formatresponse": FormatResponse(),
        }

        edges = {
            "validatetask": {"success": "processtask", "error": "error_handler"},
            "processtask": {"success": "formatresponse", "error": "error_handler"},
            "formatresponse": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

