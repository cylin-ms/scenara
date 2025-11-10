#!/usr/bin/env python3
"""
Detailed Analysis of GPT-5 Canonical Task Results
Analyzes the JSON output from analyze_prompt_with_gpt5.py
"""

import json
from collections import Counter
from pathlib import Path

# Load the JSON data
json_file = Path('docs/gutt_analysis/gpt5_canonical_analysis_20251106_230413.json')
with open(json_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=' * 80)
print('GPT-5 CANONICAL TASK ANALYSIS - DETAILED REVIEW')
print('=' * 80)
print()

# Overall Statistics
summary = data['summary']
metadata = data['metadata']
print('📊 OVERALL STATISTICS')
print('-' * 80)
print(f'Total Prompts Analyzed: {metadata["total_prompts"]}')
print(f'Total Canonical Tasks Used: {summary["total_canonical_tasks_used"]}')
print(f'Average Tasks per Prompt: {summary["average_tasks_per_prompt"]:.2f}')
print(f'Tasks Implemented: {summary["total_implemented"]} ({summary["overall_coverage_percentage"]:.1f}%)')
print(f'Tasks Need Implementation: {summary["total_needs_implementation"]} ({100-summary["overall_coverage_percentage"]:.1f}%)')
print()
print('Effort Distribution:')
for effort, count in summary['effort_distribution'].items():
    print(f'  {effort}: {count} prompts')
print()

# Task Frequency Analysis
task_usage = Counter()
task_names = {}
task_tiers = {}
needs_impl_tasks = set()

for prompt_id, analysis in data['prompt_analyses'].items():
    for task in analysis['canonical_tasks']:
        task_usage[task['task_id']] += 1
        task_names[task['task_id']] = task['task_name']
        task_tiers[task['task_id']] = task['tier']
        if task['implementation_status'] == 'needs_implementation':
            needs_impl_tasks.add(task['task_id'])

print('🏆 MOST USED CANONICAL TASKS (Top 15)')
print('-' * 80)
for rank, (task_id, count) in enumerate(task_usage.most_common(15), 1):
    tier = task_tiers.get(task_id, '?')
    name = task_names.get(task_id, 'Unknown')
    status = '⚠️' if task_id in needs_impl_tasks else '✅'
    pct = (count / metadata['total_prompts']) * 100
    print(f'{rank:2}. {status} {task_id} (T{tier}): {count}/9 ({pct:3.0f}%) - {name[:50]}')
print()

# Tier Analysis
tier_usage = Counter()
tier_tasks = {1: set(), 2: set(), 3: set()}
for task_id, tier in task_tiers.items():
    tier_usage[tier] += task_usage[task_id]
    tier_tasks[tier].add(task_id)

print('📈 USAGE BY TIER')
print('-' * 80)
for tier in sorted(tier_usage.keys()):
    count = tier_usage[tier]
    unique_tasks = len(tier_tasks[tier])
    pct = (count / summary['total_canonical_tasks_used']) * 100
    tier_name = {1: 'Universal', 2: 'Common', 3: 'Specialized'}[tier]
    print(f'Tier {tier} ({tier_name:11}): {unique_tasks:2} unique tasks, {count:2} total uses ({pct:5.1f}%)')
print()

# Tasks Needing Implementation
print('⚠️  TASKS REQUIRING IMPLEMENTATION')
print('-' * 80)
if needs_impl_tasks:
    impl_by_tier = Counter()
    for task_id in sorted(needs_impl_tasks):
        tier = task_tiers[task_id]
        name = task_names[task_id]
        count = task_usage[task_id]
        tier_name = {1: 'Universal', 2: 'Common', 3: 'Specialized'}[tier]
        impl_by_tier[tier] += 1
        print(f'  {task_id} (Tier {tier} - {tier_name:11}): Used in {count} prompt(s) - {name}')
    
    print()
    print('  Summary by Tier:')
    for tier in sorted(impl_by_tier.keys()):
        tier_name = {1: 'Universal', 2: 'Common', 3: 'Specialized'}[tier]
        print(f'    Tier {tier} ({tier_name}): {impl_by_tier[tier]} tasks need implementation')
else:
    print('  None - All tasks already implemented!')
print()

# Per-Prompt Breakdown
print('📋 PER-PROMPT BREAKDOWN')
print('-' * 80)
print(f'{"Prompt":<15} | {"Effort":^8} | {"Tasks":^6} | {"Impl":^5} | {"Need":^5} | {"Coverage":^8}')
print('-' * 80)
for prompt_id, analysis in sorted(data['prompt_analyses'].items()):
    coverage = analysis['coverage_analysis']['coverage_percentage']
    effort = analysis['implementation_effort']
    tasks_count = analysis['coverage_analysis']['total_tasks_identified']
    impl = analysis['coverage_analysis']['implemented_tasks']
    need = analysis['coverage_analysis']['needs_implementation']
    
    coverage_icon = '✅' if coverage == 100 else '⚠️'
    effort_icon = {'Low': '🟢', 'Medium': '🟡', 'High': '🔴'}[effort]
    
    print(f'{prompt_id:<15} | {effort_icon} {effort:6} | {tasks_count:^6} | {impl:^5} | {need:^5} | {coverage:6.1f}% {coverage_icon}')
print()

# Detailed prompt analysis with execution sequences
print('🔍 DETAILED PROMPT ANALYSIS')
print('-' * 80)
for prompt_id, analysis in sorted(data['prompt_analyses'].items()):
    print(f'\n{prompt_id.upper()}:')
    print(f'  Prompt: "{analysis["prompt_text"][:70]}..."')
    print(f'  Tasks: {analysis["coverage_analysis"]["total_tasks_identified"]} | Effort: {analysis["implementation_effort"]} | Coverage: {analysis["coverage_analysis"]["coverage_percentage"]:.0f}%')
    
    # List tasks by tier
    tasks_by_tier = {1: [], 2: [], 3: []}
    for task in analysis['canonical_tasks']:
        tasks_by_tier[task['tier']].append(task['task_id'])
    
    for tier in [1, 2, 3]:
        if tasks_by_tier[tier]:
            tier_name = {1: 'T1', 2: 'T2', 3: 'T3'}[tier]
            print(f'  {tier_name}: {", ".join(tasks_by_tier[tier])}')
    
    # Recommendations
    if analysis['recommendations']:
        print(f'  💡 Key Recommendation: {analysis["recommendations"][0][:70]}...')
print()

# Key Insights
print('💡 KEY INSIGHTS')
print('-' * 80)

# Most universal task
most_used = task_usage.most_common(1)[0]
print(f'1. Most Critical Task: {most_used[0]} ({task_names[most_used[0]]}) used in {most_used[1]}/9 prompts (100%)')

# Coverage leaders
perfect_coverage = [p for p, a in data['prompt_analyses'].items() if a['coverage_analysis']['coverage_percentage'] == 100]
print(f'2. Perfect Coverage: {len(perfect_coverage)}/9 prompts ({", ".join(perfect_coverage)})')

# Tier 1 dominance
tier1_count = len(tier_tasks[1])
tier1_usage = tier_usage[1]
tier1_pct = (tier1_usage / summary['total_canonical_tasks_used']) * 100
print(f'3. Tier 1 Dominance: {tier1_count} Universal tasks account for {tier1_usage}/{summary["total_canonical_tasks_used"]} uses ({tier1_pct:.1f}%)')

# Tier 3 specialization
tier3_count = len(tier_tasks[3])
tier3_usage_total = tier_usage[3]
print(f'4. Specialized Needs: {tier3_count} Tier 3 tasks used {tier3_usage_total} times across specific scenarios')

# Low effort dominance
low_effort_count = summary['effort_distribution'].get('Low', 0)
low_effort_pct = (low_effort_count / metadata['total_prompts']) * 100
print(f'5. Implementation Ready: {low_effort_count}/9 prompts ({low_effort_pct:.0f}%) are Low effort (orchestration only)')

# Implementation gap
impl_gap_pct = 100 - summary['overall_coverage_percentage']
print(f'6. Implementation Gap: Only {impl_gap_pct:.1f}% of required functionality needs new development')

# Task reusability
avg_reuse = summary['total_canonical_tasks_used'] / len(task_usage)
print(f'7. Task Reusability: Average {avg_reuse:.1f} uses per unique canonical task')

print()
print('=' * 80)
print('📝 CONCLUSION')
print('-' * 80)
print(f'The 20 Canonical Unit Tasks provide {summary["overall_coverage_percentage"]:.1f}% coverage for all 9 hero prompts.')
print(f'Only {summary["total_needs_implementation"]} tasks need implementation, primarily Tier 3 specialized capabilities.')
print(f'{low_effort_count} prompts can be built immediately with just orchestration logic.')
print(f'Tier 1 Universal tasks ({tier1_count} tasks) are the foundation - used {tier1_usage} times.')
print()
print('🎯 RECOMMENDATION: Implement Tier 3 missing tasks to achieve 100% coverage.')
print('=' * 80)
