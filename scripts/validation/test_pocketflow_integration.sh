#!/bin/bash
# PocketFlow Integration Test Script
# Tests that all tools are accessible and functional in a project environment

# Repo type detection and gating
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "${SCRIPT_DIR}/../lib/repo-detect.sh" ]]; then
  # shellcheck disable=SC1091
  source "${SCRIPT_DIR}/../lib/repo-detect.sh"
fi

echo "🧪 Testing PocketFlow Tool Integration..."

# Framework mode: perform framework-only tool checks and skip project-only checks
if type is_framework >/dev/null 2>&1 && is_framework; then
  echo "ℹ️  Framework mode detected; testing framework tool components"
  
  # Framework Test 1: PocketFlow package structure
  if [[ -d "pocketflow_tools" ]]; then
    echo "✅ PocketFlow package directory present"
  else
    echo "❌ PocketFlow package directory missing: pocketflow_tools/"
    exit 1
  fi
  
  # Framework Test 2: Developer tools directory
  if [[ -d "pocketflow-tools" ]]; then
    echo "✅ Developer tools directory present"
  else
    echo "❌ Developer tools directory missing: pocketflow-tools/"
    exit 1
  fi
  
  # Framework Test 3: Key developer tool files
  dev_tools=(
    "pocketflow-tools/pattern_analyzer.py"
    "pocketflow-tools/dependency_orchestrator.py" 
    "pocketflow-tools/agent_coordination.py"
  )
  
  for tool in "${dev_tools[@]}"; do
    if [[ -f "$tool" ]]; then
      echo "✅ $(basename "$tool") found"
    else
      echo "❌ $(basename "$tool") missing"
      exit 1
    fi
  done
  
  echo "⏭️  SKIP (framework mode): Project installation and CLI testing"
  echo "🎉 Framework tool component checks passed"
  exit 0
fi

# If we reach here, repo-detect.sh didn't detect framework mode
echo "❌ This script is designed for framework mode only"
echo "ℹ️  For project validation, use the template installed at:"
echo "    .agent-os/validation/test_pocketflow_integration.sh"
echo "ℹ️  Framework vs Usage Distinction:"
echo "    📦 Framework repository: Validates components that generate tools"  
echo "    🚀 Project repository: Validates installed and functional tools"
exit 1