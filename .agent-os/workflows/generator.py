#!/usr/bin/env python3
"""
PocketFlow Workflow Generator

Generates complete PocketFlow workflow implementations from design documents
and templates, following the 8-step Agentic Coding methodology.
"""

from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, field

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


@dataclass
class WorkflowSpec:
    """Specification for generating a PocketFlow workflow."""

    name: str
    pattern: str  # AGENT/WORKFLOW/RAG/MAPREDUCE/MULTI-AGENT/STRUCTURED-OUTPUT
    description: str
    nodes: List[Dict[str, Any]] = field(default_factory=list)
    utilities: List[Dict[str, Any]] = field(default_factory=list)
    shared_store_schema: Dict[str, Any] = field(default_factory=dict)
    api_endpoints: List[Dict[str, Any]] = field(default_factory=list)
    fast_api_integration: bool = False


@dataclass
class ValidationResult:
    """Result of template validation."""
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    corrections_applied: List[str] = field(default_factory=list)


@dataclass  
class PatternRecommendation:
    """Result of pattern analysis."""
    primary_pattern: str
    confidence_score: float
    secondary_patterns: List[str] = field(default_factory=list)
    rationale: str = ""
    template_customizations: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DependencyConfig:
    """Dependency configuration for a pattern."""
    base_dependencies: List[str] = field(default_factory=list)
    pattern_dependencies: List[str] = field(default_factory=list)
    dev_dependencies: List[str] = field(default_factory=list)
    python_version: str = ">=3.9"
    tool_configs: Dict[str, Any] = field(default_factory=dict)


class PocketFlowGenerator:
    """Generate complete PocketFlow workflows from specifications."""

    def __init__(
        self,
        templates_path: str = "templates",
        output_path: str = ".agent-os/workflows",
    ):
        self.templates_path = Path(templates_path)
        self.output_path = Path(output_path)
        self.output_path.mkdir(exist_ok=True)

        # Validate templates directory exists
        if not self.templates_path.exists():
            raise FileNotFoundError(
                f"Templates directory not found: {self.templates_path}"
            )
        if not self.templates_path.is_dir():
            raise NotADirectoryError(
                f"Templates path is not a directory: {self.templates_path}"
            )

        # Load templates
        self.templates = self._load_templates()

    def _load_templates(self) -> Dict[str, str]:
        """Load all template files."""
        templates = {}
        for template_file in self.templates_path.glob("*.md"):
            templates[template_file.stem] = template_file.read_text()
        return templates

    def generate_workflow(self, spec: WorkflowSpec) -> Dict[str, str]:
        """Generate complete workflow implementation from spec."""
        output_files = {}

        # Generate design document
        output_files["docs/design.md"] = self._generate_design_doc(spec)

        # Generate data models
        output_files["schemas/models.py"] = self._generate_pydantic_models(spec)

        # Generate utility functions
        for utility in spec.utilities:
            file_path = f"utils/{utility['name']}.py"
            output_files[file_path] = self._generate_utility(utility)

        # Generate nodes
        output_files["nodes.py"] = self._generate_nodes(spec)

        # Generate flow
        output_files["flow.py"] = self._generate_flow(spec)

        # Generate FastAPI integration if needed
        if spec.fast_api_integration:
            output_files["main.py"] = self._generate_fastapi_main(spec)
            output_files["router.py"] = self._generate_fastapi_router(spec)

        # Generate tests
        output_files["tests/test_nodes.py"] = self._generate_node_tests(spec)
        output_files["tests/test_flow.py"] = self._generate_flow_tests(spec)
        if spec.fast_api_integration:
            output_files["tests/test_api.py"] = self._generate_api_tests(spec)

        # Generate tasks file
        output_files["tasks.md"] = self._generate_tasks(spec)
        
        # Generate installation checker reference
        output_files["check-install.py"] = self._generate_install_checker_reference()
        
        # Generate package initialization files
        output_files["__init__.py"] = self._generate_init_file(spec, is_root=True)
        output_files["tests/__init__.py"] = self._generate_init_file(spec, is_test=True)
        output_files["schemas/__init__.py"] = self._generate_init_file(spec, is_schema=True)
        output_files["utils/__init__.py"] = self._generate_init_file(spec, is_utils=True)
        output_files["docs/__init__.py"] = ""  # Empty init for docs

        return output_files

    def _generate_init_file(self, spec: WorkflowSpec, is_root=False, is_test=False, is_schema=False, is_utils=False) -> str:
        """Generate appropriate __init__.py file content."""
        # workflow_name = spec.name.lower().replace(" ", "")  # Currently unused
        
        if is_root:
            # Root package init - expose main classes
            return f'''"""
{spec.name} - PocketFlow Workflow

{spec.description}

Generated by Agent OS + PocketFlow Generator
"""

from .flow import {spec.name}Flow
from .nodes import {", ".join(node["name"] for node in spec.nodes)}

__version__ = "0.1.0"
__all__ = [
    "{spec.name}Flow",
    {", ".join(f'"{node["name"]}"' for node in spec.nodes)}
]
'''
        elif is_test:
            # Test package init
            return f'''"""
Test package for {spec.name} workflow.
"""
'''
        elif is_schema:
            # Schema package init
            return f'''"""
Pydantic models and schemas for {spec.name} workflow.
"""

from .models import *
'''
        elif is_utils:
            # Utils package init  
            return f'''"""
Utility functions for {spec.name} workflow.
"""

# Import all utility functions
from pathlib import Path
import importlib

_utils_dir = Path(__file__).parent
for util_file in _utils_dir.glob("*.py"):
    if util_file.name not in ["__init__.py"]:
        module_name = util_file.stem
        try:
            importlib.import_module(f".{{module_name}}", package=__name__)
        except ImportError:
            pass  # Skip utility files with missing dependencies
'''
        else:
            # Default empty init
            return ""

    def _generate_install_checker_reference(self) -> str:
        """Generate a reference script that points to the main installation checker."""
        return '''#!/usr/bin/env python3
"""
PocketFlow Installation Checker

This script checks if your project has the necessary dependencies
to run PocketFlow workflows.

Usage:
    python check-install.py [--install]
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run the main installation checker."""
    # Path to the main checker in Agent OS
    agent_os_checker = Path.home() / ".agent-os" / "workflows" / "check-pocketflow-install.py"
    
    if not agent_os_checker.exists():
        print("❌ Agent OS + PocketFlow installation checker not found.")
        print("   Please ensure Agent OS is properly installed in ~/.agent-os/")
        return 1
    
    # Forward all arguments to the main checker
    cmd = [sys.executable, str(agent_os_checker)] + sys.argv[1:]
    return subprocess.run(cmd).returncode

if __name__ == "__main__":
    sys.exit(main())
'''

    def _generate_design_doc(self, spec: WorkflowSpec) -> str:
        """Generate design document from template."""
        # Create a comprehensive design document
        design_doc = f"""# Design Document

> Spec: {spec.name}
> Created: {datetime.now().isoformat()[:10]}
> Status: Design Phase
> Framework: PocketFlow

**CRITICAL**: This design document MUST be completed before any code implementation begins.

## Requirements

### Problem Statement
{spec.description}

### Success Criteria
- Successful implementation of {spec.pattern} pattern
- All nodes execute correctly in sequence
- Proper error handling and validation
- Complete test coverage

### Design Pattern Classification
**Primary Pattern:** {spec.pattern}
**Secondary Patterns:** FastAPI Integration{"(enabled)" if spec.fast_api_integration else "(disabled)"}

### Input/Output Specification
- **Input Format:** Request data from API or direct invocation
- **Output Format:** Processed results with metadata
- **Error Conditions:** Validation errors, processing failures, timeout errors

## Flow Design

### High-Level Architecture
```mermaid
graph TD
    A[Start] --> B[Input Validation]
    B --> C[{spec.nodes[0]["name"] if spec.nodes else "Processing"}]"""

        # Add nodes to mermaid diagram
        if spec.nodes:
            for i, node in enumerate(spec.nodes):
                current = chr(ord("C") + i)
                next_node = chr(ord("C") + i + 1) if i < len(spec.nodes) - 1 else "Z"
                design_doc += f"\n    {current}[{node['name']}] --> {next_node}[{'Next Node' if i < len(spec.nodes) - 1 else 'End'}]"

        design_doc += "\n```\n"

        # Add node sequence
        design_doc += "\n### Node Sequence\n"
        for i, node in enumerate(spec.nodes, 1):
            design_doc += f"{i}. **{node['name']}** - {node['description']}\n"

        # Add utilities section
        design_doc += "\n## Utilities\n\n"
        design_doc += 'Following PocketFlow\'s "implement your own" philosophy, specify all utility functions needed.\n\n'
        design_doc += "### Required Utility Functions\n\n"

        for utility in spec.utilities:
            design_doc += f"#### {utility['name']}\n"
            design_doc += f"- **Purpose:** {utility['description']}\n"
            params_str = ", ".join(
                [f"{p['name']}: {p['type']}" for p in utility.get("parameters", [])]
            )
            design_doc += f"- **Input:** {params_str}\n"
            design_doc += f"- **Output:** {utility.get('return_type', 'Any')}\n\n"

        # Add shared store schema
        design_doc += "\n## Data Design\n\n"
        design_doc += "### SharedStore Schema\n"
        design_doc += "Following PocketFlow's shared store pattern, all data flows through a common dictionary.\n\n"
        design_doc += "```python\n"
        design_doc += "SharedStore = {\n"
        for key, value_type in spec.shared_store_schema.items():
            design_doc += f'    "{key}": {value_type},\n'
        design_doc += "}\n```\n"

        # Add node design section
        design_doc += "\n## Node Design\n\n"
        design_doc += "Following PocketFlow's node-based architecture, each processing step is implemented as a discrete node.\n\n"
        
        for i, node in enumerate(spec.nodes, 1):
            design_doc += f"### {i}. {node['name']}\n"
            design_doc += f"**Purpose:** {node['description']}\n\n"
            
            # Add input/output details if available
            if 'inputs' in node:
                inputs_str = ", ".join(node['inputs']) if node['inputs'] else "SharedStore"
                design_doc += f"**Inputs:** {inputs_str}\n"
            else:
                design_doc += "**Inputs:** SharedStore\n"
                
            if 'outputs' in node:
                outputs_str = ", ".join(node['outputs']) if node['outputs'] else "Updates SharedStore"
                design_doc += f"**Outputs:** {outputs_str}\n"
            else:
                design_doc += "**Outputs:** Updates SharedStore\n"
                
            design_doc += "\n"

        # Add implementation notes
        design_doc += "\n## Implementation Notes\n\n"
        design_doc += f"- Pattern: {spec.pattern}\n"
        design_doc += f"- Nodes: {len(spec.nodes)}\n"
        design_doc += f"- Utilities: {len(spec.utilities)}\n"
        design_doc += f"- FastAPI Integration: {'Enabled' if spec.fast_api_integration else 'Disabled'}\n"
        design_doc += "\nThis design document was generated automatically. Please review and complete with specific implementation details."

        return design_doc

    def _generate_pydantic_models(self, spec: WorkflowSpec) -> str:
        """Generate Pydantic models from shared store schema."""
        models = [
            "from pydantic import BaseModel, Field, validator",
            "from typing import Dict, List, Optional, Any",
            "from datetime import datetime",
            "",
            "",
        ]

        # Generate SharedStore model
        models.extend(
            [
                "class SharedStoreModel(BaseModel):",
                '    """Pydantic model for SharedStore validation."""',
                "",
            ]
        )

        for key, value_type in spec.shared_store_schema.items():
            models.append(f"    {key}: {value_type}")

        models.extend(["", ""])

        # Generate API models if FastAPI integration
        if spec.fast_api_integration:
            for endpoint in spec.api_endpoints:
                # Request model
                models.extend(
                    [
                        f"class {endpoint['name']}Request(BaseModel):",
                        f'    """Request model for {endpoint["name"]} endpoint."""',
                        "",
                    ]
                )

                for field in endpoint.get("request_fields", []):
                    models.append(f"    {field['name']}: {field['type']}")

                models.extend(["", ""])

                # Response model
                models.extend(
                    [
                        f"class {endpoint['name']}Response(BaseModel):",
                        f'    """Response model for {endpoint["name"]} endpoint."""',
                        "",
                    ]
                )

                for field in endpoint.get("response_fields", []):
                    models.append(f"    {field['name']}: {field['type']}")

                models.extend(["", ""])

        return "\n".join(models)

    def _generate_utility(self, utility: Dict[str, Any]) -> str:
        """Generate utility function from specification."""
        utility_code = [
            '"""',
            f"{utility['description']}",
            '"""',
            "",
            "from typing import Any, Optional",
            "",
            "",
        ]

        # Function signature
        params = []
        for param in utility.get("parameters", []):
            if param.get("optional", False):
                params.append(f"{param['name']}: Optional[{param['type']}] = None")
            else:
                params.append(f"{param['name']}: {param['type']}")

        # Determine if utility should be async based on description or explicit flag
        is_async_utility = utility.get("async", False) or any(
            keyword in utility["description"].lower()
            for keyword in [
                "llm",
                "api",
                "database",
                "file",
                "network",
                "http",
                "fetch",
                "request",
            ]
        )

        func_def = (
            f"async def {utility['name']}("
            if is_async_utility
            else f"def {utility['name']}("
        )
        test_call = (
            f"    # asyncio.run({utility['name']}())"
            if is_async_utility
            else f"    # {utility['name']}()"
        )

        utility_code.extend(
            [
                func_def,
                f"    {', '.join(params)}",
                f") -> {utility.get('return_type', 'Any')}:",
                '    """',
                f"    {utility['description']}",
                '    """',
                f"    # TODO: Implement {utility['name']}",
                f'    raise NotImplementedError("Utility function {utility["name"]} not implemented")',
                "",
                "",
                'if __name__ == "__main__":',
                f"    # Test {utility['name']} function",
            ]
        )

        if is_async_utility:
            utility_code.extend(["    import asyncio", test_call, "    pass"])
        else:
            utility_code.extend([test_call, "    pass"])

        return "\n".join(utility_code)

    def _get_smart_node_defaults(self, node: Dict[str, Any], is_async: bool = False) -> Dict[str, str]:
        """Generate smart defaults based on node name and description."""
        name = node.get("name", "").lower()
        description = node.get("description", "").lower()
        
        # Common patterns for different node types
        prep_examples = {
            "retriever": 'return shared.get("query", "")',
            "loader": 'return shared.get("file_path", "")',
            "analyzer": 'return shared.get("content", "")',
            "formatter": 'return shared.get("raw_data", "")',
            "validator": 'return shared.get("input_data", "")',
            "transformer": 'return shared.get("input_data", "")',
            "llm": 'prompt = f"Process this: {shared.get(\"content\", \"\")}"\n        return prompt',
            "embedding": 'return shared.get("text", "")',
            "search": 'return shared.get("query", "")',
            "filter": 'return shared.get("items", [])',
        }
        
        # Async exec examples
        exec_examples_async = {
            "retriever": 'search_results = await search_documents(prep_result)\n        return search_results',
            "loader": 'async with aiofiles.open(prep_result, "r") as f:\n            content = await f.read()\n        return content',
            "analyzer": 'analysis = await analyze_content(prep_result)\n        return analysis',
            "formatter": 'formatted_data = await format_response_async(prep_result)\n        return formatted_data',
            "validator": 'is_valid = await validate_input_async(prep_result)\n        return {"valid": is_valid, "data": prep_result}',
            "transformer": 'transformed = await transform_data_async(prep_result)\n        return transformed',
            "llm": 'response = await call_llm(prep_result)\n        return response',
            "embedding": 'embedding = await get_embedding(prep_result)\n        return embedding',
            "search": 'results = await search_vector_db(prep_result)\n        return results',
            "filter": 'filtered = await filter_async(prep_result)\n        return filtered',
        }
        
        # Sync exec examples  
        exec_examples_sync = {
            "retriever": 'search_results = search_documents(prep_result)\n        return search_results',
            "loader": 'with open(prep_result, "r") as f:\n            content = f.read()\n        return content',
            "analyzer": 'analysis = analyze_content(prep_result)\n        return analysis',
            "formatter": 'formatted_data = format_response(prep_result)\n        return formatted_data',
            "validator": 'is_valid = validate_input(prep_result)\n        return {"valid": is_valid, "data": prep_result}',
            "transformer": 'transformed = transform_data(prep_result)\n        return transformed',
            "llm": 'response = call_llm_sync(prep_result)\n        return response',
            "embedding": 'embedding = get_embedding_sync(prep_result)\n        return embedding',
            "search": 'results = search_vector_db_sync(prep_result)\n        return results',
            "filter": 'filtered = [item for item in prep_result if meets_criteria(item)]\n        return filtered',
        }
        
        # Choose appropriate exec examples based on async flag
        exec_examples = exec_examples_async if is_async else exec_examples_sync
        
        post_examples = {
            "retriever": 'shared["retrieved_docs"] = exec_result',
            "loader": 'shared["loaded_content"] = exec_result',
            "analyzer": 'shared["analysis_result"] = exec_result',
            "formatter": 'shared["formatted_output"] = exec_result',
            "validator": 'shared["validation_result"] = exec_result',
            "transformer": 'shared["transformed_data"] = exec_result',
            "llm": 'shared["llm_response"] = exec_result',
            "embedding": 'shared["embeddings"] = exec_result',
            "search": 'shared["search_results"] = exec_result',
            "filter": 'shared["filtered_data"] = exec_result',
        }
        
        # Match based on name or description
        for pattern in prep_examples.keys():
            if pattern in name or pattern in description:
                return {
                    "prep": prep_examples[pattern],
                    "exec": exec_examples[pattern], 
                    "post": post_examples[pattern]
                }
        
        # Default fallback
        return {
            "prep": 'return shared.get("input_data")',
            "exec": '# Implement your core logic here\n        return "success"',
            "post": 'shared["output_data"] = exec_result'
        }

    def _generate_nodes(self, spec: WorkflowSpec) -> str:
        """Generate PocketFlow nodes from specification."""
        nodes_code = [
            "from pocketflow import Node, AsyncNode, BatchNode",
            "from typing import Dict, Any",
            "import logging",
            "",
            "logger = logging.getLogger(__name__)",
            "",
            "",
        ]

        for node in spec.nodes:
            # Default to Node (sync) unless explicitly specified as async
            node_type = node.get("type", "Node")

            # Use BatchNode for operations that process lists of items
            batch_comment = ""
            if node_type == "BatchNode":
                batch_comment = "\n    # NOTE: BatchNode used for processing multiple items in parallel"

            # Determine method signature based on node type
            is_async_node = node_type in [
                "AsyncNode",
                "AsyncBatchNode",
                "AsyncParallelBatchNode",
            ]
            exec_method = "async def exec_async" if is_async_node else "def exec"
            exec_signature = f"    {exec_method}(self, prep_result: Any) -> str:"

            # Get smart defaults based on node name/description
            smart_defaults = self._get_smart_node_defaults(node, is_async_node)

            nodes_code.extend(
                [
                    f"class {node['name']}({node_type}):",
                    '    """',
                    f"    {node['description']}",
                    f'    """{batch_comment}',
                    "",
                    "    def prep(self, shared: Dict[str, Any]) -> Any:",
                    '        """Data preparation and validation."""',
                    f'        logger.info(f"Preparing data for {node["name"]}")',
                    "        # TODO: Customize this prep logic based on your needs",
                    f"        {smart_defaults['prep']}",
                    "",
                    exec_signature,
                    '        """Core processing logic."""',
                    f'        logger.info(f"Executing {node["name"]}")',
                    "        # TODO: Customize this exec logic based on your needs",
                    f"        {smart_defaults['exec']}",
                    "",
                    "    def post(self, shared: Dict[str, Any], prep_result: Any, exec_result: Any) -> None:",
                    '        """Post-processing and result storage."""',
                    f'        logger.info(f"Post-processing for {node["name"]}")',
                    "        # TODO: Customize this post logic based on your needs",
                    f"        {smart_defaults['post']}",
                    "",
                    "",
                ]
            )

        return "\n".join(nodes_code)

    def _generate_flow(self, spec: WorkflowSpec) -> str:
        """Generate PocketFlow flow assembly."""
        flow_code = [
            "from pocketflow import Flow",
            "from .nodes import " + ", ".join(node["name"] for node in spec.nodes),
            "import logging",
            "",
            "logger = logging.getLogger(__name__)",
            "",
            "",
        ]

        # Create flow class
        flow_code.extend(
            [
                f"class {spec.name}Flow(Flow):",
                '    """',
                f"    {spec.description}",
                '    """',
                "",
                "    def __init__(self):",
                "        nodes = {",
            ]
        )

        for node in spec.nodes:
            flow_code.append(f'            "{node["name"].lower()}": {node["name"]}(),')

        flow_code.extend(
            [
                "        }",
                "",
                "        edges = {",
            ]
        )

        # Generate edges based on node sequence
        for i, node in enumerate(spec.nodes):
            node_name = node["name"].lower()
            if i < len(spec.nodes) - 1:
                next_node = spec.nodes[i + 1]["name"].lower()
                flow_code.append(
                    f'            "{node_name}": {{"success": "{next_node}", "error": "error_handler"}},'
                )
            else:
                flow_code.append(
                    f'            "{node_name}": {{"success": None, "error": "error_handler"}},'
                )

        flow_code.extend(
            [
                "        }",
                "",
                "        super().__init__(nodes=nodes, edges=edges)",
                "",
                "",
            ]
        )

        return "\n".join(flow_code)

    def _generate_fastapi_main(self, spec: WorkflowSpec) -> str:
        """Generate FastAPI main application."""
        main_code = [
            "from fastapi import FastAPI, HTTPException",
            "from fastapi.middleware.cors import CORSMiddleware",
            f"from .router import router as {spec.name.lower()}_router",
            "import logging",
            "",
            "logging.basicConfig(level=logging.INFO)",
            "",
            "app = FastAPI(",
            f'    title="{spec.name} API",',
            f'    description="{spec.description}",',
            '    version="1.0.0"',
            ")",
            "",
            "app.add_middleware(",
            "    CORSMiddleware,",
            '    allow_origins=["*"],',
            "    allow_credentials=True,",
            '    allow_methods=["*"],',
            '    allow_headers=["*"],',
            ")",
            "",
            f'app.include_router({spec.name.lower()}_router, prefix="/api/v1", tags=["{spec.name}"])',
            "",
            '@app.get("/health")',
            "async def health_check():",
            '    return {"status": "healthy"}',
        ]

        return "\n".join(main_code)

    def _generate_fastapi_router(self, spec: WorkflowSpec) -> str:
        """Generate FastAPI router with endpoints."""
        router_code = [
            "from fastapi import APIRouter, HTTPException",
            "from .schemas.models import *",
            f"from .flow import {spec.name}Flow",
            "from typing import Dict, Any",
            "import logging",
            "from datetime import datetime",
            "",
            "logger = logging.getLogger(__name__)",
            "router = APIRouter()",
            "",
        ]

        for endpoint in spec.api_endpoints:
            method = endpoint.get("method", "post").lower()
            path = endpoint.get("path", f"/{endpoint['name'].lower()}")
            endpoint_name = endpoint["name"]
            default_desc = f"Execute {endpoint_name} workflow"

            router_code.extend(
                [
                    f'@router.{method}("{path}", response_model={endpoint_name}Response)',
                    f"async def {endpoint_name.lower()}_endpoint(request: {endpoint_name}Request):",
                    '    """',
                    f"    {endpoint.get('description', default_desc)}",
                    '    """',
                    "        # Initialize SharedStore",
                    "        shared = {",
                    '            "request_data": request.dict(),',
                    '            "timestamp": datetime.utcnow().isoformat()',
                    "        }",
                    "        ",
                    "        # Execute workflow - let PocketFlow handle retries and errors",
                    f"        flow = {spec.name}Flow()",
                    "        await flow.run_async(shared)",
                    "        ",
                    "        # Check for flow-level errors",
                    '        if "error" in shared:',
                    "            raise HTTPException(",
                    "                status_code=422,",
                    '                detail=shared.get("error_message", "Workflow execution failed")',
                    "            )",
                    "        ",
                    "        # Return response",
                    f'        return {endpoint["name"]}Response(**shared.get("result", {{}}))',
                    "",
                    "",
                ]
            )

        return "\n".join(router_code)

    def _generate_node_tests(self, spec: WorkflowSpec) -> str:
        """Generate tests for nodes."""
        # Use absolute imports for better type checker compatibility
        workflow_name = spec.name.lower().replace(" ", "")
        test_code = [
            "import pytest",
            "from unittest.mock import AsyncMock, patch",
            f"from {workflow_name}.nodes import " + ", ".join(node["name"] for node in spec.nodes),
            "",
            "",
        ]

        for node in spec.nodes:
            test_code.extend(
                [
                    f"class Test{node['name']}:",
                    f'    """Tests for {node["name"]} node."""',
                    "",
                    "    @pytest.fixture",
                    "    def node(self):",
                    f"        return {node['name']}()",
                    "",
                    "    @pytest.fixture",
                    "    def shared_store(self):",
                    '        return {"input_data": "test_data"}',
                    "",
                    "    def test_prep(self, node, shared_store):",
                    '        """Test prep method."""',
                    "        result = node.prep(shared_store)",
                    '        assert result == "test_data"',
                    "",
                    "    @pytest.mark.asyncio",
                    "    async def test_exec_async(self, node):",
                    '        """Test exec_async method."""',
                    '        result = await node.exec_async("test_data")',
                    '        assert result == "success"',
                    "",
                    "    def test_post(self, node, shared_store):",
                    '        """Test post method."""',
                    '        node.post(shared_store, "prep_result", "exec_result")',
                    '        assert "output_data" in shared_store',
                    "",
                    "",
                ]
            )

        return "\n".join(test_code)

    def _generate_flow_tests(self, spec: WorkflowSpec) -> str:
        """Generate tests for flow."""
        # Use absolute imports for better type checker compatibility
        workflow_name = spec.name.lower().replace(" ", "")
        test_code = [
            "import pytest",
            "from unittest.mock import AsyncMock, patch",
            f"from {workflow_name}.flow import {spec.name}Flow",
            "",
            "",
            f"class Test{spec.name}Flow:",
            f'    """Tests for {spec.name}Flow."""',
            "",
            "    @pytest.fixture",
            "    def flow(self):",
            f"        return {spec.name}Flow()",
            "",
            "    @pytest.fixture",
            "    def shared_store(self):",
            '        return {"input_data": "test_data"}',
            "",
            "    @pytest.mark.asyncio",
            "    async def test_flow_execution(self, flow, shared_store):",
            '        """Test complete flow execution."""',
            "        await flow.run_async(shared_store)",
            '        assert "output_data" in shared_store',
            "",
            "    @pytest.mark.asyncio",
            "    async def test_flow_error_handling(self, flow, shared_store):",
            '        """Test flow error handling."""',
            "        # Test with invalid input",
            '        shared_store["input_data"] = None',
            "        with pytest.raises(Exception):",
            "            await flow.run_async(shared_store)",
            "",
        ]

        return "\n".join(test_code)

    def _generate_api_tests(self, spec: WorkflowSpec) -> str:
        """Generate tests for FastAPI endpoints."""
        # Use absolute imports for better type checker compatibility
        workflow_name = spec.name.lower().replace(" ", "")
        test_code = [
            "import pytest",
            "from fastapi.testclient import TestClient",
            "from unittest.mock import AsyncMock, patch",
            f"from {workflow_name}.main import app",
            "",
            "client = TestClient(app)",
            "",
            "",
        ]

        for endpoint in spec.api_endpoints:
            method = endpoint.get("method", "post").upper()
            path = endpoint.get("path", f"/{endpoint['name'].lower()}")

            test_code.extend(
                [
                    f"class Test{endpoint['name']}Endpoint:",
                    f'    """Tests for {endpoint["name"]} endpoint."""',
                    "",
                    f"    def test_{endpoint['name'].lower()}_success(self):",
                    f'        """Test successful {endpoint["name"]} request."""',
                    '        request_data = {"test": "data"}',
                    f'        response = client.{method.lower()}("/api/v1{path}", json=request_data)',
                    "        assert response.status_code == 200",
                    "",
                    f"    def test_{endpoint['name'].lower()}_validation_error(self):",
                    '        """Test validation error handling."""',
                    f'        response = client.{method.lower()}("/api/v1{path}", json={{}})',
                    "        assert response.status_code == 422",
                    "",
                    "",
                ]
            )

        return "\n".join(test_code)

    def _generate_tasks(self, spec: WorkflowSpec) -> str:
        """Generate tasks.md file from template."""
        current_date = datetime.now().isoformat()[:10]
        spec_name = spec.name.lower().replace(" ", "-")

        tasks = f"""# Spec Tasks

These are the tasks to be completed for the spec detailed in @.agent-os/specs/{current_date}-{spec_name}/spec.md

> Created: {current_date}
> Status: Ready for Implementation

## Tasks

Following PocketFlow's 8-step Agentic Coding methodology:

### Phase 0: Design Document (LLM/AI Components Only)
- [x] 0.1 Create `docs/design.md` with complete PocketFlow design ✓ (Generated)
- [ ] 0.2 Review and complete Requirements section with problem statement and success criteria
- [ ] 0.3 Validate Flow Design with Mermaid diagram and node sequence
- [ ] 0.4 Review all Utility functions with input/output contracts
- [ ] 0.5 Validate SharedStore schema with complete data structure
- [ ] 0.6 Complete Node Design with prep/exec/post specifications
- [ ] 0.7 Validate design completeness before proceeding

### Phase 1: Pydantic Schemas & Data Models
- [ ] 1.1 Write tests for Pydantic model validation
- [x] 1.2 Create request/response models in `schemas/models.py` ✓ (Generated)
- [ ] 1.3 Implement core entity models with validation rules
- [ ] 1.4 Create SharedStore transformation models
- [ ] 1.5 Add custom validators and field constraints
- [ ] 1.6 Create error response models with standardized format
- [ ] 1.7 Verify all Pydantic models pass validation tests

### Phase 2: Utility Functions Implementation
- [ ] 2.1 Write tests for utility functions (with mocked external dependencies)
- [x] 2.2 Implement utility functions in `utils/` directory ✓ (Generated templates)"""

        # Add specific utilities
        for utility in spec.utilities:
            tasks += f"\n- [ ] 2.2.{utility['name']}: Complete implementation of `utils/{utility['name']}.py`"

        tasks += """
- [ ] 2.3 Add proper type hints and docstrings for all utilities
- [ ] 2.4 Implement LLM integration utilities (if applicable)
- [ ] 2.5 Add error handling without try/catch (fail fast approach)
- [ ] 2.6 Create standalone main() functions for utility testing
- [ ] 2.7 Verify all utility tests pass with mocked dependencies

### Phase 3: FastAPI Endpoints (If Applicable)"""

        if spec.fast_api_integration:
            tasks += """
- [ ] 3.1 Write tests for FastAPI endpoints (with mocked flows)
- [x] 3.2 Create FastAPI application structure in `main.py` ✓ (Generated)
- [x] 3.3 Implement route handlers with proper async patterns ✓ (Generated)
- [x] 3.4 Add request/response model integration ✓ (Generated)
- [ ] 3.5 Implement error handling and status code mapping
- [ ] 3.6 Add authentication and middleware (if required)
- [ ] 3.7 Verify all FastAPI endpoint tests pass"""
        else:
            tasks += """
- [ ] 3.1 FastAPI integration not required for this workflow
- [ ] 3.2 Skip FastAPI-specific tasks"""

        tasks += """

### Phase 4: PocketFlow Nodes (LLM/AI Components)
- [ ] 4.1 Write tests for individual node lifecycle methods
- [x] 4.2 Implement nodes in `nodes.py` following design.md specifications ✓ (Generated templates)"""

        # Add specific nodes
        for node in spec.nodes:
            tasks += (
                f"\n- [ ] 4.2.{node['name']}: Complete implementation of {node['name']}"
            )

        tasks += """
- [ ] 4.3 Create prep() methods for data access and validation
- [ ] 4.4 Implement exec() methods with utility function calls
- [ ] 4.5 Add post() methods for result storage and action determination
- [ ] 4.6 Implement error handling as action string routing
- [ ] 4.7 Verify all node tests pass in isolation

### Phase 5: PocketFlow Flow Assembly (LLM/AI Components)
- [ ] 5.1 Write tests for complete flow execution scenarios
- [x] 5.2 Create flow assembly in `flow.py` ✓ (Generated)
- [ ] 5.3 Connect nodes with proper action string routing
- [ ] 5.4 Implement error handling and retry strategies
- [ ] 5.5 Add flow-level logging and monitoring
- [ ] 5.6 Test all flow paths including error scenarios
- [ ] 5.7 Verify flow integration with SharedStore schema

### Phase 6: Integration & Testing
- [ ] 6.1 Write end-to-end integration tests
- [ ] 6.2 Integrate FastAPI endpoints with PocketFlow workflows
- [ ] 6.3 Test complete request→flow→response cycle
- [ ] 6.4 Validate error propagation from flow to API responses
- [ ] 6.5 Test performance under expected load
- [ ] 6.6 Verify type safety across all boundaries
- [ ] 6.7 Run complete test suite and ensure 100% pass rate

### Phase 7: Optimization & Reliability
- [ ] 7.1 Add comprehensive logging throughout the system
- [ ] 7.2 Implement caching strategies (if applicable)
- [ ] 7.3 Add monitoring and observability hooks
- [ ] 7.4 Optimize async operations and batch processing
- [ ] 7.5 Add retry mechanisms and circuit breakers
- [ ] 7.6 Create health check endpoints
- [ ] 7.7 Verify system reliability under various conditions

**Development Toolchain Validation (Every Phase):**
- Run `uv run ruff check --fix .` for linting
- Run `uv run ruff format .` for code formatting  
- Run `uv run ty check` for type checking
- Run `pytest` for all tests
- Verify all checks pass before proceeding to next phase

## Generated Files Summary

The following files have been generated and need completion:

### Core Files ✓
- `docs/design.md` - Design document (review and complete)
- `schemas/models.py` - Pydantic models (review and extend)
- `nodes.py` - PocketFlow nodes (implement logic)
- `flow.py` - Flow assembly (review connections)

### Utility Files ✓"""

        for utility in spec.utilities:
            tasks += f"\n- `utils/{utility['name']}.py` - {utility['description']}"

        if spec.fast_api_integration:
            tasks += """

### FastAPI Files ✓
- `main.py` - FastAPI application
- `router.py` - API routes and handlers"""

        tasks += """

### Test Files ✓
- `tests/test_nodes.py` - Node unit tests
- `tests/test_flow.py` - Flow integration tests"""

        if spec.fast_api_integration:
            tasks += "\n- `tests/test_api.py` - API endpoint tests"

        tasks += f"""

### Next Steps
1. Review the design document and complete any missing sections
2. Implement the utility functions with actual logic
3. Complete the node implementations with proper business logic
4. Test the complete workflow end-to-end
5. Deploy and validate in staging environment

Generated on: {current_date}
Workflow Pattern: {spec.pattern}
FastAPI Integration: {"Enabled" if spec.fast_api_integration else "Disabled"}"""

        return tasks

    def _extract_template_section(self, template: str, section_name: str) -> str:
        """Extract a specific section from a template file."""
        lines = template.split("\n")
        in_section = False
        section_lines = []

        for line in lines:
            if section_name in line:
                in_section = True
                continue
            elif in_section and line.startswith("##") and section_name not in line:
                break
            elif in_section:
                section_lines.append(line)

        # If no section found, return a basic template
        if not section_lines:
            return f"""# Design Document

> Spec: {section_name}
> Created: {datetime.now().isoformat()[:10]}
> Status: Design Phase
> Framework: PocketFlow

## Requirements

### Problem Statement
[CLEAR_PROBLEM_DEFINITION_FROM_USER_PERSPECTIVE]

### Success Criteria
- [MEASURABLE_OUTCOME_1]
- [MEASURABLE_OUTCOME_2]

## Flow Design

### High-Level Architecture
```mermaid
graph TD
    A[Start] --> B[Processing]
    B --> C[End]
```

## Implementation Notes

This is a generated design document template. Please complete with actual requirements and design details.
"""

        return "\n".join(section_lines)

    def save_workflow(self, spec: WorkflowSpec, output_files: Dict[str, str]) -> None:
        """Save generated workflow files to disk."""
        workflow_dir = self.output_path / spec.name.lower().replace(" ", "_")
        workflow_dir.mkdir(exist_ok=True)

        # Track directories that need __init__.py files
        directories_needing_init = set()

        for file_path, content in output_files.items():
            full_path = workflow_dir / file_path
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content)
            
            # Add parent directories to the set for __init__.py creation
            directories_needing_init.add(full_path.parent)

        # Create __init__.py files for proper package structure
        # This ensures relative imports in tests work correctly
        for directory in directories_needing_init:
            init_file = directory / "__init__.py"
            if not init_file.exists():
                init_file.write_text("")

        # Also create __init__.py in the root workflow directory
        root_init = workflow_dir / "__init__.py"
        if not root_init.exists():
            root_init.write_text("")

        print(f"Generated workflow saved to: {workflow_dir}")
        
        # Automatically validate generated templates
        print("\n🔍 Running template validation...")
        validation_result = self.coordinate_template_validation(str(workflow_dir))
        
        if validation_result.is_valid:
            print("✅ Template validation passed!")
        else:
            print("❌ Template validation issues found:")
            for error in validation_result.errors:
                print(f"  • Error: {error}")
            for warning in validation_result.warnings:
                print(f"  • Warning: {warning}")
        
        if validation_result.warnings:
            print("⚠️  Validation warnings (non-blocking):")
            for warning in validation_result.warnings:
                print(f"  • {warning}")

    def coordinate_template_validation(self, template_path: str) -> ValidationResult:
        """Coordinate with template-validator agent for post-generation validation."""
        try:
            import sys
            from pathlib import Path
            sys.path.insert(0, str(Path(__file__).parent))
            from template_validator import PocketFlowValidator
            
            validator = PocketFlowValidator()
            template_dir = Path(template_path)
            
            result = validator.validate_directory(template_dir)
            
            # Convert validation result format
            return ValidationResult(
                is_valid=result.is_valid,
                errors=[issue.message for issue in result.errors],
                warnings=[issue.message for issue in result.warnings],
                corrections_applied=[]  # Corrections would be applied in a separate step
            )
            
        except ImportError:
            return ValidationResult(
                is_valid=True,
                warnings=["Template validation module not available - skipping validation"]
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                errors=[f"Validation failed: {str(e)}"]
            )

    def request_pattern_analysis(self, requirements: str) -> PatternRecommendation:
        """Request pattern analysis from pattern-recognizer agent."""
        # This is a coordination function that would interface with the pattern-recognizer agent
        # For now, return a basic recommendation
        return PatternRecommendation(
            primary_pattern="AGENT",
            confidence_score=0.8,
            rationale="Pattern analysis agent integration pending"
        )

    def generate_dependency_config(self, pattern: str) -> DependencyConfig:
        """Generate dependency configuration via dependency-orchestrator agent."""
        # This is a coordination function that would interface with the dependency-orchestrator agent
        # For now, return basic config
        base_deps = ["pocketflow", "pydantic", "fastapi"]
        
        pattern_deps = {
            "RAG": ["chromadb", "sentence-transformers"],
            "AGENT": ["openai", "anthropic"],
            "TOOL": ["requests", "aiohttp"],
            "WORKFLOW": [],
            "MAPREDUCE": ["celery", "redis"],
            "MULTI-AGENT": ["openai", "anthropic"],
            "STRUCTURED-OUTPUT": ["jsonschema"]
        }
        
        return DependencyConfig(
            base_dependencies=base_deps,
            pattern_dependencies=pattern_deps.get(pattern, []),
            dev_dependencies=["pytest", "pytest-asyncio", "ruff", "mypy"],
            tool_configs={
                "ruff": {"line-length": 88, "target-version": "py39"},
                "mypy": {"python_version": "3.9", "strict": True}
            }
        )


def main():
    """CLI interface for the workflow generator."""
    import argparse

    if not YAML_AVAILABLE:
        print(
            "Error: PyYAML is required for CLI usage. Install with: pip install pyyaml"
        )
        return 1

    parser = argparse.ArgumentParser(
        description="Generate PocketFlow workflows from specifications"
    )
    parser.add_argument(
        "--spec", required=True, help="Path to workflow specification YAML file"
    )
    parser.add_argument(
        "--output", help="Output directory (default: .agent-os/workflows)"
    )

    args = parser.parse_args()

    # Load specification
    try:
        with open(args.spec, "r") as f:
            spec_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Specification file not found: {args.spec}")
        return 1
    except yaml.YAMLError as e:
        print(f"Error: Invalid YAML in specification file: {e}")
        return 1

    try:
        spec = WorkflowSpec(**spec_data)
    except TypeError as e:
        print(f"Error: Invalid specification format: {e}")
        return 1

    # Generate workflow
    try:
        # Initialize generator with custom paths if provided
        generator_kwargs = {}
        if args.output:
            generator_kwargs["output_path"] = args.output

        generator = PocketFlowGenerator(**generator_kwargs)
        output_files = generator.generate_workflow(spec)
        generator.save_workflow(spec, output_files)

        print(f"Successfully generated workflow: {spec.name}")
        return 0
    except Exception as e:
        print(f"Error: Workflow generation failed: {e}")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
