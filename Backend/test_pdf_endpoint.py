#!/usr/bin/env python3
"""
Test script to diagnose the PDF processing endpoint issue
"""

import requests
import json
import os
import tempfile
from datetime import datetime

def create_test_pdf():
    """Create a simple test PDF file"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import letter
        
        # Create a temporary PDF file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
        temp_path = temp_file.name
        temp_file.close()
        
        # Create PDF content
        c = canvas.Canvas(temp_path, pagesize=letter)
        c.drawString(100, 750, "Test PDF Document")
        c.drawString(100, 700, "This is a test PDF for debugging the API endpoint.")
        c.drawString(100, 650, "Generated at: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        c.save()
        
        return temp_path
    except ImportError:
        print("⚠️  reportlab not available, creating text file instead")
        # Create a simple text file as fallback
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w')
        temp_file.write("Test document content\nThis is a test file for debugging.")
        temp_file.close()
        return temp_file.name

def test_pdf_endpoint_detailed():
    """Test the PDF endpoint with detailed error reporting"""
    print("🔍 Testing PDF Processing Endpoint")
    print("=" * 50)
    
    # Test 1: Check if service is running
    print("\n1. Testing service availability...")
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        print(f"✅ Service health check: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Service health check failed: {e}")
        return False
    
    # Test 2: Test PDF endpoint without file (should get 422)
    print("\n2. Testing PDF endpoint without file...")
    try:
        response = requests.post("http://localhost:8001/process-pdf", timeout=10)
        print(f"📄 PDF endpoint (no file): {response.status_code}")
        if response.status_code == 422:
            print("✅ Endpoint is available and validates input correctly")
        else:
            print(f"   Response: {response.text[:500]}")
    except Exception as e:
        print(f"❌ PDF endpoint test failed: {e}")
        return False
    
    # Test 3: Test with actual file
    print("\n3. Testing PDF endpoint with file...")
    test_file_path = None
    try:
        # Create test file
        test_file_path = create_test_pdf()
        print(f"📁 Created test file: {test_file_path}")
        
        # Test the endpoint
        with open(test_file_path, 'rb') as f:
            files = {'file': ('test.pdf', f, 'application/pdf')}
            
            print("📤 Sending file to endpoint...")
            response = requests.post(
                "http://localhost:8001/process-pdf", 
                files=files, 
                timeout=60  # Longer timeout for processing
            )
            
            print(f"📄 PDF processing result: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ PDF processing successful!")
                try:
                    result = response.json()
                    print(f"   Title: {result.get('title', 'N/A')}")
                    print(f"   Sections: {len(result.get('sections', []))}")
                    print(f"   Answer length: {len(result.get('answer', ''))}")
                except:
                    print("   Response is not JSON format")
            else:
                print(f"❌ PDF processing failed")
                print(f"   Error: {response.text[:1000]}")
                
                # Try to parse error details
                try:
                    error_data = response.json()
                    print(f"   Error detail: {error_data.get('detail', 'No detail')}")
                except:
                    pass
                    
    except Exception as e:
        print(f"❌ File upload test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Clean up test file
        if test_file_path and os.path.exists(test_file_path):
            try:
                os.remove(test_file_path)
                print(f"🗑️  Cleaned up test file")
            except:
                pass
    
    return True

def test_dependencies():
    """Test if required dependencies are available"""
    print("\n🔧 Testing Dependencies")
    print("=" * 30)
    
    dependencies = [
        ("pymongo", "MongoDB connection"),
        ("PyMuPDF", "PDF parsing (fitz)"),
        ("langchain", "LLM integration"),
        ("faiss-cpu", "Vector search"),
        ("gtts", "Text-to-speech"),
        ("sentence-transformers", "Embeddings"),
        ("groq", "Groq API client")
    ]
    
    for dep, description in dependencies:
        try:
            __import__(dep.replace("-", "_"))
            print(f"✅ {dep}: Available ({description})")
        except ImportError:
            print(f"❌ {dep}: Missing ({description})")
    
    # Test specific imports that might fail
    print("\n🔍 Testing specific imports...")
    try:
        import fitz
        print("✅ PyMuPDF (fitz): Available")
    except ImportError as e:
        print(f"❌ PyMuPDF (fitz): {e}")
    
    try:
        from langchain.embeddings import HuggingFaceEmbeddings
        print("✅ HuggingFace Embeddings: Available")
    except ImportError as e:
        print(f"❌ HuggingFace Embeddings: {e}")
    
    try:
        from langchain.vectorstores import FAISS
        print("✅ FAISS Vector Store: Available")
    except ImportError as e:
        print(f"❌ FAISS Vector Store: {e}")

def test_environment_variables():
    """Test if required environment variables are set"""
    print("\n🌍 Testing Environment Variables")
    print("=" * 35)
    
    required_vars = [
        "GROQ_API_KEY",
        "MONGO_URI"
    ]
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if "KEY" in var:
                masked = value[:8] + "..." + value[-8:] if len(value) > 16 else "***"
                print(f"✅ {var}: {masked}")
            else:
                print(f"✅ {var}: Set")
        else:
            print(f"❌ {var}: Not set")

def main():
    """Main diagnostic function"""
    print("🚀 PDF Endpoint Diagnostic Tool")
    print("=" * 50)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    test_environment_variables()
    test_dependencies()
    success = test_pdf_endpoint_detailed()
    
    print("\n📊 Diagnostic Summary")
    print("=" * 25)
    
    if success:
        print("✅ Basic connectivity tests passed")
        print("💡 If still getting 500 errors, check:")
        print("   - Server logs for detailed error messages")
        print("   - MongoDB connection")
        print("   - Groq API key validity")
        print("   - Required Python packages installation")
    else:
        print("❌ Connectivity tests failed")
        print("💡 Recommendations:")
        print("   - Ensure API Data Service is running on port 8001")
        print("   - Check service logs for startup errors")
        print("   - Verify all dependencies are installed")
        print("   - Check environment variables")
    
    print(f"\nTest completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
