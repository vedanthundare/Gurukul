#!/usr/bin/env python3
"""
Service Startup Test Script
Tests if all 7 backend services can start properly
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def test_service_files():
    """Test if all required service files exist"""
    print("🔍 Checking service files...")
    
    services = {
        "Base Backend": "Base_backend/api.py",
        "Dedicated Chatbot": "dedicated_chatbot_service/chatbot_api.py", 
        "Financial Simulator": "Financial_simulator/langgraph_api.py",
        "Memory Management": "memory_management/run_server.py",
        "Akash Service": "akash/main.py",
        "Subject Generation": "subject_generation/app.py",
        "Wellness API": "orchestration/unified_orchestration_system/simple_api.py"
    }
    
    missing_files = []
    for service_name, file_path in services.items():
        if not os.path.exists(file_path):
            missing_files.append(f"{service_name}: {file_path}")
            print(f"❌ {service_name}: {file_path} - NOT FOUND")
        else:
            print(f"✅ {service_name}: {file_path} - EXISTS")
    
    return missing_files

def test_requirements_files():
    """Test if requirements.txt files exist for each service"""
    print("\n🔍 Checking requirements.txt files...")
    
    service_dirs = [
        "Base_backend",
        "dedicated_chatbot_service", 
        "Financial_simulator",
        "memory_management",
        "akash",
        "subject_generation",
        "orchestration/unified_orchestration_system"
    ]
    
    missing_requirements = []
    for service_dir in service_dirs:
        req_file = f"{service_dir}/requirements.txt"
        if not os.path.exists(req_file):
            missing_requirements.append(req_file)
            print(f"❌ {req_file} - NOT FOUND")
        else:
            print(f"✅ {req_file} - EXISTS")
    
    return missing_requirements

def test_env_files():
    """Test if .env files exist for each service"""
    print("\n🔍 Checking .env files...")
    
    service_dirs = [
        "Base_backend",
        "dedicated_chatbot_service", 
        "Financial_simulator",
        "memory_management",
        "akash",
        "subject_generation",
        "orchestration/unified_orchestration_system"
    ]
    
    missing_env = []
    for service_dir in service_dirs:
        env_file = f"{service_dir}/.env"
        if not os.path.exists(env_file):
            missing_env.append(env_file)
            print(f"⚠️  {env_file} - NOT FOUND (will be created)")
        else:
            print(f"✅ {env_file} - EXISTS")
    
    return missing_env

def test_python_imports():
    """Test if Python can import required modules for each service"""
    print("\n🔍 Testing Python imports...")
    
    # Test basic imports that all services need
    basic_imports = ["fastapi", "uvicorn", "python-dotenv", "pymongo"]
    
    for module in basic_imports:
        try:
            if module == "python-dotenv":
                import dotenv
            elif module == "fastapi":
                import fastapi
            elif module == "uvicorn":
                import uvicorn
            elif module == "pymongo":
                import pymongo
            print(f"✅ {module} - AVAILABLE")
        except ImportError:
            print(f"❌ {module} - NOT INSTALLED")

def test_port_availability():
    """Test if required ports are available"""
    print("\n🔍 Checking port availability...")
    
    ports = {
        8000: "Base Backend",
        8001: "Dedicated Chatbot",
        8002: "Financial Simulator", 
        8003: "Memory Management",
        8004: "Akash Service",
        8005: "Subject Generation",
        8006: "Wellness API",
        3000: "Frontend"
    }
    
    occupied_ports = []
    for port, service in ports.items():
        try:
            response = requests.get(f"http://localhost:{port}", timeout=2)
            print(f"⚠️  Port {port} ({service}) - OCCUPIED (service may be running)")
            occupied_ports.append((port, service))
        except requests.exceptions.RequestException:
            print(f"✅ Port {port} ({service}) - AVAILABLE")
    
    return occupied_ports

def main():
    """Main test function"""
    print("=" * 60)
    print("    Gurukul Backend Services Startup Test")
    print("=" * 60)
    
    # Change to Backend directory
    if not os.path.exists("Base_backend"):
        print("❌ Not in Backend directory. Please run from Backend/ folder")
        sys.exit(1)
    
    # Run all tests
    missing_files = test_service_files()
    missing_requirements = test_requirements_files()
    missing_env = test_env_files()
    test_python_imports()
    occupied_ports = test_port_availability()
    
    # Summary
    print("\n" + "=" * 60)
    print("    TEST SUMMARY")
    print("=" * 60)
    
    if missing_files:
        print("❌ MISSING SERVICE FILES:")
        for file in missing_files:
            print(f"   - {file}")
    else:
        print("✅ All service files exist")
    
    if missing_requirements:
        print("\n⚠️  MISSING REQUIREMENTS FILES:")
        for req in missing_requirements:
            print(f"   - {req}")
    else:
        print("\n✅ All requirements.txt files exist")
    
    if missing_env:
        print("\n⚠️  MISSING ENV FILES (will be created by setup script):")
        for env in missing_env:
            print(f"   - {env}")
    else:
        print("\n✅ All .env files exist")
    
    if occupied_ports:
        print("\n⚠️  OCCUPIED PORTS:")
        for port, service in occupied_ports:
            print(f"   - Port {port} ({service})")
    else:
        print("\n✅ All required ports are available")
    
    # Recommendations
    print("\n" + "=" * 60)
    print("    RECOMMENDATIONS")
    print("=" * 60)
    
    if missing_files:
        print("❌ Cannot start services - missing critical files")
        return False
    
    if missing_requirements:
        print("⚠️  Run: pip install -r requirements.txt in each service directory")
    
    if missing_env:
        print("⚠️  Run: setup_and_run.bat to create missing .env files")
    
    if occupied_ports:
        print("⚠️  Stop existing services or use different ports")
    
    if not missing_files and not occupied_ports:
        print("✅ Ready to start services!")
        print("   Run: start_all_services.bat")
        return True
    
    return False

if __name__ == "__main__":
    main()
