"""
Test Script for Video Transfer Workflow
Run this to test the complete video generation and transfer system
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
MAIN_SYSTEM_URL = "http://localhost:8001"
ANIMATEDIFF_SYSTEM_URL = "https://4e6b01c6e6f2.ngrok-free.app"
API_KEY = "shashank_ka_vision786"

def test_main_system_endpoints():
    """Test that main system endpoints are accessible"""
    print("🧪 Testing main system endpoints...")
    
    try:
        # Test basic health
        response = requests.get(f"{MAIN_SYSTEM_URL}/")
        print(f"✅ Main system health check: {response.status_code}")
        
        # Test video list endpoint
        response = requests.get(f"{MAIN_SYSTEM_URL}/videos")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Video list endpoint: {data['count']} videos stored")
        else:
            print(f"❌ Video list endpoint failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Main system test failed: {str(e)}")

def test_animatediff_system():
    """Test AnimateDiff system connectivity"""
    print("🧪 Testing AnimateDiff system...")
    
    try:
        # Test basic connectivity
        headers = {
            "ngrok-skip-browser-warning": "true"
        }
        response = requests.get(f"{ANIMATEDIFF_SYSTEM_URL}/", headers=headers, timeout=10)
        print(f"✅ AnimateDiff system accessible: {response.status_code}")
        
    except Exception as e:
        print(f"❌ AnimateDiff system test failed: {str(e)}")

def simulate_video_upload():
    """Simulate uploading a video to the main system"""
    print("🧪 Testing video upload to main system...")
    
    try:
        # Create a dummy video file for testing
        dummy_video_content = b"dummy video content for testing"
        
        # Prepare metadata
        metadata = {
            "subject": "Test Subject",
            "topic": "Test Topic",
            "prompt": "Test video generation prompt",
            "generated_at": datetime.now().isoformat(),
            "file_size": len(dummy_video_content),
            "system_info": "Test_System",
            "num_frames": 16,
            "guidance_scale": 7.5,
            "steps": 25,
            "seed": 333,
            "fps": 8
        }
        
        # Prepare files and data
        files = {
            'video': ('test_video.mp4', dummy_video_content, 'video/mp4')
        }
        
        data = {
            'metadata': json.dumps(metadata)
        }
        
        headers = {
            'x-api-key': API_KEY
        }
        
        # Send POST request
        response = requests.post(
            f"{MAIN_SYSTEM_URL}/receive-video",
            files=files,
            data=data,
            headers=headers,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Video upload successful!")
            print(f"🎬 Video ID: {result['video_id']}")
            print(f"🎬 Access URL: {result['access_url']}")
            
            # Test retrieving the video
            video_id = result['video_id']
            video_response = requests.get(f"{MAIN_SYSTEM_URL}/videos/{video_id}")
            
            if video_response.status_code == 200:
                print(f"✅ Video retrieval successful! Size: {len(video_response.content)} bytes")
            else:
                print(f"❌ Video retrieval failed: {video_response.status_code}")
                
            # Test video info endpoint
            info_response = requests.get(f"{MAIN_SYSTEM_URL}/videos/{video_id}/info")
            if info_response.status_code == 200:
                info_data = info_response.json()
                print(f"✅ Video info retrieval successful: {info_data['video_info']['subject']}")
            else:
                print(f"❌ Video info retrieval failed: {info_response.status_code}")
                
        else:
            print(f"❌ Video upload failed: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Video upload test failed: {str(e)}")

def test_proxy_endpoints():
    """Test the proxy endpoints"""
    print("🧪 Testing proxy endpoints...")
    
    try:
        # Test proxy/vision endpoint
        payload = {
            "prompt": "Test video generation",
            "negative_prompt": "blurry, low quality",
            "num_frames": 16,
            "guidance_scale": 7.5,
            "steps": 25,
            "seed": 333,
            "fps": 8
        }
        
        response = requests.post(
            f"{MAIN_SYSTEM_URL}/proxy/vision",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 Proxy/vision endpoint response: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text[:200]}...")
            
        # Test test-generate-video endpoint
        response = requests.post(
            f"{MAIN_SYSTEM_URL}/test-generate-video",
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"📡 Test-generate-video endpoint response: {response.status_code}")
        if response.status_code != 200:
            print(f"   Response: {response.text[:200]}...")
            
    except Exception as e:
        print(f"❌ Proxy endpoints test failed: {str(e)}")

def main():
    """Run all tests"""
    print("🚀 Starting Video Transfer Workflow Tests")
    print("=" * 50)
    
    # Test 1: Main system endpoints
    test_main_system_endpoints()
    print()
    
    # Test 2: AnimateDiff system
    test_animatediff_system()
    print()
    
    # Test 3: Video upload simulation
    simulate_video_upload()
    print()
    
    # Test 4: Proxy endpoints
    test_proxy_endpoints()
    print()
    
    print("=" * 50)
    print("🏁 Tests completed!")
    print()
    print("📋 Next Steps:")
    print("1. Start your main backend server: python Backend/api_data/api.py")
    print("2. Ensure AnimateDiff service is running on the other system")
    print("3. Test video generation from your React frontend")
    print("4. Check that videos are properly transferred and accessible")

if __name__ == "__main__":
    main()
