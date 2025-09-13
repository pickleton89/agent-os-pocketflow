#!/usr/bin/env python3
"""
Phase 3: Status Reporting Utility for PocketFlow Framework
Enhanced user feedback and progress tracking system.
"""

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import subprocess


class StatusReporter:
    """Enhanced status reporting utility for PocketFlow operations."""
    
    def __init__(self, workflow_name: str, operation: str = "unknown"):
        self.workflow_name = workflow_name
        self.operation = operation
        self.start_time = time.time()
        self.status_file = f"/tmp/{workflow_name}_status.json"
        self.log_file = f"/tmp/{workflow_name}_operation.log"
        self.errors = []
        self.warnings = []
        self.info_messages = []
        self.current_step = 0
        self.total_steps = 0
        
        # Initialize status tracking only if no existing status file
        if not os.path.exists(self.status_file):
            self._init_status()
    
    def _init_status(self):
        """Initialize status tracking."""
        status_data = {
            "workflow_name": self.workflow_name,
            "operation": self.operation,
            "start_time": datetime.utcnow().isoformat(),
            "current_step": 0,
            "total_steps": 0,
            "status": "initializing",
            "errors": [],
            "warnings": [],
            "info": [],
            "files_created": [],
            "validation_results": None,
            "completion_percentage": 0
        }
        
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def set_total_steps(self, total: int):
        """Set the total number of steps for progress tracking."""
        self.total_steps = total
        self._update_status({"total_steps": total})
    
    def start_step(self, step_number: int, description: str):
        """Start a new step with progress indication."""
        self.current_step = step_number
        percentage = int((step_number * 100) / self.total_steps) if self.total_steps > 0 else 0
        
        # Create progress bar
        progress_bar = self._create_progress_bar(percentage)
        
        print(f"📊 Progress: [{progress_bar}] {percentage}% - Step {step_number}/{self.total_steps}: {description}")
        
        self._update_status({
            "current_step": step_number,
            "status": f"step_{step_number}",
            "current_description": description,
            "completion_percentage": percentage
        })
    
    def _create_progress_bar(self, percentage: int, width: int = 10) -> str:
        """Create a visual progress bar."""
        filled = int((percentage / 100) * width)
        return "█" * filled + "░" * (width - filled)
    
    def log_error(self, message: str, details: Optional[str] = None):
        """Log an error with optional details."""
        error_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "step": self.current_step,
            "message": message,
            "details": details
        }
        
        self.errors.append(error_entry)
        print(f"   ❌ ERROR: {message}")
        if details:
            print(f"      Details: {details}")
        
        self._update_status({"errors": self.errors})
    
    def log_warning(self, message: str, details: Optional[str] = None):
        """Log a warning with optional details."""
        warning_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "step": self.current_step,
            "message": message,
            "details": details
        }
        
        self.warnings.append(warning_entry)
        print(f"   ⚠️  WARNING: {message}")
        if details:
            print(f"      Details: {details}")
        
        self._update_status({"warnings": self.warnings})
    
    def log_info(self, message: str, details: Optional[str] = None):
        """Log an informational message."""
        info_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "step": self.current_step,
            "message": message,
            "details": details
        }
        
        self.info_messages.append(info_entry)
        print(f"   ✅ {message}")
        if details:
            print(f"      {details}")
        
        self._update_status({"info": self.info_messages})
    
    def log_success(self, message: str):
        """Log a success message."""
        print(f"   ✅ {message}")
        self.log_info(message)
    
    def add_created_file(self, file_path: str, file_type: str = "unknown"):
        """Track a file that was created."""
        file_entry = {
            "path": file_path,
            "type": file_type,
            "created_at": datetime.utcnow().isoformat(),
            "size": self._get_file_size(file_path)
        }
        
        # Load current status
        status_data = self._load_status()
        status_data["files_created"].append(file_entry)
        
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def _get_file_size(self, file_path: str) -> Optional[int]:
        """Get file size safely."""
        try:
            return os.path.getsize(file_path)
        except (OSError, FileNotFoundError):
            return None
    
    def _load_status(self) -> Dict[str, Any]:
        """Load current status data."""
        try:
            with open(self.status_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._init_status()
            with open(self.status_file, 'r') as f:
                return json.load(f)
    
    def _update_status(self, updates: Dict[str, Any]):
        """Update status file with new data."""
        status_data = self._load_status()
        status_data.update(updates)
        status_data["last_updated"] = datetime.utcnow().isoformat()
        
        with open(self.status_file, 'w') as f:
            json.dump(status_data, f, indent=2)
    
    def complete_operation(self, success: bool = True, final_message: str = None):
        """Mark operation as complete."""
        end_time = time.time()
        duration = end_time - self.start_time
        
        status = "completed" if success else "failed"
        
        completion_data = {
            "status": status,
            "end_time": datetime.utcnow().isoformat(),
            "duration_seconds": duration,
            # Avoid division by zero if total_steps is 0
            "completion_percentage": 100 if success else (int(self.current_step * 100 / self.total_steps) if self.total_steps > 0 else 0),
            "final_message": final_message or f"Operation {status}"
        }
        
        self._update_status(completion_data)
        
        # Print completion summary
        print("")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        if success:
            print(f"🎉 Operation Complete: {self.operation} for '{self.workflow_name}'")
        else:
            print(f"❌ Operation Failed: {self.operation} for '{self.workflow_name}'")
        
        print("")
        print(f"📊 Operation Summary:")
        print(f"   ⏱️  Duration: {duration:.1f}s")
        print(f"   📝 Steps Completed: {self.current_step}/{self.total_steps}")
        print(f"   ❌ Errors: {len(self.errors)}")
        print(f"   ⚠️  Warnings: {len(self.warnings)}")
        print(f"   ✅ Info Messages: {len(self.info_messages)}")
        
        if final_message:
            print(f"   💭 Final Status: {final_message}")
        
        # Return a defined value so callers can consume the result
        return self._load_status()
    
    def get_status_summary(self) -> Dict[str, Any]:
        """Get a comprehensive status summary based on persisted data."""
        status_data = self._load_status()

        # Prefer persisted lists to reflect cross-process state
        persisted_errors = status_data.get("errors", []) or []
        persisted_warnings = status_data.get("warnings", []) or []
        persisted_info = status_data.get("info", []) or []

        # Compute elapsed using persisted timestamps when available
        start_iso = status_data.get("start_time")
        end_iso = status_data.get("end_time")
        elapsed = 0.0
        try:
            if start_iso and end_iso:
                start_dt = datetime.fromisoformat(start_iso)
                end_dt = datetime.fromisoformat(end_iso)
                elapsed = max(0.0, (end_dt - start_dt).total_seconds())
            elif start_iso:
                start_dt = datetime.fromisoformat(start_iso)
                # Using UTC now for a rough elapsed during run
                now_dt = datetime.utcnow()
                elapsed = max(0.0, (now_dt - start_dt).total_seconds())
        except Exception:
            # Fallback to object lifetime if parsing fails
            elapsed = max(0.0, time.time() - self.start_time)

        summary = {
            **status_data,
            "elapsed_seconds": elapsed,
            "is_running": status_data.get("status", "").startswith("step_"),
            "has_errors": len(persisted_errors) > 0,
            "has_warnings": len(persisted_warnings) > 0,
            "error_count": len(persisted_errors),
            "warning_count": len(persisted_warnings),
            "info_count": len(persisted_info),
        }

        return summary
    
    def print_status_report(self):
        """Print a detailed status report."""
        summary = self.get_status_summary()
        
        print(f"📊 Status Report: {self.workflow_name}")
        print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"Operation: {summary['operation']}")
        print(f"Status: {summary['status']}")
        print(f"Progress: {summary.get('completion_percentage', 0)}%")
        print(f"Step: {summary.get('current_step', 0)}/{summary.get('total_steps', 0)}")
        print(f"Elapsed: {summary['elapsed_seconds']:.1f}s")
        
        if summary.get('current_description'):
            print(f"Current: {summary['current_description']}")
        
        print("")
        
        # Error summary (use persisted data)
        errors_list = summary.get('errors') or []
        if summary.get('has_errors'):
            print(f"❌ Errors ({summary.get('error_count', 0)}):")
            for error in errors_list[-3:]:  # Show last 3 errors
                msg = error.get('message', str(error))
                print(f"   • {msg}")
                details = error.get('details') if isinstance(error, dict) else None
                if details:
                    print(f"     {str(details)[:100]}...")

        # Warning summary (use persisted data)
        warnings_list = summary.get('warnings') or []
        if summary.get('has_warnings'):
            print(f"⚠️  Warnings ({summary.get('warning_count', 0)}):")
            for warning in warnings_list[-3:]:  # Show last 3 warnings
                msg = warning.get('message', str(warning)) if isinstance(warning, dict) else str(warning)
                print(f"   • {msg}")
        
        # Files created
        if summary.get('files_created'):
            print(f"📄 Files Created ({len(summary['files_created'])}):")
            for file_info in summary['files_created'][-5:]:  # Show last 5 files
                size_info = f" ({file_info['size']} bytes)" if file_info.get('size') else ""
                print(f"   • {file_info['path']}{size_info}")
        
        print("")
        print(f"📄 Status file: {self.status_file}")
        print(f"📄 Log file: {self.log_file}")


class ErrorRecoveryManager:
    """Enhanced error recovery and handling system."""
    
    def __init__(self, status_reporter: StatusReporter):
        self.reporter = status_reporter
        self.recovery_strategies = {
            "pattern_analysis_failed": self._recover_pattern_analysis,
            "template_generation_failed": self._recover_template_generation,
            "dependency_setup_failed": self._recover_dependency_setup,
            "validation_failed": self._recover_validation,
            "context_extraction_failed": self._recover_context_extraction
        }
    
    def handle_error(self, error_type: str, error_message: str, context: Dict[str, Any] = None) -> bool:
        """Handle an error with appropriate recovery strategy."""
        self.reporter.log_error(f"Error type: {error_type}", error_message)
        
        if error_type in self.recovery_strategies:
            self.reporter.log_info(f"Attempting recovery for: {error_type}")
            return self.recovery_strategies[error_type](error_message, context or {})
        else:
            self.reporter.log_error(f"No recovery strategy for: {error_type}")
            return False
    
    def _recover_pattern_analysis(self, error_message: str, context: Dict[str, Any]) -> bool:
        """Recover from pattern analysis failures."""
        self.reporter.log_info("Attempting pattern analysis recovery...")
        
        # Try fallback pattern
        fallback_pattern = "WORKFLOW"
        self.reporter.log_warning(f"Using fallback pattern: {fallback_pattern}")
        
        # Update context with fallback
        context["pattern"] = fallback_pattern
        context["confidence"] = "fallback"
        
        return True
    
    def _recover_template_generation(self, error_message: str, context: Dict[str, Any]) -> bool:
        """Recover from template generation failures."""
        self.reporter.log_info("Attempting template generation recovery...")
        
        # Check common issues
        if "templates directory not found" in error_message.lower():
            self.reporter.log_warning("Templates directory issue detected")
            self.reporter.log_info("Try running from ~/.agent-os directory")
            return False
        
        if "permission" in error_message.lower():
            self.reporter.log_warning("Permission issue detected")
            self.reporter.log_info("Check write permissions for .agent-os/workflows/")
            return False
        
        # Generic recovery attempt
        self.reporter.log_info("Attempting simplified template generation...")
        return True
    
    def _recover_dependency_setup(self, error_message: str, context: Dict[str, Any]) -> bool:
        """Recover from dependency setup failures."""
        self.reporter.log_info("Attempting dependency setup recovery...")
        
        # Check for common dependency issues
        if "network" in error_message.lower() or "connection" in error_message.lower():
            self.reporter.log_warning("Network connectivity issue detected")
            self.reporter.log_info("Consider manual dependency installation later")
            return True  # Continue without dependencies
        
        return True
    
    def _recover_validation(self, error_message: str, context: Dict[str, Any]) -> bool:
        """Recover from validation failures."""
        self.reporter.log_info("Attempting validation recovery...")
        
        # Validation failures are often non-fatal
        self.reporter.log_warning("Validation issues detected but continuing")
        self.reporter.log_info("Review validation report for details")
        
        return True
    
    def _recover_context_extraction(self, error_message: str, context: Dict[str, Any]) -> bool:
        """Recover from context extraction failures."""
        self.reporter.log_info("Attempting context extraction recovery...")
        
        # Fall back to basic context
        self.reporter.log_warning("Using minimal context fallback")
        
        return True


def main():
    """CLI interface for status reporter."""
    if len(sys.argv) < 3:
        print("Usage: python status_reporter.py <workflow_name> <operation> [action]")
        print("Actions: init, step <num> <description>, error <message>, complete")
        sys.exit(1)
    
    workflow_name = sys.argv[1]
    operation = sys.argv[2]
    
    reporter = StatusReporter(workflow_name, operation)
    
    if len(sys.argv) > 3:
        action = sys.argv[3]
        
        if action == "init":
            reporter._init_status()
            print(f"Status tracking initialized for {workflow_name}")
        
        elif action == "step" and len(sys.argv) >= 6:
            step_num = int(sys.argv[4])
            description = " ".join(sys.argv[5:])
            reporter.start_step(step_num, description)
        
        elif action == "error" and len(sys.argv) >= 5:
            message = " ".join(sys.argv[4:])
            reporter.log_error(message)
        
        elif action == "complete":
            # Interpret arguments:
            # - no extra args: success=True, no message
            # - first extra arg 'failed': success=False, rest is message
            # - otherwise: success=True, message is all remaining args
            success = True
            final_message = None
            if len(sys.argv) > 4:
                if sys.argv[4].lower() == "failed":
                    success = False
                    final_message = " ".join(sys.argv[5:]) or None
                else:
                    success = True
                    final_message = " ".join(sys.argv[4:]) or None
            reporter.complete_operation(success, final_message)
        
        elif action == "status":
            reporter.print_status_report()
        
        else:
            print(f"Unknown action: {action}")
            sys.exit(1)
    else:
        reporter.print_status_report()


if __name__ == "__main__":
    main()
