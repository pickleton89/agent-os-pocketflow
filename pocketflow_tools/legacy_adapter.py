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

    # Phase 1: override specific generation steps with new module functions
    def override_generate_utility(self, fn):
        # Bind a new method to the legacy instance that delegates to fn(utility)
        def _gen_utility(self_obj, utility):
            return fn(utility)

        self._impl._generate_utility = _gen_utility.__get__(self._impl, self._impl.__class__)

    def override_fastapi_generators(self, main_fn, router_fn):
        # Override _generate_fastapi_main
        def _gen_main(self_obj, spec):
            return main_fn(spec)

        # Override _generate_fastapi_router
        def _gen_router(self_obj, spec):
            return router_fn(spec)

        self._impl._generate_fastapi_main = _gen_main.__get__(self._impl, self._impl.__class__)
        self._impl._generate_fastapi_router = _gen_router.__get__(self._impl, self._impl.__class__)

    def override_config_generators(self, dep_files_fn, basic_dep_cfg_fn, basic_py_fn, readme_fn):
        def _gen_dep_files(self_obj, spec):
            return dep_files_fn(spec)

        def _gen_basic_dep_cfg(self_obj, pattern: str):
            return basic_dep_cfg_fn(pattern)

        def _gen_basic_py(self_obj, spec):
            return basic_py_fn(spec)

        def _gen_readme(self_obj, spec, config):
            return readme_fn(spec, config)

        self._impl._generate_dependency_files = _gen_dep_files.__get__(self._impl, self._impl.__class__)
        self._impl._generate_basic_dependency_config = _gen_basic_dep_cfg.__get__(self._impl, self._impl.__class__)
        self._impl._generate_basic_pyproject = _gen_basic_py.__get__(self._impl, self._impl.__class__)
        self._impl._generate_readme = _gen_readme.__get__(self._impl, self._impl.__class__)

    # Phase 1: override core code generation functions
    def override_core_code_generators(self, models_fn, nodes_fn, flow_fn):
        def _gen_models(self_obj, spec):
            return models_fn(spec)

        def _gen_nodes(self_obj, spec):
            return nodes_fn(spec)

        def _gen_flow(self_obj, spec):
            return flow_fn(spec)

        self._impl._generate_pydantic_models = _gen_models.__get__(self._impl, self._impl.__class__)
        self._impl._generate_nodes = _gen_nodes.__get__(self._impl, self._impl.__class__)
        self._impl._generate_flow = _gen_flow.__get__(self._impl, self._impl.__class__)

    # Phase 1: override documentation generators
    def override_doc_generators(self, design_fn, tasks_fn):
        def _gen_design(self_obj, spec):
            return design_fn(spec)

        def _gen_tasks(self_obj, spec):
            return tasks_fn(spec)

        self._impl._generate_design_doc = _gen_design.__get__(self._impl, self._impl.__class__)
        self._impl._generate_tasks = _gen_tasks.__get__(self._impl, self._impl.__class__)

    # Phase 1: share context for future use (optional)
    def set_generation_context(self, context) -> None:  # type: ignore[no-untyped-def]
        # Attach context to the legacy instance for visibility; no behavior change
        setattr(self._impl, "_generation_context", context)

    # Phase 1: override test generators
    def override_test_generators(self, node_tests_fn, flow_tests_fn, api_tests_fn):
        def _gen_node_tests(self_obj, spec):
            return node_tests_fn(spec)

        def _gen_flow_tests(self_obj, spec):
            return flow_tests_fn(spec)

        def _gen_api_tests(self_obj, spec):
            return api_tests_fn(spec)

        self._impl._generate_node_tests = _gen_node_tests.__get__(self._impl, self._impl.__class__)
        self._impl._generate_flow_tests = _gen_flow_tests.__get__(self._impl, self._impl.__class__)
        self._impl._generate_api_tests = _gen_api_tests.__get__(self._impl, self._impl.__class__)

    # Phase 1: override init file generator
    def override_init_generator(self, init_fn):
        def _gen_init(self_obj, spec, is_root=False, is_test=False, is_schema=False, is_utils=False):
            return init_fn(spec, is_root=is_root, is_test=is_test, is_schema=is_schema, is_utils=is_utils)

        self._impl._generate_init_file = _gen_init.__get__(self._impl, self._impl.__class__)

    # Phase 1: override misc generators (install checker)
    def override_install_checker(self, install_checker_fn):
        def _gen_install_checker(self_obj):
            return install_checker_fn()

        self._impl._generate_install_checker_reference = _gen_install_checker.__get__(self._impl, self._impl.__class__)
