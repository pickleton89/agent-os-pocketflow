#!/usr/bin/env python3
"""
Execute End-to-End Test Scenarios Script (Task 5.1 Completion)

Simple script to run the end-to-end test scenarios for validating
universal PocketFlow integration across all project types.
"""

import sys
import os
import argparse
from pathlib import Path

def main():
    """Main entry point for running the test scenarios."""
    parser = argparse.ArgumentParser(
        description="Run End-to-End Test Scenarios for Universal PocketFlow Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    # Run all test scenarios
  %(prog)s --verbose          # Run with detailed output  
  %(prog)s --workspace /tmp   # Use custom workspace directory
        """
    )
    
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "-w", "--workspace",
        help="Specify custom test workspace directory"
    )
    
    parser.add_argument(
        "--cleanup",
        action="store_true", 
        default=True,
        help="Clean up test workspace after completion (default: True)"
    )
    
    parser.add_argument(
        "--no-cleanup",
        dest="cleanup",
        action="store_false",
        help="Don't clean up test workspace (useful for debugging)"
    )
    
    args = parser.parse_args()
    
    # Set up logging level based on verbosity
    if args.verbose:
        import logging
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Add the current directory to Python path so we can import the test runner
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    try:
        # Import and run the test scenarios
        from end_to_end_test_scenarios import EndToEndTestRunner
        
        print("🚀 Starting End-to-End Test Scenarios for Universal PocketFlow Integration")
        print("="*80)
        print()
        print("These tests validate that the framework generates PocketFlow-structured")
        print("code for ALL project types (not just LLM/AI), fulfilling the mission")
        print("of universal PocketFlow integration.")
        print()
        
        # Create and configure the test runner
        runner = EndToEndTestRunner(test_workspace_dir=args.workspace)
        
        # Run all scenarios
        results = runner.run_all_scenarios()
        
        # Check results and exit appropriately
        failed_count = sum(1 for r in results if not r.success)
        
        if failed_count == 0:
            print()
            print("🎉 SUCCESS: All end-to-end test scenarios passed!")
            print("✅ Universal PocketFlow integration is working correctly.")
            print("✅ Framework generates PocketFlow structure for all project types.")
            print("✅ Ready for Task 5.2: Validate User Experience")
            
            if not args.cleanup:
                print(f"🔍 Test workspace preserved at: {runner.test_workspace}")
            
            return 0
        else:
            print()
            print(f"❌ FAILURE: {failed_count} test scenario(s) failed.")
            print("⚠️  Universal PocketFlow integration needs attention.")
            print("📋 Review the failed scenarios above and fix issues.")
            
            if not args.cleanup:
                print(f"🔍 Test workspace preserved at: {runner.test_workspace}")
                
            return 1
            
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print()
        print("Make sure you're running this script from the pocketflow-tools directory.")
        print("Required files:")
        print("  - end_to_end_test_scenarios.py")
        print("  - pattern_analyzer.py")
        print("  - generator.py")
        return 1
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1
        
    finally:
        # Cleanup if requested
        if args.cleanup and 'runner' in locals():
            runner.cleanup()


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)