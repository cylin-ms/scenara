#!/usr/bin/env python3
"""
GPT-5 Batch Execution Composition Analysis

Run GPT-5 on all 9 hero prompts to compose execution plans
from the 24 canonical unit tasks.
"""

import json
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools.gpt5_execution_composer import GPT5ExecutionComposer

# 9 Hero prompts
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


def main():
    print("=" * 100)
    print("GPT-5 BATCH EXECUTION COMPOSITION ANALYSIS")
    print("=" * 100)
    print(f"\nAnalyzing {len(HERO_PROMPTS)} hero prompts with GPT-5 (dev-gpt-5-chat-jj)")
    print("Framework: 24 Canonical Unit Tasks (V2.0)")
    print("=" * 100)
    
    # Initialize GPT-5 composer
    print("\n🔧 Initializing GPT-5 composer...")
    try:
        composer = GPT5ExecutionComposer()
        print("✓ GPT-5 composer initialized")
    except Exception as e:
        print(f"❌ Failed to initialize GPT-5 composer: {e}")
        return 1
    
    # Prepare results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results = {
        "metadata": {
            "analysis_date": datetime.now().isoformat(),
            "model": "dev-gpt-5-chat-jj",
            "framework_version": "2.0",
            "total_prompts": len(HERO_PROMPTS),
            "canonical_tasks_count": 24
        },
        "compositions": {}
    }
    
    # Run analysis
    print("\n" + "=" * 100)
    print("RUNNING GPT-5 ANALYSIS")
    print("=" * 100)
    
    for i, hero in enumerate(HERO_PROMPTS, 1):
        print(f"\n[{i}/{len(HERO_PROMPTS)}] {hero['id']}")
        print(f"Prompt: {hero['prompt'][:80]}...")
        print("-" * 100)
        
        try:
            composition = composer.compose_execution_plan(
                hero['prompt'],
                hero['id']
            )
            
            results['compositions'][hero['id']] = composition
            
            if 'error' in composition:
                print(f"❌ Error: {composition['error']}")
            else:
                tasks_count = len(composition.get('tasks_covered', []))
                steps_count = len(composition.get('execution_plan', []))
                print(f"✓ Composed: {tasks_count} tasks, {steps_count} steps")
                print(f"  Tasks: {', '.join(composition.get('tasks_covered', []))}")
            
            # Brief pause between requests
            if i < len(HERO_PROMPTS):
                time.sleep(1)
                
        except Exception as e:
            print(f"❌ Error: {e}")
            results['compositions'][hero['id']] = {
                "error": str(e),
                "prompt_id": hero['id'],
                "prompt_text": hero['prompt']
            }
    
    # Save results
    output_dir = Path("docs/gutt_analysis/model_comparison")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f"gpt5_compositions_{timestamp}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    # Summary
    print("\n" + "=" * 100)
    print("GPT-5 ANALYSIS COMPLETE")
    print("=" * 100)
    
    success_count = sum(1 for v in results['compositions'].values() if 'error' not in v)
    print(f"\n✓ Successful: {success_count}/{len(HERO_PROMPTS)}")
    print(f"💾 Saved to: {output_file}")
    
    # Task usage summary
    all_tasks = set()
    for comp in results['compositions'].values():
        if 'tasks_covered' in comp:
            all_tasks.update(comp['tasks_covered'])
    
    print(f"\n📊 Task Coverage:")
    print(f"  Unique tasks used: {len(all_tasks)}/24")
    print(f"  Tasks: {', '.join(sorted(all_tasks))}")
    
    print("\n" + "=" * 100)
    print("NEXT STEP: Compare against gold standard")
    print(f"  python tools/compare_gpt5_to_gold.py {output_file}")
    print("=" * 100)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
