"""PocketFlow Tools package (framework-side).

This package houses the refactored generator modules used to create
PocketFlow workflow templates. It is part of the Agent OS + PocketFlow
framework repository (not an end-user application).
"""

from .spec import WorkflowSpec  # re-export for convenience

__all__ = [
    "WorkflowSpec",
]

