#!/usr/bin/env python3
"""
Test subject generation API with Knowledge Store
"""

import requests
import json

def test_subject_generation():
    """Test subject generation API with Knowledge Store enabled"""
    
    print("🧪 Testing Subject Generation API")
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
    print(f"⏰ Making request (this may take several minutes)...")
    
    try:
        response = requests.get(url, params=params, timeout=600)  # 10 minute timeout
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success!")
            print(f"📝 Response keys: {list(data.keys())}")
            
            # Check key indicators
            knowledge_base_used = data.get('knowledge_base_used', False)
            wikipedia_used = data.get('wikipedia_used', False)
            explanation = data.get('explanation', '')
            text = data.get('text', '')
            sources_used = data.get('sources_used', [])

            print(f"🧠 Knowledge Base Used: {knowledge_base_used}")
            print(f"🌐 Wikipedia Used: {wikipedia_used}")
            print(f"📄 Explanation length: {len(explanation)}")
            print(f"📄 Text length: {len(text)}")
            print(f"🔍 Sources count: {len(sources_used)}")

            print(f"\n📄 Text content preview:")
            print(f"{text[:500]}...")

            print(f"\n📄 Explanation preview:")
            print(f"{explanation[:500]}...")
            
            print(f"\n📚 Sources:")
            for i, source in enumerate(sources_used[:3], 1):
                print(f"  {i}. {source.get('source', 'Unknown')}")
                print(f"     Store: {source.get('store', 'Unknown')}")
                print(f"     Text: {source.get('text', '')[:100]}...")
            
            # Check if we're getting authentic content
            if "108upanishads" in explanation.lower() or "vedas" in explanation.lower():
                print(f"\n✅ Authentic Vedic content detected!")
            else:
                print(f"\n⚠️  Generic content detected - Knowledge Store may not be working properly")
            
            return True, data
        else:
            print(f"❌ Failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False, None
            
    except requests.exceptions.Timeout:
        print(f"⏰ Request timed out after 10 minutes")
        return False, None
    except Exception as e:
        print(f"❌ Error: {e}")
        return False, None

if __name__ == "__main__":
    success, data = test_subject_generation()
    
    if success:
        print(f"\n🎉 Subject Generation API is working!")
        
        # Check if Knowledge Store is properly integrated
        if data.get('knowledge_base_used'):
            print(f"✅ Knowledge Store integration successful!")
        else:
            print(f"⚠️  Knowledge Store integration needs fixing")
    else:
        print(f"\n❌ Subject Generation API failed")
        print(f"🔧 Check if the API is running on port 8005")
