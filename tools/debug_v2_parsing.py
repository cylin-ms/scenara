"""
Debug V2 Prompts Parsing

Quick diagnostic to see why Organizer-1 isn't being parsed.
"""

v2_file = r"C:\Users\cyl\Projects\Scenara_v6.0_checkpoint\Scenara\docs\9_hero_prompts_v2.txt"

print("="*80)
print("V2 PROMPTS PARSING DEBUG")
print("="*80)
print()

prompts = {}
with open(v2_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
print(f"Total lines in file: {len(lines)}")
print()

for i, line in enumerate(lines, 1):
    original_line = line
    line = line.strip()
    
    print(f"Line {i}: {repr(original_line[:60])}...")
    print(f"  Stripped: {repr(line[:60])}...")
    print(f"  Has '. ': {'. ' in line}")
    print(f"  Has ': ': {': ' in line}")
    
    if not line or line.startswith('#'):
        print(f"  ❌ SKIPPED: Empty or comment")
        continue
    
    # Parse format: "1. Organizer-1: "prompt text""
    if '. ' in line and ': ' in line:
        parts = line.split(': ', 1)
        print(f"  Parts after ': ' split: {len(parts)} parts")
        
        if len(parts) == 2:
            # Extract prompt ID (e.g., "Organizer-1")
            id_part = parts[0].split('. ', 1)
            print(f"  ID part after '. ' split: {len(id_part)} parts -> {id_part}")
            
            if len(id_part) == 2:
                prompt_id = id_part[1].strip()
                # Remove quotes and clean prompt text
                prompt_text = parts[1].strip().strip('"')
                prompts[prompt_id] = prompt_text
                print(f"  ✅ PARSED: {prompt_id}")
            else:
                print(f"  ❌ FAILED: ID part has {len(id_part)} parts (expected 2)")
        else:
            print(f"  ❌ FAILED: Parts has {len(parts)} parts (expected 2)")
    else:
        print(f"  ❌ FAILED: Missing required delimiters")
    
    print()

print("="*80)
print(f"✅ Loaded {len(prompts)} prompts:")
for prompt_id in prompts.keys():
    print(f"   - {prompt_id}")
print("="*80)
