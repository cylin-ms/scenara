#!/usr/bin/env python3
"""
Batch GUTT Analysis for All 9 Hero Prompts

Runs Ollama GUTT decomposition on each of the 9 Calendar.AI hero prompts
and saves results in a structured format for comparison.
"""

import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Hero prompts from Calendar.AI evaluation framework
HERO_PROMPTS = [
    {
        "id": "organizer-1",
        "name": "Calendar Prioritization",
        "prompt": "Keep my Calendar up to date by committing to only meetings that are part of my priorities.",
        "reference_gutts": 6
    },
    {
        "id": "organizer-2",
        "name": "Meeting Prep Tracking",
        "prompt": "Track all my important meetings and flag any that require focus time to prepare for them.",
        "reference_gutts": 7
    },
    {
        "id": "organizer-3",
        "name": "Time Reclamation Analysis",
        "prompt": "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities.",
        "reference_gutts": 8
    },
    {
        "id": "schedule-1",
        "name": "Recurring 1:1 Scheduling",
        "prompt": "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts.",
        "reference_gutts": 7
    },
    {
        "id": "schedule-2",
        "name": "Block Time & Reschedule",
        "prompt": "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}.",
        "reference_gutts": 8
    },
    {
        "id": "schedule-3",
        "name": "Multi-Person Meeting Scheduling",
        "prompt": "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room.",
        "reference_gutts": 9
    },
    {
        "id": "collaborate-1",
        "name": "Agenda Creation",
        "prompt": "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks.",
        "reference_gutts": 6
    },
    {
        "id": "collaborate-2",
        "name": "Executive Briefing Prep",
        "prompt": "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses.",
        "reference_gutts": 7
    },
    {
        "id": "collaborate-3",
        "name": "Customer Meeting Prep",
        "prompt": "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company.",
        "reference_gutts": 8
    }
]


def run_ollama_analysis(prompt_data: dict, output_dir: Path, model: str = "gpt-oss:20b") -> dict:
    """
    Run Ollama GUTT analysis on a single prompt
    
    Args:
        prompt_data: Prompt information dictionary
        output_dir: Directory to save results
        model: Ollama model to use
        
    Returns:
        Result summary dictionary
    """
    prompt_id = prompt_data['id']
    prompt_text = prompt_data['prompt']
    
    output_file = output_dir / f"ollama_gutt_{prompt_id}.json"
    
    print(f"\n{'=' * 80}")
    print(f"🎯 Analyzing: {prompt_data['name']} ({prompt_id})")
    print(f"   Reference GUTTs: {prompt_data['reference_gutts']}")
    print(f"{'=' * 80}")
    
    # Run ollama_gutt_analyzer.py
    cmd = [
        "python",
        "tools/ollama_gutt_analyzer.py",
        prompt_text,
        "--model", model,
        "--output", str(output_file),
        "--quiet"  # Suppress streaming to avoid output clutter
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            # Load the generated file
            with open(output_file, 'r', encoding='utf-8') as f:
                decomposition = json.load(f)
            
            ollama_gutts = len(decomposition.get('gutts', []))
            
            print(f"\n✅ Analysis complete:")
            print(f"   Ollama GUTTs: {ollama_gutts}")
            print(f"   Reference GUTTs: {prompt_data['reference_gutts']}")
            print(f"   Ratio: {ollama_gutts / prompt_data['reference_gutts']:.2f}x")
            
            return {
                'prompt_id': prompt_id,
                'success': True,
                'ollama_gutts': ollama_gutts,
                'reference_gutts': prompt_data['reference_gutts'],
                'output_file': str(output_file)
            }
        else:
            print(f"❌ Analysis failed:")
            print(f"   Error: {result.stderr}")
            
            return {
                'prompt_id': prompt_id,
                'success': False,
                'error': result.stderr
            }
    
    except subprocess.TimeoutExpired:
        print(f"❌ Analysis timed out (>300s)")
        return {
            'prompt_id': prompt_id,
            'success': False,
            'error': 'Timeout'
        }
    
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return {
            'prompt_id': prompt_id,
            'success': False,
            'error': str(e)
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch GUTT Analysis for Hero Prompts')
    parser.add_argument('--model', default='gpt-oss:20b',
                       help='Ollama model to use (default: gpt-oss:20b)')
    parser.add_argument('--output-dir', default='hero_prompt_analysis',
                       help='Output directory for results (default: hero_prompt_analysis)')
    parser.add_argument('--prompts', nargs='+', type=int,
                       help='Specific prompt indices to analyze (1-9)')
    
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    
    print(f"\n{'=' * 80}")
    print(f"📊 BATCH GUTT ANALYSIS - 9 HERO PROMPTS")
    print(f"{'=' * 80}")
    print(f"Model: {args.model}")
    print(f"Output Directory: {output_dir}")
    print(f"Total Prompts: {len(HERO_PROMPTS)}")
    
    # Filter prompts if specific indices provided
    prompts_to_analyze = HERO_PROMPTS
    if args.prompts:
        indices = [i - 1 for i in args.prompts if 1 <= i <= 9]
        prompts_to_analyze = [HERO_PROMPTS[i] for i in indices]
        print(f"Analyzing: {len(prompts_to_analyze)} selected prompts")
    
    # Run analysis on each prompt
    results = []
    for i, prompt_data in enumerate(prompts_to_analyze, 1):
        print(f"\n\n[{i}/{len(prompts_to_analyze)}]")
        result = run_ollama_analysis(prompt_data, output_dir, args.model)
        results.append(result)
    
    # Summary
    print(f"\n\n{'=' * 80}")
    print(f"📊 BATCH ANALYSIS SUMMARY")
    print(f"{'=' * 80}")
    
    successful = [r for r in results if r['success']]
    failed = [r for r in results if not r['success']]
    
    print(f"\n✅ Successful: {len(successful)}/{len(results)}")
    print(f"❌ Failed: {len(failed)}/{len(results)}")
    
    if successful:
        print(f"\n📈 GUTT Count Comparison:")
        print(f"{'Prompt ID':<20} {'Ollama':<10} {'Reference':<10} {'Ratio':<10}")
        print("-" * 50)
        
        total_ollama = 0
        total_reference = 0
        
        for r in successful:
            ratio = r['ollama_gutts'] / r['reference_gutts']
            print(f"{r['prompt_id']:<20} {r['ollama_gutts']:<10} {r['reference_gutts']:<10} {ratio:<10.2f}x")
            total_ollama += r['ollama_gutts']
            total_reference += r['reference_gutts']
        
        overall_ratio = total_ollama / total_reference if total_reference > 0 else 0
        print("-" * 50)
        print(f"{'TOTAL':<20} {total_ollama:<10} {total_reference:<10} {overall_ratio:<10.2f}x")
    
    if failed:
        print(f"\n❌ Failed Analyses:")
        for r in failed:
            print(f"   • {r['prompt_id']}: {r.get('error', 'Unknown error')}")
    
    # Save summary
    summary_file = output_dir / "batch_analysis_summary.json"
    summary = {
        'timestamp': datetime.now().isoformat(),
        'model': args.model,
        'total_prompts': len(results),
        'successful': len(successful),
        'failed': len(failed),
        'results': results
    }
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Summary saved to: {summary_file}")
    print(f"\n{'=' * 80}\n")
    
    return 0 if not failed else 1


if __name__ == '__main__':
    sys.exit(main())
