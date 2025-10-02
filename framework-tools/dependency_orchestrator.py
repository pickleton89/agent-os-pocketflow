#!/usr/bin/env python3
"""
Dependency Orchestrator for PocketFlow Templates

Manages Python tooling configuration and dependency specifications for generated
PocketFlow templates, ensuring proper development environment setup.
"""

import logging
from dataclasses import dataclass, field
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


@dataclass
class DependencyConfig:
    """Dependency configuration for a pattern."""

    base_dependencies: List[str] = field(default_factory=list)
    pattern_dependencies: List[str] = field(default_factory=list)
    dev_dependencies: List[str] = field(default_factory=list)
    python_version: str = ">=3.12"
    tool_configs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PyProjectConfig:
    """Complete pyproject.toml configuration."""

    name: str
    version: str = "0.1.0"
    description: str = ""
    python_version: str = ">=3.12"
    dependencies: List[str] = field(default_factory=list)
    dev_dependencies: List[str] = field(default_factory=list)
    tool_configs: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolConfig:
    """Individual tool configuration."""

    name: str
    config: Dict[str, Any]
    section: str  # e.g., "tool.ruff", "tool.pytest"


class DependencyOrchestrator:
    """
    Orchestrates Python dependency management and tool configuration
    for PocketFlow template generation.
    """

    def __init__(self):
        """Initialize the dependency orchestrator."""
        self.pattern_dependency_map = self._load_pattern_dependencies()
        self.tool_configurations = self._load_tool_configurations()
        self.version_constraints = self._load_version_constraints()
        # Caching for generated configurations
        self._config_cache = {}
        self._pyproject_cache = {}
        self._cache_size_limit = 50

    def _load_pattern_dependencies(self) -> Dict[str, Dict[str, List[str]]]:
        """Load pattern-specific dependency mappings."""
        return {
            "RAG": {
                "runtime": [
                    "pocketflow",
                    "pydantic>=2.0",
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0",
                    "chromadb>=0.4.15",
                    "sentence-transformers>=2.2.2",
                    "numpy>=1.24.0",
                    "tiktoken>=0.5.0",
                ],
                "optional": [
                    "openai>=1.0.0",
                    "anthropic>=0.7.0",
                    "pinecone-client>=2.2.4",
                    "faiss-cpu>=1.7.4",
                ],
            },
            "AGENT": {
                "runtime": [
                    "pocketflow",
                    "pydantic>=2.0",
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0",
                    "openai>=1.0.0",
                    "tiktoken>=0.5.0",
                    "tenacity>=8.2.0",
                ],
                "optional": [
                    "anthropic>=0.7.0",
                    "google-generativeai>=0.3.0",
                    "langchain>=0.1.0",
                    "llama-index>=0.9.0",
                ],
            },
            "TOOL": {
                "runtime": [
                    "pocketflow",
                    "pydantic>=2.0",
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0",
                    "requests>=2.31.0",
                    "aiohttp>=3.9.0",
                    "tenacity>=8.2.0",
                ],
                "optional": [
                    "boto3>=1.29.0",
                    "google-cloud-storage>=2.10.0",
                    "azure-storage-blob>=12.19.0",
                    "paramiko>=3.3.0",
                ],
            },
            "WORKFLOW": {
                "runtime": [
                    "pocketflow",
                    "pydantic>=2.0",
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0",
                ],
                "optional": [],
            },
            "MAPREDUCE": {
                "runtime": [
                    "pocketflow",
                    "pydantic>=2.0",
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0",
                    "celery>=5.3.0",
                    "redis>=5.0.0",
                    "kombu>=5.3.0",
                ],
                "optional": [
                    "flower>=2.0.0",
                    "dask[complete]>=2023.12.0",
                    "ray[default]>=2.8.0",
                ],
            },
            "MULTI-AGENT": {
                "runtime": [
                    "pocketflow",
                    "pydantic>=2.0",
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0",
                    "openai>=1.0.0",
                    "anthropic>=0.7.0",
                    "tenacity>=8.2.0",
                    "asyncio-mqtt>=0.13.0",
                ],
                "optional": [
                    "autogen-agentchat>=0.2.0",
                    "crewai>=0.1.0",
                    "swarm-agent>=0.1.0",
                ],
            },
            "STRUCTURED-OUTPUT": {
                "runtime": [
                    "pocketflow",
                    "pydantic>=2.0",
                    "fastapi>=0.104.0",
                    "uvicorn[standard]>=0.24.0",
                    "jsonschema>=4.19.0",
                    "marshmallow>=3.20.0",
                ],
                "optional": [
                    "openai>=1.0.0",
                    "anthropic>=0.7.0",
                    "instructor>=0.4.0",
                ],
            },
        }

    def _load_tool_configurations(self) -> Dict[str, ToolConfig]:
        """Load default tool configurations."""
        return {
            "ruff": ToolConfig(
                name="ruff",
                section="tool.ruff",
                config={
                    "line-length": 88,
                    "target-version": "py312",
                    "select": ["E", "F", "I", "N", "W", "UP"],
                    "ignore": ["E501", "N806"],
                    "exclude": [".git", ".venv", "__pycache__", "build", "dist"],
                },
            ),
            "ruff-format": ToolConfig(
                name="ruff-format",
                section="tool.ruff.format",
                config={
                    "quote-style": "double",
                    "indent-style": "space",
                    "skip-magic-trailing-comma": False,
                    "line-ending": "auto",
                },
            ),
            "ty": ToolConfig(
                name="ty",
                section="tool.ty",
                config={
                    "python_version": "3.12",
                    "strict": True,
                    "warn_return_any": True,
                    "warn_unused_configs": True,
                    "disallow_untyped_defs": True,
                    "exclude": ["tests/", "build/", ".venv/"],
                },
            ),
            "pytest": ToolConfig(
                name="pytest",
                section="tool.pytest.ini_options",
                config={
                    "minversion": "7.0",
                    "addopts": [
                        "-ra",
                        "--strict-markers",
                        "--strict-config",
                        "--cov=.",
                        "--cov-report=term-missing",
                    ],
                    "testpaths": ["tests"],
                    "python_files": ["test_*.py"],
                    "python_classes": ["Test*"],
                    "python_functions": ["test_*"],
                    "markers": [
                        "slow: marks tests as slow",
                        "integration: marks tests as integration tests",
                    ],
                },
            ),
            "coverage": ToolConfig(
                name="coverage",
                section="tool.coverage.run",
                config={
                    "source": ["."],
                    "branch": True,
                    "omit": ["tests/*", ".venv/*", "build/*", "dist/*"],
                },
            ),
        }

    def _load_version_constraints(self) -> Dict[str, str]:
        """Load version constraint mappings."""
        return {
            "python": ">=3.12,<4.0",
            "pocketflow": ">=0.1.0",
            "pydantic": ">=2.0,<3.0",
            "fastapi": ">=0.104.0,<1.0.0",
            "uvicorn": ">=0.24.0,<1.0.0",
            "pytest": ">=7.0.0,<8.0.0",
            "ruff": ">=0.1.0,<1.0.0",
        }

    def generate_config_for_pattern(self, pattern: str) -> DependencyConfig:
        """Generate complete dependency configuration for a specific pattern with caching."""
        # Check cache first
        cache_key = pattern.lower().strip()
        if cache_key in self._config_cache:
            logger.debug(f"Cache hit for dependency config: {pattern}")
            return self._config_cache[cache_key]

        logger.info(f"Generating dependency config for pattern: {pattern}")

        # Get pattern-specific dependencies
        pattern_deps = self._get_pattern_dependencies(pattern)

        # Generate base dependencies
        base_deps = self._get_base_dependencies()

        # Generate development dependencies
        dev_deps = self._get_development_dependencies()

        # Generate tool configurations
        tool_configs = self._get_tool_configurations()

        # Get Python version requirement
        python_version = self.version_constraints.get("python", ">=3.12")

        config = DependencyConfig(
            base_dependencies=base_deps,
            pattern_dependencies=pattern_deps,
            dev_dependencies=dev_deps,
            python_version=python_version,
            tool_configs=tool_configs,
        )

        # Cache the result
        self._cache_config(cache_key, config)

        return config

    def _get_pattern_dependencies(self, pattern: str) -> List[str]:
        """Get dependencies specific to a pattern."""
        pattern_config = self.pattern_dependency_map.get(pattern, {})
        runtime_deps = pattern_config.get("runtime", [])

        # Apply version constraints
        constrained_deps = []
        for dep in runtime_deps:
            constrained_deps.append(self._apply_version_constraints(dep))

        return constrained_deps

    def _get_base_dependencies(self) -> List[str]:
        """Get base dependencies required for all patterns."""
        base_deps = [
            "pocketflow",
            "pydantic>=2.0",
            "fastapi>=0.104.0",
            "uvicorn[standard]>=0.24.0",
        ]

        constrained_deps = []
        for dep in base_deps:
            constrained_deps.append(self._apply_version_constraints(dep))

        return constrained_deps

    def _get_development_dependencies(self) -> List[str]:
        """Get development dependencies for testing and tooling."""
        dev_deps = [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "ruff>=0.1.0",
            "ty>=0.5.0",  # Type checker (mypy alternative)
            "httpx>=0.25.0",  # For testing async endpoints
            "factory-boy>=3.3.0",  # For test data generation
        ]

        constrained_deps = []
        for dep in dev_deps:
            constrained_deps.append(self._apply_version_constraints(dep))

        return constrained_deps

    def _get_tool_configurations(self) -> Dict[str, Any]:
        """Get tool configurations for development."""
        configs = {}

        for tool_name, tool_config in self.tool_configurations.items():
            configs[tool_config.section] = tool_config.config

        return configs

    def _apply_version_constraints(self, dependency: str) -> str:
        """Apply version constraints to a dependency if needed."""
        # If dependency already has version constraint, return as-is
        if ">=" in dependency or "==" in dependency or "~=" in dependency:
            return dependency

        # Extract package name
        package_name = dependency.split("[")[0]  # Handle extras like uvicorn[standard]

        # Apply constraint if we have one
        if package_name in self.version_constraints:
            constraint = self.version_constraints[package_name]
            if "[" in dependency:  # Preserve extras
                base, extra = dependency.split("[", 1)
                return f"{base}[{extra}{constraint}"
            else:
                return f"{package_name}{constraint}"

        return dependency

    def generate_pyproject_toml(
        self, project_name: str, pattern: str, description: str = ""
    ) -> str:
        """Generate complete pyproject.toml content."""
        config = self.generate_config_for_pattern(pattern)

        # All dependencies (base + pattern-specific)
        all_deps = list(set(config.base_dependencies + config.pattern_dependencies))

        # Build pyproject.toml content
        content = f'''[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "{project_name}"
version = "0.1.0"
description = "{description}"
readme = "README.md"
requires-python = "{config.python_version}"
dependencies = [
'''

        # Add dependencies
        for dep in sorted(all_deps):
            content += f'    "{dep}",\n'

        content += """]

[project.optional-dependencies]
dev = [
"""

        # Add dev dependencies
        for dep in sorted(config.dev_dependencies):
            content += f'    "{dep}",\n'

        content += """]

[project.urls]
Repository = "https://github.com/your-org/your-repo"
Issues = "https://github.com/your-org/your-repo/issues"

"""

        # Add tool configurations
        for section, tool_config in config.tool_configs.items():
            content += f"[{section}]\n"
            content += self._format_toml_section(tool_config)
            content += "\n"

        return content

    def _format_toml_section(self, config: Dict[str, Any], indent: int = 0) -> str:
        """Format a configuration section for TOML."""
        lines = []
        base_indent = "    " * indent

        for key, value in config.items():
            if isinstance(value, bool):
                lines.append(f"{base_indent}{key} = {str(value).lower()}")
            elif isinstance(value, str):
                lines.append(f'{base_indent}{key} = "{value}"')
            elif isinstance(value, (int, float)):
                lines.append(f"{base_indent}{key} = {value}")
            elif isinstance(value, list):
                if all(isinstance(item, str) for item in value):
                    formatted_list = '["' + '", "'.join(value) + '"]'
                else:
                    formatted_list = str(value)
                lines.append(f"{base_indent}{key} = {formatted_list}")
            elif isinstance(value, dict):
                lines.append(f"{base_indent}[{key}]")
                lines.append(self._format_toml_section(value, indent + 1))

        return "\n".join(lines)

    def generate_uv_config(self, project_name: str, pattern: str) -> Dict[str, str]:
        """Generate UV-specific configuration files."""
        config = self.generate_config_for_pattern(pattern)

        files = {}

        # .python-version file for uv (align with pyproject/tooling: Python 3.12)
        files[".python-version"] = "3.12\n"

        # uv.toml configuration
        files["uv.toml"] = """[tool.uv]
dev-dependencies = [
"""
        for dep in sorted(config.dev_dependencies):
            files["uv.toml"] += f'    "{dep}",\n'

        files["uv.toml"] += """]

[tool.uv.sources]
# Add any local package sources here if needed

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
"""

        return files

    def validate_dependencies(self, dependencies: List[str]) -> Dict[str, List[str]]:
        """Validate dependencies for compatibility issues."""
        issues = {"warnings": [], "errors": []}

        # Check for common incompatibilities
        dep_names = [dep.split(">=")[0].split("==")[0] for dep in dependencies]

        # Example validation rules
        if "django" in dep_names and "fastapi" in dep_names:
            issues["warnings"].append(
                "Both Django and FastAPI detected - consider using one web framework"
            )

        if "asyncio" in dep_names and "threading" in dep_names:
            issues["warnings"].append(
                "Both asyncio and threading patterns detected - may cause conflicts"
            )

        return issues

    def get_pattern_recommendations(self, requirements_text: str) -> List[str]:
        """Suggest additional dependencies based on requirements text."""
        recommendations = []
        text_lower = requirements_text.lower()

        # Database-related
        if any(db in text_lower for db in ["database", "postgres", "mysql", "sqlite"]):
            recommendations.extend(["sqlalchemy>=2.0.0", "alembic>=1.12.0"])

        # Authentication
        if any(auth in text_lower for auth in ["auth", "login", "jwt", "oauth"]):
            recommendations.extend(["python-jose>=3.3.0", "passlib>=1.7.4"])

        # File processing
        if any(
            file_type in text_lower for file_type in ["pdf", "excel", "csv", "json"]
        ):
            recommendations.extend(["pandas>=2.0.0", "openpyxl>=3.1.0"])

        # Machine learning
        if any(ml in text_lower for ml in ["ml", "ai", "model", "train", "predict"]):
            recommendations.extend(["scikit-learn>=1.3.0", "numpy>=1.24.0"])

        return recommendations

    def validate_configuration(
        self, config_content: str, file_type: str = "pyproject.toml"
    ) -> Dict[str, List[str]]:
        """Validate generated configuration files."""
        issues = {"errors": [], "warnings": []}

        if file_type == "pyproject.toml":
            issues.update(self._validate_pyproject_toml(config_content))
        elif file_type == "requirements.txt":
            issues.update(self._validate_requirements_txt(config_content))
        elif file_type == "uv.toml":
            issues.update(self._validate_uv_toml(config_content))

        return issues

    def _validate_pyproject_toml(self, content: str) -> Dict[str, List[str]]:
        """Validate pyproject.toml content."""
        issues = {"errors": [], "warnings": []}

        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                issues["warnings"].append(
                    "TOML parser not available - cannot validate pyproject.toml syntax"
                )
                return issues

        try:
            data = tomllib.loads(content)
        except Exception as e:
            issues["errors"].append(f"Invalid TOML syntax: {e}")
            return issues

        # Check required sections
        if "project" not in data:
            issues["errors"].append("Missing [project] section")

        if "build-system" not in data:
            issues["warnings"].append(
                "Missing [build-system] section - recommended for distribution"
            )

        # Check project metadata
        if "project" in data:
            project = data["project"]

            if "name" not in project:
                issues["errors"].append("Missing project name")

            if "version" not in project:
                issues["errors"].append("Missing project version")

            if "requires-python" not in project:
                issues["warnings"].append("Missing python version requirement")

            if "dependencies" not in project:
                issues["warnings"].append("No dependencies specified")
            else:
                # Validate dependencies format
                deps = project["dependencies"]
                if not isinstance(deps, list):
                    issues["errors"].append("Dependencies must be a list")
                else:
                    for dep in deps:
                        if not isinstance(dep, str):
                            issues["errors"].append(f"Invalid dependency format: {dep}")

        # Check for common tool configurations
        expected_tools = ["tool.ruff", "tool.pytest.ini_options"]
        for tool in expected_tools:
            if tool not in data:
                issues["warnings"].append(f"Missing {tool} configuration")

        return issues

    def _validate_requirements_txt(self, content: str) -> Dict[str, List[str]]:
        """Validate requirements.txt content."""
        issues = {"errors": [], "warnings": []}

        lines = content.strip().split("\n")
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Basic format validation
            if not any(op in line for op in [">=", "==", ">", "<", "~=", "!="]):
                issues["warnings"].append(
                    f"Line {line_num}: No version constraint specified for '{line}'"
                )

            # Check for valid package name format
            import re

            if not re.match(
                r"^[a-zA-Z0-9][a-zA-Z0-9._-]*[a-zA-Z0-9]",
                line.split("[")[0].split(">=")[0].split("==")[0],
            ):
                issues["errors"].append(
                    f"Line {line_num}: Invalid package name format '{line}'"
                )

        return issues

    def _validate_uv_toml(self, content: str) -> Dict[str, List[str]]:
        """Validate uv.toml content."""
        issues = {"errors": [], "warnings": []}

        try:
            import tomllib
        except ImportError:
            try:
                import tomli as tomllib
            except ImportError:
                issues["warnings"].append(
                    "TOML parser not available - cannot validate uv.toml syntax"
                )
                return issues

        try:
            data = tomllib.loads(content)
        except Exception as e:
            issues["errors"].append(f"Invalid TOML syntax: {e}")
            return issues

        # Check UV-specific sections
        if "tool.uv" not in data:
            issues["errors"].append("Missing [tool.uv] section")

        if "tool.uv" in data:
            uv_config = data["tool.uv"]

            if "dev-dependencies" not in uv_config:
                issues["warnings"].append("No dev-dependencies specified in UV config")

        return issues

    def validate_pattern_compatibility(
        self, pattern: str, dependencies: List[str]
    ) -> Dict[str, List[str]]:
        """Validate that dependencies are appropriate for the pattern."""
        issues = {"errors": [], "warnings": []}

        dep_names = [
            dep.split(">=")[0].split("==")[0].split("[")[0] for dep in dependencies
        ]
        pattern_config = self.pattern_dependency_map.get(pattern, {})
        expected_deps = pattern_config.get("runtime", [])
        expected_names = [
            dep.split(">=")[0].split("==")[0].split("[")[0] for dep in expected_deps
        ]

        # Check for missing critical dependencies
        for expected_dep in expected_names:
            if expected_dep not in dep_names:
                if expected_dep in ["pocketflow", "pydantic", "fastapi"]:
                    issues["errors"].append(
                        f"Missing critical dependency for {pattern} pattern: {expected_dep}"
                    )
                else:
                    issues["warnings"].append(
                        f"Missing recommended dependency for {pattern} pattern: {expected_dep}"
                    )

        # Check for pattern-specific conflicts
        if pattern == "RAG":
            if "django" in dep_names:
                issues["warnings"].append(
                    "Django detected with RAG pattern - consider FastAPI for better async support"
                )

        elif pattern == "AGENT":
            llm_clients = ["openai", "anthropic", "google-generativeai"]
            if not any(client in dep_names for client in llm_clients):
                issues["warnings"].append("No LLM client detected for AGENT pattern")

        elif pattern == "TOOL":
            http_clients = ["requests", "aiohttp", "httpx"]
            if not any(client in dep_names for client in http_clients):
                issues["warnings"].append("No HTTP client detected for TOOL pattern")

        return issues

    def _cache_config(self, cache_key: str, config: DependencyConfig):
        """Cache dependency configuration with size management."""
        if len(self._config_cache) >= self._cache_size_limit:
            # Remove oldest entry
            oldest_key = next(iter(self._config_cache))
            del self._config_cache[oldest_key]

        self._config_cache[cache_key] = config

    def clear_cache(self):
        """Clear all caches."""
        self._config_cache.clear()
        self._pyproject_cache.clear()
        logger.debug("Dependency orchestrator caches cleared")


def main():
    """CLI interface for testing the dependency orchestrator."""
    import argparse

    parser = argparse.ArgumentParser(description="Generate dependency configurations")
    parser.add_argument(
        "--pattern",
        required=True,
        choices=[
            "RAG",
            "AGENT",
            "TOOL",
            "WORKFLOW",
            "MAPREDUCE",
            "MULTI-AGENT",
            "STRUCTURED-OUTPUT",
        ],
    )
    parser.add_argument("--project-name", default="test-project")
    parser.add_argument(
        "--output-pyproject",
        action="store_true",
        help="Generate pyproject.toml content",
    )

    args = parser.parse_args()

    orchestrator = DependencyOrchestrator()

    if args.output_pyproject:
        content = orchestrator.generate_pyproject_toml(
            args.project_name, args.pattern, f"Generated {args.pattern} pattern project"
        )
        print(content)
    else:
        config = orchestrator.generate_config_for_pattern(args.pattern)
        print(f"Pattern: {args.pattern}")
        print(f"Python Version: {config.python_version}")
        print(f"Base Dependencies: {len(config.base_dependencies)}")
        print(f"Pattern Dependencies: {len(config.pattern_dependencies)}")
        print(f"Dev Dependencies: {len(config.dev_dependencies)}")
        print(f"Tool Configurations: {len(config.tool_configs)}")


if __name__ == "__main__":
    main()
