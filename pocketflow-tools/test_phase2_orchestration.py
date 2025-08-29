#!/usr/bin/env python3
"""
Test Suite for Phase 2 Workflow Orchestration

Tests the complete planning-to-implementation handoff system with
context awareness and validation feedback loops.
"""

import os
import sys
import json
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, List
import logging

# Add the current directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from context_manager import ContextManager, ProjectContext
    from validation_feedback import ValidationFeedbackAnalyzer, FeedbackLoop
except ImportError as e:
    print(f"⚠️  Import error: {e}")
    print("Make sure you're running from the pocketflow-tools directory")
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Phase2OrchestrationTester:
    """Tests the complete Phase 2 workflow orchestration system."""
    
    def __init__(self):
        self.test_results = []
        self.temp_dirs = []
    
    def cleanup(self):
        """Clean up temporary directories."""
        for temp_dir in self.temp_dirs:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)
    
    def create_test_project(self, name: str) -> Path:
        """Create a test project with sample design documents."""
        temp_dir = Path(tempfile.mkdtemp(prefix=f"test_phase2_{name}_"))
        self.temp_dirs.append(temp_dir)
        
        # Create docs directory
        docs_dir = temp_dir / "docs"
        docs_dir.mkdir()
        
        # Create sample requirements.md
        requirements_content = """# Document Search System Requirements

## Functional Requirements

### Core Search Functionality
1. Users shall be able to search through uploaded documents using natural language queries
2. The system should support semantic search with vector embeddings
3. Users can upload documents in PDF, Word, and text formats
4. Search results must be ranked by relevance

### Document Processing
- The system will extract text from uploaded documents
- Documents should be chunked for efficient retrieval  
- System supports batch processing of multiple documents
- Content must be indexed for fast search operations

## Technical Requirements

### Technology Stack
- Using Python for backend implementation
- Vector database for embeddings storage (ChromaDB or similar)
- FastAPI framework for REST API development
- React frontend for user interface

### Performance Requirements
- Search queries should return results within 2 seconds
- System must handle up to 1000 documents initially
- Concurrent user support for up to 50 users

## Integration Requirements

- Integration with cloud storage services (AWS S3, Google Drive)
- API endpoints for document upload and search
- User authentication and authorization system

## Constraints

- Must comply with data privacy regulations
- Limited to English language documents initially
- Cannot store sensitive personal information
"""
        
        (docs_dir / "requirements.md").write_text(requirements_content)
        
        # Create sample roadmap.md
        roadmap_content = """# Document Search System Roadmap

## Phase 1: Core Implementation
- Set up basic document upload functionality
- Implement text extraction pipeline
- Create vector embedding system
- Build basic search interface

## Phase 2: Enhanced Features  
- Add advanced search filters
- Implement user management
- Add document categorization
- Performance optimization

## Phase 3: Integration & Scale
- Cloud storage integration  
- Multi-language support
- Advanced analytics dashboard
- Enterprise features

## Technical Milestones
1. MVP with basic search - Week 4
2. Production-ready system - Week 8
3. Enhanced features - Week 12
4. Enterprise deployment - Week 16
"""
        
        (docs_dir / "roadmap.md").write_text(roadmap_content)
        
        # Create sample architecture.md
        architecture_content = """# System Architecture

## High-Level Architecture

The document search system follows a microservices architecture:

### Components

#### Document Processing Service
- Handles file uploads and text extraction
- Uses PyPDF2 for PDF processing
- Implements document chunking strategies

#### Search Service  
- Vector embedding generation using OpenAI embeddings
- ChromaDB for vector storage and similarity search
- Query processing and result ranking

#### API Gateway
- FastAPI-based REST API
- Authentication middleware
- Request/response handling

#### Frontend Application
- React-based single-page application  
- Document upload interface
- Search results display

## Data Flow

1. User uploads document → Document Processing Service
2. Text extraction and chunking → Vector embedding generation
3. Embeddings stored in ChromaDB vector database
4. Search query → Vector similarity search
5. Results ranked and returned to user

## Integration Points

- AWS S3 for document storage
- OpenAI API for embeddings
- Redis for caching search results
- PostgreSQL for metadata storage
"""
        
        (docs_dir / "architecture.md").write_text(architecture_content)
        
        logger.info(f"Created test project at {temp_dir}")
        return temp_dir
    
    def test_context_extraction(self, project_dir: Path) -> Dict[str, Any]:
        """Test context manager's ability to extract project context."""
        print("\n🔍 Testing Context Extraction...")
        
        try:
            context_manager = ContextManager(str(project_dir))
            context = context_manager.extract_project_context("DocumentSearchSystem")
            
            # Validate context extraction
            test_result = {
                "test_name": "context_extraction",
                "passed": True,
                "details": {},
                "issues": []
            }
            
            # Check basic context fields
            if not context.project_name:
                test_result["passed"] = False
                test_result["issues"].append("No project name extracted")
            
            if len(context.requirements) == 0:
                test_result["passed"] = False
                test_result["issues"].append("No requirements extracted")
            else:
                test_result["details"]["requirements_found"] = len(context.requirements)
            
            if len(context.technical_stack) == 0:
                test_result["passed"] = False
                test_result["issues"].append("No technical stack detected")
            else:
                test_result["details"]["technical_stack"] = context.technical_stack
            
            if len(context.patterns_detected) == 0:
                test_result["passed"] = False
                test_result["issues"].append("No patterns detected")
            else:
                test_result["details"]["patterns_detected"] = context.patterns_detected
            
            # Check source documents
            if len(context.source_documents) < 3:
                test_result["passed"] = False
                test_result["issues"].append("Expected at least 3 source documents")
            else:
                test_result["details"]["source_documents"] = len(context.source_documents)
            
            # Test workflow specification creation
            spec = context_manager.create_workflow_specification(context, "DocumentSearchSystem")
            if not spec or not spec.get("name"):
                test_result["passed"] = False
                test_result["issues"].append("Failed to create workflow specification")
            else:
                test_result["details"]["spec_created"] = True
                test_result["details"]["primary_pattern"] = spec.get("pattern")
            
            print(f"  ✅ Context extraction: {'PASSED' if test_result['passed'] else 'FAILED'}")
            if test_result["details"]:
                print(f"  📊 Details: {test_result['details']}")
            if test_result["issues"]:
                print(f"  ⚠️  Issues: {test_result['issues']}")
            
            return test_result
            
        except Exception as e:
            print(f"  ❌ Context extraction failed: {e}")
            return {
                "test_name": "context_extraction", 
                "passed": False,
                "error": str(e),
                "issues": [f"Exception: {e}"]
            }
    
    def test_validation_feedback(self, project_dir: Path) -> Dict[str, Any]:
        """Test validation feedback loop system."""
        print("\n🔄 Testing Validation Feedback Loops...")
        
        try:
            # Create mock validation output
            validation_output_file = project_dir / "mock_validation.txt"
            mock_validation_content = """
INFO: Starting validation for DocumentSearchSystem
TODO: Implement document_upload() function in workflow.py:25
TODO: Implement search_documents() function in workflow.py:45
ERROR: ImportError - missing ChromaDB dependency in requirements.txt
WARNING: No test files found in workflow directory
INFO: File structure validation passed
TODO: Implement vector_embedding() function in utils.py:15
ERROR: Configuration file missing - config.yaml not found
INFO: Validation completed with 2 errors, 1 warning, 3 TODOs
"""
            validation_output_file.write_text(mock_validation_content)
            
            # Create mock context file
            context_file = project_dir / "context.json"
            mock_context = {
                "project_name": "DocumentSearchSystem",
                "requirements": [
                    {"text": "Users shall be able to search documents", "type": "functional", "priority": "high"},
                    {"text": "System should use vector embeddings", "type": "technical", "priority": "high"}
                ],
                "technical_stack": ["Python", "FastAPI", "ChromaDB", "React"],
                "patterns_detected": ["RAG", "WORKFLOW"]
            }
            context_file.write_text(json.dumps(mock_context, indent=2))
            
            # Test validation feedback analyzer
            analyzer = ValidationFeedbackAnalyzer()
            feedback_loop = analyzer.analyze_validation_results(
                str(validation_output_file),
                str(context_file)
            )
            
            test_result = {
                "test_name": "validation_feedback",
                "passed": True,
                "details": {},
                "issues": []
            }
            
            # Validate feedback loop results
            if not feedback_loop.workflow_name:
                test_result["passed"] = False
                test_result["issues"].append("No workflow name in feedback loop")
            
            if len(feedback_loop.validation_issues) == 0:
                test_result["passed"] = False
                test_result["issues"].append("No validation issues detected")
            else:
                test_result["details"]["issues_analyzed"] = len(feedback_loop.validation_issues)
            
            if len(feedback_loop.auto_fix_actions) == 0 and len(feedback_loop.manual_review_needed) == 0:
                test_result["passed"] = False
                test_result["issues"].append("No actionable feedback generated")
            else:
                test_result["details"]["auto_fix_actions"] = len(feedback_loop.auto_fix_actions)
                test_result["details"]["manual_actions"] = len(feedback_loop.manual_review_needed)
            
            # Test report generation
            feedback_report = project_dir / "feedback_report.json"
            analyzer.create_feedback_report(feedback_loop, str(feedback_report))
            
            if not feedback_report.exists():
                test_result["passed"] = False
                test_result["issues"].append("Failed to create feedback report")
            else:
                test_result["details"]["report_created"] = True
            
            # Test markdown report generation
            markdown_report = project_dir / "feedback_report.md"
            analyzer.create_markdown_report(feedback_loop, str(markdown_report))
            
            if not markdown_report.exists():
                test_result["passed"] = False
                test_result["issues"].append("Failed to create markdown report")
            else:
                test_result["details"]["markdown_report_created"] = True
            
            print(f"  ✅ Validation feedback: {'PASSED' if test_result['passed'] else 'FAILED'}")
            if test_result["details"]:
                print(f"  📊 Details: {test_result['details']}")
            if test_result["issues"]:
                print(f"  ⚠️  Issues: {test_result['issues']}")
            
            return test_result
            
        except Exception as e:
            print(f"  ❌ Validation feedback failed: {e}")
            return {
                "test_name": "validation_feedback",
                "passed": False,
                "error": str(e),
                "issues": [f"Exception: {e}"]
            }
    
    def test_end_to_end_orchestration(self, project_dir: Path) -> Dict[str, Any]:
        """Test complete end-to-end orchestration workflow."""
        print("\n🎯 Testing End-to-End Orchestration...")
        
        try:
            test_result = {
                "test_name": "end_to_end_orchestration",
                "passed": True,
                "details": {},
                "issues": []
            }
            
            # Step 1: Context extraction
            context_manager = ContextManager(str(project_dir))
            context = context_manager.extract_project_context("DocumentSearchSystem")
            
            # Step 2: Specification creation
            spec = context_manager.create_workflow_specification(context, "DocumentSearchSystem")
            
            # Step 3: Save context analysis
            context_file = project_dir / "context_analysis.json"
            context_manager.save_context_analysis(context, str(context_file))
            
            # Step 4: Create mock validation and run feedback analysis
            validation_file = project_dir / "validation.txt"
            validation_content = """
TODO: Implement search functionality
ERROR: Missing ChromaDB dependency
INFO: Structure validation passed
"""
            validation_file.write_text(validation_content)
            
            analyzer = ValidationFeedbackAnalyzer()
            feedback_loop = analyzer.analyze_validation_results(
                str(validation_file),
                str(context_file)
            )
            
            # Step 5: Generate all outputs
            feedback_report = project_dir / "feedback.json"
            feedback_markdown = project_dir / "feedback.md"
            
            analyzer.create_feedback_report(feedback_loop, str(feedback_report))
            analyzer.create_markdown_report(feedback_loop, str(feedback_markdown))
            
            # Validate complete orchestration
            required_files = [context_file, feedback_report, feedback_markdown]
            for file_path in required_files:
                if not file_path.exists():
                    test_result["passed"] = False
                    test_result["issues"].append(f"Missing required file: {file_path.name}")
            
            # Check orchestration quality
            if len(context.requirements) < 2:
                test_result["passed"] = False
                test_result["issues"].append("Insufficient requirements extraction")
            
            if len(feedback_loop.validation_issues) == 0:
                test_result["passed"] = False
                test_result["issues"].append("No validation issues processed")
            
            # Success metrics
            test_result["details"] = {
                "context_extracted": len(context.requirements) > 0,
                "spec_created": bool(spec and spec.get("name")),
                "feedback_generated": len(feedback_loop.validation_issues) > 0,
                "reports_created": all(f.exists() for f in required_files),
                "patterns_detected": context.patterns_detected,
                "requirements_count": len(context.requirements),
                "feedback_issues": len(feedback_loop.validation_issues)
            }
            
            print(f"  ✅ End-to-end orchestration: {'PASSED' if test_result['passed'] else 'FAILED'}")
            if test_result["details"]:
                print(f"  📊 Details: {test_result['details']}")
            if test_result["issues"]:
                print(f"  ⚠️  Issues: {test_result['issues']}")
            
            return test_result
            
        except Exception as e:
            print(f"  ❌ End-to-end orchestration failed: {e}")
            return {
                "test_name": "end_to_end_orchestration",
                "passed": False,
                "error": str(e),
                "issues": [f"Exception: {e}"]
            }
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all Phase 2 orchestration tests."""
        print("🚀 Starting Phase 2 Workflow Orchestration Tests")
        print("=" * 60)
        
        try:
            # Create test project
            project_dir = self.create_test_project("orchestration")
            
            # Run individual tests
            tests = [
                self.test_context_extraction(project_dir),
                self.test_validation_feedback(project_dir), 
                self.test_end_to_end_orchestration(project_dir)
            ]
            
            self.test_results = tests
            
            # Calculate overall results
            total_tests = len(tests)
            passed_tests = sum(1 for test in tests if test["passed"])
            
            print("\n" + "=" * 60)
            print("📊 Phase 2 Orchestration Test Results")
            print("=" * 60)
            
            for test in tests:
                status = "✅ PASSED" if test["passed"] else "❌ FAILED"
                print(f"{test['test_name']}: {status}")
                if not test["passed"] and "error" in test:
                    print(f"  Error: {test['error']}")
            
            print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
            
            success_rate = (passed_tests / total_tests) * 100
            
            if success_rate >= 100:
                print("🎉 All tests passed! Phase 2 orchestration is working correctly.")
            elif success_rate >= 80:
                print("⚡ Most tests passed! Phase 2 orchestration is mostly functional.")
            elif success_rate >= 60:
                print("⚠️  Some tests failed. Phase 2 orchestration needs attention.")
            else:
                print("❌ Many tests failed. Phase 2 orchestration has significant issues.")
            
            return {
                "overall_success": success_rate >= 80,
                "success_rate": success_rate,
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "detailed_results": tests
            }
            
        except Exception as e:
            print(f"❌ Test suite failed: {e}")
            return {
                "overall_success": False,
                "error": str(e),
                "detailed_results": []
            }
        finally:
            self.cleanup()


def main():
    """Run Phase 2 orchestration tests."""
    tester = Phase2OrchestrationTester()
    
    try:
        results = tester.run_all_tests()
        
        # Exit with appropriate code
        if results["overall_success"]:
            print("\n✅ Phase 2 orchestration tests completed successfully!")
            sys.exit(0)
        else:
            print("\n❌ Phase 2 orchestration tests failed!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⚠️  Tests interrupted by user")
        tester.cleanup()
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        tester.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()