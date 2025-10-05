#!/usr/bin/env python3
"""
Test coverage analysis for the Astronaut Health Simulation Engine.
Analyzes test coverage and generates detailed reports.
"""

import sys
import os
import json
from datetime import datetime
import ast
import os

def analyze_file_coverage(file_path):
    """Analyze test coverage for a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the AST to find functions and classes
        tree = ast.parse(content)
        
        functions = []
        classes = []
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
        
        return {
            'file': file_path,
            'functions': functions,
            'classes': classes,
            'total_functions': len(functions),
            'total_classes': len(classes)
        }
    except Exception as e:
        return {
            'file': file_path,
            'error': str(e),
            'functions': [],
            'classes': [],
            'total_functions': 0,
            'total_classes': 0
        }

def generate_coverage_report():
    """Generate comprehensive test coverage report."""
    print("📊 Test Coverage Analysis for Astronaut Health Simulation Engine")
    print("=" * 70)
    print(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Define source directories
    source_dirs = [
        'src/core',
        'src/data', 
        'src/models',
        'src/api',
        'src/dashboard'
    ]
    
    # Define test directories
    test_dirs = [
        'tests'
    ]
    
    coverage_data = {
        'timestamp': datetime.now().isoformat(),
        'source_files': [],
        'test_files': [],
        'coverage_summary': {}
    }
    
    # Analyze source files
    print("🔍 Analyzing Source Files...")
    total_source_functions = 0
    total_source_classes = 0
    
    for source_dir in source_dirs:
        if os.path.exists(source_dir):
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        file_path = os.path.join(root, file)
                        analysis = analyze_file_coverage(file_path)
                        coverage_data['source_files'].append(analysis)
                        total_source_functions += analysis['total_functions']
                        total_source_classes += analysis['total_classes']
                        print(f"   📄 {file_path}: {analysis['total_functions']} functions, {analysis['total_classes']} classes")
    
    # Analyze test files
    print(f"\n🧪 Analyzing Test Files...")
    total_test_functions = 0
    total_test_classes = 0
    
    for test_dir in test_dirs:
        if os.path.exists(test_dir):
            for root, dirs, files in os.walk(test_dir):
                for file in files:
                    if file.endswith('.py') and not file.startswith('__'):
                        file_path = os.path.join(root, file)
                        analysis = analyze_file_coverage(file_path)
                        coverage_data['test_files'].append(analysis)
                        total_test_functions += analysis['total_functions']
                        total_test_classes += analysis['total_classes']
                        print(f"   🧪 {file_path}: {analysis['total_functions']} test functions, {analysis['total_classes']} test classes")
    
    # Calculate coverage metrics
    coverage_data['coverage_summary'] = {
        'total_source_files': len(coverage_data['source_files']),
        'total_test_files': len(coverage_data['test_files']),
        'total_source_functions': total_source_functions,
        'total_source_classes': total_source_classes,
        'total_test_functions': total_test_functions,
        'total_test_classes': total_test_classes,
        'test_to_source_ratio': total_test_functions / total_source_functions if total_source_functions > 0 else 0
    }
    
    # Generate report
    print(f"\n📈 Coverage Summary:")
    print(f"   Source Files: {coverage_data['coverage_summary']['total_source_files']}")
    print(f"   Test Files: {coverage_data['coverage_summary']['total_test_files']}")
    print(f"   Source Functions: {coverage_data['coverage_summary']['total_source_functions']}")
    print(f"   Test Functions: {coverage_data['coverage_summary']['total_test_functions']}")
    print(f"   Source Classes: {coverage_data['coverage_summary']['total_source_classes']}")
    print(f"   Test Classes: {coverage_data['coverage_summary']['total_test_classes']}")
    print(f"   Test-to-Source Ratio: {coverage_data['coverage_summary']['test_to_source_ratio']:.2f}")
    
    # Module-specific coverage
    print(f"\n📋 Module Coverage Analysis:")
    
    modules = {
        'Core Engine': ['src/core'],
        'Data Models': ['src/data'],
        'Recommendation Engine': ['src/models'],
        'API': ['src/api'],
        'Dashboard': ['src/dashboard']
    }
    
    for module_name, dirs in modules.items():
        module_functions = 0
        module_classes = 0
        module_files = 0
        
        for dir_path in dirs:
            if os.path.exists(dir_path):
                for root, dirs, files in os.walk(dir_path):
                    for file in files:
                        if file.endswith('.py') and not file.startswith('__'):
                            file_path = os.path.join(root, file)
                            analysis = analyze_file_coverage(file_path)
                            module_functions += analysis['total_functions']
                            module_classes += analysis['total_classes']
                            module_files += 1
        
        print(f"   📦 {module_name}: {module_files} files, {module_functions} functions, {module_classes} classes")
    
    # Test quality assessment
    print(f"\n🎯 Test Quality Assessment:")
    
    if coverage_data['coverage_summary']['test_to_source_ratio'] >= 1.0:
        print("   ✅ Excellent test coverage! Good test-to-source ratio.")
    elif coverage_data['coverage_summary']['test_to_source_ratio'] >= 0.5:
        print("   ⚠️  Moderate test coverage. Consider adding more tests.")
    else:
        print("   ❌ Low test coverage. Significant testing gaps detected.")
    
    # Recommendations
    print(f"\n💡 Recommendations:")
    
    if coverage_data['coverage_summary']['total_test_functions'] < 20:
        print("   📝 Add more unit tests for individual functions")
    
    if coverage_data['coverage_summary']['total_test_classes'] < 5:
        print("   🏗️  Add more integration tests for complete workflows")
    
    print("   🔄 Consider adding property-based testing for edge cases")
    print("   📊 Implement performance testing for large datasets")
    print("   🛡️  Add security testing for API endpoints")
    
    # Save detailed report
    with open("coverage_report.json", "w") as f:
        json.dump(coverage_data, f, indent=2)
    
    print(f"\n📄 Detailed coverage report saved to: coverage_report.json")
    
    return coverage_data

def main():
    """Main coverage analysis function."""
    try:
        coverage_data = generate_coverage_report()
        return 0
    except Exception as e:
        print(f"❌ Coverage analysis failed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
