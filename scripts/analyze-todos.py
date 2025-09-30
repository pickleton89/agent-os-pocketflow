#!/usr/bin/env python3
"""Categorize TODOs by type and priority.

This script analyzes TODO comments across the codebase and categorizes them
into different types (template placeholders, integrations, enhancements, bug fixes).

Usage:
    python scripts/analyze-todos.py > TODO_ANALYSIS.md
"""

import re
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple

# Root directory of the repository
REPO_ROOT = Path(__file__).parent.parent

# Directories to exclude from analysis
EXCLUDE_DIRS = {
    ".git", ".venv", "__pycache__", "node_modules",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "dist", "build", "*.egg-info"
}

# Files to exclude from analysis
EXCLUDE_FILES = {
    "TODO_ANALYSIS.md",  # Don't analyze our own output
}

# File extensions to search
INCLUDE_EXTENSIONS = {
    ".py", ".md", ".sh", ".yml", ".yaml", ".txt", ".json"
}

# TODO categorization patterns
TODO_CATEGORIES = {
    "TEMPLATE_PLACEHOLDER": [
        r"templates/",
        r"examples/",
        r"generated output",
        r"TODO: Implement business logic",
        r"TODO: Add your",
        r"TODO: Customize",
        r"TODO: Replace with actual",
        r"TODO: Define your",
    ],
    "INTEGRATION": [
        r"TODO: Integrate with",
        r"TODO: Connect to",
        r"TODO: Wire up",
        r"TODO: Hook up",
        r"TODO: Add integration",
    ],
    "ENHANCEMENT": [
        r"TODO: Consider",
        r"TODO: Future",
        r"TODO: Optional",
        r"TODO: Potential",
        r"TODO: Could",
        r"TODO: Maybe",
        r"TODO: Improve",
        r"TODO: Enhance",
    ],
    "BUG_FIX": [
        r"TODO: Fix",
        r"TODO: Debug",
        r"FIXME",
        r"TODO: Handle error",
        r"TODO: Add error handling",
    ],
    "DOCUMENTATION": [
        r"TODO: Document",
        r"TODO: Add docstring",
        r"TODO: Update docs",
        r"TODO: Write docs",
    ],
    "TESTING": [
        r"TODO: Test",
        r"TODO: Add test",
        r"TODO: Write test",
        r"TODO: Cover",
    ],
}


def should_skip_dir(path: Path) -> bool:
    """Check if directory should be skipped."""
    parts = path.parts
    return any(exclude in parts for exclude in EXCLUDE_DIRS)


def find_todos(file_path: Path) -> List[Tuple[int, str]]:
    """Find all TODO comments in a file.

    Returns:
        List of (line_number, todo_text) tuples
    """
    todos = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                # Match TODO, FIXME, XXX patterns
                if re.search(r'\b(TODO|FIXME|XXX)\b', line, re.IGNORECASE):
                    todos.append((line_num, line.strip()))
    except Exception as e:
        print(f"Error reading {file_path}: {e}", file=sys.stderr)

    return todos


def categorize_todo(file_path: Path, todo_text: str) -> str:
    """Categorize a TODO based on patterns and file location.

    Returns:
        Category name
    """
    file_str = str(file_path)
    combined_text = f"{file_str} {todo_text}"

    # Check each category's patterns
    for category, patterns in TODO_CATEGORIES.items():
        for pattern in patterns:
            if re.search(pattern, combined_text, re.IGNORECASE):
                return category

    return "UNCATEGORIZED"


def analyze_todos() -> Dict[str, List[Tuple[Path, int, str]]]:
    """Analyze all TODOs in the repository.

    Returns:
        Dictionary mapping category names to lists of (file_path, line_num, todo_text)
    """
    categorized_todos = defaultdict(list)

    for file_path in REPO_ROOT.rglob("*"):
        # Skip directories and excluded paths
        if file_path.is_dir() or should_skip_dir(file_path):
            continue

        # Skip excluded files
        if file_path.name in EXCLUDE_FILES:
            continue

        # Only process files with relevant extensions
        if file_path.suffix not in INCLUDE_EXTENSIONS:
            continue

        # Find TODOs in this file
        todos = find_todos(file_path)

        # Categorize each TODO
        for line_num, todo_text in todos:
            category = categorize_todo(file_path, todo_text)
            relative_path = file_path.relative_to(REPO_ROOT)
            categorized_todos[category].append((relative_path, line_num, todo_text))

    return categorized_todos


def generate_report(categorized_todos: Dict[str, List[Tuple[Path, int, str]]]) -> None:
    """Generate markdown report of categorized TODOs."""

    print("# TODO Analysis Report")
    print()
    print(f"Generated: {Path.cwd()}")
    print()

    # Summary statistics
    total_todos = sum(len(todos) for todos in categorized_todos.values())
    print(f"## Summary")
    print()
    print(f"**Total TODOs**: {total_todos}")
    print()

    # Category breakdown
    print("### By Category")
    print()
    for category in sorted(TODO_CATEGORIES.keys()) + ["UNCATEGORIZED"]:
        count = len(categorized_todos.get(category, []))
        percentage = (count / total_todos * 100) if total_todos > 0 else 0
        print(f"- **{category}**: {count} ({percentage:.1f}%)")
    print()

    # Recommended actions
    print("## Recommended Actions")
    print()
    print("### Template Placeholders")
    template_count = len(categorized_todos.get("TEMPLATE_PLACEHOLDER", []))
    print(f"**{template_count} TODOs** - These are intentional features. Keep as educational markers.")
    print()

    print("### Integration TODOs")
    integration_count = len(categorized_todos.get("INTEGRATION", []))
    print(f"**{integration_count} TODOs** - Convert to GitHub issues with `integration` label.")
    print()

    print("### Enhancement TODOs")
    enhancement_count = len(categorized_todos.get("ENHANCEMENT", []))
    print(f"**{enhancement_count} TODOs** - Convert to GitHub issues with `enhancement` label.")
    print()

    print("### Bug Fix TODOs")
    bugfix_count = len(categorized_todos.get("BUG_FIX", []))
    print(f"**{bugfix_count} TODOs** - Convert to GitHub issues with `bug` label. **Prioritize these!**")
    print()

    print("### Documentation TODOs")
    doc_count = len(categorized_todos.get("DOCUMENTATION", []))
    print(f"**{doc_count} TODOs** - Convert to GitHub issues with `documentation` label.")
    print()

    print("### Testing TODOs")
    test_count = len(categorized_todos.get("TESTING", []))
    print(f"**{test_count} TODOs** - Convert to GitHub issues with `testing` label.")
    print()

    # Detailed listings
    print("## Detailed Listings")
    print()

    for category in sorted(TODO_CATEGORIES.keys()) + ["UNCATEGORIZED"]:
        todos = categorized_todos.get(category, [])
        if not todos:
            continue

        print(f"### {category} ({len(todos)} items)")
        print()

        # Group by file
        by_file = defaultdict(list)
        for file_path, line_num, todo_text in todos:
            by_file[file_path].append((line_num, todo_text))

        # Print grouped by file
        for file_path in sorted(by_file.keys()):
            print(f"#### {file_path}")
            print()
            for line_num, todo_text in sorted(by_file[file_path]):
                # Clean up the TODO text for display
                clean_text = todo_text.replace("#", "").replace("//", "").strip()
                print(f"- Line {line_num}: `{clean_text}`")
            print()


def main():
    """Main entry point."""
    print("Analyzing TODOs...", file=sys.stderr)
    categorized_todos = analyze_todos()
    print(f"Found {sum(len(t) for t in categorized_todos.values())} TODOs", file=sys.stderr)
    print("Generating report...", file=sys.stderr)
    generate_report(categorized_todos)


if __name__ == "__main__":
    main()
