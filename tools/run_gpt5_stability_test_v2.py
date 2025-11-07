#!/usr/bin/env python3
"""
GPT-5 Execution Composition Stability Test V2.0

Run GPT-5 analysis 3 times with optimized V2.0 prompts (25 canonical tasks) to:
1. Verify V2.0 framework improvements (new CAN-25: Event Annotation/Flagging)
2. Measure stability/variance across runs
3. Compute average performance metrics
4. Identify non-deterministic behavior patterns
5. Compare V2.0 (25 tasks) vs V1.0 (24 tasks) performance

This ensures our GPT-5 V2.0 evaluation is robust and reproducible.

Version: 2.0 (Updated November 7, 2025)
Changes: Added CAN-25, renumbered tasks 1-25, optimized prompt instructions
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tools.gpt5_execution_composer_v2 import GPT5ExecutionComposerV2
except ImportError:
    try:
        from gpt5_execution_composer_v2 import GPT5ExecutionComposerV2
    except ImportError:
        print("ERROR: Could not import GPT5ExecutionComposerV2")
        print("Make sure tools/gpt5_execution_composer_v2.py is available")
        sys.exit(1)


# EXACT same 9 hero prompts for fair comparison (V2 versions)
HERO_PROMPTS_V2 = [
    {
        "id": "Organizer-1",
        "category": "organizer",
        "prompt": "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy."
    },
    {
        "id": "Organizer-2",
        "category": "organizer",
        "prompt": "I have some important meetings coming up. Help me track all my important meetings this week and flag any that require focus time to prepare for them."
    },
    {
        "id": "Organizre-3",
        "category": "organizer",
        "prompt": "Help me understand where I am spending my time across different types of meetings and suggest ways I might reclaim time for my top priorities."
    },
    {
        "id": "Schedule-1",
        "category": "schedule",
        "prompt": "Set up a weekly 30-minute 1:1 with {name}. I'd prefer afternoons and want to avoid Fridays. Automatically reschedule on declines or conflicts."
    },
    {
        "id": "Schedule-2",
        "category": "schedule",
        "prompt": "I need to clear my schedule for Thursday afternoon to focus on our product review. Help me reschedule or decline those meetings so I have dedicated time to prepare."
    },
    {
        "id": "Schedule-3",
        "category": "schedule",
        "prompt": "Find a time in the next two weeks for a 1 hour meeting with Chris, Sangya, and Kat. We need to work around Kat's schedule since she's traveling. Make the meeting in person and add a room."
    },
    {
        "id": "Collaborate-1",
        "category": "collaborate",
        "prompt": "Help me set the agenda to review the progress of Project Alpha. I want to get confirmation we are on track and discuss any blocking issues or risks."
    },
    {
        "id": "Collaborate-2",
        "category": "collaborate",
        "prompt": "I have a meeting with senior leadership tomorrow. Find the most recent meeting with them and summarize the topics into 3 discussion points. Generate any objections or concerns that might come up and give me effective responses."
    },
    {
        "id": "Collaborate-3",
        "category": "collaborate",
        "prompt": "Prepare me for my meeting with our customer Beta tomorrow. Include a background on their company, create a dossier of who will attend and include their interests so I can have better conversations."
    }
]


def run_single_trial(
    trial_num: int, 
    composer: GPT5ExecutionComposerV2,
    output_dir: Path,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Run a single trial of GPT-5 V2.0 analysis on all 9 prompts.
    
    Args:
        trial_num: Trial number (1, 2, or 3)
        composer: GPT-5 composer V2.0 instance
        output_dir: Directory to save results
        verbose: Show progress
        
    Returns:
        Trial results dictionary
    """
    print("\n" + "=" * 80)
    print(f"TRIAL {trial_num}/3 - GPT-5 EXECUTION COMPOSITION V2.0")
    print("=" * 80)
    print(f"Analyzing {len(HERO_PROMPTS_V2)} hero prompts with OPTIMIZED V2.0 prompts (25 tasks)\n")
    
    all_compositions = []
    successful = 0
    failed = 0
    
    for i, hero in enumerate(HERO_PROMPTS_V2, 1):
        if verbose:
            print(f"\n[Trial {trial_num}] Prompt {i}/{len(HERO_PROMPTS_V2)}: {hero['id']}")
            print(f"  {hero['prompt'][:80]}...")
        
        try:
            composition = composer.compose_execution_plan(
                prompt=hero['prompt'],
                prompt_id=hero['id']
            )
            
            composition['category'] = hero['category']
            composition['trial'] = trial_num
            
            if composition.get('error'):
                print(f"  ❌ Error: {composition['error']}")
                failed += 1
            else:
                task_count = len(composition.get('tasks_covered', []))
                print(f"  ✅ Success! Used {task_count}/25 tasks")
                print(f"     Tasks: {', '.join(composition.get('tasks_covered', []))}")
                successful += 1
            
            all_compositions.append(composition)
            
        except Exception as e:
            print(f"  ❌ Exception: {e}")
            failed += 1
            all_compositions.append({
                "source": "gpt-5",
                "prompt_id": hero['id'],
                "prompt_text": hero['prompt'],
                "category": hero['category'],
                "trial": trial_num,
                "framework_version": "2.0",
                "error": str(e),
                "execution_plan": [],
                "tasks_covered": []
            })
        
        # Brief pause between API calls
        if i < len(HERO_PROMPTS_V2):
            time.sleep(1)
    
    # Save trial results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    trial_file = output_dir / f"gpt5_v2_trial{trial_num}_{timestamp}.json"
    
    trial_results = {
        "metadata": {
            "trial": trial_num,
            "source": "gpt-5",
            "model": "dev-gpt-5-chat-jj",
            "model_name": "GPT-5",
            "framework_version": "2.0",
            "timestamp": timestamp,
            "total_prompts": len(HERO_PROMPTS_V2),
            "successful": successful,
            "failed": failed,
            "canonical_tasks_version": "2.0",
            "total_canonical_tasks": 25,
            "new_in_v2": "CAN-25: Event Annotation/Flagging",
            "prompt_optimization": "Optimized V2.0 November 7, 2025 - Added CAN-25, renumbered 1-25, enhanced flagging guidance"
        },
        "compositions": all_compositions
    }
    
    with open(trial_file, 'w', encoding='utf-8') as f:
        json.dump(trial_results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Trial {trial_num} complete: {successful}/{len(HERO_PROMPTS_V2)} successful")
    print(f"💾 Saved to: {trial_file}")
    
    return trial_results


def analyze_stability(trials: List[Dict[str, Any]], output_dir: Path) -> Dict[str, Any]:
    """
    Analyze stability across 3 V2.0 trials.
    
    Args:
        trials: List of 3 trial result dictionaries
        output_dir: Directory to save analysis
        
    Returns:
        Stability analysis dictionary
    """
    print("\n" + "=" * 80)
    print("STABILITY ANALYSIS V2.0 - 3 TRIALS (25 CANONICAL TASKS)")
    print("=" * 80)
    
    # Collect per-prompt task selections
    prompt_tasks = defaultdict(list)  # prompt_id -> [trial1_tasks, trial2_tasks, trial3_tasks]
    
    for trial in trials:
        for comp in trial['compositions']:
            if not comp.get('error'):
                prompt_id = comp['prompt_id']
                tasks = set(comp.get('tasks_covered', []))
                prompt_tasks[prompt_id].append(tasks)
    
    # Compute stability metrics
    stability_analysis = {
        "framework_version": "2.0",
        "total_canonical_tasks": 25,
        "new_in_v2": "CAN-25: Event Annotation/Flagging",
        "per_prompt": {},
        "aggregate": {
            "total_prompts": len(HERO_PROMPTS_V2),
            "trials": len(trials),
            "average_task_count": [],
            "task_variance": [],
            "can25_detection": {
                "description": "CAN-25 (Event Annotation/Flagging) detection rate - NEW in V2.0",
                "prompts_using_can25": []
            }
        }
    }
    
    print("\nPER-PROMPT STABILITY:")
    print("-" * 80)
    
    can25_usage = []
    
    for prompt_id in sorted(prompt_tasks.keys()):
        task_sets = prompt_tasks[prompt_id]
        
        if len(task_sets) != 3:
            print(f"⚠️  {prompt_id}: Only {len(task_sets)}/3 trials successful")
            continue
        
        # Compute intersection (always present) and union (ever present)
        intersection = task_sets[0].intersection(task_sets[1]).intersection(task_sets[2])
        union = task_sets[0].union(task_sets[1]).union(task_sets[2])
        
        # Compute per-trial task counts
        task_counts = [len(ts) for ts in task_sets]
        avg_count = sum(task_counts) / len(task_counts)
        variance = sum((c - avg_count) ** 2 for c in task_counts) / len(task_counts)
        std_dev = variance ** 0.5
        
        # Tasks that vary (in union but not in intersection)
        varying_tasks = union - intersection
        
        # Consistency percentage
        consistency_pct = (len(intersection) / len(union) * 100) if union else 100
        
        # Check CAN-25 usage (NEW in V2.0)
        can25_in_trials = sum(1 for ts in task_sets if "CAN-25" in ts)
        if can25_in_trials > 0:
            can25_usage.append({
                "prompt_id": prompt_id,
                "trials_detected": can25_in_trials,
                "consistency": f"{can25_in_trials}/3"
            })
        
        stability_analysis["per_prompt"][prompt_id] = {
            "always_selected": sorted(list(intersection)),
            "sometimes_selected": sorted(list(varying_tasks)),
            "total_unique_tasks": len(union),
            "consistency_percentage": round(consistency_pct, 2),
            "average_task_count": round(avg_count, 2),
            "task_count_variance": round(variance, 4),
            "task_count_std_dev": round(std_dev, 4),
            "can25_usage": {
                "detected": can25_in_trials > 0,
                "trials_with_can25": can25_in_trials,
                "consistency": f"{can25_in_trials}/3"
            }
        }
        
        print(f"\n{prompt_id}:")
        print(f"  Always selected ({len(intersection)} tasks): {', '.join(sorted(intersection))}")
        if varying_tasks:
            print(f"  Sometimes selected ({len(varying_tasks)} tasks): {', '.join(sorted(varying_tasks))}")
        print(f"  Consistency: {consistency_pct:.1f}%")
        print(f"  Avg tasks: {avg_count:.1f} ± {std_dev:.2f}")
        if can25_in_trials > 0:
            print(f"  🆕 CAN-25 detected: {can25_in_trials}/3 trials")
    
    # Aggregate CAN-25 statistics
    stability_analysis["aggregate"]["can25_detection"]["prompts_using_can25"] = can25_usage
    stability_analysis["aggregate"]["can25_detection"]["total_prompts_with_can25"] = len(can25_usage)
    stability_analysis["aggregate"]["can25_detection"]["percentage"] = round(
        len(can25_usage) / len(HERO_PROMPTS_V2) * 100, 2
    ) if HERO_PROMPTS_V2 else 0
    
    # Overall statistics
    all_avg_counts = [data["average_task_count"] for data in stability_analysis["per_prompt"].values()]
    all_variances = [data["task_count_variance"] for data in stability_analysis["per_prompt"].values()]
    
    stability_analysis["aggregate"]["average_task_count"] = round(
        sum(all_avg_counts) / len(all_avg_counts), 2
    ) if all_avg_counts else 0
    
    stability_analysis["aggregate"]["average_variance"] = round(
        sum(all_variances) / len(all_variances), 4
    ) if all_variances else 0
    
    stability_analysis["aggregate"]["overall_consistency_percentage"] = round(
        sum(data["consistency_percentage"] for data in stability_analysis["per_prompt"].values()) / 
        len(stability_analysis["per_prompt"]), 2
    ) if stability_analysis["per_prompt"] else 0
    
    print("\n" + "=" * 80)
    print("AGGREGATE STATISTICS V2.0")
    print("=" * 80)
    print(f"Average task count: {stability_analysis['aggregate']['average_task_count']:.2f}")
    print(f"Average variance: {stability_analysis['aggregate']['average_variance']:.4f}")
    print(f"Overall consistency: {stability_analysis['aggregate']['overall_consistency_percentage']:.2f}%")
    print(f"\n🆕 CAN-25 Detection:")
    print(f"   Prompts using CAN-25: {len(can25_usage)}/{len(HERO_PROMPTS_V2)} ({stability_analysis['aggregate']['can25_detection']['percentage']:.1f}%)")
    if can25_usage:
        for usage in can25_usage:
            print(f"   - {usage['prompt_id']}: {usage['consistency']}")
    
    # Save stability analysis
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    analysis_file = output_dir / f"gpt5_v2_stability_analysis_{timestamp}.json"
    
    with open(analysis_file, 'w', encoding='utf-8') as f:
        json.dump(stability_analysis, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Stability analysis saved to: {analysis_file}")
    
    return stability_analysis


def main():
    """Run 3-trial stability test for GPT-5 V2.0"""
    print("=" * 80)
    print("GPT-5 EXECUTION COMPOSITION STABILITY TEST V2.0")
    print("=" * 80)
    print(f"Framework: 25 Canonical Tasks V2.0")
    print(f"New in V2.0: CAN-25 (Event Annotation/Flagging)")
    print(f"Trials: 3")
    print(f"Prompts per trial: {len(HERO_PROMPTS_V2)}")
    print(f"Total API calls: {3 * len(HERO_PROMPTS_V2)}")
    print("=" * 80)
    
    # Create output directory
    output_dir = Path("docs/gutt_analysis/model_comparison/gpt5_stability_v2")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"\nOutput directory: {output_dir}")
    
    # Initialize GPT-5 Composer V2.0
    print("\nInitializing GPT-5 Execution Composer V2.0...")
    composer = GPT5ExecutionComposerV2()
    
    # Run 3 trials
    trials = []
    for trial_num in range(1, 4):
        trial_results = run_single_trial(
            trial_num=trial_num,
            composer=composer,
            output_dir=output_dir,
            verbose=True
        )
        trials.append(trial_results)
        
        # Brief pause between trials
        if trial_num < 3:
            print(f"\nPausing 3 seconds before trial {trial_num + 1}...")
            time.sleep(3)
    
    # Analyze stability
    stability_analysis = analyze_stability(trials, output_dir)
    
    print("\n" + "=" * 80)
    print("✅ STABILITY TEST V2.0 COMPLETE")
    print("=" * 80)
    print(f"Total trials: 3")
    print(f"Total API calls: {3 * len(HERO_PROMPTS_V2)}")
    print(f"Results saved to: {output_dir}")
    print(f"\nNext step: Run `python tools/compute_gpt5_average_v2.py` to compute average performance")


if __name__ == "__main__":
    main()
