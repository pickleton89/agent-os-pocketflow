#!/usr/bin/env bash
set -euo pipefail

# Phase 1 CLI smoke tests for pocketflow_tools.cli
# - Validates error messages/exit codes for missing/invalid YAML
# - Validates successful generation on example spec

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT_DIR"

echo "[cli-smoke] Using Python: $(python3 -V 2>/dev/null || echo 'python3 not found')"

# Check PyYAML availability; do not install here to keep framework clean
python3 - << 'PY' 2>/dev/null || {
  echo "[cli-smoke] SKIP: PyYAML not available. Install with: uv pip install pyyaml" >&2
  exit 0
}
try:
    import yaml  # noqa: F401
    print("ok")
except Exception:
    raise SystemExit(1)
PY

echo "[cli-smoke] PyYAML detected. Running tests..."

# 1) Missing file
set +e
out=$(python3 -m pocketflow_tools.cli --spec does-not-exist.yaml 2>&1)
code=$?
set -e
echo "$out" | rg -n "Error: Specification file not found" >/dev/null || {
  echo "[cli-smoke] FAIL: Missing file message mismatch"; echo "$out"; exit 1; }
test "$code" -ne 0 || { echo "[cli-smoke] FAIL: Missing file should return non-zero"; exit 1; }

# 2) Invalid YAML
tmp_yaml="$(mktemp -t invalid-spec.XXXXXX.yaml)"
printf 'name: "BadSpec"\npattern: [unterminated\n' > "$tmp_yaml"
set +e
out=$(python3 -m pocketflow_tools.cli --spec "$tmp_yaml" 2>&1)
code=$?
set -e
rm -f "$tmp_yaml"
echo "$out" | rg -n "Error: Invalid YAML" >/dev/null || {
  echo "[cli-smoke] FAIL: Invalid YAML message mismatch"; echo "$out"; exit 1; }
test "$code" -ne 0 || { echo "[cli-smoke] FAIL: Invalid YAML should return non-zero"; exit 1; }

# 3) Valid generation (agent example)
outdir=".agent-os/workflows/cli-smoke"
rm -rf "$outdir" || true
python3 -m pocketflow_tools.cli \
  --spec pocketflow-tools/examples/agent-workflow-spec.yaml \
  --output "$outdir"

expected=(
  "docs/design.md"
  "schemas/models.py"
  "nodes.py"
  "flow.py"
  "main.py"
  "router.py"
  "utils"
  "tests"
  "pyproject.toml"
  "requirements.txt"
  "README.md"
  ".gitignore"
)

proj_dir="$outdir/$(basename "$(ls -1 "$outdir" | head -n1)")"
test -d "$proj_dir" || { echo "[cli-smoke] FAIL: output project dir missing"; exit 1; }

for f in "${expected[@]}"; do
  if [ ! -e "$proj_dir/$f" ]; then
    echo "[cli-smoke] FAIL: Missing expected output: $f"; exit 1
  fi
done

echo "[cli-smoke] PASS: CLI smoke tests completed"

