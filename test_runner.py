#!/usr/bin/env python3
"""
Simple test runner for the Astronaut Health Simulation Engine.
Runs all tests without requiring pytest.
"""

import sys
import os
import traceback
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_test(test_func, test_name):
    """Run a single test and report results."""
    try:
        test_func()
        print(f"✅ PASS: {test_name}")
        return True
    except Exception as e:
        print(f"❌ FAIL: {test_name}")
        print(f"   Error: {str(e)}")
        print(f"   Traceback: {traceback.format_exc()}")
        return False

def run_test_class(test_class, class_name):
    """Run all tests in a test class."""
    print(f"\n🧪 Running {class_name}...")
    passed = 0
    total = 0
    
    # Create instance
    try:
        instance = test_class()
    except Exception as e:
        print(f"❌ Failed to create {class_name} instance: {e}")
        return 0, 1
    
    # Find all test methods
    test_methods = [method for method in dir(instance) if method.startswith('test_')]
    
    for method_name in test_methods:
        total += 1
        method = getattr(instance, method_name)
        
        # Run setup if it exists
        if hasattr(instance, 'setup_method'):
            try:
                instance.setup_method()
            except Exception as e:
                print(f"⚠️  Setup failed for {method_name}: {e}")
        
        # Run the test
        if run_test(method, f"{class_name}.{method_name}"):
            passed += 1
    
    return passed, total

def main():
    """Main test runner."""
    print("🚀 Astronaut Health Simulation Engine - Test Suite")
    print("=" * 60)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Import test modules
    try:
        from tests.test_simulation_engine_simple import (
            TestHealthSimulationEngine, 
            TestRecommendationEngine, 
            TestDataModels, 
            TestIntegration
        )
        test_classes = [
            (TestHealthSimulationEngine, "HealthSimulationEngine"),
            (TestRecommendationEngine, "RecommendationEngine"), 
            (TestDataModels, "DataModels"),
            (TestIntegration, "Integration")
        ]
    except ImportError as e:
        print(f"❌ Failed to import test modules: {e}")
        return 1
    
    # Run all tests
    total_passed = 0
    total_tests = 0
    
    for test_class, class_name in test_classes:
        passed, total = run_test_class(test_class, class_name)
        total_passed += passed
        total_tests += total
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0 if total_passed == total_tests else 1

if __name__ == "__main__":
    sys.exit(main())
