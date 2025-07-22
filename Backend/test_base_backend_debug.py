#!/usr/bin/env python3
"""
Debug test for Base_backend API to see detailed logs
"""

import requests
import json

def test_base_backend_debug():
    """Test Base_backend API with detailed logging"""
    
    print("🧪 Testing Base_backend API with Debug")
    print("=" * 50)
    
    url = "http://localhost:8000/generate_lesson"
    params = {
        "subject": "vedas",
        "topic": "types of vedas",
        "include_wikipedia": False,  # Disable Wikipedia
        "use_knowledge_store": True  # Enable Knowledge Store
    }
    
    print(f"🔍 URL: {url}")
    print(f"📋 Params: {params}")
    print(f"⏰ Making request...")
    
    try:
        response = requests.get(url, params=params, timeout=300)  # 5 minute timeout
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            
            # Print all response keys and their types
            print(f"\n📝 Full Response Structure:")
            for key, value in data.items():
                if isinstance(value, str):
                    print(f"  {key}: '{value[:100]}...' (length: {len(value)})")
                elif isinstance(value, list):
                    print(f"  {key}: [{len(value)} items]")
                    if value:
                        print(f"    First item: {value[0]}")
                elif isinstance(value, dict):
                    print(f"  {key}: {{{len(value)} keys}}")
                    print(f"    Keys: {list(value.keys())}")
                else:
                    print(f"  {key}: {value} ({type(value).__name__})")
            
            # Check specific fields we care about
            text = data.get('text', '')
            sources = data.get('sources', [])
            detailed_sources = data.get('detailed_sources', [])
            
            print(f"\n🔍 Key Analysis:")
            print(f"  Text contains 'upanishads': {'upanishads' in text.lower()}")
            print(f"  Text contains 'vedas': {'vedas' in text.lower()}")
            print(f"  Text contains 'authentic': {'authentic' in text.lower()}")
            print(f"  Sources count: {len(sources)}")
            print(f"  Detailed sources count: {len(detailed_sources)}")
            
            if detailed_sources:
                print(f"\n📚 Detailed Sources:")
                for i, source in enumerate(detailed_sources[:3], 1):
                    print(f"  {i}. {source}")
            
            return True, data
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

if __name__ == "__main__":
    success, data = test_base_backend_debug()
    
    if success:
        print(f"\n🎉 Test completed successfully!")
    else:
        print(f"\n❌ Test failed")
