#!/usr/bin/env python3
"""
Generate a readable summary of the gold standard analysis.
Shows all 9 prompts with their execution plans and covered tasks.
"""

import json
from pathlib import Path

def main():
    # Load gold standard analysis
    json_path = Path(__file__).parent.parent / "docs/gutt_analysis/gold_standard_analysis.json"
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=" * 100)
    print("GOLD STANDARD EXECUTION COMPOSITION ANALYSIS - SUMMARY")
    print("=" * 100)
    print(f"\nVersion: {data['metadata']['version']}")
    print(f"Date: {data['metadata']['analysis_date']}")
    print(f"Total Prompts: {data['metadata']['total_prompts']}")
    print(f"Total Canonical Tasks: {data['canonical_tasks_library']['total_tasks']}")
    
    print("\n" + "=" * 100)
    print("CORRECTIONS APPLIED")
    print("=" * 100)
    for correction in data['metadata']['corrections_applied']:
        print(f"  • {correction}")
    
    print("\n" + "=" * 100)
    print("EXECUTION PLANS BY PROMPT")
    print("=" * 100)
    
    # Track task usage
    task_usage = {}
    
    for prompt_id, analysis in data['prompt_analyses'].items():
        print(f"\n{'─' * 100}")
        print(f"📋 {prompt_id.upper()}")
        print(f"{'─' * 100}")
        print(f"\nPrompt: \"{analysis['prompt_text']}\"")
        print(f"\nExecution Plan ({len(analysis['execution_plan'])} steps):")
        
        for step in analysis['execution_plan']:
            print(f"  {step['step']}. {step['task_id']} - {step['task_name']}")
            if 'note' in step:
                print(f"     Note: {step['note']}")
            
            # Track task usage
            task_id = step['task_id']
            if task_id not in task_usage:
                task_usage[task_id] = []
            task_usage[task_id].append(prompt_id)
        
        print(f"\n✅ Tasks Covered: {', '.join(analysis['tasks_covered'])}")
        print(f"⭐ Rating: {analysis['execution_plan_rating'].upper()}")
    
    print("\n" + "=" * 100)
    print("TASK USAGE ACROSS ALL PROMPTS")
    print("=" * 100)
    
    # Sort by usage frequency
    sorted_tasks = sorted(task_usage.items(), key=lambda x: len(x[1]), reverse=True)
    
    for task_id, prompts in sorted_tasks:
        frequency = len(prompts)
        percentage = (frequency / data['metadata']['total_prompts']) * 100
        print(f"\n{task_id}: {frequency}/9 ({percentage:.0f}%)")
        print(f"  Used in: {', '.join(prompts)}")
    
    print("\n" + "=" * 100)
    print("SUMMARY STATISTICS")
    print("=" * 100)
    print(f"\n✓ Total Tasks in Library: 24 (23 IDs + CAN-02 split)")
    print(f"✓ Tasks Used: {len(task_usage)}")
    print(f"✓ Tasks Unused: {24 - len(task_usage)}")
    print(f"✓ Coverage: {(len(task_usage) / 24) * 100:.1f}%")
    print(f"✓ All Execution Plans: {'CORRECT' if all(p['execution_plan_rating'] == 'correct' for p in data['prompt_analyses'].values()) else 'PARTIAL/INCORRECT'}")
    
    print("\n" + "=" * 100)
    print("🎯 VALIDATION COMPLETE - FRAMEWORK READY FOR IMPLEMENTATION")
    print("=" * 100)

if __name__ == "__main__":
    main()
