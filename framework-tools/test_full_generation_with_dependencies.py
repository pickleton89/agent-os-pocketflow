#!/usr/bin/env python3
"""Integration test ensuring CLI generation handles dependencies."""

from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path
from subprocess import run, CalledProcessError

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLE_SPEC = Path(__file__).resolve().parent / "examples" / "agent-workflow-spec.yaml"
REQUIRED_ARTIFACTS = [
    "pyproject.toml",
    "requirements.txt",
    "flow.py",
    "nodes.py",
    "router.py",
]


def main() -> None:
    if not EXAMPLE_SPEC.exists():
        raise SystemExit(f"Example spec missing: {EXAMPLE_SPEC}")

    temp_dir = Path(tempfile.mkdtemp(prefix="pf_full_gen_"))
    os.environ.setdefault("POCKETFLOW_TEST_MODE", "1")

    try:
        cmd = [
            sys.executable,
            "-m",
            "pocketflow_tools.cli",
            "--spec",
            str(EXAMPLE_SPEC),
            "--output",
            str(temp_dir),
        ]
        result = run(cmd, check=False, capture_output=True, text=True)
        if result.returncode != 0:
            raise SystemExit(
                "CLI generation failed:\n"
                f"stdout:\n{result.stdout}\n"
                f"stderr:\n{result.stderr}"
            )

        generated_projects = [p for p in temp_dir.iterdir() if p.is_dir()]
        if not generated_projects:
            raise SystemExit(
                "CLI generation succeeded but produced no project directory"
            )

        project_dir = generated_projects[0]
        missing = [
            artifact
            for artifact in REQUIRED_ARTIFACTS
            if not (project_dir / artifact).exists()
        ]
        if missing:
            raise SystemExit(
                f"Generated project missing artifacts: {', '.join(missing)}"
            )

        requirements = (
            (project_dir / "requirements.txt").read_text(encoding="utf-8").lower()
        )
        expected_deps = ["fastapi"]
        missing_deps = [dep for dep in expected_deps if dep not in requirements]
        if missing_deps:
            raise SystemExit(
                "Generated requirements.txt missing expected dependencies: "
                + ", ".join(missing_deps)
            )

        print("Full generation with dependencies test passed.")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    try:
        main()
    except CalledProcessError as exc:
        raise SystemExit(f"Subprocess failed: {exc}")
