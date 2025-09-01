#!/usr/bin/env python3
"""
Focused tests to verify Phase 2: the generator honors simple structure
recommendations from the analyzer for both nodes and utilities.

This keeps scope tight and avoids unrelated churn.
"""

import json
import subprocess


def _run_python3(code: str) -> dict:
    """Run code in a python3 subprocess to ensure modern typing support and return parsed JSON."""
    proc = subprocess.run(
        ["python3", "-c", code], capture_output=True, text=True, check=True
    )
    return json.loads(proc.stdout.strip() or "{}")


def test_simple_workflow_nodes_and_utilities():
    code = r'''
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path('pocketflow-tools')))
import pattern_analyzer as pa
import generator as gen

req = "Simple CRUD form to submit and review entries with basic API"
analyzer = pa.PatternAnalyzer()
rec = analyzer.analyze_and_recommend(req)
g = gen.PocketFlowGenerator()
spec = g.generate_spec_from_analysis("TestSimpleWorkflow", req, rec)

out = {
    "nodes": [n["name"] for n in spec.nodes],
    "utils": [u["name"] for u in spec.utilities],
}
print(json.dumps(out))
'''
    out = _run_python3(code)
    assert out["nodes"][:3] == ["InputProcessor", "BusinessLogic", "OutputFormatter"]
    assert {"flow_controller", "state_manager"}.issubset(set(out["utils"]))


def test_basic_api_nodes_and_utilities():
    code = r'''
import sys, json
from pathlib import Path
sys.path.insert(0, str(Path('pocketflow-tools')))
import pattern_analyzer as pa
import generator as gen

req = "Integrate with external REST API, handle authentication, process responses, and return JSON. Simple basic features."
analyzer = pa.PatternAnalyzer()
rec = analyzer.analyze_and_recommend(req)
g = gen.PocketFlowGenerator()
spec = g.generate_spec_from_analysis("TestBasicAPI", req, rec)

out = {
    "nodes": [n["name"] for n in spec.nodes],
    "utils": [u["name"] for u in spec.utilities],
    "primary": getattr(rec.primary_pattern, 'value', str(rec.primary_pattern))
}
print(json.dumps(out))
'''
    out = _run_python3(code)
    assert out["nodes"][:3] == ["RequestValidator", "ResponseValidator", "ResponseProcessor"]
    assert {"request_parser", "response_formatter"}.issubset(set(out["utils"]))
