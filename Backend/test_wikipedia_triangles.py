#!/usr/bin/env python3
"""
Test script to check Wikipedia content retrieval for maths/triangles
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'pipline-24-master'))

try:
    from wikipedia_utils import get_relevant_wikipedia_info
    print("✅ Successfully imported wikipedia_utils")
except ImportError as e:
    print(f"❌ Failed to import wikipedia_utils: {e}")
    sys.exit(1)

def test_wikipedia_triangles():
    """Test Wikipedia content retrieval for maths/triangles"""
    print("🔍 Testing Wikipedia content retrieval for 'maths/triangles'")
    print("=" * 60)
    
    subject = "maths"
    topic = "triangles"
    
    try:
        print(f"📚 Searching for: {subject}/{topic}")
        wiki_data = get_relevant_wikipedia_info(subject, topic)
        
        print(f"📊 Result structure: {type(wiki_data)}")
        print(f"🔑 Keys: {list(wiki_data.keys()) if isinstance(wiki_data, dict) else 'Not a dict'}")
        
        if wiki_data and isinstance(wiki_data, dict):
            wikipedia_info = wiki_data.get("wikipedia", {})
            
            print(f"\n📖 Wikipedia Info:")
            print(f"   Title: {wikipedia_info.get('title', 'None')}")
            print(f"   Summary length: {len(wikipedia_info.get('summary', '')) if wikipedia_info.get('summary') else 0}")
            print(f"   URL: {wikipedia_info.get('url', 'None')}")
            print(f"   Related articles: {len(wikipedia_info.get('related_articles', []))}")
            
            if wikipedia_info.get('summary'):
                print(f"\n📝 Summary preview (first 200 chars):")
                print(f"   {wikipedia_info['summary'][:200]}...")
                return True
            else:
                print("❌ No summary content found")
                return False
        else:
            print("❌ No Wikipedia data returned")
            return False
            
    except Exception as e:
        print(f"❌ Error during Wikipedia retrieval: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_alternative_searches():
    """Test alternative search terms for triangles"""
    print("\n🔄 Testing alternative search terms")
    print("=" * 40)
    
    test_cases = [
        ("mathematics", "triangle"),
        ("geometry", "triangles"),
        ("math", "triangle geometry"),
        ("mathematics", "triangle properties")
    ]
    
    for subject, topic in test_cases:
        print(f"\n🔍 Testing: {subject}/{topic}")
        try:
            wiki_data = get_relevant_wikipedia_info(subject, topic)
            wikipedia_info = wiki_data.get("wikipedia", {}) if wiki_data else {}
            
            if wikipedia_info.get('title'):
                print(f"   ✅ Found: {wikipedia_info['title']}")
                print(f"   📏 Summary length: {len(wikipedia_info.get('summary', ''))}")
            else:
                print(f"   ❌ No content found")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    print("🧪 Wikipedia Content Retrieval Test for Triangles")
    print("=" * 70)
    
    # Test the specific failing case
    success = test_wikipedia_triangles()
    
    # Test alternative search terms
    test_alternative_searches()
    
    print("\n" + "=" * 70)
    if success:
        print("✅ Wikipedia content retrieval is working for triangles")
    else:
        print("❌ Wikipedia content retrieval failed for maths/triangles")
        print("💡 This explains why the lesson generation is failing")
