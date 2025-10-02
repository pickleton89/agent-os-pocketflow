#!/usr/bin/env python3
"""Smoke test for PocketFlow generator CLI."""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

from pocketflow_tools.cli import main as cli_main

EXAMPLE_SPEC = Path(__file__).resolve().parent / "examples" / "agent-workflow-spec.yaml"


def run_cli(*args: str) -> int:
    argv_backup = sys.argv[:]
    try:
        sys.argv = ["pocketflow-tools-cli", *args]
        return cli_main()
    finally:
        sys.argv = argv_backup


def ensure_generated_project(root: Path) -> Path:
    projects = [p for p in root.iterdir() if p.is_dir()]
    if not projects:
        raise SystemExit("Generator CLI did not create an output project")
    return projects[0]


def main() -> None:
    if not EXAMPLE_SPEC.exists():
        raise SystemExit(f"Missing example spec: {EXAMPLE_SPEC}")

    output_root = Path(tempfile.mkdtemp(prefix="pf_generator_smoke_"))
    try:
        exit_code = run_cli("--spec", str(EXAMPLE_SPEC), "--output", str(output_root))
        if exit_code != 0:
            raise SystemExit(f"CLI returned non-zero exit code: {exit_code}")

        project_dir = ensure_generated_project(output_root)
        expected = [
            project_dir / "pyproject.toml",
            project_dir / "flow.py",
            project_dir / "nodes.py",
        ]
        missing = [
            str(path.relative_to(project_dir)) for path in expected if not path.exists()
        ]
        if missing:
            raise SystemExit(
                "Generator output missing expected artifacts: " + ", ".join(missing)
            )

        print("Generator smoke test passed.")
    finally:
        shutil.rmtree(output_root, ignore_errors=True)


if __name__ == "__main__":
    main()
