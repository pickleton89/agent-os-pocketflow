from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class GenerationContext:
    """Shared generation context for Phase 1+.

    Internal-only wiring object to pass shared state between modules with no
    external API changes.
    """

    templates: Dict[str, str]
    extensions: Dict[str, Any]
    enable_hybrid_promotion: bool = False

