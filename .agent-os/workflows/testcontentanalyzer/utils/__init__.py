"""
Utility functions for TestContentAnalyzer workflow.
"""

# Import all utility functions
from pathlib import Path
import importlib

_utils_dir = Path(__file__).parent
for util_file in _utils_dir.glob("*.py"):
    if util_file.name not in ["__init__.py"]:
        module_name = util_file.stem
        try:
            importlib.import_module(f".{module_name}", package=__name__)
        except ImportError:
            pass  # Skip utility files with missing dependencies
