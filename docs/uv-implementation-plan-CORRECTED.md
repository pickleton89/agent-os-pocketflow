# Agent OS + PocketFlow - uv Installation Implementation Plan (CORRECTED)

**Version**: 2.0 (Corrected)
**Date**: 2025-09-30
**Status**: Ready for Implementation
**Estimated Duration**: 10-14 days
**Risk Level**: Low (backward compatible)

---

## Executive Summary

Transform Agent OS + PocketFlow from bash script distribution to modern Python package distribution using **uv** tooling.

### What We're Building

**Current (bash scripts)**:
```bash
curl .../base.sh | bash
~/.agent-os/setup/project.sh
```

**New (Python package)**:
```bash
uvx agent-os-pocketflow init
# or
uv tool install agent-os-pocketflow
agent-os init
```

### Key Changes from Original Plan

1. ✅ Create **separate installer CLI** (don't break existing workflow generation CLI)
2. ✅ Use **version 2.0.0** (not 3.0.0)
3. ✅ **Add dependencies first** (`uv add click rich`)
4. ✅ **Move data files + symlinks** (not copy - avoid duplication)
5. ✅ Use **git rev-parse** for repo root (not hard-coded paths)
6. ✅ **Install editable mode** before testing entry points

---

## Path Conventions

**Throughout this document**:
```bash
# Use this to always get repo root
cd "$(git rev-parse --show-toplevel)"
```

All commands assume you start from repository root.

---

## Prerequisites

### Verify What We Have

```bash
cd "$(git rev-parse --show-toplevel)"

# Check current structure
ls -la pocketflow_tools/
# Should show: cli.py, generators/, spec.py

# Check data directories exist
ls -la | grep -E "instructions|standards|templates|claude-code"
# Should show all four directories

# Check current version
grep "^version" pyproject.toml
# Shows: version = "0.1.0"

# Verify uv is working
uv --version
```

### Current Package State

```
agent-os-pocketflow/
├── pocketflow_tools/          # Python package
│   ├── cli.py                 # Workflow generation CLI (argparse)
│   ├── generators/            # Template generators
│   └── spec.py                # Workflow specs
├── instructions/              # Framework instructions
├── standards/                 # Coding standards
├── templates/                 # PocketFlow templates
├── claude-code/               # Claude Code integration templates
└── pyproject.toml             # Package config (version 0.1.0)
```

---

## Phase 1: Package Structure Setup (2-3 days)

### Step 1.1: Add Python Dependencies

**Why first**: Code we'll write needs these packages

```bash
cd "$(git rev-parse --show-toplevel)"

# Add CLI dependencies
uv add click rich

# Verify installation
uv run python -c "import click, rich; print('✅ Dependencies installed')"

# Check they're in pyproject.toml
grep -A 5 "dependencies" pyproject.toml
# Should now show: click>=8.1.0, rich>=13.0.0
```

**Expected result**:
```toml
dependencies = [
    "pyyaml>=6.0.2",
    "click>=8.1.0",
    "rich>=13.0.0",
]
```

**Deliverable**: Dependencies installed and in pyproject.toml

---

### Step 1.2: Update Package Configuration

**Action**: Update pyproject.toml for distribution

```bash
cd "$(git rev-parse --show-toplevel)"

# Backup current config
cp pyproject.toml pyproject.toml.backup
```

**Edit pyproject.toml** - Update these sections:

```toml
[project]
name = "agent-os-pocketflow"
version = "2.0.0"  # Changed from 0.1.0 (major refactor)
description = "Agent OS + PocketFlow Framework - LLM workflow generation"
readme = "README.md"
requires-python = ">=3.12"
authors = [
    {name = "Agent OS Contributors", email = "contact@example.com"}
]
license = {text = "MIT"}
keywords = ["llm", "workflow", "pocketflow", "agent", "code-generator"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Programming Language :: Python :: 3.12",
    "Topic :: Software Development :: Code Generators",
    "Topic :: Software Development :: Libraries :: Application Frameworks",
]

dependencies = [
    "pyyaml>=6.0.2",
    "click>=8.1.0",   # CLI framework
    "rich>=13.0.0",   # Pretty terminal output
]

[project.optional-dependencies]
dev = [
    "pytest>=8.4.1",
    "pytest-cov>=6.0.0",
    "coverage[toml]>=7.6.0",
    "ruff>=0.1.0",
]

# CLI entry points - BOTH old and new
[project.scripts]
pocketflow-generate = "pocketflow_tools.cli:main"              # Keep existing workflow CLI
agent-os = "pocketflow_tools.installer_cli:main"               # New installer CLI

# Include data files in package
[tool.setuptools.package-data]
pocketflow_tools = [
    "data/instructions/**/*.md",
    "data/standards/**/*.md",
    "data/templates/**/*",
    "data/claude-code/**/*.md",
]

[tool.setuptools.packages.find]
where = ["."]
include = ["pocketflow_tools*"]
exclude = ["setup*", "tests*", "docs*"]
```

**Test configuration**:
```bash
# Validate TOML syntax
python3 -c "import tomllib; tomllib.load(open('pyproject.toml', 'rb'))" && echo "✅ Valid TOML"
```

**Deliverable**: Updated pyproject.toml with correct version, entry points, and data files

---

### Step 1.3: Reorganize Data Files into Package

**Critical Decision**: Use **move + symlinks** approach
- Moves files into package (single source of truth)
- Creates symlinks at root (bash scripts keep working)
- No duplication, backward compatible

```bash
cd "$(git rev-parse --show-toplevel)"

# Create data directory in package
mkdir -p pocketflow_tools/data

# Move data files INTO package
echo "Moving data files into package..."
mv instructions pocketflow_tools/data/
mv standards pocketflow_tools/data/
mv templates pocketflow_tools/data/
mv claude-code pocketflow_tools/data/

# Create symlinks at root for backward compatibility with bash scripts
echo "Creating symlinks for bash script compatibility..."
ln -s pocketflow_tools/data/instructions instructions
ln -s pocketflow_tools/data/standards standards
ln -s pocketflow_tools/data/templates templates
ln -s pocketflow_tools/data/claude-code claude-code

# Verify symlinks created
ls -la | grep -E "instructions|standards|templates|claude-code"
# Should show: lrwxr-xr-x ... instructions -> pocketflow_tools/data/instructions

# Verify real data exists
ls -la pocketflow_tools/data/
# Should show: claude-code/, instructions/, standards/, templates/

echo "✅ Data reorganization complete"
```

**Create data module** for Python access:

```bash
cat > pocketflow_tools/data/__init__.py << 'EOF'
"""
Data files for Agent OS + PocketFlow.

This module provides access to bundled instructions, standards,
templates, and Claude Code configurations packaged with the framework.
"""
from pathlib import Path

# Data directory location
DATA_DIR = Path(__file__).parent

# Subdirectories
INSTRUCTIONS_DIR = DATA_DIR / "instructions"
STANDARDS_DIR = DATA_DIR / "standards"
TEMPLATES_DIR = DATA_DIR / "templates"
CLAUDE_CODE_DIR = DATA_DIR / "claude-code"

__all__ = [
    "DATA_DIR",
    "INSTRUCTIONS_DIR",
    "STANDARDS_DIR",
    "TEMPLATES_DIR",
    "CLAUDE_CODE_DIR",
]
EOF
```

**Test data access**:
```bash
cd "$(git rev-parse --show-toplevel)"

# Test Python can access data
uv run python -c "
from pocketflow_tools.data import INSTRUCTIONS_DIR, STANDARDS_DIR
print(f'Instructions: {INSTRUCTIONS_DIR}')
print(f'Standards: {STANDARDS_DIR}')
print(f'Exists: {INSTRUCTIONS_DIR.exists()}')
"
# Should print paths and "Exists: True"

# Test bash scripts can still access via symlinks
ls -la instructions/
# Should show files (following symlink)
```

**Update .gitignore** to clarify symlinks:

```bash
cat >> .gitignore << 'EOF'

# Data organization: Real files in pocketflow_tools/data/, symlinks at root
# Symlinks tracked by git, actual data in package
EOF
```

**Deliverable**:
- Data files in `pocketflow_tools/data/`
- Symlinks at root for compatibility
- Python module for accessing data

---

### Step 1.4: Create Installer Module

**Action**: Build installation logic in Python

**Create** `pocketflow_tools/installer.py`:

```python
"""
Agent OS + PocketFlow Installer.

Handles project initialization and toolkit installation.
"""
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel

from pocketflow_tools.data import (
    INSTRUCTIONS_DIR,
    STANDARDS_DIR,
    TEMPLATES_DIR,
    CLAUDE_CODE_DIR,
)

console = Console()


class InstallationError(Exception):
    """Raised when installation fails."""


def copy_directory(src: Path, dest: Path, description: str = "files") -> None:
    """
    Copy directory with validation and progress indication.

    Args:
        src: Source directory path
        dest: Destination directory path
        description: Human-readable description for logging

    Raises:
        InstallationError: If copy fails
    """
    console.print(f"📦 Copying {description}...")
    try:
        shutil.copytree(src, dest, dirs_exist_ok=True)
    except Exception as e:
        raise InstallationError(f"Failed to copy {description}: {e}")


class AgentOSInstaller:
    """Handles Agent OS installation to projects."""

    def __init__(self, target_dir: Path):
        """
        Initialize installer.

        Args:
            target_dir: Directory to install Agent OS into
        """
        self.target_dir = target_dir.resolve()
        self.agent_os_dir = self.target_dir / ".agent-os"

    def is_project_directory(self) -> bool:
        """
        Check if target looks like a project directory.

        Returns:
            True if directory has project markers (.git, pyproject.toml, etc.)
        """
        markers = [
            self.target_dir / ".git",
            self.target_dir / "pyproject.toml",
            self.target_dir / "setup.py",
            self.target_dir / "package.json",
            self.target_dir / "Cargo.toml",
        ]
        return any(marker.exists() for marker in markers)

    def check_existing_installation(self) -> bool:
        """
        Check if Agent OS is already installed.

        Returns:
            True if .agent-os directory exists
        """
        return self.agent_os_dir.exists()

    def install_project_mode(
        self,
        enable_claude_code: bool = False,
        force: bool = False,
    ) -> None:
        """
        Install Agent OS in project mode.

        Creates .agent-os/ directory with all framework files.

        Args:
            enable_claude_code: Whether to install Claude Code integration
            force: Overwrite existing installation if present

        Raises:
            InstallationError: If installation fails or preconditions not met
        """
        # Validate target directory
        if not self.is_project_directory():
            raise InstallationError(
                f"Not a project directory: {self.target_dir}\n"
                "Expected .git, pyproject.toml, or similar project markers\n"
                "Run this command from your project root"
            )

        # Check existing installation
        if self.check_existing_installation() and not force:
            raise InstallationError(
                f"Agent OS already installed at {self.agent_os_dir}\n"
                "Use --force to overwrite existing installation"
            )

        console.print(
            Panel(
                "[bold blue]Installing Agent OS + PocketFlow...[/bold blue]",
                title="🚀 Agent OS Installer",
                border_style="blue",
            )
        )

        # Create .agent-os directory
        self.agent_os_dir.mkdir(exist_ok=True)

        # Copy core framework files
        copy_directory(INSTRUCTIONS_DIR, self.agent_os_dir / "instructions", "instructions")
        copy_directory(STANDARDS_DIR, self.agent_os_dir / "standards", "standards")
        copy_directory(TEMPLATES_DIR, self.agent_os_dir / "templates", "templates")

        # Create project-specific directories
        (self.agent_os_dir / "product").mkdir(exist_ok=True)
        (self.agent_os_dir / "specs").mkdir(exist_ok=True)
        (self.agent_os_dir / "recaps").mkdir(exist_ok=True)
        console.print("📁 Created project directories")

        # Create config file
        self._create_config(enable_claude_code=enable_claude_code)

        # Install Claude Code if requested
        if enable_claude_code:
            self._install_claude_code()

        # Update .gitignore
        self._update_gitignore()

        console.print("\n[bold green]✅ Installation complete![/bold green]")
        console.print(f"\n📍 Agent OS installed at: [cyan]{self.agent_os_dir.relative_to(self.target_dir)}[/cyan]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("  • Run [cyan]agent-os plan[/cyan] to start a new product")
        console.print("  • Run [cyan]agent-os analyze[/cyan] for existing projects")
        console.print("  • See [cyan].agent-os/instructions/[/cyan] for workflow documentation")

    def _create_config(self, enable_claude_code: bool) -> None:
        """Create .agent-os/config.yml."""
        config_content = f"""# Agent OS + PocketFlow Configuration
# Generated: {datetime.now().strftime('%Y-%m-%d')}

version: "2.0.0"
installation_mode: "standalone"
installed_via: "uv-package"
created: "{datetime.now().strftime('%Y-%m-%d')}"

# Tool configuration
tools:
  pocketflow: true
  claude_code: {str(enable_claude_code).lower()}

# Project paths
paths:
  instructions: ".agent-os/instructions"
  standards: ".agent-os/standards"
  templates: ".agent-os/templates"
  product: ".agent-os/product"
  specs: ".agent-os/specs"
  recaps: ".agent-os/recaps"

# Framework identification
framework:
  name: "Agent OS + PocketFlow"
  description: "LLM workflow generation framework"
  repository: "https://github.com/pickleton89/agent-os-pocketflow"
  installed_from: "Python package"
"""
        config_path = self.agent_os_dir / "config.yml"
        config_path.write_text(config_content)
        console.print(f"📝 Created config: [cyan]{config_path.relative_to(self.target_dir)}[/cyan]")

    def _install_claude_code(self) -> None:
        """Install Claude Code integration."""
        claude_dir = self.target_dir / ".claude"
        claude_dir.mkdir(exist_ok=True)

        # Copy commands
        commands_src = CLAUDE_CODE_DIR / "commands"
        commands_dest = claude_dir / "commands"
        if commands_src.exists():
            copy_directory(commands_src, commands_dest, "Claude Code commands")
        else:
            console.print("[yellow]⚠️  No Claude Code commands found in package[/yellow]")

        # Copy agents
        agents_src = CLAUDE_CODE_DIR / "agents"
        agents_dest = claude_dir / "agents"
        if agents_src.exists():
            copy_directory(agents_src, agents_dest, "Claude Code agents")
        else:
            console.print("[yellow]⚠️  No Claude Code agents found in package[/yellow]")

        console.print("🤖 Installed Claude Code integration")

    def _update_gitignore(self) -> None:
        """Update .gitignore with Agent OS entries."""
        gitignore_path = self.target_dir / ".gitignore"

        agent_os_entries = """
# Agent OS + PocketFlow
.agent-os/__pycache__/
.agent-os/*.pyc
.agent-os/product/*.tmp
.agent-os/specs/*.tmp
.agent-os/recaps/*.tmp
"""

        if gitignore_path.exists():
            content = gitignore_path.read_text()
            if "Agent OS" not in content:
                with gitignore_path.open("a") as f:
                    f.write(agent_os_entries)
                console.print("📝 Updated .gitignore")
        else:
            gitignore_path.write_text(agent_os_entries.lstrip())
            console.print("📝 Created .gitignore")


class ToolkitInstaller:
    """Handles toolkit installation to ~/.agent-os (optional optimization)."""

    def __init__(self, toolkit_path: Optional[Path] = None):
        """
        Initialize toolkit installer.

        Args:
            toolkit_path: Custom toolkit location (default: ~/.agent-os)
        """
        self.toolkit_path = toolkit_path or Path.home() / ".agent-os"

    def install(self, force: bool = False) -> None:
        """
        Install toolkit to system location.

        The toolkit provides a local cache of framework files for faster
        project creation. Projects will automatically use it if present.

        Args:
            force: Overwrite existing toolkit

        Raises:
            InstallationError: If installation fails
        """
        if self.toolkit_path.exists() and not force:
            raise InstallationError(
                f"Toolkit already exists at {self.toolkit_path}\n"
                "Use --force to overwrite, or specify different --path"
            )

        console.print(
            Panel(
                f"[bold blue]Installing toolkit to {self.toolkit_path}...[/bold blue]",
                title="🧰 Toolkit Installer",
                border_style="blue",
            )
        )

        # Create toolkit directory
        self.toolkit_path.mkdir(parents=True, exist_ok=True)

        # Copy framework data files
        copy_directory(INSTRUCTIONS_DIR, self.toolkit_path / "instructions", "instructions")
        copy_directory(STANDARDS_DIR, self.toolkit_path / "standards", "standards")
        copy_directory(TEMPLATES_DIR, self.toolkit_path / "templates", "templates")

        # Create toolkit config
        self._create_config()

        console.print("\n[bold green]✅ Toolkit installed![/bold green]")
        console.print(f"\n📍 Toolkit location: [cyan]{self.toolkit_path}[/cyan]")
        console.print("\n[bold]How it works:[/bold]")
        console.print("  • Projects will automatically use this toolkit for faster setup")
        console.print("  • Toolkit provides local cache (no network needed)")
        console.print("  • Update toolkit: [cyan]agent-os install-toolkit --force[/cyan]")

    def _create_config(self) -> None:
        """Create toolkit configuration."""
        config_content = f"""# Agent OS + PocketFlow Toolkit Configuration
version: "2.0.0"
installation_type: "toolkit"
created: "{datetime.now().strftime('%Y-%m-%d')}"
description: "Local cache for faster project setup"
"""
        config_path = self.toolkit_path / "config.yml"
        config_path.write_text(config_content)
        console.print(f"📝 Created toolkit config")
```

**Test installer module**:
```bash
cd "$(git rev-parse --show-toplevel)"

# Test imports
uv run python -c "
from pocketflow_tools.installer import AgentOSInstaller, ToolkitInstaller
print('✅ Installer module loads successfully')
"

# Test instantiation
uv run python -c "
from pathlib import Path
from pocketflow_tools.installer import AgentOSInstaller
installer = AgentOSInstaller(Path('/tmp/test'))
print(f'✅ Installer created: {installer.target_dir}')
"
```

**Deliverable**: Working `pocketflow_tools/installer.py` module

---

### Step 1.5: Create Installer CLI (Separate from Workflow CLI)

**Why separate**: Existing `cli.py` is for workflow generation (argparse). Don't break it.

**Create** `pocketflow_tools/installer_cli.py`:

```python
"""
Agent OS + PocketFlow Installer CLI.

Separate from workflow generation CLI to avoid breaking existing functionality.
"""
import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console

from pocketflow_tools.installer import (
    AgentOSInstaller,
    ToolkitInstaller,
    InstallationError,
)

console = Console()

__version__ = "2.0.0"


@click.group()
@click.version_option(version=__version__, prog_name="agent-os")
def main():
    """
    Agent OS + PocketFlow installer.

    Initialize Agent OS in your project or install the optional toolkit.
    """
    pass


@main.command()
@click.option(
    "--claude-code",
    is_flag=True,
    help="Install Claude Code integration (.claude/ directory)",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing installation",
)
@click.option(
    "--directory",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    default=Path.cwd(),
    help="Target directory (default: current directory)",
)
def init(claude_code: bool, force: bool, directory: Path):
    """
    Initialize Agent OS in a project.

    Creates .agent-os/ directory with all framework files.

    \b
    Examples:
        agent-os init
        agent-os init --claude-code
        agent-os init --directory /path/to/project
        agent-os init --force  # Overwrite existing
    """
    try:
        installer = AgentOSInstaller(directory)
        installer.install_project_mode(
            enable_claude_code=claude_code,
            force=force,
        )
    except InstallationError as e:
        console.print(f"\n[bold red]Installation failed:[/bold red] {e}\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {e}\n")
        console.print_exception()
        sys.exit(1)


@main.command()
@click.option(
    "--path",
    type=click.Path(file_okay=False, path_type=Path),
    default=None,
    help="Custom toolkit location (default: ~/.agent-os)",
)
@click.option(
    "--force",
    is_flag=True,
    help="Overwrite existing toolkit",
)
def install_toolkit(path: Optional[Path], force: bool):
    """
    Install reusable toolkit (optional optimization).

    The toolkit speeds up project creation by caching framework files locally.
    Projects automatically use it if present.

    \b
    Examples:
        agent-os install-toolkit
        agent-os install-toolkit --path ~/my-toolkit
        agent-os install-toolkit --force  # Update existing
    """
    try:
        installer = ToolkitInstaller(toolkit_path=path)
        installer.install(force=force)
    except InstallationError as e:
        console.print(f"\n[bold red]Installation failed:[/bold red] {e}\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Unexpected error:[/bold red] {e}\n")
        console.print_exception()
        sys.exit(1)


@main.command()
def plan():
    """
    Start planning a new product (coming soon).

    This will invoke the /plan-product workflow.
    """
    console.print("[yellow]🚧 Feature coming soon![/yellow]")
    console.print("\nThis command will help you:")
    console.print("  • Define product vision and mission")
    console.print("  • Create initial roadmap")
    console.print("  • Set up product documentation")
    console.print("\nFor now, see: [cyan].agent-os/instructions/core/plan-product.md[/cyan]")


@main.command()
def analyze():
    """
    Analyze existing product (coming soon).

    This will invoke the /analyze-product workflow.
    """
    console.print("[yellow]🚧 Feature coming soon![/yellow]")
    console.print("\nThis command will help you:")
    console.print("  • Analyze existing codebase")
    console.print("  • Generate product documentation")
    console.print("  • Create roadmap from current state")
    console.print("\nFor now, see: [cyan].agent-os/instructions/core/analyze-product.md[/cyan]")


if __name__ == "__main__":
    main()
```

**Test CLI module**:
```bash
cd "$(git rev-parse --show-toplevel)"

# Test imports
uv run python -c "
from pocketflow_tools.installer_cli import main
print('✅ Installer CLI module loads successfully')
"

# Test help (doesn't need installation)
uv run python -m pocketflow_tools.installer_cli --help
uv run python -m pocketflow_tools.installer_cli init --help
uv run python -m pocketflow_tools.installer_cli install-toolkit --help
```

**Deliverable**: Working `pocketflow_tools/installer_cli.py` module

---

## Phase 2: Integration & Local Testing (3-4 days)

### Step 2.1: Install Package in Editable Mode

**Action**: Make `agent-os` command available locally

```bash
cd "$(git rev-parse --show-toplevel)"

# Install package in editable mode
uv pip install -e .

# Verify entry points created
which agent-os
which pocketflow-generate

# Test version
agent-os --version
# Should show: agent-os, version 2.0.0

# Test help
agent-os --help
agent-os init --help
agent-os install-toolkit --help

# Verify old workflow CLI still works
pocketflow-generate --help
# Should show existing argparse help for --spec, --output
```

**Expected**:
- ✅ `agent-os` command available
- ✅ `pocketflow-generate` still works (backward compatible)
- ✅ Help text displays correctly
- ✅ No import errors

**Deliverable**: Package installed locally with both CLIs working

---

### Step 2.2: Test Installation in Mock Project

**Action**: Create test project and install Agent OS

```bash
# Create test project
cd /tmp
rm -rf test-agent-os-init
mkdir test-agent-os-init && cd test-agent-os-init

# Make it look like a project
git init
echo "# Test Project" > README.md
git add README.md
git commit -m "Initial commit"

# Install Agent OS
agent-os init

# Verify installation
ls -la .agent-os/
# Should show: config.yml, instructions/, standards/, templates/, product/, specs/

# Check config
cat .agent-os/config.yml
# Should show version 2.0.0, installation_mode: standalone

# Check instructions exist
ls .agent-os/instructions/core/
# Should show: plan-product.md, analyze-product.md, etc.

# Verify .gitignore updated
cat .gitignore
# Should include Agent OS entries

echo "✅ Test installation successful"
```

**Expected**:
- ✅ `.agent-os/` directory created
- ✅ All subdirectories populated
- ✅ Config file correct
- ✅ .gitignore updated

---

### Step 2.3: Test Claude Code Integration

```bash
# Test with Claude Code flag
cd /tmp
rm -rf test-claude-code
mkdir test-claude-code && cd test-claude-code
git init

# Install with Claude Code
agent-os init --claude-code

# Verify .claude directory created
ls -la .claude/
# Should show: commands/, agents/

# Check commands
ls .claude/commands/
# Should show: plan-product.md, analyze-product.md, etc.

# Check agents
ls .claude/agents/
# Should show various agent .md files

echo "✅ Claude Code integration works"
```

---

### Step 2.4: Test Toolkit Installation

```bash
# Install toolkit
agent-os install-toolkit

# Verify toolkit created
ls -la ~/.agent-os/
# Should show: config.yml, instructions/, standards/, templates/

# Check toolkit config
cat ~/.agent-os/config.yml
# Should show installation_type: toolkit

# Test using toolkit for new project
cd /tmp
rm -rf test-with-toolkit
mkdir test-with-toolkit && cd test-with-toolkit
git init

# Install (should be faster using toolkit)
time agent-os init

# Verify it worked
ls -la .agent-os/

echo "✅ Toolkit installation and usage works"
```

---

### Step 2.5: Test Force Overwrite

```bash
cd /tmp/test-agent-os-init

# Try to install again (should fail)
agent-os init
# Should show error: "Agent OS already installed"

# Force reinstall
agent-os init --force

# Verify it reinstalled
ls -la .agent-os/

echo "✅ Force overwrite works"
```

---

### Step 2.6: Test Error Conditions

```bash
# Test in non-project directory
cd /tmp
rm -rf not-a-project
mkdir not-a-project && cd not-a-project
# No .git, no pyproject.toml

agent-os init
# Should show error: "Not a project directory"

# Test invalid directory
agent-os init --directory /nonexistent/path
# Should show error about directory not existing

echo "✅ Error handling works"
```

---

### Step 2.7: Verify Backward Compatibility

**Action**: Ensure bash scripts still work with symlinks

```bash
cd "$(git rev-parse --show-toplevel)"

# Test bash scripts can still find files via symlinks
ls -la instructions/
# Should work (symlink to pocketflow_tools/data/instructions/)

cat instructions/core/plan-product.md | head -5
# Should display file contents

# Test base.sh still works (if needed)
# ./setup/base.sh --help

echo "✅ Backward compatibility maintained"
```

---

## Phase 3: uvx Testing (2-3 days)

### Step 3.1: Test with uvx (No Installation)

**Action**: Test running directly with uvx

```bash
cd /tmp
rm -rf test-uvx
mkdir test-uvx && cd test-uvx
git init

# Run without installing package
uvx --from "$(git rev-parse --show-toplevel)" agent-os init

# Verify it worked
ls -la .agent-os/

echo "✅ uvx execution works"
```

---

### Step 3.2: Test uv tool install (Global)

```bash
cd "$(git rev-parse --show-toplevel)"

# Install as uv tool
uv tool install .

# Verify global installation
which agent-os

# Test from anywhere
cd /tmp
agent-os --version

# Test creating project
mkdir test-global && cd test-global
git init
agent-os init

ls -la .agent-os/

echo "✅ uv tool install works"

# Cleanup
uv tool uninstall agent-os-pocketflow
```

---

### Step 3.3: Test in CI/CD Environment (Docker)

**Action**: Simulate CI environment

Create test Dockerfile:

```bash
cd "$(git rev-parse --show-toplevel)"

cat > Dockerfile.test << 'EOF'
FROM python:3.12-slim

# Install uv
RUN pip install uv

# Create test project
WORKDIR /workspace
RUN git init && \
    echo "# Test" > README.md && \
    git config user.email "test@example.com" && \
    git config user.name "Test" && \
    git add . && \
    git commit -m "init"

# Copy package
COPY . /agent-os-package

# Install and run
RUN cd /agent-os-package && uv pip install -e .
RUN agent-os init

# Verify
RUN ls -la .agent-os/
RUN cat .agent-os/config.yml

CMD ["echo", "✅ CI/CD test passed"]
EOF

# Test in Docker
docker build -f Dockerfile.test -t agent-os-test .
docker run --rm agent-os-test

# Cleanup
rm Dockerfile.test
docker rmi agent-os-test
```

---

## Phase 4: Documentation & Release (2-3 days)

### Step 4.1: Update README.md

**Action**: Add uv installation instructions

Add this section to README.md:

```markdown
## 🚀 Installation

Agent OS + PocketFlow is now distributed as a modern Python package via uv.

### Quick Start (Recommended)

**Try without installing**:
```bash
cd your-project
uvx agent-os-pocketflow init
```

**Install as global tool**:
```bash
uv tool install agent-os-pocketflow
agent-os init
```

**Install in project environment**:
```bash
cd your-project
uv add --dev agent-os-pocketflow
uv run agent-os init
```

### With Claude Code Integration

```bash
agent-os init --claude-code
```

This installs:
- `.agent-os/` - Framework files (instructions, standards, templates)
- `.claude/` - Claude Code commands and agents

### Optional: Toolkit for Faster Setup

For power users creating many projects:

```bash
# Install toolkit once
agent-os install-toolkit

# Create projects (faster - uses local cache)
cd project1 && agent-os init
cd project2 && agent-os init
```

### What Gets Installed

```
your-project/
├── .agent-os/                 # Framework files
│   ├── instructions/          # Workflow instructions
│   ├── standards/             # Coding standards
│   ├── templates/             # PocketFlow templates
│   ├── product/               # Product documentation
│   ├── specs/                 # Feature specs
│   └── config.yml             # Configuration
├── .claude/                   # Claude Code (if --claude-code)
│   ├── commands/              # Slash commands
│   └── agents/                # AI agents
└── [your project files]
```

### Legacy Installation (Bash Scripts)

The old bash-based installation still works but is deprecated:

```bash
curl -sSL https://raw.githubusercontent.com/pickleton89/agent-os-pocketflow/main/setup.sh | bash
```

We recommend migrating to the uv-based installation.

### Available Commands

```bash
agent-os init              # Initialize in current project
agent-os init --force      # Overwrite existing installation
agent-os install-toolkit   # Install optional toolkit
agent-os --help            # Show all commands
agent-os --version         # Show version
```

### Workflow Generation (Existing)

PocketFlow workflow generation continues to work:

```bash
pocketflow-generate --spec workflow.yml --output .agent-os/workflows
```
```

---

### Step 4.2: Create Migration Guide

**Create** `docs/MIGRATION_GUIDE.md`:

```markdown
# Migration Guide: Bash → uv Package

## For New Users

**Just use the new way**:
```bash
uvx agent-os-pocketflow init
```

Done! No bash scripts needed.

## For Existing Users

### If You Have ~/.agent-os/ Installed

**Nothing breaks**:
- ✅ Existing projects continue working
- ✅ Bash scripts still function (via symlinks)
- ✅ New projects can use either method

**Optional: Migrate to uv**:
```bash
# Install new tool
uv tool install agent-os-pocketflow

# Create new projects with uv
cd new-project
agent-os init

# Old projects unchanged
cd old-project
ls .agent-os/  # Still works
```

### If You Use Bash Scripts in CI/CD

**Before** (.github/workflows/test.yml):
```yaml
- name: Install Agent OS
  run: curl .../setup.sh | bash --standalone
```

**After**:
```yaml
- name: Install Agent OS
  run: |
    pip install uv
    uvx agent-os-pocketflow init
```

**Benefits**:
- Faster (no curl to GitHub)
- Version pinning possible
- Standard Python tooling

### Toolkit Users

**Your ~/.agent-os/ continues working**:
- Bash scripts will use it
- Python package doesn't need it
- Keep it or remove it - your choice

**Migrate to new toolkit**:
```bash
# Remove old bash-based toolkit
rm -rf ~/.agent-os/

# Install new Python-based toolkit
agent-os install-toolkit

# Faster project creation
cd project && agent-os init
```

## Benefits of Migration

| Aspect | Bash Scripts | uv Package |
|--------|--------------|------------|
| Distribution | GitHub raw URLs | PyPI (standard) |
| Versioning | Git tags | Semantic versioning |
| Offline | Requires toolkit | pip cache |
| CI/CD | curl downloads | pip install |
| Updates | Manual | uv/pip upgrade |
| Cross-platform | bash required | Python everywhere |

## Timeline

- **Now**: Both methods work (choose your preference)
- **6 months**: uv recommended, bash supported
- **12 months**: bash deprecated, migration guides
- **18 months**: bash may be removed (TBD)

No forced migration - use what works for you!
```

---

### Step 4.3: Update CHANGELOG.md

Add entry:

```markdown
## [2.0.0] - 2025-XX-XX

### 🎉 Major: Modern Python Package Distribution

**Breaking Changes**: None (fully backward compatible)

**What's New**:
- **uv-native distribution**: Install via `uvx` or `uv tool install`
- **Separate installer CLI**: `agent-os` command for installation
- **Python package**: Data files bundled, no bash scripts required
- **Maintained compatibility**: Bash scripts still work via symlinks

**Installation**:
```bash
# New way (recommended)
uvx agent-os-pocketflow init

# Old way (still works)
curl .../setup.sh | bash
```

**Technical Changes**:
- Added `click` and `rich` dependencies
- Created `pocketflow_tools.installer` module
- Created `pocketflow_tools.installer_cli` module
- Moved data files into package (`pocketflow_tools/data/`)
- Created symlinks at root for bash compatibility
- Bumped version: 0.1.0 → 2.0.0 (major refactor)

**Migration**: See [MIGRATION_GUIDE.md](docs/MIGRATION_GUIDE.md)

### Added
- `agent-os` CLI command for installation
- `agent-os init` - Initialize Agent OS in project
- `agent-os install-toolkit` - Install optional toolkit
- Python package data files bundling
- Modern CLI with rich formatting
- Better error messages and help text

### Changed
- **Installation method**: uv package (recommended) vs bash scripts (legacy)
- **Data organization**: Files in package, symlinks at root
- **Version**: 0.1.0 → 2.0.0
- **Entry points**: Added `agent-os`, kept `pocketflow-generate`

### Maintained
- ✅ Existing `pocketflow-generate` CLI unchanged
- ✅ Bash scripts continue working
- ✅ Existing projects unaffected
- ✅ All generated files identical

**Full details**: [docs/uv-implementation-plan-CORRECTED.md](docs/uv-implementation-plan-CORRECTED.md)
```

---

### Step 4.4: Update pyproject.toml URLs

Add project URLs:

```toml
[project.urls]
Homepage = "https://github.com/pickleton89/agent-os-pocketflow"
Documentation = "https://github.com/pickleton89/agent-os-pocketflow#readme"
Repository = "https://github.com/pickleton89/agent-os-pocketflow.git"
Issues = "https://github.com/pickleton89/agent-os-pocketflow/issues"
Changelog = "https://github.com/pickleton89/agent-os-pocketflow/blob/main/CHANGELOG.md"
```

---

## Testing Checklist

Before considering complete:

### Functional Tests
- [ ] `agent-os init` creates `.agent-os/` directory
- [ ] All subdirectories populated with correct files
- [ ] Config file valid and correct version
- [ ] `--claude-code` installs `.claude/` directory
- [ ] `--force` overwrites existing installation
- [ ] Error handling for non-project directories
- [ ] `install-toolkit` creates `~/.agent-os/`
- [ ] .gitignore updated correctly

### Compatibility Tests
- [ ] `pocketflow-generate` still works (existing CLI)
- [ ] Bash scripts can access symlinked directories
- [ ] Existing projects unaffected
- [ ] Old bash installation method still works

### Distribution Tests
- [ ] `uvx agent-os-pocketflow init` works
- [ ] `uv tool install` works globally
- [ ] `uv add agent-os-pocketflow` works in project
- [ ] Package installable with `pip install -e .`

### Platform Tests
- [ ] Works on macOS
- [ ] Works on Linux
- [ ] Works in Docker
- [ ] Works in GitHub Actions

### Edge Cases
- [ ] Multiple installations in same project (with --force)
- [ ] Installation in empty directory (error)
- [ ] Installation in directory with existing files
- [ ] Toolkit already exists (error handling)

---

## Success Criteria

### Quantitative
- ✅ Installation time: <5s (with toolkit) or <15s (standalone)
- ✅ Test pass rate: 100%
- ✅ Backward compatibility: 100% (all old commands work)
- ✅ Code coverage: >80% for installer module

### Qualitative
- ✅ Clear error messages
- ✅ Pretty terminal output
- ✅ Intuitive command structure
- ✅ Helpful documentation

---

## Rollback Plan

If critical issues discovered:

```bash
cd "$(git rev-parse --show-toplevel)"

# Option 1: Revert commits
git revert HEAD~n  # Revert last n commits

# Option 2: Return to v0.1.0
git checkout v0.1.0
git checkout -b hotfix/revert-v2

# Option 3: Keep both versions
git tag v2.0.0-deprecated
git checkout v0.1.0
git tag v0.1.0-stable
```

Update documentation to point to stable version.

---

## Timeline

| Phase | Duration | Days |
|-------|----------|------|
| **Phase 1: Package Setup** | 2-3 days | Day 1-3 |
| **Phase 2: Local Testing** | 3-4 days | Day 4-7 |
| **Phase 3: uvx Testing** | 2-3 days | Day 8-10 |
| **Phase 4: Documentation** | 2-3 days | Day 11-13 |
| **Buffer** | 1-2 days | Day 14 |
| **Total** | **10-14 days** | |

---

## Next Steps

1. **Review this plan** - Any questions or concerns?
2. **Create GitHub issue** - Track implementation progress
3. **Set up branch** - `git checkout -b feature/uv-distribution`
4. **Begin Phase 1** - Start with Step 1.1 (add dependencies)
5. **Commit frequently** - Small, atomic commits for easy rollback

**Ready to begin?** Start with Phase 1, Step 1.1! 🚀
