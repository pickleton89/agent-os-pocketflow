#!/usr/bin/env python3
"""
Smart Features CLI for Agent OS + PocketFlow Documentation Discovery
Provides command-line interface for testing and using smart features.
"""

import argparse
import sys
import yaml
from pathlib import Path

from smart_features import (
    TechPatternDetector,
    ProgressiveDisclosure, 
    VersionManager,
    analyze_specification_for_documentation
)


def cmd_analyze(args):
    """Analyze a specification file for documentation needs"""
    spec_path = Path(args.spec_file)
    
    if not spec_path.exists():
        print(f"❌ Specification file not found: {args.spec_file}")
        return 1
    
    # Read specification content
    try:
        with open(spec_path, 'r') as f:
            spec_content = f.read()
    except Exception as e:
        print(f"❌ Error reading specification file: {e}")
        return 1
    
    # Analyze specification
    print(f"🔍 Analyzing specification: {spec_path.name}")
    print(f"📝 Context: {args.context}")
    print("-" * 50)
    
    try:
        result = analyze_specification_for_documentation(
            spec_text=spec_content,
            context=args.context,
            registry_path=args.registry
        )
        
        # Display results
        print("\n📊 Analysis Results:")
        print(f"   Total suggestions: {result['pattern_suggestions']['total_suggestions']}")
        print(f"   Version issues: {result['version_compatibility']['needs_attention']}")
        print(f"   Recommended disclosure level: {result['progressive_disclosure']['recommended_level']}")
        
        # Show pattern suggestions
        if result['pattern_suggestions']['by_priority']:
            print("\n🔧 Technology Suggestions:")
            for suggestion in result['pattern_suggestions']['by_priority']:
                print(f"   {suggestion['technology']} ({suggestion['priority']} priority)")
                print(f"     Confidence: {suggestion['confidence']:.1%}")
                print(f"     Category: {suggestion['category']}")
                print(f"     Matched: {', '.join(suggestion['matched_patterns'][:3])}")
        
        # Show recommendations
        if result['recommendations']:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(result['recommendations'], 1):
                print(f"   {i}. {rec['title']} ({rec['priority']} priority)")
                print(f"      {rec['description']}")
                if 'action' in rec:
                    print(f"      Action: {rec['action']}")
        
        # Save results if requested
        if args.output:
            output_path = Path(args.output)
            try:
                with open(output_path, 'w') as f:
                    yaml.dump(result, f, default_flow_style=False, indent=2)
                print(f"\n💾 Results saved to: {output_path}")
            except Exception as e:
                print(f"\n❌ Error saving results: {e}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error during analysis: {e}")
        return 1


def cmd_detect_patterns(args):
    """Detect patterns in text input"""
    if args.text:
        spec_text = args.text
    elif args.file:
        try:
            with open(args.file, 'r') as f:
                spec_text = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return 1
    else:
        print("❌ Must provide either --text or --file")
        return 1
    
    print("🔍 Detecting patterns in text...")
    print(f"📝 Context: {args.context}")
    print("-" * 50)
    
    try:
        detector = TechPatternDetector(args.registry)
        suggestions = detector.detect_documentation_needs(spec_text, args.context)
        
        if suggestions:
            print(f"\n🔧 Found {len(suggestions)} technology patterns:")
            for suggestion in suggestions:
                print(f"   📋 {suggestion['technology']} ({suggestion['category']})")
                print(f"      Priority: {suggestion['priority']}")
                print(f"      Confidence: {suggestion['confidence']:.1%}")
                print(f"      Patterns: {', '.join(suggestion['matched_patterns'])}")
                print()
        else:
            print("📭 No patterns detected")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error detecting patterns: {e}")
        return 1


def cmd_check_versions(args):
    """Check version compatibility"""
    print("🔍 Checking version compatibility...")
    print(f"📋 Registry: {args.registry}")
    print("-" * 50)
    
    try:
        version_manager = VersionManager(args.registry)
        
        if args.tech:
            # Check specific technology
            compatibility = version_manager.check_compatibility(args.tech, args.version)
            
            print(f"\n📦 {args.tech}:")
            print(f"   Registry version: {compatibility.get('registry_version', 'Unknown')}")
            print(f"   Project version: {compatibility.get('project_version', 'Unknown')}")
            print(f"   Status: {compatibility['status']}")
            
            if compatibility['warnings']:
                print("   ⚠️  Warnings:")
                for warning in compatibility['warnings']:
                    print(f"      - {warning}")
            
            if compatibility['suggestions']:
                print("   💡 Suggestions:")
                for suggestion in compatibility['suggestions']:
                    print(f"      - {suggestion}")
        else:
            # Check all technologies in registry
            registry_path = Path(args.registry)
            if not registry_path.exists():
                print(f"❌ Registry not found: {args.registry}")
                return 1
            
            with open(registry_path, 'r') as f:
                registry = yaml.safe_load(f)
            
            tech_stack = registry.get('tech_stack', {})
            if not tech_stack:
                print("📭 No technologies in registry")
                return 0
            
            print(f"\n📦 Checking {len(tech_stack)} technologies:")
            for tech in tech_stack:
                compatibility = version_manager.check_compatibility(tech)
                status_icon = "✅" if compatibility['status'] == "compatible" else "⚠️"
                print(f"   {status_icon} {tech}: {compatibility['status']}")
                
                if compatibility['warnings']:
                    for warning in compatibility['warnings']:
                        print(f"      - {warning}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error checking versions: {e}")
        return 1


def cmd_test_disclosure(args):
    """Test progressive disclosure levels"""
    print("🔍 Testing progressive disclosure...")
    print(f"📋 Source: {args.source}")
    print(f"📈 Level: {args.level}")
    print("-" * 50)
    
    try:
        disclosure = ProgressiveDisclosure(cache_dir=args.cache_dir)
        content = disclosure.get_content_for_level(args.source, args.level)
        
        print(f"\n📖 Content for {args.level} level:")
        print(f"   Source: {content['source']}")
        print(f"   Sections: {', '.join(content['sections'])}")
        print(f"   Priority: {content['priority']}")
        print(f"   Cache TTL: {content['metadata']['ttl_hours']} hours")
        print(f"   Timestamp: {content['timestamp']}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Error testing disclosure: {e}")
        return 1


def cmd_run_tests(args):
    """Run test suite"""
    print("🧪 Running Smart Features Test Suite...")
    print("=" * 50)
    
    try:
        # Import and run test functions
        from test_smart_features import main as run_tests
        return run_tests()
    except ImportError:
        print("❌ Test module not found - ensure test_smart_features.py is available")
        return 1
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Smart Features CLI for Agent OS + PocketFlow Documentation Discovery",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Analyze a specification file
  python smart_cli.py analyze docs/my-spec.md --context create-spec

  # Detect patterns in text
  python smart_cli.py detect --text "Build FastAPI app with Stripe payments"

  # Check version compatibility
  python smart_cli.py versions --tech fastapi --version 0.104.1

  # Test progressive disclosure
  python smart_cli.py disclosure --source fastapi --level implementation

  # Run test suite
  python smart_cli.py test
        """
    )
    
    # Global arguments
    parser.add_argument(
        '--registry', 
        default='.agent-os/docs-registry.yaml',
        help='Path to documentation registry (default: .agent-os/docs-registry.yaml)'
    )
    
    # Create subcommands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze specification for documentation needs')
    analyze_parser.add_argument('spec_file', help='Path to specification file')
    analyze_parser.add_argument('--context', choices=['plan-product', 'create-spec', 'execute-tasks'], 
                               default='create-spec', help='Workflow context')
    analyze_parser.add_argument('--output', help='Save results to YAML file')
    
    # Pattern detection command
    detect_parser = subparsers.add_parser('detect', help='Detect technology patterns')
    detect_group = detect_parser.add_mutually_exclusive_group(required=True)
    detect_group.add_argument('--text', help='Text to analyze')
    detect_group.add_argument('--file', help='File to analyze')
    detect_parser.add_argument('--context', choices=['plan-product', 'create-spec', 'execute-tasks'],
                              default='create-spec', help='Workflow context')
    
    # Version checking command
    versions_parser = subparsers.add_parser('versions', help='Check version compatibility')
    versions_parser.add_argument('--tech', help='Specific technology to check')
    versions_parser.add_argument('--version', help='Project version to compare against')
    
    # Progressive disclosure command
    disclosure_parser = subparsers.add_parser('disclosure', help='Test progressive disclosure')
    disclosure_parser.add_argument('--source', required=True, help='Documentation source identifier')
    disclosure_parser.add_argument('--level', choices=['overview', 'planning', 'implementation', 'optimization'],
                                  default='overview', help='Disclosure level')
    disclosure_parser.add_argument('--cache-dir', default='.agent-os/cache', help='Cache directory')
    
    # Test command
    subparsers.add_parser('test', help='Run test suite')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Check if command was provided
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate command handler
    commands = {
        'analyze': cmd_analyze,
        'detect': cmd_detect_patterns,
        'versions': cmd_check_versions,
        'disclosure': cmd_test_disclosure,
        'test': cmd_run_tests
    }
    
    handler = commands.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())