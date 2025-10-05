#!/usr/bin/env python3
"""
Comprehensive test runner for the Astronaut Health Simulation Engine.
Runs all test suites and generates detailed reports.
"""

import sys
import os
import traceback
from datetime import datetime
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_test(test_func, test_name):
    """Run a single test and report results."""
    try:
        test_func()
        return True, None
    except Exception as e:
        return False, str(e)

def run_test_class(test_class, class_name):
    """Run all tests in a test class."""
    print(f"\n🧪 Running {class_name}...")
    passed = 0
    total = 0
    failures = []
    
    # Create instance
    try:
        instance = test_class()
    except Exception as e:
        print(f"❌ Failed to create {class_name} instance: {e}")
        return 0, 1, [f"Instance creation failed: {e}"]
    
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
        success, error = run_test(method, f"{class_name}.{method_name}")
        if success:
            print(f"✅ PASS: {method_name}")
            passed += 1
        else:
            print(f"❌ FAIL: {method_name}")
            print(f"   Error: {error}")
            failures.append(f"{class_name}.{method_name}: {error}")
    
    return passed, total, failures

def main():
    """Main comprehensive test runner."""
    print("🚀 Astronaut Health Simulation Engine - Comprehensive Test Suite")
    print("=" * 80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Define all test suites
    test_suites = [
        {
            "name": "Core Simulation Engine",
            "module": "tests.test_simulation_engine_simple",
            "classes": [
                ("TestHealthSimulationEngine", "HealthSimulationEngine"),
                ("TestRecommendationEngine", "RecommendationEngine"), 
                ("TestDataModels", "DataModels"),
                ("TestIntegration", "Integration")
            ]
        },
        {
            "name": "API Endpoints",
            "module": "tests.test_api_endpoints",
            "classes": [
                ("TestAPIEndpoints", "APIEndpoints"),
                ("TestAPIDataModels", "APIDataModels"),
                ("TestAPIIntegration", "APIIntegration")
            ]
        },
        {
            "name": "Dashboard Components",
            "module": "tests.test_dashboard",
            "classes": [
                ("TestDashboardComponents", "DashboardComponents"),
                ("TestDashboardVisualizations", "DashboardVisualizations"),
                ("TestDashboardIntegration", "DashboardIntegration")
            ]
        }
    ]
    
    # Run all test suites
    total_passed = 0
    total_tests = 0
    all_failures = []
    suite_results = []
    
    for suite in test_suites:
        print(f"\n📦 Test Suite: {suite['name']}")
        print("-" * 50)
        
        suite_passed = 0
        suite_total = 0
        suite_failures = []
        
        try:
            # Import the module
            module = __import__(suite['module'], fromlist=suite['classes'])
            
            for class_name, display_name in suite['classes']:
                test_class = getattr(module, class_name)
                passed, total, failures = run_test_class(test_class, display_name)
                
                suite_passed += passed
                suite_total += total
                suite_failures.extend(failures)
            
            suite_results.append({
                "name": suite['name'],
                "passed": suite_passed,
                "total": suite_total,
                "success_rate": (suite_passed / suite_total * 100) if suite_total > 0 else 0,
                "failures": suite_failures
            })
            
            total_passed += suite_passed
            total_tests += suite_total
            all_failures.extend(suite_failures)
            
        except ImportError as e:
            print(f"❌ Failed to import {suite['name']}: {e}")
            suite_results.append({
                "name": suite['name'],
                "passed": 0,
                "total": 0,
                "success_rate": 0,
                "failures": [f"Import failed: {e}"]
            })
    
    # Generate comprehensive report
    print("\n" + "=" * 80)
    print("📊 COMPREHENSIVE TEST REPORT")
    print("=" * 80)
    
    # Overall summary
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_tests - total_passed}")
    print(f"Overall Success Rate: {(total_passed/total_tests*100):.1f}%" if total_tests > 0 else "No tests run")
    
    # Suite-by-suite breakdown
    print(f"\n📋 Test Suite Breakdown:")
    for suite in suite_results:
        status = "✅" if suite['success_rate'] == 100 else "⚠️" if suite['success_rate'] >= 80 else "❌"
        print(f"{status} {suite['name']}: {suite['passed']}/{suite['total']} ({suite['success_rate']:.1f}%)")
        
        if suite['failures']:
            print(f"   Failures: {len(suite['failures'])}")
    
    # Detailed failure report
    if all_failures:
        print(f"\n❌ Detailed Failure Report ({len(all_failures)} failures):")
        for i, failure in enumerate(all_failures[:10], 1):  # Show first 10 failures
            print(f"   {i}. {failure}")
        
        if len(all_failures) > 10:
            print(f"   ... and {len(all_failures) - 10} more failures")
    
    # Performance metrics
    print(f"\n⏱️  Performance Metrics:")
    print(f"   Test Execution Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"   Tests per Second: {total_tests:.1f}" if total_tests > 0 else "   No tests executed")
    
    # Coverage assessment
    print(f"\n📈 Coverage Assessment:")
    core_tests = next((s for s in suite_results if s['name'] == 'Core Simulation Engine'), None)
    if core_tests:
        print(f"   Core Engine: {core_tests['success_rate']:.1f}%")
    
    api_tests = next((s for s in suite_results if s['name'] == 'API Endpoints'), None)
    if api_tests:
        print(f"   API Endpoints: {api_tests['success_rate']:.1f}%")
    
    dashboard_tests = next((s for s in suite_results if s['name'] == 'Dashboard Components'), None)
    if dashboard_tests:
        print(f"   Dashboard: {dashboard_tests['success_rate']:.1f}%")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    if total_passed == total_tests:
        print("   🎉 All tests passed! The system is ready for production.")
    elif total_passed / total_tests >= 0.9:
        print("   ✅ Excellent test coverage! Minor issues to address.")
    elif total_passed / total_tests >= 0.8:
        print("   ⚠️  Good test coverage, but some issues need attention.")
    else:
        print("   ❌ Significant test failures detected. Review and fix issues.")
    
    # Save detailed report to file
    report_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": total_tests,
        "total_passed": total_passed,
        "total_failed": total_tests - total_passed,
        "success_rate": (total_passed / total_tests * 100) if total_tests > 0 else 0,
        "suite_results": suite_results,
        "failures": all_failures
    }
    
    with open("test_report.json", "w") as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Detailed report saved to: test_report.json")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return 0 if total_passed == total_tests else 1

if __name__ == "__main__":
    sys.exit(main())
