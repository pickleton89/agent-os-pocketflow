#!/usr/bin/env python3
"""
Focused tests for Phase 3: HYBRID composition (opt-in).

Ensures that when combination_info indicates a known combo and
enable_hybrid_promotion=True, the generator composes nodes from
both base patterns and the design doc includes a composed graph.
"""

import json
import subprocess


def _run_python3(code: str) -> dict:
    proc = subprocess.run(["python3", "-c", code], capture_output=True, text=True, check=True)
    # Parse JSON from the last non-empty line to avoid mixing with other prints
    lines = [ln for ln in (proc.stdout or "").splitlines() if ln.strip()]
    if not lines:
        return {}
    tail = lines[-1]
    return json.loads(tail)


def test_hybrid_nodes_and_graph_for_rag_agent_combo():
    code = (
        "import sys, json\n"
        "from pathlib import Path\n"
        "sys.path.insert(0, str(Path('pocketflow-tools')))\n"
        "import pattern_analyzer as pa\n"
        "import generator as gen\n\n"
        "req = (\n"
        "    'RAG with search retrieval and vector embeddings plus an intelligent agent '"
        "    'that performs decision making, planning, reasoning and autonomous action execution'\n"
        ")\n"
        "analyzer = pa.PatternAnalyzer()\n"
        "rec = analyzer.analyze_and_recommend(req)\n\n"
        "g = gen.PocketFlowGenerator(enable_hybrid_promotion=True)\n"
        "files = g.generate_workflow_from_requirements('HybridApp', req)\n\n"
        "design = files['docs/design.md']\n"
        "nodes_in_design = ('Retriever' in design) and ('TaskAnalyzer' in design)\n\n"
        "spec = g.generate_spec_from_analysis('HybridApp', req, rec)\n"
        "node_names = [n['name'] for n in spec.nodes]\n"
        "out = {\n"
        "    'has_retriever': 'Retriever' in node_names,\n"
        "    'has_task_analyzer': 'TaskAnalyzer' in node_names,\n"
        "    'design_has_mermaid': '```mermaid' in design,\n"
        "    'design_has_both': nodes_in_design,\n"
        "}\n"
        "print(json.dumps(out))\n"
    )
    out = _run_python3(code)
    assert out["has_retriever"] and out["has_task_analyzer"], "Hybrid nodes should include RAG and AGENT nodes"
    assert out["design_has_mermaid"], "Design should include a Mermaid diagram"
    assert out["design_has_both"], "Diagram should include nodes from both patterns"
