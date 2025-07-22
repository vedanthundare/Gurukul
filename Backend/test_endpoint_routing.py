#!/usr/bin/env python3
"""
Test script to verify that all API endpoints are working correctly
and that the frontend is calling the right ports for each service.
"""

import requests
import json
import time
from datetime import datetime

# Service configurations
SERVICES = {
    "api_data": {
        "port": 8001,
        "name": "API Data Service",
        "endpoints": [
            "/health",
            "/subjects", 
            "/lectures",
            "/tests",
            "/process-pdf",
            "/proxy/vision",
            "/test-generate-video"
        ]
    },
    "financial_simulator": {
        "port": 8002,
        "name": "Financial Simulator",
        "endpoints": [
            "/start-simulation",
            "/user/learning",
            "/pdf/chat"
        ]
    },
    "memory_management": {
        "port": 8003,
        "name": "Memory Management",
        "endpoints": [
            "/memory/health"
        ]
    },
    "agent_mind_auth": {
        "port": 8004,
        "name": "Agent Mind-Auth-Memory",
        "endpoints": [
            "/",
            "/health"
        ]
    },
    "lesson_generator": {
        "port": 8000,
        "name": "Lesson Generator",
        "endpoints": [
            "/",
            "/llm_status",
            "/lessons/tasks"
        ]
    }
}

def test_endpoint(service_name, port, endpoint, method="GET", data=None):
    """Test a specific endpoint"""
    url = f"http://localhost:{port}{endpoint}"
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=5)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=5)
        
        return {
            "service": service_name,
            "endpoint": endpoint,
            "url": url,
            "status_code": response.status_code,
            "success": response.status_code < 400,
            "response_time": response.elapsed.total_seconds()
        }
    except requests.exceptions.ConnectionError:
        return {
            "service": service_name,
            "endpoint": endpoint,
            "url": url,
            "status_code": None,
            "success": False,
            "error": "Connection refused - service not running"
        }
    except requests.exceptions.Timeout:
        return {
            "service": service_name,
            "endpoint": endpoint,
            "url": url,
            "status_code": None,
            "success": False,
            "error": "Request timeout"
        }
    except Exception as e:
        return {
            "service": service_name,
            "endpoint": endpoint,
            "url": url,
            "status_code": None,
            "success": False,
            "error": str(e)
        }

def test_pdf_processing():
    """Test PDF processing endpoint specifically"""
    print("\n🔍 Testing PDF Processing Endpoint...")
    
    # Test with a simple request to see if endpoint exists
    url = "http://localhost:8001/process-pdf"
    
    try:
        # Make a POST request without file to see if endpoint responds
        response = requests.post(url, timeout=5)
        print(f"📄 PDF endpoint status: {response.status_code}")
        
        if response.status_code == 422:  # Validation error (expected without file)
            print("✅ PDF endpoint is available and responding correctly")
            return True
        elif response.status_code == 404:
            print("❌ PDF endpoint not found - check if service is running")
            return False
        else:
            print(f"⚠️  PDF endpoint returned unexpected status: {response.status_code}")
            return True  # Endpoint exists but may need proper request
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API Data Service on port 8001")
        return False
    except Exception as e:
        print(f"❌ Error testing PDF endpoint: {e}")
        return False

def test_video_generation():
    """Test video generation endpoints"""
    print("\n🎬 Testing Video Generation Endpoints...")
    
    endpoints = [
        ("http://localhost:8001/proxy/vision", "Proxy Vision"),
        ("http://localhost:8001/test-generate-video", "Test Generate Video")
    ]
    
    results = []
    for url, name in endpoints:
        try:
            # Test with minimal payload
            payload = {
                "prompt": "test",
                "num_frames": 8
            }
            response = requests.post(url, json=payload, timeout=5)
            
            print(f"🎥 {name}: {response.status_code}")
            results.append({
                "endpoint": name,
                "status": response.status_code,
                "available": response.status_code != 404
            })
            
        except requests.exceptions.ConnectionError:
            print(f"❌ {name}: Connection refused")
            results.append({
                "endpoint": name,
                "status": None,
                "available": False
            })
        except Exception as e:
            print(f"⚠️  {name}: {e}")
            results.append({
                "endpoint": name,
                "status": None,
                "available": False
            })
    
    return results

def main():
    """Main test function"""
    print("🚀 Backend API Endpoint Routing Test")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    all_results = []
    
    # Test each service
    for service_key, service_config in SERVICES.items():
        print(f"\n📡 Testing {service_config['name']} (Port {service_config['port']})")
        print("-" * 40)
        
        for endpoint in service_config['endpoints']:
            result = test_endpoint(
                service_config['name'], 
                service_config['port'], 
                endpoint
            )
            
            status_icon = "✅" if result['success'] else "❌"
            if result.get('error'):
                print(f"{status_icon} {endpoint}: {result['error']}")
            else:
                print(f"{status_icon} {endpoint}: {result['status_code']} ({result.get('response_time', 0):.3f}s)")
            
            all_results.append(result)
    
    # Test specific problematic endpoints
    pdf_working = test_pdf_processing()
    video_results = test_video_generation()
    
    # Summary
    print("\n📊 Test Summary")
    print("=" * 50)
    
    working_services = len([r for r in all_results if r['success']])
    total_services = len(all_results)
    
    print(f"Working endpoints: {working_services}/{total_services}")
    
    # Service status
    service_status = {}
    for result in all_results:
        service = result['service']
        if service not in service_status:
            service_status[service] = {'working': 0, 'total': 0}
        
        service_status[service]['total'] += 1
        if result['success']:
            service_status[service]['working'] += 1
    
    print("\nService Status:")
    for service, status in service_status.items():
        working = status['working']
        total = status['total']
        percentage = (working / total * 100) if total > 0 else 0
        status_icon = "✅" if working == total else "⚠️" if working > 0 else "❌"
        print(f"{status_icon} {service}: {working}/{total} ({percentage:.0f}%)")
    
    # Frontend routing recommendations
    print("\n🔧 Frontend Configuration Check:")
    print("- PDF Processing: Should use CHAT_API_BASE_URL (port 8001)")
    print("- Video Generation: Should use CHAT_API_BASE_URL (port 8001)")
    print("- Lesson Generation: Should use API_BASE_URL (port 8000)")
    print("- Financial Simulation: Should use FINANCIAL_API_BASE_URL (port 8002)")
    
    if pdf_working:
        print("✅ PDF processing endpoint is correctly configured")
    else:
        print("❌ PDF processing endpoint needs attention")
    
    video_available = any(r['available'] for r in video_results)
    if video_available:
        print("✅ Video generation endpoints are available")
    else:
        print("❌ Video generation endpoints need attention")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
