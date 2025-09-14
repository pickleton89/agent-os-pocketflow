#!/usr/bin/env python3
"""
Document Creation Performance Metrics for Agent OS + PocketFlow Framework

Monitors and analyzes performance of document creation agents.
Part of Phase 4 optimization for the document creation subagent refactoring.

Usage:
    python3 document-creation-metrics.py [--analyze] [--export] [--reset]
"""

import json
import time
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import statistics
import sqlite3


@dataclass
class AgentMetric:
    """Performance metrics for a single agent execution"""
    agent_name: str
    start_time: float
    end_time: float
    duration: float
    token_usage: Optional[int] = None
    success: bool = True
    error_message: Optional[str] = None
    output_file: Optional[str] = None
    file_size_bytes: Optional[int] = None


@dataclass
class OrchestrationMetric:
    """Performance metrics for an orchestration session"""
    session_id: str
    start_time: float
    end_time: float
    total_duration: float
    parallel_groups: int
    total_agents: int
    successful_agents: int
    failed_agents: int
    total_tokens: Optional[int] = None
    sequential_baseline_estimate: Optional[float] = None
    performance_improvement: Optional[float] = None


class DocumentCreationMetrics:
    """Performance monitoring and metrics collection for document creation agents"""

    def __init__(self, project_root: Path = None, metrics_db_path: Path = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()

        # Metrics database location
        if metrics_db_path:
            self.metrics_db = metrics_db_path
        else:
            self.metrics_db = self.project_root / '.agent-os' / 'metrics' / 'document_creation.db'

        # Ensure metrics directory exists
        self.metrics_db.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

        # Current session tracking
        self.current_session_id: Optional[str] = None
        self.session_start_time: Optional[float] = None
        self.current_agent_metrics: List[AgentMetric] = []

    def _init_database(self) -> None:
        """Initialize SQLite database for metrics storage"""
        with sqlite3.connect(self.metrics_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS orchestration_sessions (
                    session_id TEXT PRIMARY KEY,
                    start_time REAL,
                    end_time REAL,
                    total_duration REAL,
                    parallel_groups INTEGER,
                    total_agents INTEGER,
                    successful_agents INTEGER,
                    failed_agents INTEGER,
                    total_tokens INTEGER,
                    sequential_baseline_estimate REAL,
                    performance_improvement REAL,
                    created_date TEXT
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS agent_executions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    agent_name TEXT,
                    start_time REAL,
                    end_time REAL,
                    duration REAL,
                    token_usage INTEGER,
                    success BOOLEAN,
                    error_message TEXT,
                    output_file TEXT,
                    file_size_bytes INTEGER,
                    created_date TEXT,
                    FOREIGN KEY (session_id) REFERENCES orchestration_sessions (session_id)
                )
            """)

            conn.commit()

    def start_session(self, session_id: Optional[str] = None) -> str:
        """Start a new orchestration session"""
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{int(time.time() * 1000) % 10000}"

        self.current_session_id = session_id
        self.session_start_time = time.time()
        self.current_agent_metrics = []

        print(f"📊 Started metrics session: {session_id}")
        return session_id

    def record_agent_start(self, agent_name: str) -> float:
        """Record agent execution start"""
        start_time = time.time()
        print(f"⏱️  Started {agent_name} at {datetime.now().strftime('%H:%M:%S')}")
        return start_time

    def record_agent_completion(self, agent_name: str, start_time: float,
                              success: bool = True, error_message: Optional[str] = None,
                              token_usage: Optional[int] = None,
                              output_file: Optional[str] = None) -> AgentMetric:
        """Record agent execution completion"""
        end_time = time.time()
        duration = end_time - start_time

        # Get file size if output file provided
        file_size_bytes = None
        if output_file and Path(output_file).exists():
            file_size_bytes = Path(output_file).stat().st_size

        metric = AgentMetric(
            agent_name=agent_name,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
            token_usage=token_usage,
            success=success,
            error_message=error_message,
            output_file=output_file,
            file_size_bytes=file_size_bytes
        )

        self.current_agent_metrics.append(metric)

        status = "✅" if success else "❌"
        print(f"{status} Completed {agent_name} in {duration:.2f}s")

        return metric

    def finish_session(self, parallel_groups: int = 1) -> OrchestrationMetric:
        """Finish the current orchestration session and record metrics"""
        if not self.current_session_id or self.session_start_time is None:
            raise ValueError("No active session to finish")

        end_time = time.time()
        total_duration = end_time - self.session_start_time

        # Calculate metrics
        successful_agents = len([m for m in self.current_agent_metrics if m.success])
        failed_agents = len([m for m in self.current_agent_metrics if not m.success])
        total_tokens = sum(m.token_usage for m in self.current_agent_metrics if m.token_usage)

        # Estimate sequential baseline (sum of all agent durations)
        sequential_baseline = sum(m.duration for m in self.current_agent_metrics)

        # Calculate performance improvement
        performance_improvement = None
        if sequential_baseline > 0:
            performance_improvement = ((sequential_baseline - total_duration) / sequential_baseline) * 100

        orchestration_metric = OrchestrationMetric(
            session_id=self.current_session_id,
            start_time=self.session_start_time,
            end_time=end_time,
            total_duration=total_duration,
            parallel_groups=parallel_groups,
            total_agents=len(self.current_agent_metrics),
            successful_agents=successful_agents,
            failed_agents=failed_agents,
            total_tokens=total_tokens if total_tokens > 0 else None,
            sequential_baseline_estimate=sequential_baseline,
            performance_improvement=performance_improvement
        )

        # Store in database
        self._store_session_metrics(orchestration_metric)

        # Print summary
        print(f"🎯 Session {self.current_session_id} complete:")
        print(f"   Total time: {total_duration:.2f}s")
        print(f"   Sequential baseline: {sequential_baseline:.2f}s")
        if performance_improvement:
            print(f"   Performance improvement: {performance_improvement:.1f}%")
        print(f"   Success rate: {successful_agents}/{len(self.current_agent_metrics)} agents")

        # Reset session
        self.current_session_id = None
        self.session_start_time = None
        self.current_agent_metrics = []

        return orchestration_metric

    def _store_session_metrics(self, orchestration_metric: OrchestrationMetric) -> None:
        """Store orchestration session metrics in database"""
        with sqlite3.connect(self.metrics_db) as conn:
            # Store orchestration session
            conn.execute("""
                INSERT INTO orchestration_sessions
                (session_id, start_time, end_time, total_duration, parallel_groups,
                 total_agents, successful_agents, failed_agents, total_tokens,
                 sequential_baseline_estimate, performance_improvement, created_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                orchestration_metric.session_id,
                orchestration_metric.start_time,
                orchestration_metric.end_time,
                orchestration_metric.total_duration,
                orchestration_metric.parallel_groups,
                orchestration_metric.total_agents,
                orchestration_metric.successful_agents,
                orchestration_metric.failed_agents,
                orchestration_metric.total_tokens,
                orchestration_metric.sequential_baseline_estimate,
                orchestration_metric.performance_improvement,
                datetime.now().isoformat()
            ))

            # Store individual agent metrics
            for agent_metric in self.current_agent_metrics:
                conn.execute("""
                    INSERT INTO agent_executions
                    (session_id, agent_name, start_time, end_time, duration,
                     token_usage, success, error_message, output_file,
                     file_size_bytes, created_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    orchestration_metric.session_id,
                    agent_metric.agent_name,
                    agent_metric.start_time,
                    agent_metric.end_time,
                    agent_metric.duration,
                    agent_metric.token_usage,
                    agent_metric.success,
                    agent_metric.error_message,
                    agent_metric.output_file,
                    agent_metric.file_size_bytes,
                    datetime.now().isoformat()
                ))

            conn.commit()

    def analyze_performance(self, days: int = 30) -> Dict[str, Any]:
        """Analyze performance trends over specified period"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)

        with sqlite3.connect(self.metrics_db) as conn:
            # Get orchestration sessions
            sessions = conn.execute("""
                SELECT * FROM orchestration_sessions
                WHERE start_time > ?
                ORDER BY start_time DESC
            """, (cutoff_time,)).fetchall()

            # Get agent executions
            agents = conn.execute("""
                SELECT * FROM agent_executions
                WHERE start_time > ?
                ORDER BY start_time DESC
            """, (cutoff_time,)).fetchall()

        if not sessions:
            return {"error": "No sessions found in specified time period"}

        # Analyze orchestration performance
        total_durations = [row[3] for row in sessions]  # total_duration
        performance_improvements = [row[10] for row in sessions if row[10] is not None]
        success_rates = [row[6] / row[5] if row[5] > 0 else 0 for row in sessions]  # successful/total

        # Analyze agent performance
        agent_stats = {}
        for agent_row in agents:
            agent_name = agent_row[2]
            if agent_name not in agent_stats:
                agent_stats[agent_name] = {
                    'executions': 0,
                    'successes': 0,
                    'durations': [],
                    'token_usage': []
                }

            agent_stats[agent_name]['executions'] += 1
            if agent_row[6]:  # success
                agent_stats[agent_name]['successes'] += 1
            agent_stats[agent_name]['durations'].append(agent_row[5])  # duration
            if agent_row[7]:  # token_usage
                agent_stats[agent_name]['token_usage'].append(agent_row[7])

        # Calculate statistics
        analysis = {
            "period_days": days,
            "total_sessions": len(sessions),
            "orchestration_performance": {
                "avg_duration": statistics.mean(total_durations),
                "min_duration": min(total_durations),
                "max_duration": max(total_durations),
                "std_duration": statistics.stdev(total_durations) if len(total_durations) > 1 else 0,
                "avg_performance_improvement": statistics.mean(performance_improvements) if performance_improvements else None,
                "avg_success_rate": statistics.mean(success_rates)
            },
            "agent_performance": {}
        }

        # Agent-specific analysis
        for agent_name, stats in agent_stats.items():
            durations = stats['durations']
            analysis["agent_performance"][agent_name] = {
                "total_executions": stats['executions'],
                "success_rate": stats['successes'] / stats['executions'] if stats['executions'] > 0 else 0,
                "avg_duration": statistics.mean(durations),
                "min_duration": min(durations),
                "max_duration": max(durations),
                "std_duration": statistics.stdev(durations) if len(durations) > 1 else 0,
                "avg_tokens": statistics.mean(stats['token_usage']) if stats['token_usage'] else None
            }

        return analysis

    def generate_report(self, days: int = 30) -> str:
        """Generate a formatted performance report"""
        analysis = self.analyze_performance(days)

        if "error" in analysis:
            return f"❌ {analysis['error']}"

        report = []
        report.append(f"# Document Creation Performance Report")
        report.append(f"*Analysis for last {days} days*\n")

        # Overall statistics
        orchestration = analysis["orchestration_performance"]
        report.append(f"## Overall Performance")
        report.append(f"- **Total Sessions**: {analysis['total_sessions']}")
        report.append(f"- **Average Duration**: {orchestration['avg_duration']:.2f}s")
        report.append(f"- **Duration Range**: {orchestration['min_duration']:.2f}s - {orchestration['max_duration']:.2f}s")
        report.append(f"- **Average Success Rate**: {orchestration['avg_success_rate']:.1%}")

        if orchestration['avg_performance_improvement']:
            report.append(f"- **Average Performance Improvement**: {orchestration['avg_performance_improvement']:.1f}%")

        report.append("")

        # Agent-specific performance
        report.append(f"## Agent Performance")

        for agent_name, stats in analysis["agent_performance"].items():
            report.append(f"### {agent_name}")
            report.append(f"- **Executions**: {stats['total_executions']}")
            report.append(f"- **Success Rate**: {stats['success_rate']:.1%}")
            report.append(f"- **Average Duration**: {stats['avg_duration']:.2f}s")
            report.append(f"- **Duration Range**: {stats['min_duration']:.2f}s - {stats['max_duration']:.2f}s")

            if stats['avg_tokens']:
                report.append(f"- **Average Token Usage**: {stats['avg_tokens']:.0f} tokens")

            report.append("")

        # Performance recommendations
        report.append(f"## Recommendations")

        # Identify slow agents
        slow_agents = []
        fast_agents = []

        for agent_name, stats in analysis["agent_performance"].items():
            if stats['avg_duration'] > 30:  # Threshold: 30 seconds
                slow_agents.append((agent_name, stats['avg_duration']))
            elif stats['avg_duration'] < 5:  # Threshold: 5 seconds
                fast_agents.append((agent_name, stats['avg_duration']))

        if slow_agents:
            report.append(f"### Slow Agents (>30s average)")
            for agent, duration in sorted(slow_agents, key=lambda x: x[1], reverse=True):
                report.append(f"- **{agent}**: {duration:.1f}s average - consider optimization")

        if fast_agents:
            report.append(f"### Fast Agents (<5s average)")
            for agent, duration in sorted(fast_agents, key=lambda x: x[1]):
                report.append(f"- **{agent}**: {duration:.1f}s average - good performance")

        # Performance improvement opportunities
        if orchestration['avg_performance_improvement'] and orchestration['avg_performance_improvement'] < 20:
            report.append(f"### Parallelization Opportunity")
            report.append(f"- Current improvement: {orchestration['avg_performance_improvement']:.1f}%")
            report.append(f"- Consider reviewing agent dependencies for better parallel execution")

        return "\n".join(report)

    def export_metrics(self, output_path: Path, format: str = "json") -> None:
        """Export metrics data to file"""
        analysis = self.analyze_performance(days=365)  # Export all data

        if format == "json":
            with open(output_path, 'w') as f:
                json.dump(analysis, f, indent=2)
        elif format == "csv":
            import csv

            with open(output_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Agent', 'Executions', 'Success Rate', 'Avg Duration', 'Min Duration', 'Max Duration', 'Avg Tokens'])

                for agent_name, stats in analysis["agent_performance"].items():
                    writer.writerow([
                        agent_name,
                        stats['total_executions'],
                        f"{stats['success_rate']:.1%}",
                        f"{stats['avg_duration']:.2f}",
                        f"{stats['min_duration']:.2f}",
                        f"{stats['max_duration']:.2f}",
                        f"{stats['avg_tokens']:.0f}" if stats['avg_tokens'] else "N/A"
                    ])

        print(f"📊 Metrics exported to: {output_path}")

    def clear_old_metrics(self, days: int = 90) -> int:
        """Clear metrics older than specified days"""
        cutoff_time = time.time() - (days * 24 * 60 * 60)

        with sqlite3.connect(self.metrics_db) as conn:
            # Count records to be deleted
            count_result = conn.execute("""
                SELECT COUNT(*) FROM orchestration_sessions WHERE start_time < ?
            """, (cutoff_time,)).fetchone()

            sessions_to_delete = count_result[0] if count_result else 0

            # Delete old records
            conn.execute("""
                DELETE FROM agent_executions
                WHERE session_id IN (
                    SELECT session_id FROM orchestration_sessions WHERE start_time < ?
                )
            """, (cutoff_time,))

            conn.execute("""
                DELETE FROM orchestration_sessions WHERE start_time < ?
            """, (cutoff_time,))

            conn.commit()

        print(f"🧹 Cleared {sessions_to_delete} old sessions (older than {days} days)")
        return sessions_to_delete


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Document creation performance metrics")
    parser.add_argument("--analyze", action="store_true", help="Analyze recent performance")
    parser.add_argument("--export", help="Export metrics to file (JSON or CSV)")
    parser.add_argument("--format", choices=["json", "csv"], default="json", help="Export format")
    parser.add_argument("--days", type=int, default=30, help="Days to analyze (default: 30)")
    parser.add_argument("--clear", type=int, help="Clear metrics older than N days")
    parser.add_argument("--project-root", default=".", help="Project root directory")

    args = parser.parse_args()

    metrics = DocumentCreationMetrics(Path(args.project_root))

    if args.clear:
        cleared = metrics.clear_old_metrics(args.clear)
        return 0

    if args.export:
        output_path = Path(args.export)
        metrics.export_metrics(output_path, args.format)
        return 0

    if args.analyze:
        report = metrics.generate_report(args.days)
        print(report)
        return 0

    # Interactive mode
    print("📊 Document Creation Metrics")
    print("No action specified. Use --help for options.")
    print(f"Metrics database: {metrics.metrics_db}")

    return 0


if __name__ == "__main__":
    exit(main())