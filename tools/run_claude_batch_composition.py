#!/usr/bin/env python3
"""
Run Claude Sonnet 4.5 Batch Execution Composition Analysis

Runs the EXACT SAME 9 hero prompts through Claude Sonnet 4.5 for fair comparison with GPT-5.

This uses the ANTHROPIC API directly (not SilverFlow, which only supports Microsoft models).
Requires ANTHROPIC_API_KEY environment variable.
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from tools.claude_execution_composer import ClaudeExecutionComposer
except ImportError:
    try:
        from claude_execution_composer import ClaudeExecutionComposer
    except ImportError:
        print("ERROR: Could not import ClaudeExecutionComposer")
        print("Make sure tools/claude_execution_composer.py is available")
        sys.exit(1)


# EXACT SAME 9 hero prompts as GPT-5 for fair comparison
HERO_PROMPTS = [
    {
        "id": "organizer-1",
        "category": "organizer",
        "prompt": "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy."
    },
    {
        "id": "organizer-2",
        "category": "organizer",
        "prompt": "I have some important meetings this week—flag the ones I need to prep for, and put time on my calendar to prepare."
    },
    {
        "id": "organizer-3",
        "category": "organizer",
        "prompt": "Show me how my meeting time is broken down this month and where I could reclaim time to focus on product development."
    },
    {
        "id": "schedule-1",
        "category": "schedule",
        "prompt": "Schedule my weekly 1:1 with Alex every Monday at 10am. If there's a conflict, auto-bump movable meetings."
    },
    {
        "id": "schedule-2",
        "category": "schedule",
        "prompt": "I need to focus this afternoon. Bump all movable meetings to tomorrow or later this week."
    },
    {
        "id": "schedule-3",
        "category": "schedule",
        "prompt": "Set up a team sync for next Tuesday at 2pm with Sarah, Mike, and the design team. Book the large conference room and prioritize this over non-customer meetings if there's a conflict."
    },
    {
        "id": "collaborate-1",
        "category": "collaborate",
        "prompt": "Pull together a prep agenda for my customer pitch on Friday, including recent work updates from the team."
    },
    {
        "id": "collaborate-2",
        "category": "collaborate",
        "prompt": "Pull a briefing doc for my 1:1 with Jamie tomorrow, including what we've been working on."
    },
    {
        "id": "collaborate-3",
        "category": "collaborate",
        "prompt": "Create a summary of all team meetings this quarter and what we accomplished."
    }
]


def run_batch_analysis(output_dir: str = "docs/gutt_analysis/model_comparison", verbose: bool = True):
    """
    Run Claude analysis on all 9 hero prompts for fair comparison with GPT-5.
    
    Args:
        output_dir: Directory to save results
        verbose: Show progress
    """
    
    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("\nPlease set your Anthropic API key:")
        print("  Windows (PowerShell): $env:ANTHROPIC_API_KEY='your-key-here'")
        print("  Linux/Mac: export ANTHROPIC_API_KEY='your-key-here'")
        print("\nGet your API key from: https://console.anthropic.com/")
        return False
    
    # Initialize composer
    print("=" * 80)
    print("CLAUDE SONNET 4.5 BATCH EXECUTION COMPOSITION ANALYSIS")
    print("=" * 80)
    print(f"\n📋 Analyzing {len(HERO_PROMPTS)} hero prompts")
    print("Model: claude-sonnet-4-20250514 (Claude Sonnet 4.5)")
    print(f"Output Directory: {output_dir}\n")
    
    try:
        composer = ClaudeExecutionComposer(model="claude-sonnet-4-20250514")
    except Exception as e:
        print(f"❌ Failed to initialize Claude composer: {e}")
        return False
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Results collection
    all_compositions = []
    successful = 0
    failed = 0
    
    # Process each prompt
    for i, hero in enumerate(HERO_PROMPTS, 1):
        print("\n" + "=" * 80)
        print(f"PROMPT {i}/{len(HERO_PROMPTS)}: {hero['id']} ({hero['category']})")
        print("=" * 80)
        print(f"Prompt: {hero['prompt']}\n")
        
        try:
            # Compose execution plan
            composition = composer.compose_execution_plan(
                prompt=hero['prompt'],
                prompt_id=hero['id'],
                verbose=verbose
            )
            
            # Add category metadata
            composition['category'] = hero['category']
            
            # Check for errors
            if composition.get('error'):
                print(f"⚠️  Composition failed: {composition['error']}")
                failed += 1
            else:
                task_count = len(composition.get('tasks_covered', []))
                print(f"✅ Success! Used {task_count}/24 canonical tasks")
                print(f"   Tasks: {', '.join(composition.get('tasks_covered', []))}")
                successful += 1
            
            all_compositions.append(composition)
            
        except Exception as e:
            print(f"❌ Error processing {hero['id']}: {e}")
            failed += 1
            all_compositions.append({
                "source": "claude",
                "prompt_id": hero['id'],
                "prompt_text": hero['prompt'],
                "category": hero['category'],
                "error": str(e),
                "execution_plan": [],
                "tasks_covered": []
            })
        
        # Brief pause between API calls
        if i < len(HERO_PROMPTS):
            import time
            time.sleep(1)
    
    # Save batch results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    batch_file = output_path / f"claude_compositions_{timestamp}.json"
    
    batch_results = {
        "metadata": {
            "source": "claude",
            "model": "claude-sonnet-4-20250514",
            "model_name": "Claude Sonnet 4.5",
            "timestamp": timestamp,
            "total_prompts": len(HERO_PROMPTS),
            "successful": successful,
            "failed": failed,
            "canonical_tasks_version": "2.0",
            "total_canonical_tasks": 24
        },
        "compositions": all_compositions
    }
    
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(batch_results, f, indent=2, ensure_ascii=False)
    
    # Print summary
    print("\n" + "=" * 80)
    print("BATCH ANALYSIS COMPLETE")
    print("=" * 80)
    print(f"✅ Successful: {successful}/{len(HERO_PROMPTS)}")
    print(f"❌ Failed: {failed}/{len(HERO_PROMPTS)}")
    print(f"\n💾 Results saved to: {batch_file}")
    
    # Calculate aggregate statistics
    if successful > 0:
        all_tasks_used = set()
        task_frequency = {}
        
        for comp in all_compositions:
            if not comp.get('error'):
                for task_id in comp.get('tasks_covered', []):
                    all_tasks_used.add(task_id)
                    task_frequency[task_id] = task_frequency.get(task_id, 0) + 1
        
        print(f"\n📊 Aggregate Statistics:")
        print(f"   Unique tasks used: {len(all_tasks_used)}/24")
        print(f"   Tasks used: {', '.join(sorted(all_tasks_used))}")
        
        if task_frequency:
            print(f"\n🔥 Most frequent tasks:")
            sorted_tasks = sorted(task_frequency.items(), key=lambda x: x[1], reverse=True)
            for task_id, count in sorted_tasks[:10]:
                pct = (count / successful) * 100
                print(f"   {task_id}: {count}/{successful} prompts ({pct:.1f}%)")
    
    print("\n" + "=" * 80)
    print("READY FOR COMPARISON")
    print("=" * 80)
    print(f"\nTo compare with gold standard, run:")
    print(f"  python tools/compare_to_gold.py {batch_file}")
    print(f"\nGold standard file: docs/gutt_analysis/model_comparison/gold_standard_analysis.json")
    print("\n" + "=" * 80)
    
    return successful == len(HERO_PROMPTS)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Run Claude Sonnet 4.5 batch execution composition analysis"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="docs/gutt_analysis/model_comparison",
        help="Directory to save results (default: docs/gutt_analysis/model_comparison)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress verbose output"
    )
    
    args = parser.parse_args()
    
    success = run_batch_analysis(
        output_dir=args.output_dir,
        verbose=not args.quiet
    )
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
