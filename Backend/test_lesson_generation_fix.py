#!/usr/bin/env python3
"""
Test script to verify the lesson generation fix
This script tests the complete lesson generation workflow
"""

import requests
import json
import time
from datetime import datetime

# Configuration
LESSON_API_BASE = "http://localhost:8000"

def test_lesson_generation():
    """Test the complete lesson generation workflow"""
    print("🧪 Testing Lesson Generation Fix")
    print("=" * 50)
    
    # Test data
    test_data = {
        "subject": "Mathematics",
        "topic": "Basic Algebra",
        "user_id": "test-user",
        "include_wikipedia": True,
        "force_regenerate": True
    }
    
    print(f"📚 Testing lesson generation for: {test_data['subject']} - {test_data['topic']}")
    
    try:
        # Step 1: Create lesson
        print("\n🚀 Step 1: Creating lesson...")
        create_url = f"{LESSON_API_BASE}/lessons"
        print(f"POST URL: {create_url}")
        
        response = requests.post(create_url, json=test_data, timeout=30)
        print(f"Response Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Failed to create lesson: {response.text}")
            return False
            
        create_result = response.json()
        task_id = create_result.get("task_id")
        print(f"✅ Lesson creation initiated. Task ID: {task_id}")
        
        # Step 2: Poll for completion
        print("\n⏳ Step 2: Polling for completion...")
        status_url = f"{LESSON_API_BASE}/lessons/status/{task_id}"
        
        max_attempts = 60  # 2 minutes
        for attempt in range(1, max_attempts + 1):
            print(f"Polling attempt {attempt}/{max_attempts}...")
            
            try:
                status_response = requests.get(status_url, timeout=10)
                if status_response.status_code == 200:
                    status_data = status_response.json()
                    print(f"Status: {status_data.get('status')}")
                    
                    if status_data.get('status') == 'completed':
                        lesson_data = status_data.get('lesson_data')
                        if lesson_data:
                            print("✅ Lesson generation completed successfully!")
                            print(f"📖 Title: {lesson_data.get('title', 'N/A')}")
                            print(f"🔤 Shloka: {lesson_data.get('shloka', 'N/A')[:100]}...")
                            print(f"📝 Explanation: {lesson_data.get('explanation', 'N/A')[:100]}...")
                            return True
                        else:
                            print("❌ Lesson completed but no data returned")
                            return False
                    elif status_data.get('status') == 'failed':
                        print(f"❌ Lesson generation failed: {status_data.get('error_message')}")
                        return False
                    elif status_data.get('status') in ['pending', 'in_progress']:
                        print("⏳ Still processing...")
                        time.sleep(2)
                        continue
                else:
                    print(f"⚠️ Status check failed: {status_response.status_code}")
                    
            except requests.Timeout:
                print("⏰ Status check timed out, retrying...")
            except Exception as e:
                print(f"❌ Error during status check: {e}")
                
            time.sleep(2)
        
        print("❌ Lesson generation timed out")
        return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def test_service_health():
    """Test if all required services are running"""
    print("\n🏥 Testing Service Health")
    print("=" * 30)
    
    services = [
        ("Lesson Generator", "http://localhost:8000/"),
        ("API Data Service", "http://localhost:8001/health"),
    ]
    
    all_healthy = True
    for service_name, url in services:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name}: Healthy")
            else:
                print(f"⚠️ {service_name}: Responded with {response.status_code}")
                all_healthy = False
        except Exception as e:
            print(f"❌ {service_name}: Not accessible - {e}")
            all_healthy = False
    
    return all_healthy

if __name__ == "__main__":
    print("🔧 Gurukul Lesson Generation Fix Test")
    print("=" * 60)
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Test service health first
    if not test_service_health():
        print("\n❌ Some services are not healthy. Please check the backend services.")
        exit(1)
    
    # Test lesson generation
    success = test_lesson_generation()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests passed! The lesson generation fix is working correctly.")
        print("✅ Frontend should now display generated lesson content properly.")
    else:
        print("❌ Tests failed. Please check the logs above for details.")
    
    print(f"⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
