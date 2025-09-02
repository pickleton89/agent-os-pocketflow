from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Dict


logger = logging.getLogger(__name__)


class TemplateEngine:
    """Load templates and enhanced extensions for generation.

    Mirrors the legacy generator's behavior to preserve output parity.
    """

    def __init__(self, templates_path: Path) -> None:
        self.templates_path = templates_path

    def load_templates(self) -> Dict[str, str]:
        """Load all template files from the templates directory (*.md)."""
        templates: Dict[str, str] = {}
        for template_file in self.templates_path.glob("*.md"):
            templates[template_file.stem] = template_file.read_text()
        return templates

    def load_enhanced_extensions(self) -> Dict[str, Any]:
        """Load enhanced extensions for improved template generation.

        Follows the same fallback path logic as the legacy implementation:
        prefer ./instructions/extensions, then ../instructions/extensions.
        """
        extensions: Dict[str, Any] = {}

        extensions_path = Path("instructions/extensions")
        if not extensions_path.exists():
            extensions_path = Path("../instructions/extensions")
            if not extensions_path.exists():
                logging.warning(
                    "Enhanced extensions not found, using basic template generation"
                )
                return {}

        try:
            extension_files = {
                "design_enforcement": "design-first-enforcement.md",
                "llm_workflow": "llm-workflow-extension.md",
                "pocketflow_integration": "pocketflow-integration.md",
            }

            for key, filename in extension_files.items():
                ext_file = extensions_path / filename
                if ext_file.exists():
                    content = ext_file.read_text()
                    extensions[key] = self._parse_extension_templates(content)
                else:
                    logging.warning(f"Extension not found: {filename}")
        except Exception as e:  # pragma: no cover - defensive parity
            logging.warning(f"Failed to load enhanced extensions: {e}")
            return {}

        return extensions

    def _parse_extension_templates(self, content: str) -> Dict[str, Any]:
        """Parse extension content to extract template guidance.

        Matches the legacy regex-based extraction of code blocks and TODO lines.
        """
        templates: Dict[str, Any] = {
            "code_templates": [],
            "todo_guidance": [],
            "orchestrator_integration": [],
        }

        code_blocks = re.findall(r"```(?:python|bash)\n(.*?)```", content, re.DOTALL)
        templates["code_templates"] = code_blocks

        todo_lines = re.findall(r"#.*TODO:.*", content)
        templates["todo_guidance"] = todo_lines

        orchestrator_matches = re.findall(r"claude-code.*orchestrator[^\n]*", content)
        templates["orchestrator_integration"] = orchestrator_matches

        return templates

