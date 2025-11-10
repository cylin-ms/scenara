#!/usr/bin/env python3
"""
AI-Powered Execution Composition Evaluator

Uses GitHub Copilot (Claude Sonnet 4.5) backend reasoning to evaluate 
GPT-5 and Claude execution compositions against gold standard.

This follows the lesson learned: "Use AI reasoning for semantic tasks"
instead of building complex similarity algorithms.
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


# Load the gold standard and batch analysis results
def load_analysis_files():
    """Load gold standard and any existing batch analysis"""
    gold_path = Path("docs/gutt_analysis/gold_standard_analysis.json")
    
    if not gold_path.exists():
        print(f"❌ Gold standard not found at {gold_path}")
        sys.exit(1)
    
    with open(gold_path, 'r', encoding='utf-8') as f:
        gold_standard = json.load(f)
    
    print(f"✓ Loaded gold standard: {len(gold_standard['prompt_analyses'])} prompts")
    return gold_standard


def main():
    print("=" * 100)
    print("AI-POWERED EXECUTION COMPOSITION EVALUATION")
    print("Using GitHub Copilot (Claude Sonnet 4.5) Backend Reasoning")
    print("=" * 100)
    
    gold_standard = load_analysis_files()
    
    print("\n📊 Gold Standard Summary:")
    print(f"  Total Prompts: {gold_standard['metadata']['total_prompts']}")
    print(f"  Canonical Tasks: {gold_standard['canonical_tasks_library']['total_tasks']}")
    print(f"  Framework Version: {gold_standard['metadata']['version']}")
    
    # Show task coverage from gold standard
    print("\n📋 Task Coverage in Gold Standard:")
    task_usage = {}
    for prompt_id, analysis in gold_standard['prompt_analyses'].items():
        for task in analysis['tasks_covered']:
            if task not in task_usage:
                task_usage[task] = []
            task_usage[task].append(prompt_id)
    
    sorted_tasks = sorted(task_usage.items(), key=lambda x: len(x[1]), reverse=True)
    for task, prompts in sorted_tasks[:10]:  # Top 10
        freq = len(prompts)
        pct = (freq / gold_standard['metadata']['total_prompts']) * 100
        print(f"  {task}: {freq}/9 ({pct:.0f}%) - {', '.join(prompts[:3])}{' ...' if len(prompts) > 3 else ''}")
    
    print("\n" + "=" * 100)
    print("📝 READY FOR AI-POWERED EVALUATION")
    print("=" * 100)
    print("\nGitHub Copilot can now use its backend AI reasoning to:")
    print("  1. Analyze execution composition quality")
    print("  2. Identify gaps and systematic patterns")
    print("  3. Compare model performance")
    print("  4. Generate insights without external API calls")
    print("\nThis follows the lesson: 'Use AI reasoning for semantic tasks'")
    print("=" * 100)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
