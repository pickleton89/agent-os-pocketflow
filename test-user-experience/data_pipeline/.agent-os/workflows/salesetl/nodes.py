from pocketflow import Node, AsyncNode, BatchNode
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class DataExtractor(AsyncNode):
    """
    Extract data from multiple sources
    """

    def prep(self, shared: Dict[str, Any]) -> Any:
        """Data preparation and validation."""
        logger.info(f"Preparing data for DataExtractor")
        # TODO: Customize this prep logic based on your needs
        return shared.get("input_data")

    async def exec_async(self, prep_result: Any) -> str:
        """Core processing logic."""
        logger.info(f"Executing DataExtractor")
        # TODO: Customize this exec logic based on your needs
        # Implement your core logic here
        return "success"

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None:
        """Post-processing and result storage."""
        logger.info(f"Post-processing for DataExtractor")
        # TODO: Customize this post logic based on your needs
        shared["output_data"] = exec_result


class DataTransformer(BatchNode):
    """
    Transform and clean data
    """
    # NOTE: BatchNode used for processing multiple items in parallel

    def prep(self, shared: Dict[str, Any]) -> Any:
        """Data preparation and validation."""
        logger.info(f"Preparing data for DataTransformer")
        # TODO: Customize this prep logic based on your needs
        return shared.get("input_data", "")

    def exec(self, prep_result: Any) -> str:
        """Core processing logic."""
        logger.info(f"Executing DataTransformer")
        # TODO: Customize this exec logic based on your needs
        transformed = transform_data(prep_result)
        return transformed

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None:
        """Post-processing and result storage."""
        logger.info(f"Post-processing for DataTransformer")
        # TODO: Customize this post logic based on your needs
        shared["transformed_data"] = exec_result


class DataLoader(AsyncNode):
    """
    Load into data warehouse
    """

    def prep(self, shared: Dict[str, Any]) -> Any:
        """Data preparation and validation."""
        logger.info(f"Preparing data for DataLoader")
        # TODO: Customize this prep logic based on your needs
        return shared.get("file_path", "")

    async def exec_async(self, prep_result: Any) -> str:
        """Core processing logic."""
        logger.info(f"Executing DataLoader")
        # TODO: Customize this exec logic based on your needs
        async with aiofiles.open(prep_result, "r") as f:
            content = await f.read()
        return content

    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None:
        """Post-processing and result storage."""
        logger.info(f"Post-processing for DataLoader")
        # TODO: Customize this post logic based on your needs
        shared["loaded_content"] = exec_result

