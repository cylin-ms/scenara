#!/usr/bin/env python3
"""
Test GPT-5 Composition Analysis with ONE Prompt
Focus on execution plan and data flow composition
"""

import json
import sys
from pathlib import Path

# Add project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier, DEFAULT_ENDPOINT, DEFAULT_MODEL

# Initialize GPT-5 client
gpt5_client = GPT5MeetingClassifier(
    model=DEFAULT_MODEL,
    endpoint=DEFAULT_ENDPOINT
)

# Load canonical library
canonical_lib_path = project_root / "docs/gutt_analysis/CANONICAL_UNIT_TASKS_REFERENCE.md"
with open(canonical_lib_path, 'r', encoding='utf-8') as f:
    canonical_library = f.read()

# Test with organizer-1 prompt
prompt_id = "organizer-1"
prompt_text = "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy."

print("=" * 80)
print("GPT-5 COMPOSITION ANALYSIS TEST")
print("=" * 80)
print(f"\nPrompt: {prompt_text}\n")

# Construct analysis prompt
analysis_prompt = f"""You are an expert at designing computational workflows for Calendar.AI prompts.

CANONICAL UNIT TASKS LIBRARY:
{canonical_library}

USER PROMPT TO ANALYZE:
ID: {prompt_id}
Text: "{prompt_text}"

ANALYSIS INSTRUCTIONS:
1. Identify ALL canonical tasks needed (use task IDs: CAN-01, CAN-02, etc.)
2. Design an EXECUTION PLAN showing how tasks compose together computationally
3. For each step, show:
   - Which canonical task is used
   - Input data (what it receives)
   - Processing/transformation (what it does)
   - Output data (what it produces)
   - How output flows to next task
4. Show the complete data flow from user input to final result
5. Identify any orchestration logic needed between tasks

OUTPUT FORMAT (JSON):
{{
  "prompt_id": "{prompt_id}",
  "prompt_text": "{prompt_text}",
  "execution_plan": [
    {{
      "step": 1,
      "task_id": "CAN-XX",
      "task_name": "Task Name",
      "tier": 1,
      "input": {{
        "type": "user_prompt|previous_step_output|external_data",
        "description": "What data this step receives",
        "schema": "Brief schema or example"
      }},
      "processing": "Detailed description of the transformation/computation",
      "output": {{
        "description": "What data this step produces",
        "schema": "Brief schema or example"
      }},
      "flows_to": ["step_2", "step_5"]
    }}
  ],
  "data_flow_summary": "High-level description of how data flows through the composition",
  "orchestration_logic": [
    "Conditional logic needed",
    "Error handling requirements",
    "Retry or fallback strategies"
  ],
  "composition_pattern": "sequential|parallel|conditional|iterative",
  "final_output": {{
    "type": "JSON|UI_display|API_response|calendar_update",
    "description": "What the user ultimately receives",
    "schema": "Expected output structure"
  }}
}}

Provide ONLY the JSON output, no additional text.
"""

# Call GPT-5
print("Calling GPT-5...")
system_message = """You are an expert at designing computational workflows for Calendar.AI prompts.
Focus on data flow, transformations, and how tasks compose together.
Think like a software architect designing a processing pipeline."""

result = gpt5_client._call_gpt5_api(
    system_message=system_message,
    user_prompt=analysis_prompt,
    timeout=60
)

if not result.success:
    print(f"ERROR: {result.error}")
    sys.exit(1)

# Parse response
response_text = result.response_content.strip()
if response_text.startswith("```json"):
    response_text = response_text.split("```json")[1].split("```")[0].strip()
elif response_text.startswith("```"):
    response_text = response_text.split("```")[1].split("```")[0].strip()

try:
    analysis = json.loads(response_text)
    
    print("\nSUCCESS! Received composition analysis\n")
    print("=" * 80)
    print("EXECUTION PLAN")
    print("=" * 80)
    
    for step in analysis.get('execution_plan', []):
        print(f"\nStep {step['step']}: {step['task_id']} - {step['task_name']}")
        print(f"  Tier: {step['tier']}")
        print(f"  Input: {step['input']['description']}")
        print(f"  Processing: {step['processing'][:100]}...")
        print(f"  Output: {step['output']['description']}")
        if step.get('flows_to'):
            print(f"  Flows to: {', '.join(step['flows_to'])}")
    
    print("\n" + "=" * 80)
    print("DATA FLOW SUMMARY")
    print("=" * 80)
    print(f"\n{analysis.get('data_flow_summary', 'N/A')}\n")
    
    print("=" * 80)
    print("COMPOSITION PATTERN")
    print("=" * 80)
    print(f"\n{analysis.get('composition_pattern', 'N/A')}\n")
    
    print("=" * 80)
    print("FINAL OUTPUT")
    print("=" * 80)
    final_output = analysis.get('final_output', {})
    print(f"\nType: {final_output.get('type', 'N/A')}")
    print(f"Description: {final_output.get('description', 'N/A')}")
    print(f"Schema: {final_output.get('schema', 'N/A')}\n")
    
    # Save full result
    output_file = project_root / f"docs/gutt_analysis/composition_test_{prompt_id}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2)
    
    print(f"\nFull analysis saved to: {output_file}")
    print("=" * 80)

except json.JSONDecodeError as e:
    print(f"\nERROR parsing JSON: {e}")
    print(f"\nRaw response:\n{response_text[:500]}")
