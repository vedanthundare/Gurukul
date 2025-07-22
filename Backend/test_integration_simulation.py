#!/usr/bin/env python3
"""
Simulate the fixed integration between enhanced lesson generator and subject_generation API
"""

import sys
import os

# Add the subject_generation directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'subject_generation'))

def simulate_fixed_integration():
    """Simulate the fixed integration"""
    
    print("🧪 Simulating Fixed Integration")
    print("=" * 50)
    
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
        
        print(f"\n⏰ Step 1: Calling enhanced lesson generator...")
        
        lesson_data = create_enhanced_lesson(subject, topic, include_wikipedia, use_knowledge_store)
        
        print(f"\n✅ Step 2: Enhanced lesson generator completed!")
        
        # Simulate the fixed API logic
        authentic_content = lesson_data.get("explanation", "")
        fallback_content = f"This comprehensive lesson explores {topic} within the context of {subject}. Drawing from educational knowledge bases, we examine the fundamental principles, practical applications, and significance of this topic in modern learning."
        
        final_lesson_text = authentic_content if authentic_content else fallback_content
        
        print(f"\n🔍 Step 3: Content Selection Logic (FIXED)")
        print(f"  Authentic content length: {len(authentic_content)}")
        print(f"  Fallback content length: {len(fallback_content)}")
        print(f"  Using: {'AUTHENTIC' if authentic_content else 'FALLBACK'} content")
        print(f"  Final content length: {len(final_lesson_text)}")
        
        # Simulate the API response
        formatted_lesson = {
            "title": lesson_data.get("title", f"Understanding {topic} in {subject}"),
            "level": "intermediate",
            "text": final_lesson_text,
            "subject": subject,
            "topic": topic,
            "knowledge_base_used": lesson_data.get("knowledge_base_used", False),
            "detailed_sources": lesson_data.get("detailed_sources", []),
            "sources": lesson_data.get("sources", [])
        }
        
        print(f"\n📄 Step 4: Final API Response")
        print(f"  Title: {formatted_lesson['title']}")
        print(f"  Text length: {len(formatted_lesson['text'])}")
        print(f"  Knowledge base used: {formatted_lesson['knowledge_base_used']}")
        print(f"  Detailed sources count: {len(formatted_lesson['detailed_sources'])}")
        
        print(f"\n📄 Text Preview:")
        print(f"  {formatted_lesson['text'][:300]}...")
        
        # Check if we're getting authentic content
        if "108upanishads" in formatted_lesson['text'].lower() or "brahman" in formatted_lesson['text'].lower():
            print(f"\n🎉 SUCCESS: Authentic Vedic content detected!")
            print(f"✅ Knowledge Store integration is working properly!")
            return True, formatted_lesson
        else:
            print(f"\n⚠️  Still getting generic content")
            return False, formatted_lesson
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False, None

if __name__ == "__main__":
    success, data = simulate_fixed_integration()
    
    if success:
        print(f"\n🎉 Integration simulation successful!")
        print(f"✅ The fix will work once the API server is restarted")
    else:
        print(f"\n❌ Integration simulation failed")
        print(f"🔧 Need to investigate further")
