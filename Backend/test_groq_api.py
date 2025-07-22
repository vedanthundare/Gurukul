#!/usr/bin/env python3
"""
Test script to verify Groq API key validity
"""

import os
import requests
from dotenv import load_dotenv

def test_groq_api():
    print("🔍 Testing Groq API Key")
    print("=" * 30)
    
    # Load environment variables
    env_path = os.path.join("Backend", "api_data", ".env")
    load_dotenv(env_path)
    
    groq_api_key = os.getenv("GROQ_API_KEY")
    
    if not groq_api_key:
        print("❌ GROQ_API_KEY not found in environment variables")
        return False
    
    print(f"🔑 API Key: {groq_api_key[:8]}...{groq_api_key[-8:]}")
    
    # Test the API key with a simple request
    print("\n📡 Testing API key with Groq API...")
    
    try:
        headers = {
            "Authorization": f"Bearer {groq_api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": "Hello, this is a test message. Please respond with 'API key is working'."
                }
            ],
            "model": "llama3-8b-8192",
            "max_tokens": 50,
            "temperature": 0.1
        }
        
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            message = result.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"✅ API Key is valid!")
            print(f"📝 Response: {message}")
            return True
        else:
            print(f"❌ API Key test failed")
            try:
                error_data = response.json()
                print(f"📄 Error: {error_data}")
            except:
                print(f"📄 Raw response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API test failed with exception: {e}")
        return False

def test_alternative_keys():
    """Test other API keys as fallback"""
    print("\n🔄 Testing Alternative API Keys")
    print("=" * 35)
    
    env_path = os.path.join("Backend", "api_data", ".env")
    load_dotenv(env_path)
    
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        print(f"🔑 OpenAI Key available: {openai_key[:8]}...{openai_key[-8:]}")
        
        # Test OpenAI API
        try:
            headers = {
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": "Test message"
                    }
                ],
                "max_tokens": 10
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                print("✅ OpenAI API key is valid")
                return True
            else:
                print(f"❌ OpenAI API key test failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ OpenAI API test failed: {e}")
    
    return False

def main():
    print("🚀 API Key Validation Test")
    print("=" * 40)
    
    groq_valid = test_groq_api()
    
    if not groq_valid:
        print("\n💡 Groq API key is invalid. Testing alternatives...")
        openai_valid = test_alternative_keys()
        
        if openai_valid:
            print("\n✅ OpenAI API key works as fallback")
            print("💡 Consider updating the code to use OpenAI when Groq fails")
        else:
            print("\n❌ No valid API keys found")
            print("💡 Recommendations:")
            print("   1. Get a new Groq API key from https://console.groq.com/keys")
            print("   2. Update the GROQ_API_KEY in Backend/api_data/.env")
            print("   3. Restart the API service")
    else:
        print("\n✅ Groq API key is working correctly")
        print("🎉 PDF processing should work now!")

if __name__ == "__main__":
    main()
