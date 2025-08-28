from pocketflow import Flow
from .nodes import DataExtractor, DataTransformer, DataLoader
import logging

logger = logging.getLogger(__name__)


class SalesETLFlow(Flow):
    """
    Data processing pipeline for sales analytics
    """

    def __init__(self):
        nodes = {
            "dataextractor": DataExtractor(),
            "datatransformer": DataTransformer(),
            "dataloader": DataLoader(),
        }

        edges = {
            "dataextractor": {"success": "datatransformer", "error": "error_handler"},
            "datatransformer": {"success": "dataloader", "error": "error_handler"},
            "dataloader": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

