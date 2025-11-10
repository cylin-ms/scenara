#!/usr/bin/env python3
"""
Master Orchestration Script: LLM Performance Evaluation

Complete workflow:
1. Run batch composition analysis with GPT-5 and Claude Sonnet 4.5
2. Compare results against gold standard
3. Generate evaluation report
4. Identify performance gaps

Usage:
    python tools/run_complete_evaluation.py
"""

import sys
import subprocess
from pathlib import Path
from datetime import datetime


def run_command(cmd: list, description: str) -> tuple:
    """Run a command and return success status"""
    print(f"\n{'='*100}")
    print(f"{description}")
    print(f"{'='*100}")
    print(f"Command: {' '.join(cmd)}\n")
    
    result = subprocess.run(cmd, capture_output=False, text=True)
    return result.returncode == 0, result


def main():
    print("="*100)
    print("LLM EXECUTION COMPOSITION EVALUATION - COMPLETE WORKFLOW")
    print("="*100)
    print("\nFramework: 24 Canonical Unit Tasks (V2.0)")
    print("Models: GPT-5 vs Claude Sonnet 4.5")
    print("Prompts: 9 hero prompts (organizer + schedule + collaborate)")
    print("\nWorkflow:")
    print("  1. Run batch composition analysis (GPT-5 + Claude)")
    print("  2. Compare against gold standard")
    print("  3. Generate evaluation report")
    print("  4. Identify performance gaps")
    print("="*100)
    
    # Confirm
    response = input("\nProceed with evaluation? (y/n): ")
    if response.lower() != 'y':
        print("Aborted.")
        return 1
    
    # Step 1: Run batch composition analysis
    success, result = run_command(
        ["python", "tools/run_batch_composition_analysis.py"],
        "STEP 1: Running Batch Composition Analysis"
    )
    
    if not success:
        print("\n❌ Batch analysis failed!")
        return 1
    
    # Find the generated batch analysis file
    batch_dir = Path("docs/gutt_analysis/model_comparison")
    batch_files = sorted(batch_dir.glob("batch_composition_analysis_*.json"))
    
    if not batch_files:
        print("\n❌ No batch analysis file found!")
        return 1
    
    batch_file = batch_files[-1]  # Most recent
    print(f"\n✓ Batch analysis complete: {batch_file}")
    
    # Step 2: Compare against gold standard
    success, result = run_command(
        [
            "python", "tools/compare_against_gold_standard.py",
            str(batch_file),
            "--gold-standard", "docs/gutt_analysis/gold_standard_analysis.json"
        ],
        "STEP 2: Comparing Against Gold Standard"
    )
    
    if not success:
        print("\n❌ Comparison failed!")
        return 1
    
    # Find the evaluation results file
    eval_files = sorted(batch_dir.glob("evaluation_results_*.json"))
    
    if not eval_files:
        print("\n❌ No evaluation results file found!")
        return 1
    
    eval_file = eval_files[-1]  # Most recent
    print(f"\n✓ Evaluation complete: {eval_file}")
    
    # Step 3: Generate summary report
    print("\n" + "="*100)
    print("STEP 3: Generating Summary Report")
    print("="*100)
    
    # Read evaluation results
    import json
    with open(eval_file, 'r', encoding='utf-8') as f:
        eval_data = json.load(f)
    
    # Print summary
    print("\n" + "="*100)
    print("EVALUATION SUMMARY")
    print("="*100)
    
    gpt5_scores = eval_data['gpt5_evaluation']['aggregate_scores']
    claude_scores = eval_data['claude_evaluation']['aggregate_scores']
    comparison = eval_data['model_comparison']
    
    print(f"\n🤖 GPT-5 Performance:")
    print(f"   Precision: {gpt5_scores['average_precision']:.2%}")
    print(f"   Recall:    {gpt5_scores['average_recall']:.2%}")
    print(f"   F1 Score:  {gpt5_scores['average_f1']:.2%}")
    
    print(f"\n🤖 Claude Sonnet 4.5 Performance:")
    print(f"   Precision: {claude_scores['average_precision']:.2%}")
    print(f"   Recall:    {claude_scores['average_recall']:.2%}")
    print(f"   F1 Score:  {claude_scores['average_f1']:.2%}")
    
    print(f"\n🏆 Winner: {comparison['winner']}")
    print(f"   F1 Difference: {comparison['difference']:.2%}")
    
    print(f"\n📊 Per-Prompt Breakdown:")
    print(f"   GPT-5 wins:    {len(comparison['prompts_where_gpt5_better'])} prompts")
    print(f"   Claude wins:   {len(comparison['prompts_where_claude_better'])} prompts")
    print(f"   Tied:          {len(comparison['prompts_tied'])} prompts")
    
    if eval_data['systematic_gaps']:
        print(f"\n⚠️  Systematic Gaps Identified: {len(eval_data['systematic_gaps'])}")
        for gap in eval_data['systematic_gaps']:
            print(f"   • {gap['type']}: {gap['description']}")
    
    print("\n" + "="*100)
    print("COMPLETE EVALUATION FINISHED")
    print("="*100)
    print(f"\n📁 Output Files:")
    print(f"   Batch Analysis:     {batch_file}")
    print(f"   Evaluation Results: {eval_file}")
    
    print("\n💡 Next Steps:")
    print("   1. Review evaluation results JSON for detailed breakdown")
    print("   2. Analyze systematic gaps to improve prompting strategies")
    print("   3. Consider fine-tuning based on identified weaknesses")
    print("   4. Update gold standard if needed based on insights")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
