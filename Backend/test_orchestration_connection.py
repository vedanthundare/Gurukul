#!/usr/bin/env python3
"""
Test script to verify orchestration system connection and response
"""

import requests
import json
import time

def test_orchestration_system():
    """Test the orchestration system endpoints"""
    
    print("🧪 Testing Orchestration System Connection")
    print("=" * 60)
    
    # Test different ports where orchestration might be running
    test_ports = [8000, 8002, 8006]
    
    for port in test_ports:
        print(f"\n🔍 Testing port {port}...")
        
        try:
            # Test root endpoint first
            root_url = f"http://localhost:{port}/"
            response = requests.get(root_url, timeout=5)
            
            if response.status_code == 200:
                print(f"✅ Port {port} is responding")
                data = response.json()
                print(f"📋 Service: {data.get('message', 'Unknown')}")
                
                # Test edumentor endpoint
                edumentor_url = f"http://localhost:{port}/edumentor"
                test_query = "Explain vedas in hinduism"
                
                print(f"🧪 Testing edumentor endpoint...")
                edumentor_response = requests.get(
                    edumentor_url,
                    params={"query": test_query, "user_id": "test_user"},
                    timeout=30
                )
                
                if edumentor_response.status_code == 200:
                    edumentor_data = edumentor_response.json()
                    print(f"✅ Edumentor endpoint working")
                    print(f"📝 Response keys: {list(edumentor_data.keys())}")
                    print(f"📄 Response preview: {str(edumentor_data.get('response', ''))[:200]}...")
                    print(f"🔍 Sources count: {len(edumentor_data.get('sources', []))}")
                    
                    # Show first source if available
                    sources = edumentor_data.get('sources', [])
                    if sources:
                        first_source = sources[0]
                        print(f"📚 First source: {first_source}")
                    
                    return port, edumentor_data
                else:
                    print(f"❌ Edumentor endpoint failed: {edumentor_response.status_code}")
                    print(f"Response: {edumentor_response.text[:200]}...")
            else:
                print(f"❌ Port {port} returned status {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"❌ Port {port} - Connection refused")
        except requests.exceptions.Timeout:
            print(f"⏰ Port {port} - Timeout")
        except Exception as e:
            print(f"❌ Port {port} - Error: {e}")
    
    print(f"\n❌ No working orchestration system found on ports {test_ports}")
    return None, None

def test_subject_generation_integration():
    """Test the subject generation API's integration with orchestration"""
    
    print(f"\n🧪 Testing Subject Generation Integration")
    print("=" * 60)
    
    try:
        # Test the subject generation API
        subject_api_url = "http://localhost:8005/generate_lesson"
        params = {
            "subject": "vedas",
            "topic": "types of vedas", 
            "include_wikipedia": False,
            "use_knowledge_store": True
        }
        
        print(f"🔍 Testing subject generation with Knowledge Store...")
        print(f"📋 Parameters: {params}")
        
        response = requests.get(subject_api_url, params=params, timeout=60)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Subject generation API working")
            print(f"📝 Response keys: {list(data.keys())}")
            print(f"🧠 Knowledge base used: {data.get('knowledge_base_used', False)}")
            print(f"🌐 Wikipedia used: {data.get('wikipedia_used', False)}")
            print(f"📄 Explanation preview: {str(data.get('explanation', ''))[:300]}...")
            
            sources = data.get('sources_used', [])
            print(f"🔍 Sources count: {len(sources)}")
            
            if sources:
                for i, source in enumerate(sources[:3], 1):
                    print(f"📚 Source {i}: {source.get('source', 'Unknown')}")
            
            return True, data
        else:
            print(f"❌ Subject generation API failed: {response.status_code}")
            print(f"Response: {response.text[:300]}...")
            return False, None
            
    except Exception as e:
        print(f"❌ Subject generation test failed: {e}")
        return False, None

if __name__ == "__main__":
    print("🚀 Starting Orchestration System Tests")
    print("=" * 60)
    
    # Test orchestration system
    working_port, orchestration_data = test_orchestration_system()
    
    if working_port:
        print(f"\n✅ Found working orchestration system on port {working_port}")
        
        # Test subject generation integration
        integration_success, subject_data = test_subject_generation_integration()
        
        if integration_success:
            print(f"\n🎉 Integration test successful!")
            print(f"✅ Knowledge Store is working properly")
        else:
            print(f"\n❌ Integration test failed")
            print(f"🔧 Check if subject generation API is running on port 8005")
    else:
        print(f"\n❌ No orchestration system found")
        print(f"🔧 Start the orchestration system first:")
        print(f"   cd Backend/orchestration/unified_orchestration_system")
        print(f"   python simple_api.py --port 8006")
    
    print(f"\n" + "=" * 60)
    print(f"Test completed!")
