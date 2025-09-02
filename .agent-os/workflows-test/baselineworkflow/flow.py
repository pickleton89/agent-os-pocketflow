from pocketflow import Flow
from .nodes import 
import logging

logger = logging.getLogger(__name__)


class BaselineWorkflowFlow(Flow):
    """
    Test workflow
    """

    def __init__(self):
        nodes = {
        }

        edges = {
        }

        super().__init__(nodes=nodes, edges=edges)

