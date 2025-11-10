#!/usr/bin/env python3
"""
Batch Execution Composition Analysis

Run both GPT-5 and Claude Sonnet 4.5 on all 9 hero prompts,
then compare their performance against the gold standard.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List

# Hero prompts (same 9 prompts used in original analysis)
HERO_PROMPTS = [
    {
        "id": "organizer-1",
        "prompt": "Show me my pending invitations and which ones I should prioritize based on my priorities for this week: customer meetings and product strategy."
    },
    {
        "id": "organizer-2",
        "prompt": "I have some important meetings this week—flag the ones I need to prep for, and put time on my calendar to prepare."
    },
    {
        "id": "organizer-3",
        "prompt": "Show me patterns in the kinds of meetings that fill up my week, and suggest ways to reclaim some time."
    },
    {
        "id": "schedule-1",
        "prompt": "Land a weekly 30min 1:1 with Sarah for me, afternoons preferred, avoid Fridays. If her schedule changes, automatically find a new time."
    },
    {
        "id": "schedule-2",
        "prompt": "Bump all my meetings that can move to later in the week, I need to focus today and tomorrow."
    },
    {
        "id": "schedule-3",
        "prompt": "I have a weekly team-sync on Tuesdays at 2pm. My 1:1s with my manager take priority and can bump it. Book a room."
    },
    {
        "id": "collaborate-1",
        "prompt": "Prep an agenda for my next meeting with the Project Alpha team. Pull in updates from their work."
    },
    {
        "id": "collaborate-2",
        "prompt": "Before my 1:1 with Jordan, pull together a briefing on their open tasks, recent updates, and any blockers."
    },
    {
        "id": "collaborate-3",
        "prompt": "Create a doc summarizing who on my team is working on what this quarter, based on their calendar and recent activity."
    }
]


def run_batch_analysis():
    """Run batch analysis with both GPT-5 and Claude"""
    
    print("=" * 100)
    print("BATCH EXECUTION COMPOSITION ANALYSIS")
    print("=" * 100)
    print(f"\nAnalyzing {len(HERO_PROMPTS)} hero prompts with:")
    print("  1. GPT-5 (dev-gpt-5-chat-jj)")
    print("  2. Claude Sonnet 4.5 (claude-sonnet-4-20250514)")
    print("\nFramework: 24 Canonical Unit Tasks (V2.0)")
    print("=" * 100)
    
    # Import analyzers - add parent directory to path if needed
    import sys
    from pathlib import Path
    tools_dir = Path(__file__).parent
    if str(tools_dir.parent) not in sys.path:
        sys.path.insert(0, str(tools_dir.parent))
    
    try:
        from tools.gpt5_execution_composer import GPT5ExecutionComposer
    except ImportError:
        from gpt5_execution_composer import GPT5ExecutionComposer
    
    try:
        from tools.claude_execution_composer import ClaudeExecutionComposer
    except ImportError:
        from claude_execution_composer import ClaudeExecutionComposer
    
    # Initialize composers
    print("\n🔧 Initializing LLM composers...")
    gpt5_composer = GPT5ExecutionComposer()
    claude_composer = ClaudeExecutionComposer()
    
    # Prepare output structure
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "framework_version": "2.0",
            "total_prompts": len(HERO_PROMPTS),
            "canonical_tasks_count": 24,
            "models": [
                {"name": "GPT-5", "id": "dev-gpt-5-chat-jj"},
                {"name": "Claude Sonnet 4.5", "id": "claude-sonnet-4-20250514"}
            ]
        },
        "gpt5_analyses": {},
        "claude_analyses": {}
    }
    
    # Run GPT-5 analysis
    print("\n" + "=" * 100)
    print("PHASE 1: GPT-5 ANALYSIS")
    print("=" * 100)
    
    for i, hero in enumerate(HERO_PROMPTS, 1):
        print(f"\n[{i}/{len(HERO_PROMPTS)}] Analyzing: {hero['id']}")
        print(f"Prompt: {hero['prompt'][:80]}...")
        
        try:
            composition = gpt5_composer.compose_execution_plan(
                hero['prompt'],
                hero['id']
            )
            results['gpt5_analyses'][hero['id']] = composition
            
            tasks_count = len(composition.get('tasks_covered', []))
            steps_count = len(composition.get('execution_plan', []))
            print(f"✓ {tasks_count} tasks, {steps_count} steps")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results['gpt5_analyses'][hero['id']] = {
                "error": str(e),
                "prompt_id": hero['id'],
                "prompt_text": hero['prompt']
            }
    
    # Run Claude analysis
    print("\n" + "=" * 100)
    print("PHASE 2: CLAUDE SONNET 4.5 ANALYSIS")
    print("=" * 100)
    
    for i, hero in enumerate(HERO_PROMPTS, 1):
        print(f"\n[{i}/{len(HERO_PROMPTS)}] Analyzing: {hero['id']}")
        print(f"Prompt: {hero['prompt'][:80]}...")
        
        try:
            composition = claude_composer.compose_execution_plan(
                hero['prompt'],
                hero['id'],
                verbose=False
            )
            results['claude_analyses'][hero['id']] = composition
            
            tasks_count = len(composition.get('tasks_covered', []))
            steps_count = len(composition.get('execution_plan', []))
            print(f"✓ {tasks_count} tasks, {steps_count} steps")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results['claude_analyses'][hero['id']] = {
                "error": str(e),
                "prompt_id": hero['id'],
                "prompt_text": hero['prompt']
            }
    
    # Save results
    output_dir = Path("docs/gutt_analysis/model_comparison")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"batch_composition_analysis_{timestamp}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 100)
    print("ANALYSIS COMPLETE")
    print("=" * 100)
    print(f"\n💾 Results saved to: {output_file}")
    
    # Print summary
    print("\n" + "=" * 100)
    print("SUMMARY")
    print("=" * 100)
    
    gpt5_success = sum(1 for v in results['gpt5_analyses'].values() if 'error' not in v)
    claude_success = sum(1 for v in results['claude_analyses'].values() if 'error' not in v)
    
    print(f"\nGPT-5:          {gpt5_success}/{len(HERO_PROMPTS)} successful")
    print(f"Claude Sonnet:  {claude_success}/{len(HERO_PROMPTS)} successful")
    
    # Task usage statistics
    print("\n" + "-" * 100)
    print("TASK USAGE COMPARISON")
    print("-" * 100)
    
    gpt5_tasks = set()
    claude_tasks = set()
    
    for analysis in results['gpt5_analyses'].values():
        if 'tasks_covered' in analysis:
            gpt5_tasks.update(analysis['tasks_covered'])
    
    for analysis in results['claude_analyses'].values():
        if 'tasks_covered' in analysis:
            claude_tasks.update(analysis['tasks_covered'])
    
    print(f"\nGPT-5 unique tasks used:     {len(gpt5_tasks)}/24")
    print(f"Claude unique tasks used:    {len(claude_tasks)}/24")
    print(f"Tasks used by both:          {len(gpt5_tasks & claude_tasks)}")
    print(f"Tasks only in GPT-5:         {gpt5_tasks - claude_tasks}")
    print(f"Tasks only in Claude:        {claude_tasks - gpt5_tasks}")
    
    print("\n" + "=" * 100)
    print("NEXT STEP: Run comparative evaluation against gold standard")
    print("=" * 100)
    print("\nTo evaluate results:")
    print(f"  python tools/compare_against_gold_standard.py {output_file}")
    
    return output_file


if __name__ == "__main__":
    try:
        output_file = run_batch_analysis()
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
