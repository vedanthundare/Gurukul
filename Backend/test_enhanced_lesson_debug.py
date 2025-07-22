#!/usr/bin/env python3
"""
Debug test for enhanced lesson generator
"""

import sys
import os

# Add the subject_generation directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'subject_generation'))

def test_enhanced_lesson_generator():
    """Test the enhanced lesson generator directly"""
    
    print("🧪 Testing Enhanced Lesson Generator Directly")
    print("=" * 60)
    
    try:
        from generate_lesson_enhanced import create_enhanced_lesson
        
        subject = "vedas"
        topic = "types of vedas"
        include_wikipedia = False
        use_knowledge_store = True
        
        print(f"📋 Parameters:")
        print(f"  Subject: {subject}")
        print(f"  Topic: {topic}")
        print(f"  Include Wikipedia: {include_wikipedia}")
        print(f"  Use Knowledge Store: {use_knowledge_store}")
        
        print(f"\n⏰ Calling create_enhanced_lesson...")
        
        lesson_data = create_enhanced_lesson(subject, topic, include_wikipedia, use_knowledge_store)
        
        print(f"\n✅ Enhanced lesson generator completed!")
        print(f"📝 Response keys: {list(lesson_data.keys())}")
        
        # Check key fields
        explanation = lesson_data.get("explanation", "")
        detailed_sources = lesson_data.get("detailed_sources", [])
        knowledge_base_used = lesson_data.get("knowledge_base_used", False)
        
        print(f"\n🔍 Key Analysis:")
        print(f"  Explanation length: {len(explanation)}")
        print(f"  Detailed sources count: {len(detailed_sources)}")
        print(f"  Knowledge base used: {knowledge_base_used}")
        
        if explanation:
            print(f"\n📄 Explanation preview:")
            print(f"  {explanation[:300]}...")
        else:
            print(f"\n⚠️  No explanation generated")
        
        if detailed_sources:
            print(f"\n📚 First detailed source:")
            first_source = detailed_sources[0]
            print(f"  Type: {first_source.get('source_type', 'Unknown')}")
            print(f"  Name: {first_source.get('source_name', 'Unknown')}")
            print(f"  Content preview: {first_source.get('content_preview', '')[:200]}...")
        else:
            print(f"\n⚠️  No detailed sources found")
        
        return True, lesson_data
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False, None

if __name__ == "__main__":
    success, data = test_enhanced_lesson_generator()
    
    if success:
        print(f"\n🎉 Test completed successfully!")
    else:
        print(f"\n❌ Test failed")
