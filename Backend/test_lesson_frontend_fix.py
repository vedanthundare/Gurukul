#!/usr/bin/env python3
"""
Test script to verify the lesson generation fix works correctly
"""

import requests
import json

def test_lesson_generation_fix():
    print("🔍 Testing Lesson Generation Fix")
    print("=" * 50)
    
    # Test the exact request that the frontend makes
    url = "http://localhost:8000/lessons"
    
    # Use the same data structure as the frontend
    test_data = {
        "subject": "maths",
        "topic": "algebra", 
        "user_id": "81bddc54-d80c-4c0c-ab31-47d3ead8cb6f",
        "include_wikipedia": True,
        "force_regenerate": True
    }
    
    print(f"📡 URL: {url}")
    print(f"📊 Request Data: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"\n📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            
            print("✅ SUCCESS! Lesson generation working")
            print(f"📋 Response Keys: {list(response_data.keys())}")
            
            # Check what the frontend expects
            has_task_id = 'task_id' in response_data
            has_content = 'content' in response_data
            has_status = response_data.get('status') == 'success'
            
            print(f"\n🔍 Frontend Compatibility Check:")
            print(f"   Has task_id: {has_task_id}")
            print(f"   Has content: {has_content}")
            print(f"   Status success: {has_status}")
            
            if has_task_id:
                print(f"   ✅ Will use async processing (task_id: {response_data['task_id']})")
            elif has_content or has_status:
                print(f"   ✅ Will use immediate processing")
                print(f"   📝 Content preview: {response_data.get('content', 'N/A')[:100]}...")
            else:
                print(f"   ❌ Response format not compatible with frontend")
                
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"📄 Response: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

def test_both_endpoints():
    print("\n🔍 Testing Both Lesson Endpoints")
    print("=" * 50)
    
    endpoints = [
        {"name": "Main API (Port 8000)", "url": "http://localhost:8000/lessons"},
        {"name": "Subject Generation (Port 8005)", "url": "http://localhost:8005/lessons"}
    ]
    
    test_data = {
        "subject": "science",
        "topic": "physics",
        "user_id": "test-user",
        "include_wikipedia": False,
        "force_regenerate": False
    }
    
    for endpoint in endpoints:
        print(f"\n🧪 Testing {endpoint['name']}")
        print("-" * 30)
        
        try:
            response = requests.post(endpoint['url'], json=test_data, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                has_task_id = 'task_id' in data
                has_content = 'content' in data
                
                print(f"   ✅ Status: 200 OK")
                print(f"   📋 Response type: {'Async (task_id)' if has_task_id else 'Immediate (content)'}")
                
                if has_task_id:
                    print(f"   🔄 Task ID: {data['task_id']}")
                elif has_content:
                    print(f"   📝 Content length: {len(data.get('content', ''))}")
                    
            else:
                print(f"   ❌ Status: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"   ❌ Service not running")
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    test_lesson_generation_fix()
    test_both_endpoints()
    
    print(f"\n🎯 Summary:")
    print(f"   - Frontend fix should handle both response types")
    print(f"   - Port 8000: Immediate responses (no task_id)")
    print(f"   - Port 8005: Async responses (with task_id)")
    print(f"   - Both should work with the updated frontend code")
