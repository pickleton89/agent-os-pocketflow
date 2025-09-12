#!/usr/bin/env python3
"""
Smart Features Module for Agent OS + PocketFlow Documentation Discovery
Framework component that provides pattern detection, version management, 
and progressive disclosure for the documentation discovery system.

This module is PART OF the Agent OS + PocketFlow framework and generates 
templates/tools for end-user projects to use in their documentation discovery workflows.
"""

import re
import yaml
from typing import Dict, List, Tuple, Optional, Any
from pathlib import Path
from datetime import datetime, timedelta
import hashlib


class TechPatternDetector:
    """
    Intelligent pattern detection for identifying documentation needs
    based on specification content and project context.
    """
    
    def __init__(self, registry_path: Optional[str] = None):
        self.registry_path = Path(registry_path or ".agent-os/docs-registry.yaml")
        self.tech_patterns = self._load_tech_patterns()
        self._load_registry()
    
    def _load_tech_patterns(self) -> Dict[str, Dict]:
        """Load technology pattern definitions with weights and contexts"""
        return {
            "stripe": {
                "patterns": ["payment", "subscription", "checkout", "billing", "invoice", "webhook"],
                "weight": 3,
                "category": "payment_processing",
                "contexts": ["plan-product", "create-spec", "execute-tasks"]
            },
            "auth0": {
                "patterns": ["authentication", "login", "jwt", "oauth", "sso", "identity"],
                "weight": 3,
                "category": "authentication",
                "contexts": ["plan-product", "create-spec", "execute-tasks"]
            },
            "aws": {
                "patterns": ["s3", "lambda", "dynamodb", "sqs", "ec2", "rds", "cloudfront"],
                "weight": 2,
                "category": "cloud_infrastructure",
                "contexts": ["plan-product", "execute-tasks"]
            },
            "fastapi": {
                "patterns": ["api", "endpoint", "router", "dependency", "middleware", "pydantic", "fastapi", "rest"],
                "weight": 4,
                "category": "api_framework",
                "contexts": ["create-spec", "execute-tasks"]
            },
            "django": {
                "patterns": ["model", "view", "template", "orm", "admin", "middleware"],
                "weight": 4,
                "category": "web_framework",
                "contexts": ["create-spec", "execute-tasks"]
            },
            "react": {
                "patterns": ["component", "jsx", "state", "hook", "props", "context"],
                "weight": 4,
                "category": "frontend_framework",
                "contexts": ["create-spec", "execute-tasks"]
            },
            "postgresql": {
                "patterns": ["database", "query", "transaction", "index", "migration", "schema", "postgres", "postgresql"],
                "weight": 3,
                "category": "database",
                "contexts": ["plan-product", "create-spec", "execute-tasks"]
            },
            "redis": {
                "patterns": ["cache", "caching", "session", "queue", "pubsub", "key-value", "redis"],
                "weight": 2,
                "category": "caching",
                "contexts": ["create-spec", "execute-tasks"]
            },
            "docker": {
                "patterns": ["container", "dockerfile", "image", "compose", "deploy"],
                "weight": 2,
                "category": "containerization",
                "contexts": ["plan-product", "execute-tasks"]
            },
            "kubernetes": {
                "patterns": ["k8s", "pod", "service", "deployment", "ingress", "cluster"],
                "weight": 2,
                "category": "orchestration",
                "contexts": ["plan-product", "execute-tasks"]
            },
            "openai": {
                "patterns": ["gpt", "embedding", "completion", "chat", "ai", "llm"],
                "weight": 4,
                "category": "ai_services",
                "contexts": ["create-spec", "execute-tasks"]
            },
            "langchain": {
                "patterns": ["retrieval", "chain", "agent", "embedding", "vector", "rag"],
                "weight": 4,
                "category": "ai_framework",
                "contexts": ["create-spec", "execute-tasks"]
            },
            "anthropic": {
                "patterns": ["claude", "anthropic", "constitutional", "ai"],
                "weight": 4,
                "category": "ai_services", 
                "contexts": ["create-spec", "execute-tasks"]
            },
            "pocketflow": {
                "patterns": ["workflow", "node", "flow", "batch", "agent", "tool"],
                "weight": 5,
                "category": "workflow_framework",
                "contexts": ["create-spec", "execute-tasks"]
            }
        }
    
    def _load_registry(self) -> None:
        """Load existing documentation registry if available"""
        self.registry = {}
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    data = yaml.safe_load(f)
                    if data:
                        self.registry = data.get('tech_stack', {})
            except Exception:
                pass  # Registry will remain empty
    
    def detect_documentation_needs(self, spec_text: str, context: str = "create-spec") -> List[Dict[str, Any]]:
        """
        Detect documentation needs based on specification content
        
        Args:
            spec_text: Text content to analyze
            context: Workflow context (plan-product, create-spec, execute-tasks)
            
        Returns:
            List of documentation suggestions with priorities and metadata
        """
        suggestions = []
        spec_lower = spec_text.lower()
        
        for tech, config in self.tech_patterns.items():
            if context not in config["contexts"]:
                continue
                
            # Check if already in registry
            if tech in self.registry:
                continue
                
            # Calculate match score - use substring matching for better detection
            matches = sum(1 for pattern in config["patterns"] 
                         if pattern in spec_lower)
            
            if matches > 0:
                confidence = min(matches * 0.3, 1.0)  # Cap at 100%
                priority = self._calculate_priority(matches, config["weight"], context)
                
                suggestions.append({
                    "technology": tech,
                    "category": config["category"],
                    "matches": matches,
                    "confidence": confidence,
                    "priority": priority,
                    "reason": f"Detected {matches} {tech} patterns in specification",
                    "matched_patterns": [p for p in config["patterns"] 
                                       if p in spec_lower],
                    "context": context
                })
        
        # Sort by priority and confidence
        suggestions.sort(key=lambda x: (x["priority"], x["confidence"]), reverse=True)
        return suggestions
    
    def _calculate_priority(self, matches: int, weight: int, context: str) -> str:
        """Calculate suggestion priority based on matches, weight, and context"""
        score = matches * weight
        
        # Context multipliers
        context_multipliers = {
            "plan-product": 0.8,  # Lower priority during planning
            "create-spec": 1.2,   # Higher priority during spec creation
            "execute-tasks": 1.0  # Standard priority during execution
        }
        
        score *= context_multipliers.get(context, 1.0)
        
        if score >= 8:
            return "critical"
        elif score >= 5:
            return "high"
        elif score >= 3:
            return "medium"
        else:
            return "low"


class ProgressiveDisclosure:
    """
    Manages progressive disclosure of documentation content based on workflow phase
    and user needs. Implements caching and intelligent content prioritization.
    """
    
    def __init__(self, cache_dir: str = ".agent-os/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.disclosure_levels = {
            "overview": {
                "sections": ["introduction", "getting-started", "overview", "concepts"],
                "priority": 1,
                "cache_ttl_hours": 24
            },
            "planning": {
                "sections": ["architecture", "patterns", "best-practices", "design-principles"],
                "priority": 2,
                "cache_ttl_hours": 12
            },
            "implementation": {
                "sections": ["api-reference", "examples", "integration", "configuration"],
                "priority": 3,
                "cache_ttl_hours": 6
            },
            "optimization": {
                "sections": ["performance", "scaling", "troubleshooting", "monitoring"],
                "priority": 4,
                "cache_ttl_hours": 24
            }
        }
    
    def get_content_for_level(self, documentation_source: str, level: str) -> Dict[str, Any]:
        """
        Get documentation content appropriate for the specified disclosure level
        
        Args:
            documentation_source: Source identifier (tech name or URL hash)
            level: Disclosure level (overview, planning, implementation, optimization)
            
        Returns:
            Dictionary containing filtered content and metadata
        """
        if level not in self.disclosure_levels:
            raise ValueError(f"Unknown disclosure level: {level}")
        
        level_config = self.disclosure_levels[level]
        cache_key = self._generate_cache_key(documentation_source, level)
        
        # Check cache first
        cached_content = self._get_cached_content(cache_key, level_config["cache_ttl_hours"])
        if cached_content:
            return cached_content
        
        # Generate content for level (would integrate with actual documentation fetching)
        content = {
            "source": documentation_source,
            "level": level,
            "sections": level_config["sections"],
            "priority": level_config["priority"],
            "timestamp": datetime.now().isoformat(),
            "content": f"TODO: Implement actual content extraction for {level} level",
            "metadata": {
                "extracted_at": datetime.now().isoformat(),
                "ttl_hours": level_config["cache_ttl_hours"],
                "sections_requested": level_config["sections"]
            }
        }
        
        # Cache the content
        self._cache_content(cache_key, content)
        return content
    
    def _generate_cache_key(self, source: str, level: str) -> str:
        """Generate cache key for content"""
        return hashlib.md5(f"{source}:{level}".encode()).hexdigest()
    
    def _get_cached_content(self, cache_key: str, ttl_hours: int) -> Optional[Dict[str, Any]]:
        """Retrieve cached content if still valid"""
        cache_file = self.cache_dir / f"{cache_key}.yaml"
        
        if not cache_file.exists():
            return None
            
        try:
            with open(cache_file, 'r') as f:
                content = yaml.safe_load(f)
            
            # Check TTL
            cached_time = datetime.fromisoformat(content["timestamp"])
            if datetime.now() - cached_time > timedelta(hours=ttl_hours):
                cache_file.unlink()  # Remove expired cache
                return None
                
            return content
        except Exception:
            # Remove corrupted cache
            try:
                cache_file.unlink()
            except:
                pass
            return None
    
    def _cache_content(self, cache_key: str, content: Dict[str, Any]) -> None:
        """Cache content for future use"""
        cache_file = self.cache_dir / f"{cache_key}.yaml"
        
        try:
            with open(cache_file, 'w') as f:
                yaml.dump(content, f, default_flow_style=False)
        except Exception:
            pass  # Silently fail caching


class VersionManager:
    """
    Manages version tracking and compatibility checking for documentation sources.
    Provides warnings and suggestions for version mismatches.
    """
    
    def __init__(self, registry_path: str = ".agent-os/docs-registry.yaml"):
        self.registry_path = Path(registry_path)
        self.version_patterns = {
            "semantic": r"(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9\-]+))?",
            "date": r"(\d{4})-(\d{2})-(\d{2})",
            "simple": r"v?(\d+)(?:\.(\d+))?",
        }
    
    def detect_version(self, content: str, tech: str) -> Optional[str]:
        """
        Detect version information from documentation content
        
        Args:
            content: Documentation content to analyze
            tech: Technology name for context
            
        Returns:
            Detected version string or None
        """
        # Look for common version patterns
        for pattern_name, pattern in self.version_patterns.items():
            matches = re.findall(pattern, content.lower())
            if matches:
                if pattern_name == "semantic":
                    # Return first semantic version found
                    match = matches[0]
                    version = f"{match[0]}.{match[1]}.{match[2]}"
                    if match[3]:  # Pre-release suffix
                        version += f"-{match[3]}"
                    return version
                elif pattern_name == "date":
                    # Return first date version found
                    match = matches[0]
                    return f"{match[0]}-{match[1]}-{match[2]}"
                elif pattern_name == "simple":
                    # Return first simple version found
                    match = matches[0]
                    version = match[0]
                    if match[1]:
                        version += f".{match[1]}"
                    return version
        
        return None
    
    def check_compatibility(self, tech: str, project_version: Optional[str] = None) -> Dict[str, Any]:
        """
        Check version compatibility for a technology
        
        Args:
            tech: Technology name
            project_version: Version used in project (if known)
            
        Returns:
            Compatibility report with warnings and suggestions
        """
        registry_version = self._get_registry_version(tech)
        
        report = {
            "technology": tech,
            "registry_version": registry_version,
            "project_version": project_version,
            "status": "unknown",
            "warnings": [],
            "suggestions": []
        }
        
        if not registry_version and not project_version:
            report["status"] = "no_version_info"
            report["warnings"].append("No version information available for comparison")
            return report
        
        if not project_version:
            report["status"] = "project_version_unknown"
            report["warnings"].append("Project version unknown - cannot verify compatibility")
            report["suggestions"].append("Add version information to project configuration")
            return report
        
        if not registry_version:
            report["status"] = "registry_version_unknown"
            report["warnings"].append("Documentation version unknown")
            report["suggestions"].append("Update documentation registry with version information")
            return report
        
        # Compare versions
        comparison = self._compare_versions(registry_version, project_version)
        
        if comparison == "exact_match":
            report["status"] = "compatible"
        elif comparison == "minor_diff":
            report["status"] = "probably_compatible"
            report["warnings"].append(f"Minor version difference: docs={registry_version}, project={project_version}")
        elif comparison == "major_diff":
            report["status"] = "potentially_incompatible"
            report["warnings"].append(f"Major version difference: docs={registry_version}, project={project_version}")
            report["suggestions"].append("Consider updating documentation or project version")
        else:
            report["status"] = "version_format_mismatch"
            report["warnings"].append("Cannot compare versions - different formats")
        
        return report
    
    def _get_registry_version(self, tech: str) -> Optional[str]:
        """Get version for technology from registry"""
        if not self.registry_path.exists():
            return None
            
        try:
            with open(self.registry_path, 'r') as f:
                data = yaml.safe_load(f)
            
            tech_data = data.get('tech_stack', {}).get(tech, {})
            return tech_data.get('version')
        except Exception:
            return None
    
    def _compare_versions(self, version1: str, version2: str) -> str:
        """
        Compare two version strings
        
        Returns:
            'exact_match', 'minor_diff', 'major_diff', or 'format_mismatch'
        """
        # Try semantic version comparison
        sem1 = re.match(self.version_patterns["semantic"], version1)
        sem2 = re.match(self.version_patterns["semantic"], version2)
        
        if sem1 and sem2:
            major1, minor1, patch1 = int(sem1.group(1)), int(sem1.group(2)), int(sem1.group(3))
            major2, minor2, patch2 = int(sem2.group(1)), int(sem2.group(2)), int(sem2.group(3))
            
            if (major1, minor1, patch1) == (major2, minor2, patch2):
                return "exact_match"
            elif major1 == major2:
                return "minor_diff"
            else:
                return "major_diff"
        
        # Fall back to string comparison
        if version1 == version2:
            return "exact_match"
        else:
            return "format_mismatch"


class IntelligentSuggestionSystem:
    """
    Combines pattern detection, version management, and usage analytics to provide
    intelligent documentation suggestions.
    """
    
    def __init__(self, registry_path: str = ".agent-os/docs-registry.yaml"):
        self.pattern_detector = TechPatternDetector(registry_path)
        self.version_manager = VersionManager(registry_path)
        self.progressive_disclosure = ProgressiveDisclosure()
        self.registry_path = Path(registry_path)
    
    def generate_suggestions(
        self, 
        spec_text: str, 
        context: str = "create-spec",
        workflow_history: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive documentation suggestions
        
        Args:
            spec_text: Specification content to analyze
            context: Current workflow context
            workflow_history: Previous workflow contexts for learning
            
        Returns:
            Comprehensive suggestion report
        """
        # Detect patterns
        pattern_suggestions = self.pattern_detector.detect_documentation_needs(spec_text, context)
        
        # Group suggestions by category
        categorized_suggestions = {}
        for suggestion in pattern_suggestions:
            category = suggestion["category"]
            if category not in categorized_suggestions:
                categorized_suggestions[category] = []
            categorized_suggestions[category].append(suggestion)
        
        # Check version compatibility for existing registry entries
        compatibility_reports = []
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    registry = yaml.safe_load(f)
                
                for tech in registry.get('tech_stack', {}):
                    report = self.version_manager.check_compatibility(tech)
                    if report["warnings"] or report["status"] != "compatible":
                        compatibility_reports.append(report)
            except Exception:
                pass
        
        # Generate progressive disclosure recommendations
        disclosure_level = self._determine_disclosure_level(context, workflow_history or [])
        
        return {
            "context": context,
            "pattern_suggestions": {
                "by_priority": pattern_suggestions,
                "by_category": categorized_suggestions,
                "total_suggestions": len(pattern_suggestions)
            },
            "version_compatibility": {
                "reports": compatibility_reports,
                "needs_attention": len([r for r in compatibility_reports if r["warnings"]])
            },
            "progressive_disclosure": {
                "recommended_level": disclosure_level,
                "sections": self.progressive_disclosure.disclosure_levels[disclosure_level]["sections"]
            },
            "recommendations": self._generate_actionable_recommendations(
                pattern_suggestions, compatibility_reports, context
            )
        }
    
    def _determine_disclosure_level(self, context: str, workflow_history: List[str]) -> str:
        """Determine appropriate disclosure level based on context and history"""
        context_mapping = {
            "plan-product": "overview",
            "create-spec": "planning", 
            "execute-tasks": "implementation"
        }
        
        base_level = context_mapping.get(context, "overview")
        
        # Adjust based on workflow history
        if len(workflow_history) > 2:  # Experienced user
            level_progression = ["overview", "planning", "implementation", "optimization"]
            current_index = level_progression.index(base_level)
            if current_index < len(level_progression) - 1:
                return level_progression[current_index + 1]
        
        return base_level
    
    def _generate_actionable_recommendations(
        self, 
        pattern_suggestions: List[Dict], 
        compatibility_reports: List[Dict], 
        context: str
    ) -> List[Dict[str, Any]]:
        """Generate prioritized, actionable recommendations"""
        recommendations = []
        
        # High-priority pattern suggestions
        critical_suggestions = [s for s in pattern_suggestions if s["priority"] == "critical"]
        if critical_suggestions:
            recommendations.append({
                "type": "critical_documentation",
                "priority": "high",
                "title": "Critical Documentation Needed",
                "description": f"Found {len(critical_suggestions)} critical technologies requiring documentation",
                "action": "Add documentation for: " + ", ".join(s["technology"] for s in critical_suggestions),
                "technologies": [s["technology"] for s in critical_suggestions]
            })
        
        # Version compatibility issues
        problematic_versions = [r for r in compatibility_reports 
                              if r["status"] in ["potentially_incompatible", "registry_version_unknown"]]
        if problematic_versions:
            recommendations.append({
                "type": "version_compatibility",
                "priority": "medium",
                "title": "Version Compatibility Issues",
                "description": f"Found {len(problematic_versions)} technologies with version concerns",
                "action": "Review version compatibility for: " + ", ".join(r["technology"] for r in problematic_versions),
                "technologies": [r["technology"] for r in problematic_versions]
            })
        
        # Context-specific recommendations
        if context == "execute-tasks":
            implementation_suggestions = [s for s in pattern_suggestions if s["priority"] in ["high", "critical"]]
            if implementation_suggestions:
                recommendations.append({
                    "type": "implementation_documentation",
                    "priority": "high", 
                    "title": "Implementation Documentation Needed",
                    "description": "Implementation phase requires detailed technical documentation",
                    "action": "Load implementation-level documentation for detected technologies",
                    "technologies": [s["technology"] for s in implementation_suggestions]
                })
        
        return recommendations


# Main interface function for integration with workflows
def analyze_specification_for_documentation(
    spec_text: str,
    context: str = "create-spec",
    registry_path: str = ".agent-os/docs-registry.yaml"
) -> Dict[str, Any]:
    """
    Main entry point for smart documentation analysis
    
    Args:
        spec_text: Specification content to analyze
        context: Workflow context
        registry_path: Path to documentation registry
        
    Returns:
        Complete analysis with suggestions and recommendations
    """
    suggestion_system = IntelligentSuggestionSystem(registry_path)
    return suggestion_system.generate_suggestions(spec_text, context)


if __name__ == "__main__":
    # Demo/testing functionality
    sample_spec = """
    We need to build a payment processing system that integrates with Stripe for handling
    subscriptions and one-time payments. The system should use FastAPI for the REST API
    and PostgreSQL for data storage. We'll need authentication via Auth0 and deploy 
    using Docker containers on AWS.
    """
    
    result = analyze_specification_for_documentation(sample_spec, "create-spec")
    print("=== Smart Documentation Analysis ===")
    print(yaml.dump(result, default_flow_style=False, indent=2))