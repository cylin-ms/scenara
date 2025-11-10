#!/usr/bin/env python3
"""
Compare LLM Performance Against Gold Standard

Evaluate GPT-5 and Claude Sonnet 4.5 execution compositions
against the validated gold standard analysis.

Metrics:
- Task coverage accuracy (which tasks were selected)
- Task sequencing correctness (order of tasks)
- Completeness (missing critical tasks)
- Over-selection (unnecessary tasks)
- Dependency handling (CAN-07 parent task, CAN-01 → CAN-06, etc.)
"""

import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any
from datetime import datetime


class CompositionEvaluator:
    """Evaluate execution compositions against gold standard"""
    
    def __init__(self, gold_standard_path: str):
        """Load gold standard analysis"""
        with open(gold_standard_path, 'r', encoding='utf-8') as f:
            self.gold_standard = json.load(f)
        
        print(f"✓ Loaded gold standard from {gold_standard_path}")
        print(f"  Total prompts: {self.gold_standard['metadata']['total_prompts']}")
    
    def evaluate_model(self, model_name: str, model_analyses: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a model's performance against gold standard
        
        Args:
            model_name: "GPT-5" or "Claude Sonnet 4.5"
            model_analyses: Dictionary of prompt_id -> composition
            
        Returns:
            Evaluation results with scores and detailed comparison
        """
        print(f"\n{'='*100}")
        print(f"EVALUATING: {model_name}")
        print(f"{'='*100}")
        
        results = {
            "model_name": model_name,
            "total_prompts": len(model_analyses),
            "per_prompt_scores": {},
            "aggregate_scores": {},
            "gaps_identified": []
        }
        
        # Evaluate each prompt
        precision_scores = []
        recall_scores = []
        f1_scores = []
        
        for prompt_id, analysis in model_analyses.items():
            if 'error' in analysis:
                print(f"\n❌ {prompt_id}: Error in analysis - {analysis['error']}")
                continue
            
            # Get gold standard for this prompt
            if prompt_id not in self.gold_standard['prompt_analyses']:
                print(f"\n⚠️  {prompt_id}: Not in gold standard")
                continue
            
            gold = self.gold_standard['prompt_analyses'][prompt_id]
            
            # Evaluate task coverage
            score = self._evaluate_task_coverage(prompt_id, analysis, gold)
            results['per_prompt_scores'][prompt_id] = score
            
            precision_scores.append(score['precision'])
            recall_scores.append(score['recall'])
            f1_scores.append(score['f1'])
            
            # Print summary
            status = "✓" if score['f1'] >= 0.8 else "⚠️" if score['f1'] >= 0.6 else "❌"
            print(f"\n{status} {prompt_id}:")
            print(f"   Precision: {score['precision']:.2%} | Recall: {score['recall']:.2%} | F1: {score['f1']:.2%}")
            if score['missing_tasks']:
                print(f"   Missing: {', '.join(score['missing_tasks'])}")
            if score['extra_tasks']:
                print(f"   Extra: {', '.join(score['extra_tasks'])}")
        
        # Aggregate scores
        results['aggregate_scores'] = {
            "average_precision": sum(precision_scores) / len(precision_scores) if precision_scores else 0,
            "average_recall": sum(recall_scores) / len(recall_scores) if recall_scores else 0,
            "average_f1": sum(f1_scores) / len(f1_scores) if f1_scores else 0,
            "prompts_evaluated": len(precision_scores)
        }
        
        print(f"\n{'─'*100}")
        print(f"AGGREGATE SCORES FOR {model_name}:")
        print(f"  Average Precision: {results['aggregate_scores']['average_precision']:.2%}")
        print(f"  Average Recall:    {results['aggregate_scores']['average_recall']:.2%}")
        print(f"  Average F1:        {results['aggregate_scores']['average_f1']:.2%}")
        
        return results
    
    def _evaluate_task_coverage(self, prompt_id: str, analysis: Dict, gold: Dict) -> Dict[str, Any]:
        """Evaluate task coverage for a single prompt"""
        
        # Extract task sets
        predicted_tasks = set(analysis.get('tasks_covered', []))
        gold_tasks = set(gold.get('tasks_covered', []))
        
        # Calculate metrics
        true_positives = predicted_tasks & gold_tasks
        false_positives = predicted_tasks - gold_tasks
        false_negatives = gold_tasks - predicted_tasks
        
        precision = len(true_positives) / len(predicted_tasks) if predicted_tasks else 0
        recall = len(true_positives) / len(gold_tasks) if gold_tasks else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        return {
            "prompt_id": prompt_id,
            "predicted_tasks": list(predicted_tasks),
            "gold_tasks": list(gold_tasks),
            "correct_tasks": list(true_positives),
            "missing_tasks": list(false_negatives),
            "extra_tasks": list(false_positives),
            "precision": precision,
            "recall": recall,
            "f1": f1
        }
    
    def compare_models(self, gpt5_eval: Dict, claude_eval: Dict) -> Dict[str, Any]:
        """Compare GPT-5 vs Claude performance"""
        
        print(f"\n{'='*100}")
        print("MODEL COMPARISON")
        print(f"{'='*100}")
        
        comparison = {
            "gpt5_f1": gpt5_eval['aggregate_scores']['average_f1'],
            "claude_f1": claude_eval['aggregate_scores']['average_f1'],
            "difference": abs(gpt5_eval['aggregate_scores']['average_f1'] - claude_eval['aggregate_scores']['average_f1']),
            "winner": None,
            "prompts_where_gpt5_better": [],
            "prompts_where_claude_better": [],
            "prompts_tied": []
        }
        
        # Determine overall winner
        if gpt5_eval['aggregate_scores']['average_f1'] > claude_eval['aggregate_scores']['average_f1']:
            comparison['winner'] = "GPT-5"
        elif claude_eval['aggregate_scores']['average_f1'] > gpt5_eval['aggregate_scores']['average_f1']:
            comparison['winner'] = "Claude Sonnet 4.5"
        else:
            comparison['winner'] = "Tied"
        
        # Per-prompt comparison
        common_prompts = set(gpt5_eval['per_prompt_scores'].keys()) & set(claude_eval['per_prompt_scores'].keys())
        
        for prompt_id in common_prompts:
            gpt5_f1 = gpt5_eval['per_prompt_scores'][prompt_id]['f1']
            claude_f1 = claude_eval['per_prompt_scores'][prompt_id]['f1']
            
            if gpt5_f1 > claude_f1 + 0.01:
                comparison['prompts_where_gpt5_better'].append(prompt_id)
            elif claude_f1 > gpt5_f1 + 0.01:
                comparison['prompts_where_claude_better'].append(prompt_id)
            else:
                comparison['prompts_tied'].append(prompt_id)
        
        # Print comparison
        print(f"\n🏆 Winner: {comparison['winner']}")
        print(f"\nOverall F1 Scores:")
        print(f"  GPT-5:          {comparison['gpt5_f1']:.2%}")
        print(f"  Claude Sonnet:  {comparison['claude_f1']:.2%}")
        print(f"  Difference:     {comparison['difference']:.2%}")
        
        print(f"\nPer-Prompt Results:")
        print(f"  GPT-5 better:   {len(comparison['prompts_where_gpt5_better'])} prompts")
        print(f"  Claude better:  {len(comparison['prompts_where_claude_better'])} prompts")
        print(f"  Tied:           {len(comparison['prompts_tied'])} prompts")
        
        if comparison['prompts_where_gpt5_better']:
            print(f"\n  GPT-5 wins on: {', '.join(comparison['prompts_where_gpt5_better'])}")
        if comparison['prompts_where_claude_better']:
            print(f"  Claude wins on: {', '.join(comparison['prompts_where_claude_better'])}")
        
        return comparison
    
    def identify_systematic_gaps(self, gpt5_eval: Dict, claude_eval: Dict) -> List[Dict[str, Any]]:
        """Identify systematic gaps across both models"""
        
        print(f"\n{'='*100}")
        print("SYSTEMATIC GAP ANALYSIS")
        print(f"{'='*100}")
        
        gaps = []
        
        # Find tasks commonly missed by both models
        gpt5_all_missing = set()
        claude_all_missing = set()
        
        for prompt_id, score in gpt5_eval['per_prompt_scores'].items():
            gpt5_all_missing.update(score['missing_tasks'])
        
        for prompt_id, score in claude_eval['per_prompt_scores'].items():
            claude_all_missing.update(score['missing_tasks'])
        
        commonly_missed = gpt5_all_missing & claude_all_missing
        
        if commonly_missed:
            gaps.append({
                "type": "commonly_missed_tasks",
                "severity": "high",
                "description": f"Both models frequently miss these tasks: {', '.join(commonly_missed)}",
                "tasks": list(commonly_missed)
            })
        
        # Find tasks commonly over-selected
        gpt5_all_extra = set()
        claude_all_extra = set()
        
        for prompt_id, score in gpt5_eval['per_prompt_scores'].items():
            gpt5_all_extra.update(score['extra_tasks'])
        
        for prompt_id, score in claude_eval['per_prompt_scores'].items():
            claude_all_extra.update(score['extra_tasks'])
        
        commonly_extra = gpt5_all_extra & claude_all_extra
        
        if commonly_extra:
            gaps.append({
                "type": "commonly_over_selected_tasks",
                "severity": "medium",
                "description": f"Both models frequently add unnecessary tasks: {', '.join(commonly_extra)}",
                "tasks": list(commonly_extra)
            })
        
        # Print gaps
        print(f"\nIdentified {len(gaps)} systematic gaps:")
        for gap in gaps:
            print(f"\n  • {gap['type'].upper()} (Severity: {gap['severity']})")
            print(f"    {gap['description']}")
        
        return gaps


def main():
    parser = argparse.ArgumentParser(
        description="Compare LLM execution compositions against gold standard"
    )
    parser.add_argument(
        "batch_analysis_file",
        type=str,
        help="Path to batch composition analysis JSON file"
    )
    parser.add_argument(
        "--gold-standard",
        type=str,
        default="docs/gutt_analysis/gold_standard_analysis.json",
        help="Path to gold standard analysis file"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output file for evaluation results"
    )
    
    args = parser.parse_args()
    
    # Load batch analysis
    print(f"Loading batch analysis from {args.batch_analysis_file}...")
    with open(args.batch_analysis_file, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)
    
    # Initialize evaluator
    evaluator = CompositionEvaluator(args.gold_standard)
    
    # Evaluate both models
    gpt5_eval = evaluator.evaluate_model("GPT-5", batch_data['gpt5_analyses'])
    claude_eval = evaluator.evaluate_model("Claude Sonnet 4.5", batch_data['claude_analyses'])
    
    # Compare models
    comparison = evaluator.compare_models(gpt5_eval, claude_eval)
    
    # Identify gaps
    gaps = evaluator.identify_systematic_gaps(gpt5_eval, claude_eval)
    
    # Save results
    results = {
        "metadata": {
            "evaluation_date": datetime.now().isoformat(),
            "gold_standard_path": args.gold_standard,
            "batch_analysis_path": args.batch_analysis_file
        },
        "gpt5_evaluation": gpt5_eval,
        "claude_evaluation": claude_eval,
        "model_comparison": comparison,
        "systematic_gaps": gaps
    }
    
    if args.output:
        output_file = args.output
    else:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"docs/gutt_analysis/model_comparison/evaluation_results_{timestamp}.json"
    
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*100}")
    print("EVALUATION COMPLETE")
    print(f"{'='*100}")
    print(f"\n💾 Results saved to: {output_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
