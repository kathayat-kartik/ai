"""
Quick start script for the Astronaut Health Simulation Engine.
Run this to see the system in action.
"""

import subprocess
import sys
import os
from pathlib import Path


def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import plotly
        import pandas
        import numpy
        print("✅ All required dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies: pip install -r requirements.txt")
        return False


def run_demo():
    """Run the demo script."""
    print("🚀 Starting Astronaut Health Simulation Engine Demo...")
    
    if not check_dependencies():
        return False
    
    try:
        # Run the demo
        result = subprocess.run([sys.executable, "demo.py"], capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
            print("\n✅ Demo completed successfully!")
            return True
        else:
            print(f"❌ Demo failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        return False


def run_dashboard():
    """Run the Streamlit dashboard."""
    print("🌐 Starting AHSE Dashboard...")
    
    if not check_dependencies():
        return False
    
    try:
        # Start Streamlit dashboard
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/dashboard/app.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
        return True
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        return False


def run_api():
    """Run the FastAPI server."""
    print("🔌 Starting AHSE API Server...")
    
    try:
        # Start FastAPI server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "src.api.main:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
        return True
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        return False


def run_tests():
    """Run the test suite."""
    print("🧪 Running AHSE Test Suite...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", "-v", "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
            return True
        else:
            print("❌ Some tests failed")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Main entry point."""
    print("="*60)
    print("🚀 ASTRONAUT HEALTH SIMULATION ENGINE")
    print("="*60)
    print()
    print("Choose an option:")
    print("1. Run Demo")
    print("2. Start Dashboard")
    print("3. Start API Server")
    print("4. Run Tests")
    print("5. Install Dependencies")
    print("6. Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                run_demo()
                break
            elif choice == "2":
                run_dashboard()
                break
            elif choice == "3":
                run_api()
                break
            elif choice == "4":
                run_tests()
                break
            elif choice == "5":
                print("📦 Installing dependencies...")
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
                print("✅ Dependencies installed!")
                break
            elif choice == "6":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            break


if __name__ == "__main__":
    main()

