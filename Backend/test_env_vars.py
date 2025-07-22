#!/usr/bin/env python3
"""
Test script to check if environment variables are loaded correctly
"""

import os
from dotenv import load_dotenv

def test_env_loading():
    print("🔍 Testing Environment Variable Loading")
    print("=" * 50)
    
    # Test 1: Load from current directory
    print("\n1. Testing load_dotenv() from current directory...")
    load_dotenv()
    groq_key = os.getenv("GROQ_API_KEY")
    mongo_uri = os.getenv("MONGO_URI")
    
    if groq_key:
        print(f"✅ GROQ_API_KEY: {groq_key[:8]}...{groq_key[-8:]}")
    else:
        print("❌ GROQ_API_KEY: Not found")
    
    if mongo_uri:
        print(f"✅ MONGO_URI: Found (length: {len(mongo_uri)})")
    else:
        print("❌ MONGO_URI: Not found")
    
    # Test 2: Load from api_data directory
    print("\n2. Testing load_dotenv() from api_data directory...")
    api_data_env = os.path.join("Backend", "api_data", ".env")
    if os.path.exists(api_data_env):
        print(f"📁 Found .env file at: {api_data_env}")
        load_dotenv(api_data_env)
        
        groq_key = os.getenv("GROQ_API_KEY")
        mongo_uri = os.getenv("MONGO_URI")
        
        if groq_key:
            print(f"✅ GROQ_API_KEY: {groq_key[:8]}...{groq_key[-8:]}")
        else:
            print("❌ GROQ_API_KEY: Not found")
        
        if mongo_uri:
            print(f"✅ MONGO_URI: Found (length: {len(mongo_uri)})")
        else:
            print("❌ MONGO_URI: Not found")
    else:
        print(f"❌ .env file not found at: {api_data_env}")
    
    # Test 3: Check .env file content
    print("\n3. Checking .env file content...")
    if os.path.exists(api_data_env):
        with open(api_data_env, 'r') as f:
            content = f.read()
            lines = content.strip().split('\n')
            print(f"📄 .env file has {len(lines)} lines")
            
            for line in lines:
                if line.strip() and not line.startswith('#'):
                    key = line.split('=')[0]
                    print(f"   - {key}")
    
    # Test 4: Test API endpoint for environment status
    print("\n4. Testing API service environment status...")
    try:
        import requests
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ API service is responding")
            
            # Try to make a request that would use environment variables
            # This will help us see if the service has the env vars loaded
            test_response = requests.post(
                "http://localhost:8001/process-pdf",
                timeout=5
            )
            print(f"📄 PDF endpoint response: {test_response.status_code}")
            if test_response.status_code == 422:
                print("✅ PDF endpoint is working (validation error expected)")
            elif test_response.status_code == 500:
                error_text = test_response.text
                if "GROQ_API_KEY" in error_text:
                    print("❌ API service missing GROQ_API_KEY")
                elif "MONGO_URI" in error_text:
                    print("❌ API service missing MONGO_URI")
                else:
                    print(f"❌ API service error: {error_text[:200]}")
        else:
            print(f"❌ API service error: {response.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to API service: {e}")

if __name__ == "__main__":
    test_env_loading()
