#!/usr/bin/env python3
"""
Performance Analysis CLI for Agent OS + PocketFlow Projects
Provides command-line access to document creation performance metrics and analysis.

This script is automatically installed in end-user projects at:
.agent-os/framework-tools/performance-cli.py

Usage:
    python3 .agent-os/framework-tools/performance-cli.py [command] [options]

    OR (if in project root):
    python3 -m .agent-os.framework-tools.performance-cli [command] [options]
"""

import argparse
from pathlib import Path
import json

def main():
    """Main CLI entry point for performance analysis"""
    parser = argparse.ArgumentParser(
        description="Performance analysis for Agent OS + PocketFlow document creation workflows"
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Analyze command
    analyze_parser = subparsers.add_parser(
        'analyze',
        help='Analyze recent performance metrics'
    )
    analyze_parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to analyze (default: 30)'
    )
    analyze_parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    # Report command
    report_parser = subparsers.add_parser(
        'report',
        help='Generate detailed performance report'
    )
    report_parser.add_argument(
        '--days',
        type=int,
        default=7,
        help='Number of days to include in report (default: 7)'
    )
    report_parser.add_argument(
        '--save',
        help='Save report to file (optional)'
    )

    # Export command
    export_parser = subparsers.add_parser(
        'export',
        help='Export metrics data to file'
    )
    export_parser.add_argument(
        'output_file',
        help='Output file path'
    )
    export_parser.add_argument(
        '--format',
        choices=['json', 'csv'],
        default='json',
        help='Export format (default: json)'
    )

    # Clear command
    clear_parser = subparsers.add_parser(
        'clear',
        help='Clear old metrics data'
    )
    clear_parser.add_argument(
        '--older-than',
        type=int,
        default=90,
        help='Clear metrics older than N days (default: 90)'
    )

    # Status command
    subparsers.add_parser(
        'status',
        help='Show metrics database status'
    )

    # Optimization command
    optimize_parser = subparsers.add_parser(
        'optimize',
        help='Show context optimization metrics and analysis'
    )
    optimize_parser.add_argument(
        '--days',
        type=int,
        default=30,
        help='Number of days to analyze (default: 30)'
    )
    optimize_parser.add_argument(
        '--format',
        choices=['text', 'json'],
        default='text',
        help='Output format (default: text)'
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Import the monitoring module - try different paths
    try:
        # Try importing from Claude Code monitoring module (if available)
        import sys
        project_root = Path.cwd()

        # Check if we can find the monitoring module
        claude_code_path = None

        # Look for claude-code directory in common locations
        possible_paths = [
            project_root / '.agent-os' / 'claude-code',
            project_root / 'claude-code',
            Path.home() / '.agent-os' / 'claude-code'
        ]

        for path in possible_paths:
            if (path / 'monitoring' / 'document-creation-metrics.py').exists():
                claude_code_path = path
                break

        if claude_code_path:
            sys.path.insert(0, str(claude_code_path))
            from monitoring.document_creation_metrics import DocumentCreationMetrics
        else:
            print("❌ Error: Performance monitoring module not found.")
            print("   This may indicate:")
            print("   1. Agent OS + PocketFlow framework not properly installed")
            print("   2. Document orchestration coordinator not yet used")
            print("   3. Missing claude-code components in project")
            print("   ")
            print("   Try running a document creation workflow first:")
            print("   /plan-product")
            return 1

    except ImportError as e:
        print(f"❌ Error importing performance monitoring: {e}")
        print("   Make sure the Agent OS + PocketFlow framework is properly installed.")
        return 1

    # Initialize metrics system
    try:
        metrics = DocumentCreationMetrics(project_root=project_root)
    except Exception as e:
        print(f"❌ Error initializing metrics: {e}")
        return 1

    # Execute commands
    try:
        if args.command == 'analyze':
            return cmd_analyze(metrics, args)
        elif args.command == 'report':
            return cmd_report(metrics, args)
        elif args.command == 'export':
            return cmd_export(metrics, args)
        elif args.command == 'clear':
            return cmd_clear(metrics, args)
        elif args.command == 'status':
            return cmd_status(metrics, args)
        elif args.command == 'optimize':
            return cmd_optimize(metrics, args)
        else:
            print(f"❌ Unknown command: {args.command}")
            return 1
    except Exception as e:
        print(f"❌ Command failed: {e}")
        return 1

def cmd_analyze(metrics, args):
    """Analyze performance command"""
    print(f"📊 Analyzing performance for last {args.days} days...")

    analysis = metrics.analyze_performance(days=args.days)

    if "error" in analysis:
        print(f"❌ {analysis['error']}")
        return 1

    if args.format == 'json':
        print(json.dumps(analysis, indent=2))
    else:
        # Text format
        orchestration = analysis["orchestration_performance"]
        print("\n📈 PERFORMANCE SUMMARY:")
        print(f"   Total sessions: {analysis['total_sessions']}")
        print(f"   Average duration: {orchestration['avg_duration']:.2f}s")
        print(f"   Success rate: {orchestration['avg_success_rate']:.1%}")

        if orchestration['avg_performance_improvement']:
            print(f"   Performance improvement: {orchestration['avg_performance_improvement']:.1f}%")

        print("\n🤖 TOP AGENT PERFORMANCE:")
        for agent_name, stats in list(analysis["agent_performance"].items())[:5]:
            print(f"   {agent_name}: {stats['avg_duration']:.1f}s avg, {stats['success_rate']:.1%} success")

    return 0

def cmd_report(metrics, args):
    """Generate detailed report command"""
    print(f"📋 Generating performance report for last {args.days} days...")

    report = metrics.generate_report(days=args.days)

    if args.save:
        with open(args.save, 'w') as f:
            f.write(report)
        print(f"📄 Report saved to: {args.save}")
    else:
        print("\n" + report)

    return 0

def cmd_export(metrics, args):
    """Export metrics command"""
    output_path = Path(args.output_file)
    print(f"📤 Exporting metrics to {output_path} in {args.format} format...")

    metrics.export_metrics(output_path, format=args.format)
    return 0

def cmd_clear(metrics, args):
    """Clear old metrics command"""
    print(f"🧹 Clearing metrics older than {args.older_than} days...")

    deleted_count = metrics.clear_old_metrics(days=args.older_than)
    print(f"✅ Cleared {deleted_count} old sessions")

    return 0

def cmd_status(metrics, args):
    """Show metrics status command"""
    print("📊 PERFORMANCE METRICS STATUS:")
    print(f"   Database: {metrics.metrics_db}")
    print(f"   Database exists: {'✅' if metrics.metrics_db.exists() else '❌'}")

    if metrics.metrics_db.exists():
        # Get database stats
        import sqlite3
        with sqlite3.connect(metrics.metrics_db) as conn:
            session_count = conn.execute("SELECT COUNT(*) FROM orchestration_sessions").fetchone()[0]
            agent_count = conn.execute("SELECT COUNT(*) FROM agent_executions").fetchone()[0]

        print(f"   Total sessions: {session_count}")
        print(f"   Total agent executions: {agent_count}")

        if session_count > 0:
            # Get recent activity
            with sqlite3.connect(metrics.metrics_db) as conn:
                recent = conn.execute("""
                    SELECT session_id, created_date, total_agents, successful_agents
                    FROM orchestration_sessions
                    ORDER BY start_time DESC
                    LIMIT 5
                """).fetchall()

            print("\n🕒 RECENT SESSIONS:")
            for row in recent:
                session_id, created_date, total_agents, successful_agents = row
                print(f"   {session_id}: {successful_agents}/{total_agents} agents - {created_date[:19]}")
    else:
        print("   No metrics database found - run a document creation workflow first")

    return 0

def cmd_optimize(metrics, args):
    """Show context optimization analysis command"""
    print(f"🎯 Analyzing context optimization for last {args.days} days...")

    try:
        optimization_stats = metrics.get_optimization_statistics(days=args.days)
    except Exception as e:
        print(f"❌ Error getting optimization statistics: {e}")
        print("   This may indicate:")
        print("   1. No optimization metrics recorded yet")
        print("   2. Document orchestration coordinator not used with context optimization")
        print("   3. Database schema needs to be updated")
        print("")
        print("   Try running a document creation workflow with optimization first:")
        print("   /plan-product")
        return 1

    if optimization_stats['total_sessions'] == 0:
        print("❌ No optimization data found for the specified time period.")
        print("   Run document creation workflows to generate optimization metrics:")
        print("   /plan-product")
        return 1

    if args.format == 'json':
        print(json.dumps(optimization_stats, indent=2))
    else:
        # Text format
        print("\n🎯 CONTEXT OPTIMIZATION SUMMARY:")
        print(f"   Optimization sessions: {optimization_stats['total_sessions']}")
        print(f"   Average token reduction: {optimization_stats['avg_token_reduction']:.1f}%")
        print(f"   Token reduction range: {optimization_stats['min_token_reduction']:.1f}% - {optimization_stats['max_token_reduction']:.1f}%")
        print(f"   Total token savings: {optimization_stats['total_token_savings']:,} tokens")
        print(f"   Average agents optimized: {optimization_stats['avg_agents_optimized']:.1f} per session")

        # Optimization trend with emoji
        trend_emoji = {"improving": "📈", "declining": "📉", "stable": "📊", "insufficient_data": "❓", "no_data": "❌"}
        trend_text = {
            "improving": "Optimization effectiveness is improving",
            "declining": "Optimization effectiveness is declining",
            "stable": "Optimization effectiveness is stable",
            "insufficient_data": "Insufficient data to determine trend",
            "no_data": "No optimization data available"
        }

        print(f"   Optimization trend: {trend_emoji[optimization_stats['optimization_trend']]} {trend_text[optimization_stats['optimization_trend']]}")

        if optimization_stats['total_fields_excluded'] > 0 or optimization_stats['total_fields_compressed'] > 0:
            print(f"   Fields excluded: {optimization_stats['total_fields_excluded']}")
            print(f"   Fields compressed: {optimization_stats['total_fields_compressed']}")

        # Recent sessions summary
        if optimization_stats['recent_sessions']:
            print("\n📋 RECENT OPTIMIZATION SESSIONS:")
            for i, session in enumerate(optimization_stats['recent_sessions'][:3], 1):
                reduction_pct, orig_tokens, opt_tokens, savings, agents, excluded, compressed, date = session
                print(f"   {i}. {reduction_pct:.1f}% reduction ({savings:,} tokens saved, {agents} agents) - {date[:19]}")

        # Recommendations
        print("\n💡 OPTIMIZATION RECOMMENDATIONS:")
        if optimization_stats['avg_token_reduction'] < 20:
            print("   🔧 Current token reduction is below target (20%+)")
            print("   📝 Consider reviewing agent context requirements and field priorities")
            print("   🎯 Target: 30-50% token reduction for optimal efficiency")
        elif optimization_stats['avg_token_reduction'] > 60:
            print("   ⚠️  High token reduction detected (>60%)")
            print("   ✅ Verify document quality is maintained with aggressive optimization")
            print("   📊 Consider sampling document outputs for quality validation")
        else:
            print("   ✅ Optimization performance is within target range (20-60%)")
            print("   📈 Continue monitoring for consistent efficiency gains")

    return 0

if __name__ == "__main__":
    exit(main())