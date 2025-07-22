import requests
import json

def test_api_endpoints():
    base_url = "http://localhost:8001"
    
    # Test health endpoint
    print("Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health Status: {response.status_code}")
        print(f"Health Response: {response.text}")
    except Exception as e:
        print(f"Health Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test subjects endpoint
    print("Testing subjects endpoint...")
    try:
        response = requests.get(f"{base_url}/subjects")
        print(f"Subjects Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Subjects Count: {len(data)}")
            if data:
                print(f"First Subject: {data[0]}")
        else:
            print(f"Subjects Error Response: {response.text}")
    except Exception as e:
        print(f"Subjects Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test lectures endpoint
    print("Testing lectures endpoint...")
    try:
        response = requests.get(f"{base_url}/lectures")
        print(f"Lectures Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Lectures Count: {len(data)}")
            if data:
                print(f"First Lecture: {data[0]}")
        else:
            print(f"Lectures Error Response: {response.text}")
    except Exception as e:
        print(f"Lectures Error: {e}")
    
    print("\n" + "="*50 + "\n")
    
    # Test tests endpoint
    print("Testing tests endpoint...")
    try:
        response = requests.get(f"{base_url}/tests")
        print(f"Tests Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Tests Count: {len(data)}")
            if data:
                print(f"First Test: {data[0]}")
        else:
            print(f"Tests Error Response: {response.text}")
    except Exception as e:
        print(f"Tests Error: {e}")

    print("\n" + "="*50 + "\n")

    # Test lesson generation endpoint
    print("Testing lesson generation endpoint...")
    try:
        params = {
            "subject": "Mathematics",
            "topic": "Quadratic Equations",
            "include_wikipedia": True,
            "use_knowledge_store": True
        }
        response = requests.get(f"{base_url}/generate_lesson", params=params)
        print(f"Generate Lesson Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Lesson Subject: {data.get('subject')}")
            print(f"Lesson Topic: {data.get('topic')}")
            print(f"Lesson Status: {data.get('status')}")
            if data.get('content'):
                content_preview = data['content'][:200] + "..." if len(data['content']) > 200 else data['content']
                print(f"Content Preview: {content_preview}")
        else:
            print(f"Generate Lesson Error Response: {response.text}")
    except Exception as e:
        print(f"Generate Lesson Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
