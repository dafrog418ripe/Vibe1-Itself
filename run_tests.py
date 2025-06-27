#!/usr/bin/env python3
"""
Test runner for the Task Manager application.
This script runs all unit tests and provides a summary report.
"""

import sys
import unittest
import os

def run_tests():
    """Run all tests and return the result."""
    # Add the current directory to the Python path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result

def main():
    """Main function to run tests."""
    print("🧪 Running Task Manager Unit Tests")
    print("=" * 50)
    
    try:
        result = run_tests()
        
        print("\n" + "=" * 50)
        print("📊 Test Results Summary:")
        print(f"   Tests run: {result.testsRun}")
        print(f"   Failures: {len(result.failures)}")
        print(f"   Errors: {len(result.errors)}")
        print(f"   Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
        
        if result.failures:
            print("\n❌ Failures:")
            for test, traceback in result.failures:
                print(f"   - {test}: {traceback.split('AssertionError:')[-1].strip()}")
        
        if result.errors:
            print("\n💥 Errors:")
            for test, traceback in result.errors:
                print(f"   - {test}: {traceback.split('Exception:')[-1].strip()}")
        
        if result.wasSuccessful():
            print("\n✅ All tests passed!")
            return 0
        else:
            print("\n❌ Some tests failed!")
            return 1
            
    except Exception as e:
        print(f"\n💥 Error running tests: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main()) 