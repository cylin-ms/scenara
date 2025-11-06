#!/usr/bin/env python3
"""
Analyze GPT-5 Composition Results
Extract insights about execution patterns, data flow complexity, orchestration requirements
"""

import json
import sys
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load results
results_file = project_root / "docs/gutt_analysis/gpt5_composition_analysis_20251106_232748.json"

with open(results_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

metadata = data['metadata']
results = data['results']

print("=" * 80)
print("GPT-5 COMPOSITION ANALYSIS INSIGHTS")
print("=" * 80)
print(f"\nTimestamp: {metadata['timestamp']}")
print(f"Model: {metadata['model']}")
print(f"Total Prompts: {metadata['total_prompts']}")
print(f"Analysis Type: {metadata['analysis_type']}")

# 1. COMPOSITION PATTERNS
print("\n" + "=" * 80)
print("1. COMPOSITION PATTERNS")
print("=" * 80)

patterns = Counter()
for r in results:
    pattern = r.get('composition_pattern', 'unknown')
    patterns[pattern] += 1

print(f"\nDistribution of {len(patterns)} unique patterns:")
for pattern, count in patterns.most_common():
    pct = (count / len(results)) * 100
    print(f"  [{count}/9] ({pct:5.1f}%) {pattern}")

# 2. EXECUTION COMPLEXITY
print("\n" + "=" * 80)
print("2. EXECUTION COMPLEXITY")
print("=" * 80)

steps_per_prompt = []
for r in results:
    steps = len(r.get('execution_plan', []))
    steps_per_prompt.append((r['prompt_id'], steps))

steps_per_prompt.sort(key=lambda x: -x[1])

total_steps = sum(s for _, s in steps_per_prompt)
avg_steps = total_steps / len(results)

print(f"\nTotal Execution Steps: {total_steps}")
print(f"Average Steps per Prompt: {avg_steps:.1f}")
print(f"Min Steps: {min(s for _, s in steps_per_prompt)}")
print(f"Max Steps: {max(s for _, s in steps_per_prompt)}")

print(f"\nSteps by Prompt (sorted by complexity):")
for prompt_id, steps in steps_per_prompt:
    bar = "█" * steps
    print(f"  {prompt_id:15s} [{steps}] {bar}")

# 3. TASK USAGE IN EXECUTION PLANS
print("\n" + "=" * 80)
print("3. CANONICAL TASK USAGE")
print("=" * 80)

task_usage = Counter()
tier_usage = Counter()

for r in results:
    for step in r.get('execution_plan', []):
        task_id = step.get('task_id', 'unknown')
        task_name = step.get('task_name', 'unknown')
        tier = step.get('tier', 0)
        
        task_usage[f"{task_id} - {task_name}"] += 1
        tier_usage[f"Tier {tier}"] += 1

print(f"\nTop 15 Most Used Tasks in Execution Plans:")
for i, (task, count) in enumerate(task_usage.most_common(15), 1):
    pct = (count / total_steps) * 100
    print(f"  {i:2d}. [{count:2d} uses] ({pct:5.1f}%) {task}")

print(f"\nTier Distribution:")
for tier, count in sorted(tier_usage.items()):
    pct = (count / total_steps) * 100
    print(f"  {tier}: {count:2d} uses ({pct:5.1f}%)")

# 4. DATA FLOW PATTERNS
print("\n" + "=" * 80)
print("4. DATA FLOW PATTERNS")
print("=" * 80)

input_types = Counter()
output_types = Counter()

for r in results:
    for step in r.get('execution_plan', []):
        input_info = step.get('input', {})
        input_type = input_info.get('type', 'unknown')
        input_types[input_type] += 1
        
        # Track final output types
        if not step.get('flows_to'):
            final_output = r.get('final_output', {})
            output_type = final_output.get('type', 'unknown')
            output_types[output_type] += 1

print(f"\nInput Data Types (how steps receive data):")
for input_type, count in input_types.most_common():
    pct = (count / total_steps) * 100
    print(f"  [{count:2d}] ({pct:5.1f}%) {input_type}")

print(f"\nFinal Output Types (what users receive):")
for output_type, count in output_types.most_common():
    print(f"  [{count}/9] {output_type}")

# 5. ORCHESTRATION REQUIREMENTS
print("\n" + "=" * 80)
print("5. ORCHESTRATION REQUIREMENTS")
print("=" * 80)

orchestration_keywords = defaultdict(list)

for r in results:
    prompt_id = r['prompt_id']
    for logic in r.get('orchestration_logic', []):
        logic_lower = logic.lower()
        if 'error' in logic_lower or 'fail' in logic_lower:
            orchestration_keywords['error_handling'].append(prompt_id)
        if 'fallback' in logic_lower or 'retry' in logic_lower:
            orchestration_keywords['fallback/retry'].append(prompt_id)
        if 'parallel' in logic_lower:
            orchestration_keywords['parallelization'].append(prompt_id)
        if 'conditional' in logic_lower or 'if' in logic_lower:
            orchestration_keywords['conditional_logic'].append(prompt_id)

print(f"\nOrchestration Patterns Found:")
for pattern, prompts in sorted(orchestration_keywords.items()):
    unique_prompts = set(prompts)
    print(f"  {pattern:20s} [{len(unique_prompts)}/9 prompts]: {', '.join(sorted(unique_prompts))}")

# 6. TIER 3 TASKS (NEEDS IMPLEMENTATION)
print("\n" + "=" * 80)
print("6. TIER 3 TASKS (NEEDS IMPLEMENTATION)")
print("=" * 80)

tier3_tasks = Counter()
tier3_prompts = defaultdict(list)

for r in results:
    prompt_id = r['prompt_id']
    for step in r.get('execution_plan', []):
        if step.get('tier') == 3:
            task = f"{step['task_id']} - {step['task_name']}"
            tier3_tasks[task] += 1
            tier3_prompts[task].append(prompt_id)

if tier3_tasks:
    print(f"\nFound {len(tier3_tasks)} Tier 3 tasks needing implementation:")
    for task, count in tier3_tasks.most_common():
        prompts = tier3_prompts[task]
        print(f"\n  {task}")
        print(f"    Used in {count} execution step(s)")
        print(f"    Prompts: {', '.join(prompts)}")
else:
    print("\n[EXCELLENT] No Tier 3 tasks needed - all execution plans use Tier 1+2 only!")

# 7. COMPLEX PROMPTS ANALYSIS
print("\n" + "=" * 80)
print("7. COMPLEX vs SIMPLE PROMPTS")
print("=" * 80)

# Complex = 6+ steps OR hybrid pattern OR uses Tier 3
complex_prompts = []
simple_prompts = []

for r in results:
    prompt_id = r['prompt_id']
    steps = len(r.get('execution_plan', []))
    pattern = r.get('composition_pattern', '')
    has_tier3 = any(step.get('tier') == 3 for step in r.get('execution_plan', []))
    
    if steps >= 6 or 'hybrid' in pattern or has_tier3:
        complex_prompts.append((prompt_id, steps, pattern, has_tier3))
    else:
        simple_prompts.append((prompt_id, steps, pattern, has_tier3))

print(f"\nCOMPLEX PROMPTS ({len(complex_prompts)}/9):")
for prompt_id, steps, pattern, has_tier3 in complex_prompts:
    tier3_marker = " [TIER 3 NEEDED]" if has_tier3 else ""
    print(f"  - {prompt_id:15s} [{steps} steps] {pattern}{tier3_marker}")

print(f"\nSIMPLE PROMPTS ({len(simple_prompts)}/9):")
for prompt_id, steps, pattern, has_tier3 in simple_prompts:
    print(f"  - {prompt_id:15s} [{steps} steps] {pattern}")

# 8. IMPLEMENTATION RECOMMENDATIONS
print("\n" + "=" * 80)
print("8. IMPLEMENTATION RECOMMENDATIONS")
print("=" * 80)

print("\nPHASE 1: Quick Wins (Simple Prompts)")
print("  Target: Sequential patterns with Tier 1+2 tasks only")
print("  Candidates:")
for prompt_id, steps, pattern, has_tier3 in simple_prompts:
    if not has_tier3:
        print(f"    - {prompt_id} ({steps} steps, {pattern})")

print("\nPHASE 2: Medium Complexity (Hybrid Patterns)")
print("  Target: Hybrid patterns with parallel execution")
print("  Candidates:")
for prompt_id, steps, pattern, has_tier3 in complex_prompts:
    if 'hybrid' in pattern and not has_tier3:
        print(f"    - {prompt_id} ({steps} steps, {pattern})")

print("\nPHASE 3: Advanced (Tier 3 Dependencies)")
print("  Target: Prompts requiring unimplemented Tier 3 tasks")
print("  Candidates:")
for prompt_id, steps, pattern, has_tier3 in complex_prompts:
    if has_tier3:
        # Find which Tier 3 tasks
        tier3_used = [step['task_id'] for step in results[complex_prompts.index((prompt_id, steps, pattern, has_tier3))].get('execution_plan', []) if step.get('tier') == 3]
        print(f"    - {prompt_id} ({steps} steps, needs: {', '.join(tier3_used)})")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
