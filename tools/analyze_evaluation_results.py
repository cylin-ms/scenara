#!/usr/bin/env python3
"""
Analyze User Evaluation Results and Identify Unused Canonical Tasks
"""

import json
from pathlib import Path
from collections import Counter, defaultdict

project_root = Path(__file__).parent.parent

# Load evaluation results
eval_file = project_root / "docs/gutt_analysis/evaluation_results_20251107_005227.json"
with open(eval_file, 'r', encoding='utf-8') as f:
    eval_data = json.load(f)

# Load canonical tasks reference
canonical_tasks = [
    {"id": "CAN-01", "name": "Calendar Events Retrieval", "tier": 1},
    {"id": "CAN-02", "name": "Meeting Classification", "tier": 1},
    {"id": "CAN-03", "name": "Calendar Event Creation/Update", "tier": 1},
    {"id": "CAN-04", "name": "Natural Language Understanding (Constraint/Intent Extraction)", "tier": 1},
    {"id": "CAN-05", "name": "Attendee/Contact Resolution", "tier": 1},
    {"id": "CAN-06", "name": "Availability Checking (Free/Busy)", "tier": 2},
    {"id": "CAN-07", "name": "Meeting Metadata Extraction", "tier": 2},
    {"id": "CAN-08", "name": "Document/Content Retrieval", "tier": 2},
    {"id": "CAN-09", "name": "Document Generation/Formatting", "tier": 2},
    {"id": "CAN-10", "name": "Time Aggregation/Statistical Analysis", "tier": 2},
    {"id": "CAN-11", "name": "Priority/Preference Matching", "tier": 2},
    {"id": "CAN-12", "name": "Constraint Satisfaction", "tier": 2},
    {"id": "CAN-13", "name": "RSVP Status Update", "tier": 2},
    {"id": "CAN-14", "name": "Recommendation Engine", "tier": 2},
    {"id": "CAN-15", "name": "Recurrence Rule Generation", "tier": 3},
    {"id": "CAN-16", "name": "Event Monitoring/Change Detection", "tier": 3},
    {"id": "CAN-17", "name": "Automatic Rescheduling", "tier": 3},
    {"id": "CAN-18", "name": "Objection/Risk Anticipation", "tier": 3},
    {"id": "CAN-19", "name": "Resource Booking (Rooms/Equipment)", "tier": 3},
    {"id": "CAN-20", "name": "Data Visualization/Reporting", "tier": 3},
]

print("=" * 80)
print("EVALUATION ANALYSIS REPORT")
print("=" * 80)
print(f"\nEvaluator: {eval_data['metadata']['evaluator']}")
print(f"Date: {eval_data['metadata']['timestamp']}")
print(f"Total Prompts: {eval_data['metadata']['total_prompts']}")

# 1. TASK USAGE ANALYSIS
print("\n" + "=" * 80)
print("1. CANONICAL TASK USAGE ACROSS ALL PROMPTS")
print("=" * 80)

tasks_used = Counter()
tasks_by_prompt = defaultdict(list)

for prompt_id, result in eval_data['evaluations'].items():
    for step_num, step in result['steps'].items():
        task_id = step['task_id']
        tasks_used[task_id] += 1
        tasks_by_prompt[task_id].append(prompt_id)

print(f"\nTasks Used (sorted by frequency):")
for task_id, count in tasks_used.most_common():
    task_name = next(t['name'] for t in canonical_tasks if t['id'] == task_id)
    tier = next(t['tier'] for t in canonical_tasks if t['id'] == task_id)
    pct = (count / 9) * 100
    prompts = ', '.join(tasks_by_prompt[task_id])
    print(f"  {task_id} (Tier {tier}) - {task_name}")
    print(f"    Used {count} times ({pct:.0f}% of prompts): {prompts}")
    print()

# 2. UNUSED TASKS
print("=" * 80)
print("2. UNUSED CANONICAL TASKS (CRITICAL FINDING)")
print("=" * 80)

used_task_ids = set(tasks_used.keys())
all_task_ids = set(t['id'] for t in canonical_tasks)
unused_task_ids = all_task_ids - used_task_ids

print(f"\n❌ {len(unused_task_ids)} tasks NEVER used in any execution plan:\n")
for task_id in sorted(unused_task_ids):
    task = next(t for t in canonical_tasks if t['id'] == task_id)
    print(f"  {task_id} (Tier {task['tier']}) - {task['name']}")

print(f"\n⚠️  PROBLEM: These tasks came from GPT-5's own analysis of GUTTs!")
print(f"    They should appear in at least one of the 9 prompts.")
print(f"    This indicates a disconnect between V1 (task identification)")
print(f"    and V2 (execution composition) analysis.")

# 3. MISSING TASKS IDENTIFIED BY USER
print("\n" + "=" * 80)
print("3. MISSING TASKS IDENTIFIED BY EVALUATOR")
print("=" * 80)

missing_tasks_total = Counter()
for prompt_id, result in eval_data['evaluations'].items():
    if result['missing_tasks']:
        print(f"\n{prompt_id}:")
        for task_id in result['missing_tasks']:
            task_name = next(t['name'] for t in canonical_tasks if t['id'] == task_id)
            print(f"  + {task_id}: {task_name}")
            missing_tasks_total[task_id] += 1

if not any(result['missing_tasks'] for result in eval_data['evaluations'].values()):
    print("\n✓ No missing tasks identified")

# 4. EXECUTION PLAN RATINGS
print("\n" + "=" * 80)
print("4. EXECUTION PLAN QUALITY RATINGS")
print("=" * 80)

ratings = Counter()
for prompt_id, result in eval_data['evaluations'].items():
    rating = result['execution_plan_rating']
    ratings[rating] += 1

total = len(eval_data['evaluations'])
print(f"\n✅ Correct: {ratings['correct']}/{total} ({ratings['correct']/total*100:.0f}%)")
print(f"⚠️  Partially Correct: {ratings['partial']}/{total} ({ratings['partial']/total*100:.0f}%)")
print(f"❌ Incorrect: {ratings['incorrect']}/{total} ({ratings['incorrect']/total*100:.0f}%)")

# 5. KEY ISSUES FROM EVALUATOR NOTES
print("\n" + "=" * 80)
print("5. KEY ISSUES IDENTIFIED BY EVALUATOR")
print("=" * 80)

print("\nIssue #1: Meeting Classification Conflation")
print("-" * 60)
print("CAN-02 'Meeting Classification' conflates TWO distinct capabilities:")
print("  1. Meeting TYPE classification (format-based: 1:1, team, customer, etc.)")
print("  2. Meeting IMPORTANCE/PRIORITY (value-based: important vs unimportant)")
print("\nEvidence from notes:")
print("  - organizer-1: 'lump two types: meeting type and meeting priority'")
print("  - organizer-2: 'meeting type and meeting priority are separate'")
print("  - organizer-3: 'important vs unimportant ones'")
print("  - schedule-2: 'classify reschedulable or not = important or not?'")

print("\nIssue #2: CAN-02 vs CAN-11 Overlap")
print("-" * 60)
print("organizer-3 notes: 'Does CAN-11 overlap with CAN-02?'")
print("  - CAN-02: Meeting Classification (includes importance?)")
print("  - CAN-11: Priority/Preference Matching (aligning with user goals)")
print("Question: If CAN-02 identifies important vs unimportant,")
print("          why do we need CAN-11 for priority matching?")

print("\nIssue #3: Missing CAN-04 (NLU) in organizer-3")
print("-" * 60)
print("organizer-3 notes: 'Isn't NLP CAN-04 needed for all prompts?'")
print("  - CAN-04 is powered by Copilot Reasoning and Language Understanding")
print("  - Should be universal across all natural language prompts")

print("\nIssue #4: CAN-01 vs CAN-06 Dependency")
print("-" * 60)
print("schedule-1 notes: 'Does CAN-06 depend on CAN-01?'")
print("  - CAN-01: Calendar Event Retrieval (find meetings)")
print("  - CAN-06: Availability Checking (find free timeslots)")
print("  - CAN-06 is complement of CAN-01")
print("  - Other prompts call CAN-01 first, then CAN-06")

print("\nIssue #5: Missing Capability - Task Duration Estimation")
print("-" * 60)
print("organizer-2 notes:")
print("  'Missing task: capability to estimate time for prep'")
print("  'How much time does this person typically need for a task?'")

print("\nIssue #6: Missing Capability - Who Works On What")
print("-" * 60)
print("collaborate-1 notes:")
print("  'Documents don't tell us who is working on what'")
print("  'Need capability to discover who works on what'")

print("\nIssue #7: Document Generation Scope")
print("-" * 60)
print("collaborate-1 notes:")
print("  'CAN-09 includes agenda generation?'")
print("  'Does this include all document types: PPT, spreadsheet, code, etc?'")
print("  'Do we need specialized generation for different formats?'")

print("\nIssue #8: Conflict Resolution")
print("-" * 60)
print("schedule-1 notes:")
print("  'Do we assume we can always find a time?'")
print("  'If not, do we have conflict resolution module?'")

# 6. TIER USAGE
print("\n" + "=" * 80)
print("6. TIER USAGE ANALYSIS")
print("=" * 80)

tier_usage = Counter()
for task_id, count in tasks_used.items():
    tier = next(t['tier'] for t in canonical_tasks if t['id'] == task_id)
    tier_usage[tier] += count

total_steps = sum(tier_usage.values())
print(f"\nTotal execution steps: {total_steps}")
for tier in [1, 2, 3]:
    count = tier_usage[tier]
    pct = (count / total_steps) * 100
    print(f"  Tier {tier}: {count} steps ({pct:.1f}%)")

# 7. RECOMMENDATIONS
print("\n" + "=" * 80)
print("7. RECOMMENDATIONS")
print("=" * 80)

print("\n1. SPLIT CAN-02 INTO TWO TASKS:")
print("   - CAN-02A: Meeting Type Classification (format-based)")
print("   - CAN-02B: Meeting Importance/Priority Assessment (value-based)")

print("\n2. CLARIFY CAN-02 vs CAN-11:")
print("   - Define clear boundaries between classification and preference matching")
print("   - Or merge into single capability if truly overlapping")

print("\n3. ADD MISSING CAPABILITIES:")
print("   - Task Duration Estimation (for organizer-2)")
print("   - Who Works On What Discovery (for collaborate-1)")
print("   - Conflict Resolution (for schedule-1)")

print("\n4. MAKE CAN-04 (NLU) UNIVERSAL:")
print("   - Should appear in ALL natural language prompts")
print("   - Currently missing from organizer-3")

print("\n5. INVESTIGATE UNUSED TASKS:")
print("   - Why are 7 canonical tasks never used?")
print("   - Re-run V1 analysis to check task identification")
print("   - Verify consistency between V1 and V2 analysis")

print("\n6. ESTABLISH TASK DEPENDENCIES:")
print("   - Document: CAN-06 depends on CAN-01")
print("   - Create dependency graph for all tasks")

print("\n7. REFINE CAN-09 SCOPE:")
print("   - Clarify if it covers all document types or needs specialization")
print("   - Consider separate tasks for PPT, spreadsheet, code generation")

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
