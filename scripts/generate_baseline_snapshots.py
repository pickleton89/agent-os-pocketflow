#!/usr/bin/env python3
"""
Generate baseline workflow outputs for multiple patterns and save them
under `baseline_out/` for deterministic comparison during the refactor.

Note: Uses programmatically constructed WorkflowSpec objects (to avoid
external YAML dependency) mirroring the approach in
`pocketflow-tools/test_full_generation_with_dependencies.py`.
"""

from pathlib import Path
from typing import Dict

import sys

# Local imports from tools folder
sys.path.insert(0, str(Path("pocketflow-tools")))

from generator import PocketFlowGenerator, WorkflowSpec  # type: ignore


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    baseline_root = repo_root / "baseline_out"
    ensure_dir(baseline_root)

    patterns = [
        "RAG",
        "AGENT",
        "TOOL",
        "WORKFLOW",
    ]

    print(f"Baseline output root: {baseline_root}")

    total_files: Dict[str, int] = {}

    for pattern in patterns:
        name = f"Baseline{pattern}Workflow"
        description = f"Baseline generation snapshot for {pattern} pattern"

        # Programmatic spec mirrors comprehensive tests (minimal fields)
        spec = WorkflowSpec(name=name, pattern=pattern, description=description)

        # Initialize generator with baseline output path
        generator = PocketFlowGenerator(output_path=str(baseline_root))

        # Generate and save
        output_files = generator.generate_workflow(spec)
        generator.save_workflow(spec, output_files)

        saved_root = baseline_root / spec.name.lower().replace(" ", "_")
        count = sum(1 for _ in saved_root.rglob("*") if _.is_file())
        total_files[pattern] = count

        print(f"Saved {count} files for {pattern} at: {saved_root}")

    grand_total = sum(total_files.values())
    print("\nBaseline snapshot complete.")
    print("Per-pattern file counts:")
    for p in patterns:
        print(f"  - {p}: {total_files.get(p, 0)} files")
    print(f"Grand total files: {grand_total}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

