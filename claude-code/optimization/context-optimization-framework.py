#!/usr/bin/env python3
"""
Context Optimization Framework for Agent OS + PocketFlow Document Creation

Optimizes context passing between document creation agents to minimize token usage
and maximize information efficiency. Part of Phase 4 optimization.

Usage:
    python3 context-optimization-framework.py --analyze [project] --optimize [context_file]
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass


@dataclass
class ContextField:
    """Represents a context field with metadata"""

    name: str
    value: Any
    required_by: Set[str]  # Agent names that require this field
    token_cost: int
    priority: int  # 1=critical, 2=important, 3=optional
    source: str  # Where this field originated


@dataclass
class AgentContextRequirement:
    """Context requirements for a specific agent"""

    agent_name: str
    required_fields: Set[str]
    optional_fields: Set[str]
    context_templates: Dict[str, str]
    estimated_token_usage: Optional[int] = None


@dataclass
class ContextOptimizationResult:
    """Results from context optimization"""

    original_size: int
    optimized_size: int
    reduction_percentage: float
    removed_fields: List[str]
    compressed_fields: List[str]
    agent_specific_contexts: Dict[str, Dict[str, Any]]


class ContextOptimizer:
    """Optimizes context passing between document creation agents"""

    def __init__(self):
        # Define agent context requirements based on their functionality
        self.agent_requirements = {
            "mission-document-creator": AgentContextRequirement(
                agent_name="mission-document-creator",
                required_fields={"main_idea", "key_features", "target_users"},
                optional_fields={
                    "tech_stack",
                    "competitive_analysis",
                    "business_model",
                },
                context_templates={
                    "product_focus": "product_info + business_context",
                    "user_focus": "target_users + user_context",
                    "feature_focus": "key_features + feature_priorities",
                },
            ),
            "tech-stack-document-creator": AgentContextRequirement(
                agent_name="tech-stack-document-creator",
                required_fields={"tech_stack", "main_idea"},
                optional_fields={
                    "key_features",
                    "target_users",
                    "deployment_preferences",
                },
                context_templates={
                    "technical_focus": "tech_stack + architecture_preferences",
                    "integration_focus": "main_idea + key_features + tech_stack",
                },
            ),
            "roadmap-document-creator": AgentContextRequirement(
                agent_name="roadmap-document-creator",
                required_fields={"key_features", "main_idea"},
                optional_fields={"tech_stack", "target_users", "timeline_preferences"},
                context_templates={
                    "planning_focus": "key_features + priorities + timeline",
                    "feature_focus": "key_features + feature_dependencies",
                },
            ),
            "pre-flight-checklist-creator": AgentContextRequirement(
                agent_name="pre-flight-checklist-creator",
                required_fields={"tech_stack", "key_features"},
                optional_fields={"main_idea", "target_users", "complexity_level"},
                context_templates={
                    "validation_focus": "tech_stack + key_features + architecture",
                    "readiness_focus": "all_context_minimal",
                },
            ),
            "claude-md-manager": AgentContextRequirement(
                agent_name="claude-md-manager",
                required_fields={"main_idea", "generated_documents"},
                optional_fields={"tech_stack", "key_features", "project_structure"},
                context_templates={
                    "integration_focus": "project_metadata + generated_documents",
                    "workflow_focus": "main_idea + tech_stack + workflow_preferences",
                },
            ),
            "spec-document-creator": AgentContextRequirement(
                agent_name="spec-document-creator",
                required_fields={"feature_specification", "main_idea"},
                optional_fields={"tech_stack", "existing_design", "user_stories"},
                context_templates={
                    "feature_focus": "feature_specification + design_context",
                    "requirements_focus": "feature_specification + user_stories",
                },
            ),
            "design-document-creator": AgentContextRequirement(
                agent_name="design-document-creator",
                required_fields={"main_idea", "tech_stack", "key_features"},
                optional_fields={"existing_codebase", "architecture_preferences"},
                context_templates={
                    "architecture_focus": "tech_stack + key_features + architecture",
                    "design_focus": "main_idea + key_features + tech_stack + design_constraints",
                },
            ),
        }

        # Define context field priorities and relationships
        self.field_priorities = {
            # Critical fields (always include)
            "main_idea": 1,
            "key_features": 1,
            "target_users": 1,
            "tech_stack": 1,
            # Important fields (include if space allows)
            "feature_specification": 2,
            "generated_documents": 2,
            "project_metadata": 2,
            "architecture_preferences": 2,
            # Optional fields (include for context richness)
            "competitive_analysis": 3,
            "business_model": 3,
            "timeline_preferences": 3,
            "deployment_preferences": 3,
            "existing_codebase": 3,
            "user_stories": 3,
        }

    def analyze_context_usage(
        self, context_data: Dict[str, Any], target_agents: List[str]
    ) -> Dict[str, Any]:
        """Analyze how context fields are used across target agents"""
        usage_analysis = {
            "field_usage": {},
            "agent_requirements": {},
            "optimization_opportunities": [],
            "token_distribution": {},
        }

        # Analyze field usage across agents
        for field_name, field_value in context_data.items():
            required_by = set()
            optional_for = set()

            for agent_name in target_agents:
                if agent_name in self.agent_requirements:
                    req = self.agent_requirements[agent_name]
                    if field_name in req.required_fields:
                        required_by.add(agent_name)
                    elif field_name in req.optional_fields:
                        optional_for.add(agent_name)

            # Estimate token cost for this field
            token_cost = self._estimate_token_cost(field_value)

            usage_analysis["field_usage"][field_name] = {
                "required_by": list(required_by),
                "optional_for": list(optional_for),
                "token_cost": token_cost,
                "priority": self.field_priorities.get(field_name, 3),
                "usage_ratio": len(required_by) / len(target_agents)
                if target_agents
                else 0,
            }

        # Identify optimization opportunities
        for field_name, usage in usage_analysis["field_usage"].items():
            if usage["usage_ratio"] < 0.5 and usage["token_cost"] > 100:
                usage_analysis["optimization_opportunities"].append(
                    {
                        "field": field_name,
                        "opportunity": "agent_specific_inclusion",
                        "potential_savings": usage["token_cost"]
                        * (1 - usage["usage_ratio"]),
                        "description": f"Field used by {usage['usage_ratio']:.1%} of agents, high token cost",
                    }
                )

            if usage["priority"] == 3 and usage["token_cost"] > 200:
                usage_analysis["optimization_opportunities"].append(
                    {
                        "field": field_name,
                        "opportunity": "optional_field_compression",
                        "potential_savings": usage["token_cost"] * 0.5,
                        "description": "Optional field with high token cost, consider summarization",
                    }
                )

        return usage_analysis

    def optimize_context_for_agent(
        self, context_data: Dict[str, Any], agent_name: str
    ) -> Dict[str, Any]:
        """Create optimized context for a specific agent"""
        if agent_name not in self.agent_requirements:
            # If agent not defined, include all critical and important fields
            return self._create_fallback_context(context_data)

        req = self.agent_requirements[agent_name]
        optimized_context = {}

        # Always include required fields
        for field_name in req.required_fields:
            if field_name in context_data:
                optimized_context[field_name] = context_data[field_name]
            else:
                print(
                    f"⚠️  Warning: Required field '{field_name}' missing for {agent_name}"
                )

        # Include optional fields based on priority and token budget
        current_tokens = sum(
            self._estimate_token_cost(v) for v in optimized_context.values()
        )
        token_budget = 8000  # Conservative token budget per agent

        # Sort optional fields by priority and token efficiency
        optional_fields = []
        for field_name in req.optional_fields:
            if field_name in context_data:
                token_cost = self._estimate_token_cost(context_data[field_name])
                priority = self.field_priorities.get(field_name, 3)
                efficiency = 1 / (
                    priority * token_cost
                )  # Higher efficiency = better value
                optional_fields.append((field_name, priority, token_cost, efficiency))

        # Sort by efficiency (higher first) and priority (lower first)
        optional_fields.sort(key=lambda x: (-x[3], x[1]))

        # Add optional fields within token budget
        for field_name, priority, token_cost, efficiency in optional_fields:
            if current_tokens + token_cost <= token_budget:
                optimized_context[field_name] = context_data[field_name]
                current_tokens += token_cost
            elif (
                priority <= 2
            ):  # Critical/important fields get compressed instead of excluded
                compressed_value = self._compress_field_value(context_data[field_name])
                compressed_cost = self._estimate_token_cost(compressed_value)
                if current_tokens + compressed_cost <= token_budget:
                    optimized_context[field_name] = compressed_value
                    current_tokens += compressed_cost

        # Add agent-specific metadata
        optimized_context["_agent_context"] = {
            "target_agent": agent_name,
            "optimization_applied": True,
            "token_estimate": current_tokens,
            "excluded_fields": [
                f
                for f in context_data.keys()
                if f not in optimized_context and not f.startswith("_")
            ],
        }

        return optimized_context

    def create_parallel_contexts(
        self, context_data: Dict[str, Any], agent_names: List[str]
    ) -> Dict[str, Dict[str, Any]]:
        """Create optimized contexts for parallel agent execution"""
        parallel_contexts = {}
        shared_context = self._extract_shared_context(context_data, agent_names)

        for agent_name in agent_names:
            # Start with shared context
            agent_context = shared_context.copy()

            # Add agent-specific optimizations
            agent_specific = self.optimize_context_for_agent(context_data, agent_name)

            # Merge, preferring agent-specific optimizations
            for key, value in agent_specific.items():
                agent_context[key] = value

            parallel_contexts[agent_name] = agent_context

        return parallel_contexts

    def _extract_shared_context(
        self, context_data: Dict[str, Any], agent_names: List[str]
    ) -> Dict[str, Any]:
        """Extract context fields shared by multiple agents"""
        shared_context = {}

        # Find fields required by multiple agents
        field_usage = {}
        for agent_name in agent_names:
            if agent_name in self.agent_requirements:
                req = self.agent_requirements[agent_name]
                for field in req.required_fields | req.optional_fields:
                    if field not in field_usage:
                        field_usage[field] = set()
                    field_usage[field].add(agent_name)

        # Include fields used by multiple agents (shared context)
        for field_name, using_agents in field_usage.items():
            if len(using_agents) > 1 and field_name in context_data:
                shared_context[field_name] = context_data[field_name]

        return shared_context

    def _create_fallback_context(self, context_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create fallback context when agent requirements are unknown"""
        fallback_context = {}

        # Include all priority 1 and 2 fields
        for field_name, field_value in context_data.items():
            priority = self.field_priorities.get(field_name, 3)
            if priority <= 2:
                fallback_context[field_name] = field_value

        return fallback_context

    def _estimate_token_cost(self, value: Any) -> int:
        """Estimate token cost for a context field value"""
        if isinstance(value, str):
            # Rough approximation: 1 token per 4 characters
            return len(value) // 4
        elif isinstance(value, (list, tuple)):
            return sum(self._estimate_token_cost(item) for item in value)
        elif isinstance(value, dict):
            return sum(
                self._estimate_token_cost(k) + self._estimate_token_cost(v)
                for k, v in value.items()
            )
        else:
            # Convert to string and estimate
            return len(str(value)) // 4

    def _compress_field_value(self, value: Any) -> Any:
        """Compress a field value to reduce token usage while preserving key information"""
        if isinstance(value, str):
            if len(value) > 500:
                # Extract key sentences and bullet points
                sentences = re.split(r"[.!?]+", value)
                key_sentences = []

                # Prioritize sentences with important keywords
                important_patterns = [
                    r"\b(key|important|critical|main|primary|core)\b",
                    r"\b(feature|requirement|goal|objective)\b",
                    r"\b(user|customer|client|stakeholder)\b",
                ]

                for sentence in sentences[:10]:  # Limit to first 10 sentences
                    sentence = sentence.strip()
                    if sentence:
                        for pattern in important_patterns:
                            if re.search(pattern, sentence, re.IGNORECASE):
                                key_sentences.append(sentence)
                                break
                        if len(key_sentences) >= 5:  # Limit compressed content
                            break

                if key_sentences:
                    return ". ".join(key_sentences) + "."
                else:
                    # Fallback to first few sentences
                    return ". ".join(sentences[:3]) + "."

            return value

        elif isinstance(value, list):
            if len(value) > 10:
                return value[:10]  # Limit list length
            return value

        elif isinstance(value, dict):
            # Keep only most important keys
            important_keys = set()
            for key in value.keys():
                if any(
                    keyword in key.lower()
                    for keyword in ["key", "main", "primary", "core", "important"]
                ):
                    important_keys.add(key)

            if important_keys:
                return {k: v for k, v in value.items() if k in important_keys}
            else:
                # Keep first 5 items
                return dict(list(value.items())[:5])

        return value

    def generate_optimization_report(
        self, context_data: Dict[str, Any], agent_names: List[str]
    ) -> str:
        """Generate a report on context optimization opportunities"""
        analysis = self.analyze_context_usage(context_data, agent_names)
        optimized_contexts = self.create_parallel_contexts(context_data, agent_names)

        report = []
        report.append("# Context Optimization Analysis Report\n")

        # Overall statistics
        original_size = sum(self._estimate_token_cost(v) for v in context_data.values())
        optimized_total = sum(
            sum(self._estimate_token_cost(v) for v in ctx.values())
            for ctx in optimized_contexts.values()
        )

        report.append("## Overall Optimization Results")
        report.append(f"- **Original Context Size**: {original_size:,} tokens")
        report.append(f"- **Total Optimized Size**: {optimized_total:,} tokens")
        report.append(
            f"- **Average per Agent**: {optimized_total // len(agent_names):,} tokens"
        )
        report.append(
            f"- **Memory Efficiency**: {(original_size * len(agent_names) - optimized_total) / (original_size * len(agent_names)):.1%} reduction"
        )
        report.append("")

        # Field usage analysis
        report.append("## Field Usage Analysis")
        report.append("| Field | Priority | Token Cost | Usage Ratio | Required By |")
        report.append("|-------|----------|------------|-------------|-------------|")

        for field_name, usage in analysis["field_usage"].items():
            priority_name = {1: "Critical", 2: "Important", 3: "Optional"}[
                usage["priority"]
            ]
            required_by = ", ".join(usage["required_by"][:3])  # Limit display
            if len(usage["required_by"]) > 3:
                required_by += f" (+{len(usage['required_by']) - 3} more)"

            report.append(
                f"| {field_name} | {priority_name} | {usage['token_cost']} | {usage['usage_ratio']:.1%} | {required_by} |"
            )

        report.append("")

        # Optimization opportunities
        if analysis["optimization_opportunities"]:
            report.append("## Optimization Opportunities")
            for i, opp in enumerate(analysis["optimization_opportunities"], 1):
                report.append(f"### {i}. {opp['field']} - {opp['opportunity']}")
                report.append(
                    f"**Potential Savings**: {opp['potential_savings']:.0f} tokens"
                )
                report.append(f"**Description**: {opp['description']}")
                report.append("")

        # Agent-specific optimizations
        report.append("## Agent-Specific Context Sizes")
        report.append("| Agent | Original | Optimized | Reduction | Excluded Fields |")
        report.append("|-------|----------|-----------|-----------|-----------------|")

        for agent_name, ctx in optimized_contexts.items():
            agent_original = original_size
            agent_optimized = sum(
                self._estimate_token_cost(v)
                for v in ctx.values()
                if not str(v).startswith("_")
            )
            reduction = (
                (agent_original - agent_optimized) / agent_original
                if agent_original > 0
                else 0
            )
            excluded = len(ctx.get("_agent_context", {}).get("excluded_fields", []))

            report.append(
                f"| {agent_name} | {agent_original} | {agent_optimized} | {reduction:.1%} | {excluded} fields |"
            )

        report.append("")

        # Recommendations
        report.append("## Recommendations")

        high_cost_fields = [
            f
            for f, u in analysis["field_usage"].items()
            if u["token_cost"] > 1000 and u["priority"] >= 2
        ]
        if high_cost_fields:
            report.append("### High-Cost Fields")
            report.append("Consider compressing or summarizing these fields:")
            for field in high_cost_fields:
                report.append(
                    f"- **{field}**: {analysis['field_usage'][field]['token_cost']} tokens"
                )
            report.append("")

        underused_fields = [
            f
            for f, u in analysis["field_usage"].items()
            if u["usage_ratio"] < 0.3 and u["token_cost"] > 200
        ]
        if underused_fields:
            report.append("### Underused Fields")
            report.append(
                "These fields have high token cost but low usage - consider agent-specific inclusion:"
            )
            for field in underused_fields:
                usage = analysis["field_usage"][field]
                report.append(
                    f"- **{field}**: {usage['token_cost']} tokens, used by {usage['usage_ratio']:.1%} of agents"
                )
            report.append("")

        report.append("### General Recommendations")
        report.append(
            "1. **Use agent-specific contexts** for parallel execution to minimize token usage"
        )
        report.append("2. **Compress optional fields** with high token costs")
        report.append("3. **Share common context** efficiently between agents")
        report.append(
            "4. **Monitor field usage patterns** and adjust priorities based on actual needs"
        )

        return "\n".join(report)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Context optimization for document creation agents"
    )
    parser.add_argument("--analyze", help="Analyze context usage for project")
    parser.add_argument("--optimize", help="Optimize context file")
    parser.add_argument(
        "--agents",
        nargs="+",
        help="Target agent names",
        default=[
            "mission-document-creator",
            "tech-stack-document-creator",
            "roadmap-document-creator",
        ],
    )
    parser.add_argument("--output", help="Output file for optimized context")
    parser.add_argument("--report", help="Generate optimization report to file")

    args = parser.parse_args()

    optimizer = ContextOptimizer()

    if args.analyze:
        # Mock context data for demonstration
        context_data = {
            "main_idea": "AI-powered content management system for small businesses",
            "key_features": [
                "Automated content generation",
                "SEO optimization",
                "Multi-platform publishing",
                "Analytics dashboard",
                "Team collaboration tools",
            ],
            "target_users": [
                {
                    "role": "Small business owner",
                    "age": "25-45",
                    "context": "Limited time for content creation",
                },
                {
                    "role": "Marketing manager",
                    "age": "28-40",
                    "context": "Needs efficient content workflows",
                },
            ],
            "tech_stack": {
                "backend": "Python FastAPI",
                "frontend": "React",
                "database": "PostgreSQL",
                "ai_provider": "OpenAI",
            },
            "competitive_analysis": "Long competitive analysis text here..." * 100,
            "business_model": "SaaS subscription with tiered pricing",
            "timeline_preferences": "MVP in 3 months, full product in 6 months",
        }

        report = optimizer.generate_optimization_report(context_data, args.agents)

        if args.report:
            Path(args.report).write_text(report)
            print(f"📊 Optimization report saved to: {args.report}")
        else:
            print(report)

    elif args.optimize:
        context_file = Path(args.optimize)
        if not context_file.exists():
            print(f"❌ Context file not found: {context_file}")
            return 1

        with open(context_file) as f:
            context_data = json.load(f)

        optimized_contexts = optimizer.create_parallel_contexts(
            context_data, args.agents
        )

        output_file = (
            Path(args.output)
            if args.output
            else context_file.with_suffix(".optimized.json")
        )

        with open(output_file, "w") as f:
            json.dump(optimized_contexts, f, indent=2)

        print(f"✅ Optimized contexts saved to: {output_file}")

        # Show summary
        original_size = sum(
            optimizer._estimate_token_cost(v) for v in context_data.values()
        )
        total_optimized = sum(
            sum(optimizer._estimate_token_cost(v) for v in ctx.values())
            for ctx in optimized_contexts.values()
        )

        print("📈 Optimization Summary:")
        print(
            f"   Original: {original_size:,} tokens × {len(args.agents)} agents = {original_size * len(args.agents):,} tokens"
        )
        print(f"   Optimized: {total_optimized:,} tokens total")
        print(
            f"   Reduction: {((original_size * len(args.agents) - total_optimized) / (original_size * len(args.agents))):.1%}"
        )

    else:
        print("🔧 Context Optimization Framework")
        print("Use --help for usage information")
        return 0

    return 0


if __name__ == "__main__":
    exit(main())
