#!/usr/bin/env python3
"""
PocketFlow Installation Checker

This script checks if your project has the necessary dependencies
to run PocketFlow workflows.

Usage:
    python check-install.py [--install]
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Run the main installation checker."""
    # Path to the main checker in Agent OS
    agent_os_checker = Path.home() / ".agent-os" / "workflows" / "check-pocketflow-install.py"
    
    if not agent_os_checker.exists():
        print("❌ Agent OS + PocketFlow installation checker not found.")
        print("   Please ensure Agent OS is properly installed in ~/.agent-os/")
        return 1
    
    # Forward all arguments to the main checker
    cmd = [sys.executable, str(agent_os_checker)] + sys.argv[1:]
    return subprocess.run(cmd).returncode

if __name__ == "__main__":
    sys.exit(main())
