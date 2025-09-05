#!/usr/bin/env python3
"""
Comprehensive test suite for the PocketFlow Antipattern Detector

Tests all antipattern detection logic and edge cases to ensure accurate identification
of problematic patterns in PocketFlow code.

Usage:
    python test_antipattern_detector.py
    python -m pytest test_antipattern_detector.py -v

Author: Agent OS + PocketFlow Framework  
Version: 1.0.0
"""

import ast
import tempfile
import os
from pathlib import Path
import pytest
from typing import List, Dict, Any

from antipattern_detector import (
    AntipatternDetector, 
    AntipatternViolation,
    PocketFlowASTVisitor,
    AntipatternReporter,
    Severity
)


class TestAntipatternDetector:
    """Test the main antipattern detector functionality"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.detector = AntipatternDetector()
    
    def create_test_file(self, content: str, suffix: str = ".py") -> str:
        """Create a temporary test file with given content"""
        with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
            f.write(content)
            return f.name
    
    def test_monolithic_node_detection(self):
        """Test detection of monolithic node antipattern"""
        code = """
from pocketflow import Node, call_llm

class BadProcessDocuments(Node):
    def exec(self, docs):
        # This is too long and does too many things
        validated_docs = []
        for doc in docs:
            if self.validate_document(doc):
                validated_docs.append(doc)
        
        extracted_texts = []
        for doc in validated_docs:
            text = self.extract_text(doc)
            extracted_texts.append(text)
        
        entities = []
        for text in extracted_texts:
            entity = call_llm(f"Extract entities: {text}")
            entities.append(entity)
        
        summaries = []
        for entity in entities:
            summary = call_llm(f"Summarize: {entity}")
            summaries.append(summary)
        
        report = self.generate_report(summaries)
        self.send_notifications(report)
        
        return report
"""
        
        test_file = self.create_test_file(code)
        try:
            violations = self.detector.detect_file(test_file)
            
            # Should detect monolithic node
            monolithic_violations = [v for v in violations if v.antipattern_id == "monolithic_node"]
            assert len(monolithic_violations) > 0
            
            # Should detect multiple LLM calls
            llm_violations = [v for v in monolithic_violations if "LLM calls" in v.message]
            assert len(llm_violations) > 0
            
        finally:
            os.unlink(test_file)
    
    def test_shared_store_access_detection(self):
        """Test detection of shared store access in exec()"""
        code = """
from pocketflow import Node

class BadNode(Node):
    def prep(self, shared):
        return shared["user_id"]
    
    def exec(self, user_id):
        # BAD: Direct shared store access in exec
        user_data = self.shared["users"][user_id]
        preferences = self.shared["user_preferences"][user_id]
        
        # BAD: More shared store access
        if self.shared["is_premium_user"]:
            result = self.premium_processing(user_data, preferences)
        else:
            result = self.standard_processing(user_data, preferences)
        
        return result
"""
        
        test_file = self.create_test_file(code)
        try:
            violations = self.detector.detect_file(test_file)
            
            # Should detect shared store access violations
            shared_violations = [v for v in violations if v.antipattern_id == "shared_store_in_exec"]
            assert len(shared_violations) > 0
            
            # Check that it's marked as critical
            assert any(v.severity == Severity.CRITICAL for v in shared_violations)
            
        finally:
            os.unlink(test_file)
    
    def test_lifecycle_confusion_detection(self):
        """Test detection of lifecycle method confusion"""
        code = """
from pocketflow import Node, call_llm

class BadLifecycleNode(Node):
    def prep(self, shared):
        # BAD: Complex computation in prep
        data = shared["raw_data"]
        processed_data = self.complex_processing(data)
        # BAD: LLM call in prep
        analysis_result = call_llm(f"Analyze: {processed_data}")
        return analysis_result
    
    def exec(self, prep_result):
        # BAD: Simple formatting (should be in prep)
        formatted_result = prep_result.upper()
        return formatted_result
    
    def post(self, shared, prep_res, exec_res):
        # BAD: Complex logic in post
        if "error" in exec_res:
            corrected_result = call_llm(f"Fix this error: {exec_res}")
            shared["analysis"] = corrected_result
        else:
            shared["analysis"] = exec_res
        return "complete"
"""
        
        test_file = self.create_test_file(code)
        try:
            violations = self.detector.detect_file(test_file)
            
            # Should detect lifecycle confusion
            lifecycle_violations = [v for v in violations if v.antipattern_id == "lifecycle_confusion"]
            assert len(lifecycle_violations) > 0
            
            # Should detect LLM calls in prep
            prep_llm_violations = [v for v in lifecycle_violations if "prep" in v.message and "LLM" in v.message]
            assert len(prep_llm_violations) > 0
            
        finally:
            os.unlink(test_file)
    
    def test_business_logic_in_utils_detection(self):
        """Test detection of business logic in utility functions"""
        code = """
from pocketflow import call_llm

def process_customer_inquiry(inquiry, customer_data, shared_store):
    # BAD: Complex business logic in utility
    if customer_data["tier"] == "premium":
        priority = "high"
    elif customer_data["complaints"] > 3:
        priority = "urgent"
    elif "cancel" in inquiry.lower() or "refund" in inquiry.lower():
        priority = "retention"
    else:
        priority = "normal"
    
    # BAD: LLM call in utility
    sentiment = call_llm(f"Analyze sentiment: {inquiry}")
    
    # BAD: More complex routing logic
    if sentiment == "angry" and priority != "urgent":
        priority = "escalated"
        send_manager_alert(customer_data["id"], inquiry)
    
    return {"sentiment": sentiment, "priority": priority}

def simple_utility_function():
    # This should not trigger violations
    return "simple operation"
"""
        
        test_file = self.create_test_file(code)
        try:
            violations = self.detector.detect_file(test_file)
            
            # Should detect business logic in utilities
            util_violations = [v for v in violations if v.antipattern_id == "business_logic_in_utils"]
            assert len(util_violations) > 0
            
            # Should detect LLM calls in utilities
            util_llm_violations = [v for v in util_violations if "LLM calls" in v.message]
            assert len(util_llm_violations) > 0
            
            # Should detect complex branching
            util_branch_violations = [v for v in util_violations if "branching logic" in v.message]
            assert len(util_branch_violations) > 0
            
        finally:
            os.unlink(test_file)
    
    def test_good_code_no_violations(self):
        """Test that good code doesn't trigger violations"""
        code = """
from pocketflow import Node, call_llm

class GoodNode(Node):
    def prep(self, shared):
        # GOOD: Simple data preparation
        return {
            "user_data": shared["user_data"],
            "config": shared["config"]
        }
    
    def exec(self, prep_result):
        # GOOD: Pure computation using only prep_result
        result = call_llm(f"Process: {prep_result['user_data']}")
        return result
    
    def post(self, shared, prep_res, exec_res):
        # GOOD: Simple state update
        shared["result"] = exec_res
        return "success"

def simple_utility(data):
    # GOOD: Simple external interface
    return external_service.process(data)
"""
        
        test_file = self.create_test_file(code)
        try:
            violations = self.detector.detect_file(test_file)
            
            # Should have no major violations
            major_violations = [v for v in violations if v.severity in [Severity.CRITICAL, Severity.HIGH]]
            assert len(major_violations) == 0
            
        finally:
            os.unlink(test_file)
    
    def test_syntax_error_handling(self):
        """Test handling of files with syntax errors"""
        code = """
# This file has syntax errors
def bad_function(
    # Missing closing parenthesis
    return "error"
"""
        
        test_file = self.create_test_file(code)
        try:
            violations = self.detector.detect_file(test_file)
            
            # Should detect syntax error
            syntax_violations = [v for v in violations if v.antipattern_id == "syntax_error"]
            assert len(syntax_violations) > 0
            assert syntax_violations[0].severity == Severity.CRITICAL
            
        finally:
            os.unlink(test_file)
    
    def test_multiple_verbs_class_name(self):
        """Test detection of class names with multiple verbs"""
        code = """
from pocketflow import Node

class ProcessAndValidateDocuments(Node):
    def exec(self, docs):
        return docs

class FetchThenProcessData(Node):
    def exec(self, data):
        return data

class GoodSinglePurposeNode(Node):
    def exec(self, data):
        return data
"""
        
        test_file = self.create_test_file(code)
        try:
            violations = self.detector.detect_file(test_file)
            
            # Should detect multiple verb class names
            name_violations = [v for v in violations if "multiple responsibilities" in v.message]
            assert len(name_violations) >= 2  # Should catch both bad class names
            
        finally:
            os.unlink(test_file)
    
    def test_directory_analysis(self):
        """Test analyzing entire directories"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create test files
            good_file = os.path.join(temp_dir, "good.py")
            bad_file = os.path.join(temp_dir, "bad.py")
            
            with open(good_file, 'w') as f:
                f.write("""
from pocketflow import Node

class GoodNode(Node):
    def prep(self, shared):
        return shared["data"]
    def exec(self, data):
        return data
    def post(self, shared, prep_res, exec_res):
        shared["result"] = exec_res
        return "success"
""")
            
            with open(bad_file, 'w') as f:
                f.write("""
from pocketflow import Node

class BadNode(Node):
    def exec(self, data):
        # BAD: shared store access
        config = self.shared["config"]
        return config
""")
            
            violations = self.detector.detect_directory(temp_dir)
            
            # Should find violations only in bad file
            bad_violations = [v for v in violations if v.file_path == bad_file]
            good_violations = [v for v in violations if v.file_path == good_file]
            
            assert len(bad_violations) > 0
            assert len(good_violations) == 0


class TestPocketFlowASTVisitor:
    """Test the AST visitor component"""
    
    def test_extract_methods(self):
        """Test method extraction from class definitions"""
        code = """
class TestNode:
    def prep(self, shared):
        pass
    
    def exec(self, data):
        pass
    
    def post(self, shared, prep_res, exec_res):
        pass
"""
        
        tree = ast.parse(code)
        visitor = PocketFlowASTVisitor("test.py")
        visitor.visit(tree)
        
        class_def = tree.body[0]
        methods = visitor._extract_methods(class_def)
        
        assert "prep" in methods
        assert "exec" in methods
        assert "post" in methods
        assert len(methods["prep"]["args"]) == 2  # self, shared
        assert len(methods["exec"]["args"]) == 2  # self, data
        assert len(methods["post"]["args"]) == 4  # self, shared, prep_res, exec_res
    
    def test_llm_call_counting(self):
        """Test counting of LLM calls"""
        code = """
def test_function():
    result1 = call_llm("test")
    result2 = openai.ChatCompletion.create()
    result3 = anthropic.messages.create()
    regular_call = some_function()
"""
        
        tree = ast.parse(code)
        visitor = PocketFlowASTVisitor("test.py")
        func_node = tree.body[0]
        
        llm_count = visitor._count_llm_calls(func_node)
        assert llm_count == 3  # Should count the 3 LLM-related calls
    
    def test_shared_store_access_detection(self):
        """Test detection of shared store access patterns"""
        code = """
def test_method(self, data):
    config = self.shared["config"]
    settings = self.shared.get("settings")
    self.shared["result"] = data
"""
        
        tree = ast.parse(code)
        visitor = PocketFlowASTVisitor("test.py")
        func_node = tree.body[0]
        
        access_patterns = visitor._find_shared_store_access(func_node)
        assert len(access_patterns) >= 2  # Should find the shared store accesses
    
    def test_complex_computation_detection(self):
        """Test detection of complex computation patterns"""
        # Simple case - should not be complex
        simple_code = """
def simple_function():
    return data.upper()
"""
        tree = ast.parse(simple_code)
        visitor = PocketFlowASTVisitor("test.py")
        func_node = tree.body[0]
        assert not visitor._has_complex_computation(func_node)
        
        # Complex case - should be complex
        complex_code = """
def complex_function():
    for item in items:
        result = process_item(item)
        filtered = filter_result(result)
        transformed = transform_result(filtered)
        validated = validate_result(transformed)
    return results
"""
        tree = ast.parse(complex_code)
        visitor = PocketFlowASTVisitor("test.py")
        func_node = tree.body[0]
        assert visitor._has_complex_computation(func_node)


class TestAntipatternReporter:
    """Test the reporting functionality"""
    
    def create_sample_violations(self) -> List[AntipatternViolation]:
        """Create sample violations for testing"""
        return [
            AntipatternViolation(
                antipattern_id="monolithic_node",
                name="Monolithic Node Syndrome",
                severity=Severity.CRITICAL,
                file_path="/test/bad_node.py",
                line_number=10,
                message="Node has too many responsibilities",
                suggestion="Split into focused nodes"
            ),
            AntipatternViolation(
                antipattern_id="shared_store_in_exec",
                name="Shared Store Access in exec()",
                severity=Severity.CRITICAL,
                file_path="/test/bad_node.py",
                line_number=15,
                message="Direct shared store access in exec method",
                suggestion="Use prep_result parameter"
            ),
            AntipatternViolation(
                antipattern_id="lifecycle_confusion",
                name="Lifecycle Method Confusion",
                severity=Severity.MEDIUM,
                file_path="/test/other_node.py",
                line_number=5,
                message="Computation in prep method",
                suggestion="Move to exec method"
            )
        ]
    
    def test_summary_generation(self):
        """Test summary generation"""
        violations = self.create_sample_violations()
        reporter = AntipatternReporter(violations)
        summary = reporter.generate_summary()
        
        assert summary["total_violations"] == 3
        assert summary["critical_count"] == 2
        assert summary["medium_count"] == 1
        assert summary["by_severity"]["critical"] == 2
        assert summary["by_severity"]["medium"] == 1
        assert summary["by_antipattern"]["monolithic_node"] == 1
        assert summary["by_file"]["/test/bad_node.py"] == 2
    
    def test_console_report_generation(self):
        """Test console report generation"""
        violations = self.create_sample_violations()
        reporter = AntipatternReporter(violations)
        report = reporter.generate_console_report()
        
        assert "PocketFlow Antipattern Detection Report" in report
        assert "🔴 Critical: 2" in report
        assert "🟠 Medium: 1" in report
        assert "/test/bad_node.py" in report
        assert "Monolithic Node Syndrome" in report
    
    def test_json_report_generation(self):
        """Test JSON report generation"""
        violations = self.create_sample_violations()
        reporter = AntipatternReporter(violations)
        report = reporter.generate_json_report()
        
        import json
        data = json.loads(report)
        
        assert "summary" in data
        assert "violations" in data
        assert data["summary"]["total_violations"] == 3
        assert len(data["violations"]) == 3
    
    def test_markdown_report_generation(self):
        """Test Markdown report generation"""
        violations = self.create_sample_violations()
        reporter = AntipatternReporter(violations)
        report = reporter.generate_markdown_report()
        
        assert "# 🔍 PocketFlow Antipattern Detection Report" in report
        assert "## Summary" in report
        assert "| 🔴 Critical | 2 |" in report
        assert "### `/test/bad_node.py`" in report
        assert "#### 🔴 Monolithic Node Syndrome" in report
    
    def test_empty_violations_report(self):
        """Test report generation with no violations"""
        reporter = AntipatternReporter([])
        
        console_report = reporter.generate_console_report()
        assert "No antipatterns detected" in console_report
        
        markdown_report = reporter.generate_markdown_report()
        assert "No Antipatterns Detected" in markdown_report


class TestRegexPatterns:
    """Test regex-based pattern detection"""
    
    def test_synchronous_collection_processing(self):
        """Test detection of synchronous collection processing"""
        code = """
from pocketflow import Node

class BadSyncNode(Node):
    def exec(self, items):
        # BAD: Loop in regular Node
        for item in items:
            result = process_item(item)
        return results

class GoodBatchNode(BatchNode):
    def exec(self, single_item):
        # GOOD: BatchNode for collection processing
        return process_item(single_item)
"""
        
        detector = AntipatternDetector()
        violations = detector._detect_regex_patterns("test.py", code)
        
        # Should detect loop in regular node but not in BatchNode
        sync_violations = [v for v in violations if v.antipattern_id == "sync_collection_processing"]
        assert len(sync_violations) == 1  # Only the bad case
    
    def test_blocking_io_detection(self):
        """Test detection of blocking I/O operations"""
        code = """
from pocketflow import Node, AsyncNode
import requests

class BadSyncIONode(Node):
    def exec(self, data):
        # BAD: Blocking I/O in regular Node
        response = requests.get("http://example.com")
        return response.text

class GoodAsyncIONode(AsyncNode):
    async def exec_async(self, data):
        # GOOD: Async I/O in AsyncNode
        response = await aiohttp.get("http://example.com")
        return response.text
"""
        
        detector = AntipatternDetector()
        violations = detector._detect_regex_patterns("test.py", code)
        
        # Should detect blocking I/O in regular node but not in AsyncNode
        io_violations = [v for v in violations if v.antipattern_id == "blocking_io_in_node"]
        assert len(io_violations) == 1  # Only the bad case


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_empty_file(self):
        """Test handling of empty files"""
        detector = AntipatternDetector()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("")  # Empty file
            temp_file = f.name
        
        try:
            violations = detector.detect_file(temp_file)
            # Empty file should not cause errors and should have no violations
            assert isinstance(violations, list)
        finally:
            os.unlink(temp_file)
    
    def test_non_python_file(self):
        """Test handling of non-Python files"""
        detector = AntipatternDetector()
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is not Python code")
            temp_file = f.name
        
        try:
            violations = detector.detect_file(temp_file)
            # Should handle gracefully with syntax error
            assert len(violations) > 0
            assert violations[0].antipattern_id == "syntax_error"
        finally:
            os.unlink(temp_file)
    
    def test_nonexistent_file(self):
        """Test handling of nonexistent files"""
        detector = AntipatternDetector()
        violations = detector.detect_file("/nonexistent/file.py")
        
        # Should return error violation
        assert len(violations) > 0
        assert violations[0].antipattern_id in ["analysis_error", "syntax_error"]
    
    def test_binary_file(self):
        """Test handling of binary files"""
        detector = AntipatternDetector()
        
        with tempfile.NamedTemporaryFile(mode='wb', suffix='.py', delete=False) as f:
            f.write(b'\x00\x01\x02\x03')  # Binary data
            temp_file = f.name
        
        try:
            violations = detector.detect_file(temp_file)
            # Should handle gracefully
            assert isinstance(violations, list)
        finally:
            os.unlink(temp_file)


def run_integration_tests():
    """Run integration tests with real files"""
    print("Running integration tests...")
    
    # Test with the antipattern detector itself
    detector = AntipatternDetector()
    current_file = __file__
    violations = detector.detect_file(current_file)
    
    print(f"Analyzed {current_file}")
    print(f"Found {len(violations)} violations")
    
    if violations:
        reporter = AntipatternReporter(violations)
        print(reporter.generate_console_report())
    
    # Test with some pocketflow-tools files
    tools_dir = Path(__file__).parent
    py_files = list(tools_dir.glob("*.py"))
    
    for py_file in py_files[:3]:  # Test first 3 files to avoid too much output
        violations = detector.detect_file(str(py_file))
        print(f"Analyzed {py_file.name}: {len(violations)} violations")


if __name__ == '__main__':
    # Run basic tests
    print("Running antipattern detector tests...")
    
    # Run integration tests
    run_integration_tests()
    
    print("\nTo run complete test suite with pytest:")
    print("  python -m pytest test_antipattern_detector.py -v")
    print("\nTo run specific test class:")
    print("  python -m pytest test_antipattern_detector.py::TestAntipatternDetector -v")