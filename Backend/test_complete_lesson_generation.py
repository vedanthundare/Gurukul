#!/usr/bin/env python3
"""
Test script to reproduce the exact lesson generation error for maths/triangles
"""

import sys
import os
import requests
import json
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'pipline-24-master'))

try:
    from generate_lesson_enhanced import create_enhanced_lesson
    print("✅ Successfully imported create_enhanced_lesson")
except ImportError as e:
    print(f"❌ Failed to import create_enhanced_lesson: {e}")
    sys.exit(1)

def test_complete_lesson_generation():
    """Test the complete lesson generation workflow that's failing"""
    print("🧪 Testing Complete Lesson Generation for 'maths/triangles'")
    print("=" * 70)
    
    subject = "maths"
    topic = "triangles"
    
    try:
        print(f"🚀 Generating lesson for: {subject}/{topic}")
        print("⏱️ This may take up to 2 minutes...")
        
        start_time = time.time()
        lesson_data = create_enhanced_lesson(subject, topic)
        end_time = time.time()
        
        print(f"✅ Lesson generation completed in {end_time - start_time:.2f} seconds")
        
        if lesson_data:
            print("\n📚 Generated Lesson Content:")
            print(f"   📖 Title: {lesson_data.get('title', 'N/A')}")
            print(f"   🔤 Shloka: {lesson_data.get('shloka', 'N/A')[:100]}...")
            print(f"   🌐 Translation: {lesson_data.get('translation', 'N/A')[:100]}...")
            print(f"   📝 Explanation: {lesson_data.get('explanation', 'N/A')[:100]}...")
            print(f"   🎯 Activity: {lesson_data.get('activity', 'N/A')[:100]}...")
            print(f"   ❓ Question: {lesson_data.get('question', 'N/A')[:100]}...")
            print(f"   📊 Sources: {lesson_data.get('sources', [])}")
            
            # Check if Wikipedia info is included
            if lesson_data.get('wikipedia_info'):
                wiki_info = lesson_data['wikipedia_info']
                print(f"   🌐 Wikipedia: {wiki_info.get('title', 'N/A')}")
            else:
                print("   🌐 Wikipedia: Not included")
            
            return True, lesson_data
        else:
            print("❌ Lesson generation returned None")
            return False, None
            
    except ValueError as e:
        print(f"❌ ValueError during lesson generation: {e}")
        if "No content sources available" in str(e):
            print("💡 This is the exact error reported in the frontend!")
        return False, None
    except Exception as e:
        print(f"❌ Unexpected error during lesson generation: {e}")
        import traceback
        traceback.print_exc()
        return False, None

def test_api_endpoint():
    """Test the actual API endpoint that the frontend calls"""
    print("\n🌐 Testing API Endpoint (POST /lessons)")
    print("=" * 50)
    
    try:
        # Test the exact API call that the frontend makes
        api_url = "http://localhost:8000/lessons"
        payload = {
            "subject": "maths",
            "topic": "triangles",
            "user_id": "test-user",
            "include_wikipedia": True,
            "force_regenerate": True
        }
        
        print(f"📡 Making POST request to: {api_url}")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(api_url, json=payload, timeout=30)
        
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("task_id")
            print(f"✅ Lesson creation initiated")
            print(f"🆔 Task ID: {task_id}")
            
            if task_id:
                # Poll for completion
                print("\n⏳ Polling for completion...")
                status_url = f"http://localhost:8000/lessons/status/{task_id}"
                
                for attempt in range(1, 11):  # Poll for up to 10 attempts
                    print(f"   Attempt {attempt}/10...")
                    
                    try:
                        status_response = requests.get(status_url, timeout=10)
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            status = status_data.get('status')
                            print(f"   Status: {status}")
                            
                            if status == 'completed':
                                lesson_data = status_data.get('lesson_data')
                                if lesson_data:
                                    print("✅ API endpoint test successful!")
                                    return True
                                else:
                                    print("❌ Completed but no lesson data")
                                    return False
                            elif status == 'failed':
                                error_msg = status_data.get('error_message', 'Unknown error')
                                print(f"❌ API generation failed: {error_msg}")
                                return False
                            elif status in ['pending', 'in_progress']:
                                time.sleep(3)  # Wait 3 seconds between polls
                                continue
                        else:
                            print(f"   ⚠️ Status check failed: {status_response.status_code}")
                            
                    except Exception as e:
                        print(f"   ❌ Error during status check: {e}")
                    
                    time.sleep(3)
                
                print("❌ API endpoint test timed out")
                return False
            else:
                print("❌ No task ID received")
                return False
        else:
            print(f"❌ API request failed: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API endpoint: {e}")
        return False

if __name__ == "__main__":
    print("🔧 Complete Lesson Generation Test")
    print("=" * 80)
    print("🎯 Goal: Reproduce the exact error from the frontend")
    print()
    
    # Test the direct function call
    direct_success, lesson_data = test_complete_lesson_generation()
    
    # Test the API endpoint
    api_success = test_api_endpoint()
    
    print("\n" + "=" * 80)
    print("📊 Final Test Results:")
    print(f"   🔧 Direct function call: {'✅' if direct_success else '❌'}")
    print(f"   🌐 API endpoint test: {'✅' if api_success else '❌'}")
    
    if direct_success and api_success:
        print("\n🎉 All tests passed!")
        print("💡 The lesson generation should be working correctly")
        print("🔍 If the frontend is still failing, the issue may be elsewhere")
    elif direct_success and not api_success:
        print("\n⚠️ Direct function works but API fails")
        print("💡 There may be an issue with the API layer or async processing")
    elif not direct_success:
        print("\n❌ Direct function call failed")
        print("💡 This confirms the core lesson generation issue")
        print("🔧 Need to implement better fallback mechanisms")
    else:
        print("\n❓ Unexpected result combination")
        print("🔍 Further investigation needed")
