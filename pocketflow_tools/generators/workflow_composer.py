from pathlib import Path
from typing import Dict

from pocketflow_tools.spec import WorkflowSpec
from pocketflow_tools.generators.template_engine import TemplateEngine
from pocketflow_tools.generators.code_generators import (
    generate_utility,
    generate_pydantic_models,
    generate_nodes,
    generate_flow,
    generate_init_file,
    generate_install_checker_reference,
    generate_fastapi_main,
    generate_fastapi_router,
)
from pocketflow_tools.generators.doc_generators import (
    generate_design_doc,
    generate_tasks,
)
from pocketflow_tools.generators.test_generators import (
    generate_node_tests,
    generate_flow_tests,
    generate_api_tests,
)
from pocketflow_tools.generators.config_generators import (
    generate_dependency_files,
    generate_basic_dependency_config,
    generate_basic_pyproject,
    generate_readme,
)
from pocketflow_tools.generators.context import GenerationContext


class PocketFlowGenerator:
    """Compose and generate PocketFlow workflows.

    Complete modular implementation using all new generator functions.
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

        # Ensure output directory exists 
        self.output_path.mkdir(exist_ok=True, parents=True)

        # Load templates and extensions via new TemplateEngine
        # Create fallback empty context if templates directory doesn't exist
        try:
            engine = TemplateEngine(self.templates_path)
            templates = engine.load_templates()
            extensions = engine.load_enhanced_extensions()
        except (FileNotFoundError, OSError):
            # Fallback to empty templates/extensions if directory missing
            templates = {}
            extensions = {}
        
        # Build generation context for sharing across generation steps
        self.context = GenerationContext(
            templates=templates,
            extensions=extensions,
            enable_hybrid_promotion=self.enable_hybrid_promotion,
        )

    def generate_workflow(self, spec: WorkflowSpec) -> Dict[str, str]:
        """Generate all workflow files using the new modular generators."""
        output_files = {}
        
        # Generate core code files - these return strings, need to map to filenames
        output_files["schemas/models.py"] = generate_pydantic_models(spec)
        output_files["nodes.py"] = generate_nodes(spec) 
        output_files["flow.py"] = generate_flow(spec)
        output_files["__init__.py"] = generate_init_file(spec, is_root=True)
        output_files["schemas/__init__.py"] = generate_init_file(spec, is_schema=True)
        output_files["tests/__init__.py"] = generate_init_file(spec, is_test=True)
        output_files["utils/__init__.py"] = generate_init_file(spec, is_utils=True)
        
        # Generate utilities - need to pass individual utilities from spec
        for utility in spec.utilities:
            utility_content = generate_utility(utility)
            utility_name = utility.get('name', 'utility').lower()
            output_files[f"utils/{utility_name}.py"] = utility_content
        
        # Generate FastAPI components  
        output_files["main.py"] = generate_fastapi_main(spec)
        output_files["router.py"] = generate_fastapi_router(spec)
        
        # Generate configuration files - this returns a Dict[str, str] including README.md
        output_files.update(generate_dependency_files(spec))
        
        output_files["pyproject.toml"] = generate_basic_pyproject(spec)
        
        # Generate documentation
        output_files["docs/design.md"] = generate_design_doc(spec)
        output_files["docs/tasks.md"] = generate_tasks(spec)
        
        # Generate tests
        output_files["tests/test_nodes.py"] = generate_node_tests(spec)
        output_files["tests/test_flow.py"] = generate_flow_tests(spec)
        output_files["tests/test_api.py"] = generate_api_tests(spec)
        
        # Generate install checker reference - no parameters
        output_files["check_install.py"] = generate_install_checker_reference()
        
        return output_files

    def save_workflow(self, spec: WorkflowSpec, output_files: Dict[str, str]) -> None:
        """Save generated workflow files to disk."""
        # Safely sanitize workflow directory name
        import re
        safe_name = re.sub(r'[^a-zA-Z0-9]', '', spec.name.lower())
        if not safe_name:  # Fallback if name becomes empty after sanitization
            safe_name = "workflow"
            
        workflow_dir = self.output_path / safe_name
        workflow_dir.mkdir(parents=True, exist_ok=True)
        
        for relative_path, content in output_files.items():
            file_path = workflow_dir / relative_path
            # Ensure we don't create files outside the workflow directory
            if not str(file_path).startswith(str(workflow_dir)):
                continue  # Skip potentially dangerous paths
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding='utf-8')

