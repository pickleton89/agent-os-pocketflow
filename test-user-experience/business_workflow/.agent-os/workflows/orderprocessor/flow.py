from pocketflow import Flow
from .nodes import OrderValidator, InventoryChecker, PaymentProcessor, ShippingCoordinator
import logging

logger = logging.getLogger(__name__)


class OrderProcessorFlow(Flow):
    """
    Complex business workflow for e-commerce orders
    """

    def __init__(self):
        nodes = {
            "ordervalidator": OrderValidator(),
            "inventorychecker": InventoryChecker(),
            "paymentprocessor": PaymentProcessor(),
            "shippingcoordinator": ShippingCoordinator(),
        }

        edges = {
            "ordervalidator": {"success": "inventorychecker", "error": "error_handler"},
            "inventorychecker": {"success": "paymentprocessor", "error": "error_handler"},
            "paymentprocessor": {"success": "shippingcoordinator", "error": "error_handler"},
            "shippingcoordinator": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

