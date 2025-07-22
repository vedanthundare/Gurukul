#!/usr/bin/env python3
"""
Test script to verify the fallback mechanism when both Ollama and Wikipedia fail
"""

import sys
import os
import unittest.mock as mock

sys.path.append(os.path.join(os.path.dirname(__file__), 'pipline-24-master'))

def test_fallback_when_all_sources_fail():
    """Test that the system provides fallback content when all sources fail"""
    print("🧪 Testing Fallback Mechanism When All Sources Fail")
    print("=" * 70)
    
    try:
        # Mock the imports to simulate failure conditions
        with mock.patch('generate_lesson_enhanced.check_ollama_service') as mock_ollama, \
             mock.patch('generate_lesson_enhanced.get_relevant_wikipedia_info') as mock_wiki:
            
            # Mock Ollama as not available
            mock_ollama.return_value = (False, "")
            
            # Mock Wikipedia as returning no content
            mock_wiki.return_value = {
                "subject": "test",
                "topic": "test",
                "wikipedia": {
                    "title": None,
                    "summary": None,
                    "content": None,
                    "url": None,
                    "related_articles": []
                }
            }
            
            # Import after mocking
            from generate_lesson_enhanced import create_enhanced_lesson
            
            print("🚫 Simulating conditions:")
            print("   • Ollama: Not available")
            print("   • Wikipedia: No content found")
            
            # Test with a topic that should trigger fallback
            subject = "test_subject"
            topic = "test_topic"
            
            print(f"\n🚀 Generating lesson for: {subject}/{topic}")
            lesson_data = create_enhanced_lesson(subject, topic)
            
            if lesson_data:
                print("✅ Fallback mechanism worked!")
                print(f"   📖 Title: {lesson_data.get('title', 'N/A')}")
                print(f"   📝 Explanation: {lesson_data.get('explanation', 'N/A')[:100]}...")
                print(f"   🎯 Activity: {lesson_data.get('activity', 'N/A')[:100]}...")
                print(f"   ❓ Question: {lesson_data.get('question', 'N/A')[:100]}...")
                print(f"   📊 Sources: {lesson_data.get('sources', [])}")
                
                # Verify that fallback content was used
                if "Basic Template" in lesson_data.get('sources', []):
                    print("✅ Confirmed: Basic Template fallback was used")
                    return True
                else:
                    print("⚠️ Warning: Expected 'Basic Template' in sources")
                    return False
            else:
                print("❌ Fallback mechanism failed - no lesson data returned")
                return False
                
    except Exception as e:
        print(f"❌ Error during fallback test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_with_wikipedia_only():
    """Test fallback when only Wikipedia is available"""
    print("\n🧪 Testing Fallback with Wikipedia Only")
    print("=" * 50)
    
    try:
        with mock.patch('generate_lesson_enhanced.check_ollama_service') as mock_ollama:
            
            # Mock Ollama as not available
            mock_ollama.return_value = (False, "")
            
            # Import after mocking
            from generate_lesson_enhanced import create_enhanced_lesson
            
            print("🚫 Simulating conditions:")
            print("   • Ollama: Not available")
            print("   • Wikipedia: Available (real data)")
            
            # Test with a topic that should have Wikipedia content
            subject = "mathematics"
            topic = "triangle"
            
            print(f"\n🚀 Generating lesson for: {subject}/{topic}")
            lesson_data = create_enhanced_lesson(subject, topic)
            
            if lesson_data:
                print("✅ Wikipedia fallback worked!")
                print(f"   📖 Title: {lesson_data.get('title', 'N/A')}")
                print(f"   📝 Explanation: {lesson_data.get('explanation', 'N/A')[:100]}...")
                print(f"   📊 Sources: {lesson_data.get('sources', [])}")
                
                # Verify that Wikipedia was used
                if "Wikipedia" in lesson_data.get('sources', []):
                    print("✅ Confirmed: Wikipedia fallback was used")
                    return True
                else:
                    print("⚠️ Warning: Expected 'Wikipedia' in sources")
                    return False
            else:
                print("❌ Wikipedia fallback failed - no lesson data returned")
                return False
                
    except Exception as e:
        print(f"❌ Error during Wikipedia fallback test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ollama_timeout_fallback():
    """Test fallback when Ollama times out"""
    print("\n🧪 Testing Ollama Timeout Fallback")
    print("=" * 40)
    
    try:
        with mock.patch('generate_lesson_enhanced.check_ollama_service') as mock_ollama, \
             mock.patch('generate_lesson_enhanced.generate_with_ollama') as mock_generate:
            
            # Mock Ollama as available but generation fails
            mock_ollama.return_value = (True, "test-model")
            mock_generate.side_effect = Exception("Connection timeout")
            
            # Import after mocking
            from generate_lesson_enhanced import create_enhanced_lesson
            
            print("🚫 Simulating conditions:")
            print("   • Ollama: Available but times out")
            print("   • Wikipedia: Available (real data)")
            
            # Test with a topic that should have Wikipedia content
            subject = "mathematics"
            topic = "triangle"
            
            print(f"\n🚀 Generating lesson for: {subject}/{topic}")
            lesson_data = create_enhanced_lesson(subject, topic)
            
            if lesson_data:
                print("✅ Timeout fallback worked!")
                print(f"   📖 Title: {lesson_data.get('title', 'N/A')}")
                print(f"   📊 Sources: {lesson_data.get('sources', [])}")
                
                # Should fall back to Wikipedia
                if "Wikipedia" in lesson_data.get('sources', []):
                    print("✅ Confirmed: Fell back to Wikipedia after Ollama timeout")
                    return True
                else:
                    print("⚠️ Warning: Expected fallback to Wikipedia")
                    return False
            else:
                print("❌ Timeout fallback failed - no lesson data returned")
                return False
                
    except Exception as e:
        print(f"❌ Error during timeout fallback test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 Comprehensive Fallback Mechanism Test")
    print("=" * 80)
    print("🎯 Goal: Verify that the system gracefully handles all failure scenarios")
    print()
    
    # Test 1: Complete failure fallback
    test1_success = test_fallback_when_all_sources_fail()
    
    # Test 2: Wikipedia-only fallback
    test2_success = test_fallback_with_wikipedia_only()
    
    # Test 3: Ollama timeout fallback
    test3_success = test_ollama_timeout_fallback()
    
    print("\n" + "=" * 80)
    print("📊 Fallback Test Results:")
    print(f"   🚫 All sources fail: {'✅' if test1_success else '❌'}")
    print(f"   📚 Wikipedia only: {'✅' if test2_success else '❌'}")
    print(f"   ⏰ Ollama timeout: {'✅' if test3_success else '❌'}")
    
    if all([test1_success, test2_success, test3_success]):
        print("\n🎉 All fallback tests passed!")
        print("💡 The system should now handle all error scenarios gracefully")
        print("🔧 The original error should be resolved")
    else:
        print("\n❌ Some fallback tests failed")
        print("🔍 Additional fixes may be needed")
        
    print("\n💡 Next steps:")
    print("   1. Test the frontend with the updated backend")
    print("   2. Verify error messages are user-friendly")
    print("   3. Confirm lesson generation works for various topics")
