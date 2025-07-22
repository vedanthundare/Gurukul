#!/usr/bin/env python3
"""
Test script to check Ollama functionality for maths/triangles lesson generation
"""

import sys
import os
import requests
import json

sys.path.append(os.path.join(os.path.dirname(__file__), 'pipline-24-master'))

try:
    from generate_lesson_enhanced import check_ollama_service, generate_with_ollama
    print("✅ Successfully imported generate_lesson_enhanced")
except ImportError as e:
    print(f"❌ Failed to import generate_lesson_enhanced: {e}")
    sys.exit(1)

def test_ollama_service():
    """Test Ollama service connectivity and available models"""
    print("🔍 Testing Ollama service status")
    print("=" * 40)
    
    try:
        running, model = check_ollama_service()
        print(f"🤖 Ollama running: {running}")
        print(f"📦 Available model: {model}")
        
        if running and model:
            print("✅ Ollama service is operational")
            return True, model
        else:
            print("❌ Ollama service is not operational")
            return False, None
            
    except Exception as e:
        print(f"❌ Error checking Ollama service: {e}")
        return False, None

def test_ollama_generation():
    """Test Ollama lesson generation for maths/triangles"""
    print("\n🧠 Testing Ollama lesson generation for 'maths/triangles'")
    print("=" * 60)
    
    subject = "maths"
    topic = "triangles"
    
    # First check if Ollama is available
    running, model = test_ollama_service()
    if not running or not model:
        print("❌ Cannot test generation - Ollama not available")
        return False
    
    try:
        print(f"🚀 Generating lesson with model: {model}")
        lesson_data = generate_with_ollama(subject, topic, model)
        
        if lesson_data:
            print("✅ Lesson generation successful!")
            print(f"📖 Title: {lesson_data.get('title', 'N/A')}")
            print(f"🔤 Shloka: {lesson_data.get('shloka', 'N/A')[:100]}...")
            print(f"🌐 Translation: {lesson_data.get('translation', 'N/A')[:100]}...")
            print(f"📝 Explanation: {lesson_data.get('explanation', 'N/A')[:100]}...")
            print(f"🎯 Activity: {lesson_data.get('activity', 'N/A')[:100]}...")
            print(f"❓ Question: {lesson_data.get('question', 'N/A')[:100]}...")
            return True
        else:
            print("❌ Lesson generation returned None")
            return False
            
    except Exception as e:
        print(f"❌ Error during lesson generation: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_direct_ollama_api():
    """Test direct Ollama API call"""
    print("\n🔗 Testing direct Ollama API call")
    print("=" * 40)
    
    try:
        # Test basic connectivity
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            print(f"✅ Ollama API accessible")
            print(f"📦 Available models: {len(models.get('models', []))}")
            
            # Test generation with a simple prompt
            if models.get('models'):
                model_name = models['models'][0]['name']
                print(f"🧪 Testing generation with model: {model_name}")
                
                gen_response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": model_name,
                        "prompt": "What is a triangle? Respond in JSON format with title, explanation fields.",
                        "stream": False,
                        "options": {"temperature": 0.7}
                    },
                    timeout=30
                )
                
                if gen_response.status_code == 200:
                    result = gen_response.json()
                    response_text = result.get("response", "")
                    print(f"✅ Generation successful")
                    print(f"📝 Response length: {len(response_text)}")
                    print(f"📄 Response preview: {response_text[:200]}...")
                    return True
                else:
                    print(f"❌ Generation failed: {gen_response.status_code}")
                    return False
            else:
                print("❌ No models available")
                return False
        else:
            print(f"❌ Ollama API not accessible: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Ollama API: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Ollama Functionality Test for Triangles")
    print("=" * 70)
    
    # Test direct API access
    api_success = test_direct_ollama_api()
    
    # Test service check function
    service_success, model = test_ollama_service()
    
    # Test lesson generation
    generation_success = False
    if service_success:
        generation_success = test_ollama_generation()
    
    print("\n" + "=" * 70)
    print("📊 Test Results Summary:")
    print(f"   🔗 Direct API access: {'✅' if api_success else '❌'}")
    print(f"   🤖 Service check: {'✅' if service_success else '❌'}")
    print(f"   🧠 Lesson generation: {'✅' if generation_success else '❌'}")
    
    if all([api_success, service_success, generation_success]):
        print("\n🎉 All Ollama tests passed!")
        print("💡 Ollama should be working for lesson generation")
    else:
        print("\n❌ Some Ollama tests failed")
        print("💡 This may explain why lesson generation is failing")
