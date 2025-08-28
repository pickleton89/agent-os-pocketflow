from pocketflow import Flow
from .nodes import AuthValidator, UserManager, TokenHandler
import logging

logger = logging.getLogger(__name__)


class UserAuthServiceFlow(Flow):
    """
    REST API service for user management and authentication
    """

    def __init__(self):
        nodes = {
            "authvalidator": AuthValidator(),
            "usermanager": UserManager(),
            "tokenhandler": TokenHandler(),
        }

        edges = {
            "authvalidator": {"success": "usermanager", "error": "error_handler"},
            "usermanager": {"success": "tokenhandler", "error": "error_handler"},
            "tokenhandler": {"success": None, "error": "error_handler"},
        }

        super().__init__(nodes=nodes, edges=edges)

