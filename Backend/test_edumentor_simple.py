#!/usr/bin/env python3
"""
Simple test for edumentor endpoint
"""

import requests
import json

def test_edumentor():
    """Test edumentor endpoint with simple query"""
    
    print("🧪 Testing Edumentor Endpoint")
    print("=" * 40)
    
    url = "http://localhost:8006/edumentor"
    params = {
        "query": "vedas",
        "user_id": "test_user"
    }
    
    print(f"🔍 URL: {url}")
    print(f"📋 Params: {params}")
    print(f"⏰ Making request...")
    
    try:
        response = requests.get(url, params=params, timeout=120)  # 2 minute timeout
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"📝 Response keys: {list(data.keys())}")
            
            # Show response details
            response_text = data.get('response', '')
            sources = data.get('sources', [])
            
            print(f"📄 Response length: {len(response_text)}")
            print(f"📄 Response preview: {response_text[:200]}...")
            print(f"🔍 Sources count: {len(sources)}")
            
            if sources:
                print(f"📚 First source: {sources[0]}")
            
            return True, data
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except requests.exceptions.Timeout:
        print(f"⏰ Request timed out after 120 seconds")
        return False, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

if __name__ == "__main__":
    success, data = test_edumentor()
    
    if success:
        print(f"\n🎉 Edumentor endpoint is working!")
    else:
        print(f"\n❌ Edumentor endpoint failed")
        print(f"🔧 Check if vector stores are properly initialized")
