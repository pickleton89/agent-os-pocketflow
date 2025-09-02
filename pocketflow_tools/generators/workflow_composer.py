from pathlib import Path
from typing import Dict

from pocketflow_tools.spec import WorkflowSpec
from pocketflow_tools.generators.template_engine import TemplateEngine


class PocketFlowGenerator:
    """Compose and generate PocketFlow workflows.

    Phase 1 implementation temporarily delegates to the legacy generator to
    preserve behavior and outputs while we complete the modular split.
    """

    def __init__(
        self,
        templates_path: str = "templates",
        output_path: str = ".agent-os/workflows",
        enable_hybrid_promotion: bool = False,
    ) -> None:
        self.templates_path = Path(templates_path)
        self.output_path = Path(output_path)
        self.enable_hybrid_promotion = enable_hybrid_promotion

        # Ensure output directory exists (match legacy behavior)
        self.output_path.mkdir(exist_ok=True, parents=True)

        # Defer heavy lifting to legacy class for now
        from pocketflow_tools.legacy_adapter import LegacyGeneratorAdapter

        self._adapter = LegacyGeneratorAdapter(
            templates_path=str(self.templates_path),
            output_path=str(self.output_path),
            enable_hybrid_promotion=self.enable_hybrid_promotion,
        )

        # Phase 1: preload templates and extensions via new TemplateEngine (parity)
        try:
            engine = TemplateEngine(self.templates_path)
            templates = engine.load_templates()
            extensions = engine.load_enhanced_extensions()
            self._adapter.set_templates_extensions(templates, extensions)
        except Exception:
            # Non-fatal: legacy adapter already loaded these internally
            pass

    def generate_workflow(self, spec: WorkflowSpec) -> Dict[str, str]:
        return self._adapter.generate_workflow(spec)

    def save_workflow(self, spec: WorkflowSpec, output_files: Dict[str, str]) -> None:
        self._adapter.save_workflow(spec, output_files)


# Internal temporary adapter to the legacy implementation.
# This exists only during Phase 1 of the refactor to maintain parity.
class LegacyGeneratorAdapter:
    def __init__(
        self,
        templates_path: str,
        output_path: str,
        enable_hybrid_promotion: bool,
    ) -> None:
        # Import inside to avoid hard coupling at import time
        from pocketflow_tools.legacy_adapter import LegacyGeneratorAdapter as Impl

        self._impl = Impl(
            templates_path=templates_path,
            output_path=output_path,
            enable_hybrid_promotion=enable_hybrid_promotion,
        )

    def generate_workflow(self, spec: WorkflowSpec) -> Dict[str, str]:
        return self._impl.generate_workflow(spec)

    def save_workflow(self, spec: WorkflowSpec, output_files: Dict[str, str]) -> None:
        self._impl.save_workflow(spec, output_files)
