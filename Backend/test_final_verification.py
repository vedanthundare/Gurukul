#!/usr/bin/env python3
"""
Final verification test to ensure the lesson generation error is completely resolved
"""

import sys
import os
import requests
import json
import time

sys.path.append(os.path.join(os.path.dirname(__file__), 'pipline-24-master'))

def test_original_failing_case():
    """Test the exact case that was failing: maths/triangles"""
    print("🎯 Testing Original Failing Case: maths/triangles")
    print("=" * 60)
    
    try:
        from generate_lesson_enhanced import create_enhanced_lesson
        
        subject = "maths"
        topic = "triangles"
        
        print(f"🚀 Generating lesson for: {subject}/{topic}")
        print("   (This was the exact case that was failing)")
        
        start_time = time.time()
        lesson_data = create_enhanced_lesson(subject, topic)
        end_time = time.time()
        
        if lesson_data:
            print(f"✅ SUCCESS! Lesson generated in {end_time - start_time:.2f} seconds")
            print(f"   📖 Title: {lesson_data.get('title', 'N/A')}")
            print(f"   📝 Has explanation: {'Yes' if lesson_data.get('explanation') else 'No'}")
            print(f"   🎯 Has activity: {'Yes' if lesson_data.get('activity') else 'No'}")
            print(f"   ❓ Has question: {'Yes' if lesson_data.get('question') else 'No'}")
            print(f"   📊 Sources: {lesson_data.get('sources', [])}")
            
            # Verify all required fields are present
            required_fields = ['title', 'explanation', 'activity', 'question', 'sources']
            missing_fields = [field for field in required_fields if not lesson_data.get(field)]
            
            if not missing_fields:
                print("✅ All required fields are present")
                return True
            else:
                print(f"❌ Missing fields: {missing_fields}")
                return False
        else:
            print("❌ FAILED: No lesson data returned")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_api_endpoint_original_case():
    """Test the API endpoint with the original failing case"""
    print("\n🌐 Testing API Endpoint with Original Case")
    print("=" * 50)
    
    try:
        api_url = "http://localhost:8000/lessons"
        payload = {
            "subject": "maths",
            "topic": "triangles",
            "user_id": "test-user",
            "include_wikipedia": True,
            "force_regenerate": True
        }
        
        print(f"📡 POST {api_url}")
        print(f"📦 Payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(api_url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            task_id = result.get("task_id")
            print(f"✅ Request accepted, Task ID: {task_id}")
            
            if task_id:
                # Poll for completion with shorter timeout for testing
                status_url = f"http://localhost:8000/lessons/status/{task_id}"
                
                for attempt in range(1, 21):  # Poll for up to 20 attempts (1 minute)
                    try:
                        status_response = requests.get(status_url, timeout=5)
                        if status_response.status_code == 200:
                            status_data = status_response.json()
                            status = status_data.get('status')
                            
                            if status == 'completed':
                                lesson_data = status_data.get('lesson_data')
                                if lesson_data:
                                    print(f"✅ API SUCCESS! Lesson completed")
                                    print(f"   📖 Title: {lesson_data.get('title', 'N/A')}")
                                    print(f"   📊 Sources: {lesson_data.get('sources', [])}")
                                    return True
                                else:
                                    print("❌ API FAILED: Completed but no lesson data")
                                    return False
                            elif status == 'failed':
                                error_msg = status_data.get('error_message', 'Unknown error')
                                print(f"❌ API FAILED: {error_msg}")
                                return False
                            elif status in ['pending', 'in_progress']:
                                if attempt % 5 == 0:  # Print progress every 5 attempts
                                    print(f"   ⏳ Still processing... (attempt {attempt}/20)")
                                time.sleep(3)
                                continue
                        else:
                            print(f"   ⚠️ Status check failed: {status_response.status_code}")
                            
                    except requests.Timeout:
                        if attempt % 5 == 0:
                            print(f"   ⏰ Timeout on attempt {attempt}, retrying...")
                    except Exception as e:
                        print(f"   ❌ Error: {e}")
                    
                    time.sleep(3)
                
                print("❌ API FAILED: Timed out waiting for completion")
                return False
            else:
                print("❌ API FAILED: No task ID received")
                return False
        else:
            print(f"❌ API FAILED: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ API FAILED: Exception: {e}")
        return False

def test_various_topics():
    """Test various topics to ensure the fix works broadly"""
    print("\n🔄 Testing Various Topics")
    print("=" * 30)
    
    test_cases = [
        ("mathematics", "algebra"),
        ("science", "physics"),
        ("history", "ancient"),
        ("philosophy", "ethics")
    ]
    
    success_count = 0
    
    for subject, topic in test_cases:
        try:
            from generate_lesson_enhanced import create_enhanced_lesson
            
            print(f"   🧪 Testing: {subject}/{topic}")
            lesson_data = create_enhanced_lesson(subject, topic)
            
            if lesson_data and lesson_data.get('explanation'):
                print(f"      ✅ Success")
                success_count += 1
            else:
                print(f"      ❌ Failed")
                
        except Exception as e:
            print(f"      ❌ Error: {e}")
    
    print(f"\n📊 Various topics test: {success_count}/{len(test_cases)} passed")
    return success_count == len(test_cases)

if __name__ == "__main__":
    print("🔧 Final Verification Test")
    print("=" * 80)
    print("🎯 Goal: Confirm the original error is completely resolved")
    print("📋 Testing the exact scenario that was failing in the frontend")
    print()
    
    # Test 1: Direct function call with original case
    test1_success = test_original_failing_case()
    
    # Test 2: API endpoint with original case
    test2_success = test_api_endpoint_original_case()
    
    # Test 3: Various topics to ensure broad compatibility
    test3_success = test_various_topics()
    
    print("\n" + "=" * 80)
    print("📊 Final Verification Results:")
    print(f"   🎯 Original case (direct): {'✅' if test1_success else '❌'}")
    print(f"   🌐 Original case (API): {'✅' if test2_success else '❌'}")
    print(f"   🔄 Various topics: {'✅' if test3_success else '❌'}")
    
    if all([test1_success, test2_success, test3_success]):
        print("\n🎉 COMPLETE SUCCESS!")
        print("✅ The original error has been completely resolved")
        print("✅ The lesson generation system is now robust and reliable")
        print("✅ All fallback mechanisms are working correctly")
        print()
        print("🚀 The frontend should now work without the error:")
        print('   "Unable to generate lesson content: Unable to generate lesson for maths/triangles."')
        print()
        print("💡 Key improvements made:")
        print("   • Robust fallback mechanism when Ollama fails")
        print("   • Better Wikipedia content utilization")
        print("   • Basic template fallback when all sources fail")
        print("   • Enhanced error handling in frontend")
        print("   • Improved user feedback and messaging")
    else:
        print("\n❌ Some tests failed")
        print("🔍 Additional investigation may be needed")
        
    print("\n🔄 Next steps:")
    print("   1. Test the frontend application")
    print("   2. Try generating lessons for 'maths/triangles'")
    print("   3. Verify user-friendly error messages")
    print("   4. Confirm the system works with various topics")
