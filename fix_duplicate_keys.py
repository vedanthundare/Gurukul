#!/usr/bin/env python3
"""
Script to fix duplicate keys in AgentSimulator.jsx by replacing Date.now() with generateUniqueId()
"""

import re

def fix_duplicate_keys():
    file_path = "new frontend/src/pages/AgentSimulator.jsx"
    
    print("🔧 Fixing duplicate keys in AgentSimulator.jsx")
    
    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count original occurrences
    original_count = len(re.findall(r'id:\s*Date\.now\(\)', content))
    print(f"📊 Found {original_count} instances of 'id: Date.now()'")
    
    # Replace all instances of 'id: Date.now()' with 'id: generateUniqueId()'
    content = re.sub(r'id:\s*Date\.now\(\)', 'id: generateUniqueId()', content)
    
    # Also replace instances with arithmetic like 'Date.now() + 1'
    content = re.sub(r'id:\s*Date\.now\(\)\s*\+\s*\d+', 'id: generateUniqueId()', content)
    
    # Replace standalone Date.now() used for message IDs
    content = re.sub(r'const\s+(\w*[Mm]essage[Ii]d)\s*=\s*Date\.now\(\)(?:\s*\+\s*\d+)?', r'const \1 = generateUniqueId()', content)
    content = re.sub(r'let\s+(\w*[Mm]essage[Ii]d)\s*=\s*Date\.now\(\)(?:\s*\+\s*\d+)?', r'let \1 = generateUniqueId()', content)
    
    # Count after replacement
    remaining_count = len(re.findall(r'id:\s*Date\.now\(\)', content))
    fixed_count = original_count - remaining_count
    
    print(f"✅ Fixed {fixed_count} instances")
    if remaining_count > 0:
        print(f"⚠️  {remaining_count} instances still remain (may need manual review)")
    
    # Write the file back
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"💾 File updated successfully")
    
    # Show some examples of what was changed
    print(f"\n📝 Changes made:")
    print(f"   - 'id: Date.now()' → 'id: generateUniqueId()'")
    print(f"   - 'id: Date.now() + 1' → 'id: generateUniqueId()'")
    print(f"   - 'const messageId = Date.now()' → 'const messageId = generateUniqueId()'")

if __name__ == "__main__":
    fix_duplicate_keys()
