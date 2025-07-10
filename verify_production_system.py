"""
Production System Verification Script
Run this to verify the production team's system configuration
"""

import requests
import json
import time
from datetime import datetime

# ========================================
# CONFIGURATION TO VERIFY
# ========================================

# These are the values we need to confirm with the production team:
CONFIGS_TO_TEST = [
    {
        "name": "Current Assumption",
        "ip": "192.168.0.121",
        "port": "8001",
        "endpoint": "/receive-video",
        "api_key": "shashank_ka_vision786"
    },
    {
        "name": "Alternative 1 (Different Port)",
        "ip": "192.168.0.121",
        "port": "8000",
        "endpoint": "/receive-video",
        "api_key": "shashank_ka_vision786"
    },
    {
        "name": "Alternative 2 (Different Endpoint)",
        "ip": "192.168.0.121",
        "port": "8001",
        "endpoint": "/upload-video",
        "api_key": "shashank_ka_vision786"
    }
]

def test_system_connectivity(config):
    """Test if the production system is reachable"""
    print(f"\n🧪 Testing: {config['name']}")
    print(f"   URL: http://{config['ip']}:{config['port']}")
    
    try:
        # Test basic connectivity
        base_url = f"http://{config['ip']}:{config['port']}"
        
        print(f"   ⏳ Testing basic connectivity...")
        response = requests.get(base_url, timeout=5)
        print(f"   ✅ Basic connectivity: {response.status_code}")
        
        # Test if the specific endpoint exists
        endpoint_url = f"{base_url}{config['endpoint']}"
        print(f"   ⏳ Testing endpoint: {config['endpoint']}")
        
        # Try a simple GET first to see if endpoint exists
        try:
            get_response = requests.get(endpoint_url, timeout=5)
            print(f"   📡 GET {config['endpoint']}: {get_response.status_code}")
        except:
            print(f"   📡 GET {config['endpoint']}: Not accessible")
        
        # Try OPTIONS to check allowed methods
        try:
            options_response = requests.options(endpoint_url, timeout=5)
            print(f"   📡 OPTIONS {config['endpoint']}: {options_response.status_code}")
            if 'Allow' in options_response.headers:
                print(f"   📋 Allowed methods: {options_response.headers['Allow']}")
        except:
            print(f"   📡 OPTIONS {config['endpoint']}: Not accessible")
            
        return True
        
    except requests.exceptions.ConnectError:
        print(f"   ❌ Connection failed: Cannot reach {config['ip']}:{config['port']}")
        return False
    except requests.exceptions.Timeout:
        print(f"   ❌ Timeout: {config['ip']}:{config['port']} is not responding")
        return False
    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return False

def test_video_upload(config):
    """Test video upload to the production system"""
    print(f"\n🎬 Testing video upload to: {config['name']}")
    
    try:
        # Create dummy video content
        dummy_video_content = b"dummy video content for testing"
        
        # Prepare metadata
        metadata = {
            "subject": "Test Subject",
            "topic": "Test Topic", 
            "prompt": "Test video upload",
            "generated_at": datetime.now().isoformat(),
            "file_size": len(dummy_video_content),
            "system_info": "Test_AnimateDiff_System"
        }
        
        # Prepare request
        url = f"http://{config['ip']}:{config['port']}{config['endpoint']}"
        
        files = {
            'video': ('test_video.mp4', dummy_video_content, 'video/mp4')
        }
        
        data = {
            'metadata': json.dumps(metadata)
        }
        
        headers = {
            'x-api-key': config['api_key']
        }
        
        print(f"   ⏳ Sending POST request...")
        print(f"   📍 URL: {url}")
        print(f"   🔑 API Key: {config['api_key']}")
        
        response = requests.post(url, files=files, data=data, headers=headers, timeout=30)
        
        print(f"   📡 Response Status: {response.status_code}")
        print(f"   📄 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"   ✅ Upload successful!")
                print(f"   📋 Response: {json.dumps(result, indent=2)}")
                return True
            except:
                print(f"   ✅ Upload successful (non-JSON response)")
                print(f"   📄 Response text: {response.text[:200]}...")
                return True
        else:
            print(f"   ❌ Upload failed: {response.status_code}")
            print(f"   📄 Response: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"   ❌ Upload test failed: {str(e)}")
        return False

def main():
    """Run verification tests"""
    print("🚀 Production System Verification")
    print("=" * 50)
    print("This script will test different configurations to find the correct one.")
    print()
    
    connectivity_results = []
    upload_results = []
    
    # Test connectivity for all configurations
    print("📡 CONNECTIVITY TESTS")
    print("-" * 30)
    for config in CONFIGS_TO_TEST:
        result = test_system_connectivity(config)
        connectivity_results.append((config, result))
    
    # Test video upload for configurations that passed connectivity
    print("\n🎬 VIDEO UPLOAD TESTS")
    print("-" * 30)
    for config, connected in connectivity_results:
        if connected:
            result = test_video_upload(config)
            upload_results.append((config, result))
        else:
            print(f"\n⏭️  Skipping upload test for {config['name']} (not connected)")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 50)
    
    print("\n🔌 Connectivity Results:")
    for config, result in connectivity_results:
        status = "✅ CONNECTED" if result else "❌ FAILED"
        print(f"   {config['name']}: {status}")
    
    print("\n🎬 Upload Results:")
    if upload_results:
        for config, result in upload_results:
            status = "✅ SUCCESS" if result else "❌ FAILED"
            print(f"   {config['name']}: {status}")
    else:
        print("   No upload tests performed (no systems connected)")
    
    # Recommendations
    print("\n💡 RECOMMENDATIONS:")
    
    successful_configs = [config for config, result in upload_results if result]
    
    if successful_configs:
        print("   ✅ Working configuration found!")
        for config in successful_configs:
            print(f"   📍 Use: http://{config['ip']}:{config['port']}{config['endpoint']}")
            print(f"   🔑 API Key: {config['api_key']}")
    else:
        print("   ❌ No working configuration found!")
        print("   📞 Contact the production team to confirm:")
        print("      1. Exact IP address and port")
        print("      2. Exact endpoint URL")
        print("      3. Required authentication")
        print("      4. Whether their system is running")
    
    print("\n📞 QUESTIONS FOR PRODUCTION TEAM:")
    print("   1. What is your exact IP address and port?")
    print("   2. What is your exact endpoint URL for receiving videos?")
    print("   3. What authentication do you expect?")
    print("   4. Is your receiving system currently running?")
    print("   5. Can you test connectivity from your end?")

if __name__ == "__main__":
    main()
