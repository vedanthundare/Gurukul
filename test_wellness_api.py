#!/usr/bin/env python3
"""
Test script to check the wellness API and identify why it's returning hardcoded values
"""

import requests
import json
import sys
from datetime import datetime

def test_wellness_api():
    """Test the wellness API endpoints"""
    
    # Test data
    test_query = "I'm feeling stressed about work and need some guidance"
    user_id = "test_user_123"
    
    # API base URL
    base_url = "http://localhost:8006"
    
    print("🔍 Testing Wellness API...")
    print(f"Base URL: {base_url}")
    print(f"Test Query: {test_query}")
    print("-" * 50)
    
    # Test 1: Simple wellness endpoint (POST)
    print("\n1️⃣ Testing POST /wellness endpoint...")
    try:
        response = requests.post(
            f"{base_url}/wellness",
            json={
                "query": test_query,
                "user_id": user_id
            },
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! Response:")
            print(json.dumps(data, indent=2))
            
            # Check if response looks like LLM-generated or hardcoded
            response_text = data.get('response', '')
            if 'Thank you for reaching out' in response_text and 'gentle suggestions' in response_text:
                print("⚠️  WARNING: This looks like a hardcoded fallback response!")
            else:
                print("✅ Response appears to be LLM-generated")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection Error: Wellness API server is not running")
        print("💡 Start the server with: cd Backend/orchestration/unified_orchestration_system && python simple_api.py --port 8006")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Full orchestration endpoint (POST)
    print("\n2️⃣ Testing POST /ask-wellness endpoint...")
    try:
        response = requests.post(
            f"{base_url}/ask-wellness",
            json={
                "query": test_query,
                "user_id": user_id,
                "mood_score": 4.0,
                "stress_level": 7.0
            },
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ Success! Full orchestration response:")
            print(json.dumps(data, indent=2))
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Test 3: Check server health
    print("\n3️⃣ Testing server health...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"Health check status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Server is healthy")
        else:
            print("⚠️  Server may have issues")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    return True

def test_gemini_api_directly():
    """Test Gemini API directly to see if it's working"""
    print("\n🤖 Testing Gemini API directly...")
    
    try:
        import google.generativeai as genai
        import os
        from dotenv import load_dotenv
        
        # Load environment variables
        load_dotenv("Backend/orchestration/unified_orchestration_system/.env")
        
        # Get API keys
        primary_key = os.getenv("GEMINI_API_KEY")
        backup_key = os.getenv("GEMINI_API_KEY_BACKUP")
        
        print(f"Primary key present: {'Yes' if primary_key else 'No'}")
        print(f"Backup key present: {'Yes' if backup_key else 'No'}")
        
        if primary_key:
            print("\n🔑 Testing primary Gemini API key...")
            try:
                genai.configure(api_key=primary_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                test_prompt = "You are a wellness counselor. Provide brief advice for someone feeling stressed about work."
                response = model.generate_content(test_prompt)
                
                if response and response.text:
                    print("✅ Primary Gemini API key works!")
                    print(f"Sample response: {response.text[:200]}...")
                    return True
                else:
                    print("❌ Primary key failed - no response text")
            except Exception as e:
                print(f"❌ Primary key error: {e}")
        
        if backup_key:
            print("\n🔑 Testing backup Gemini API key...")
            try:
                genai.configure(api_key=backup_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                test_prompt = "You are a wellness counselor. Provide brief advice for someone feeling stressed about work."
                response = model.generate_content(test_prompt)
                
                if response and response.text:
                    print("✅ Backup Gemini API key works!")
                    print(f"Sample response: {response.text[:200]}...")
                    return True
                else:
                    print("❌ Backup key failed - no response text")
            except Exception as e:
                print(f"❌ Backup key error: {e}")
        
        print("❌ Both Gemini API keys failed!")
        return False
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Install with: pip install google-generativeai python-dotenv")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Wellness API Diagnostic Tool")
    print("=" * 50)
    
    # Test Gemini API first
    gemini_works = test_gemini_api_directly()
    
    # Test wellness API
    api_works = test_wellness_api()
    
    print("\n📊 Summary:")
    print(f"Gemini API: {'✅ Working' if gemini_works else '❌ Failed'}")
    print(f"Wellness API: {'✅ Accessible' if api_works else '❌ Not accessible'}")
    
    if not gemini_works:
        print("\n💡 Recommendations:")
        print("1. Check your Gemini API keys in Backend/orchestration/unified_orchestration_system/.env")
        print("2. Verify the keys are valid at https://makersuite.google.com/app/apikey")
        print("3. Ensure you have billing enabled for the Google Cloud project")
        print("4. Check if there are any quota limits or restrictions")
    
    if not api_works:
        print("\n💡 To start the wellness API:")
        print("cd Backend/orchestration/unified_orchestration_system")
        print("python simple_api.py --port 8006")
