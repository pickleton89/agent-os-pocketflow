#!/usr/bin/env python3
"""PocketFlow Tools CLI (Phase 1).

Replicates legacy CLI flags/messages/exit codes while using the new
import surface. Generation is delegated to the legacy implementation
via the workflow composer during Phase 1.
"""

from __future__ import annotations

import argparse
from typing import Any

from pocketflow_tools.generators.workflow_composer import PocketFlowGenerator
from pocketflow_tools.spec import WorkflowSpec


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate PocketFlow workflows from specifications"
    )
    parser.add_argument("--spec", required=True, help="Path to workflow specification YAML file")
    parser.add_argument("--output", help="Output directory (default: .agent-os/workflows)")

    args = parser.parse_args()

    # Check PyYAML availability only after parsing args (allows --help to work)
    try:
        import yaml  # type: ignore
    except ImportError:
        print("Error: PyYAML is required for CLI usage. Install with: uv pip install pyyaml")
        return 1

    # Load specification
    try:
        with open(args.spec, "r") as f:
            spec_data: Any = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Specification file not found: {args.spec}")
        return 1
    except Exception as e:
        # Match legacy YAML error messaging
        print(f"Error: Invalid YAML in specification file: {e}")
        return 1

    try:
        spec = WorkflowSpec(**spec_data)
    except TypeError as e:
        print(f"Error: Invalid specification format: {e}")
        return 1

    try:
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

