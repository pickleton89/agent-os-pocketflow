"""Temporary adapter to the legacy monolithic generator.

This allows the new CLI and import surface to function during Phase 1
while we split the legacy implementation into modular components.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Dict

from pocketflow_tools.spec import WorkflowSpec


def _load_legacy_generator_module():
    """Dynamically load the legacy generator module from file path."""
    root = Path(__file__).resolve().parent.parent
    tools_dir = root / "pocketflow-tools"
    legacy_path = tools_dir / "generator.py"
    if not legacy_path.exists():
        raise FileNotFoundError(f"Legacy generator not found at {legacy_path}")

    # Ensure the tools directory is importable for legacy absolute imports
    import sys
    tools_dir_str = str(tools_dir)
    if tools_dir_str not in sys.path:
        sys.path.insert(0, tools_dir_str)

    spec = importlib.util.spec_from_file_location("legacy_generator", str(legacy_path))
    if spec is None or spec.loader is None:
        raise ImportError("Unable to load legacy generator module spec")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[misc]
    return module


class LegacyGeneratorAdapter:
    """Adapter delegating calls to the legacy PocketFlowGenerator class."""

    def __init__(
        self,
        templates_path: str,
        output_path: str,
        enable_hybrid_promotion: bool,
    ) -> None:
        legacy_module = _load_legacy_generator_module()
        LegacyPFGenerator = getattr(legacy_module, "PocketFlowGenerator")
        self._impl = LegacyPFGenerator(
            templates_path=templates_path,
            output_path=output_path,
            enable_hybrid_promotion=enable_hybrid_promotion,
        )

    def generate_workflow(self, spec: WorkflowSpec) -> Dict[str, str]:
        return self._impl.generate_workflow(spec)

    def save_workflow(self, spec: WorkflowSpec, output_files: Dict[str, str]) -> None:
        self._impl.save_workflow(spec, output_files)

    # Phase 1: allow preloading templates/extensions computed by new modules
    def set_templates_extensions(self, templates: Dict[str, str], extensions: Dict[str, Dict]):
        if hasattr(self._impl, "templates"):
            self._impl.templates = templates
        if hasattr(self._impl, "extensions"):
            self._impl.extensions = extensions
