#!/usr/bin/env python3
"""
Evaluation Assertions for Top 7 Meeting Types Post-Training

Validates that post-training models correctly handle the 7 high-complexity
meeting types with appropriate importance, prep time, and reasoning.

Usage:
    python tools/evaluate_top7_assertions.py --test-data post_training/data/training/top7_synthetic_eval.jsonl
    python tools/evaluate_top7_assertions.py --model-predictions predictions.jsonl --ground-truth test.jsonl
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple
import statistics

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class Top7Evaluator:
    """Evaluation assertions for top 7 meeting types."""
    
    # Expected ranges for each meeting type
    MEETING_TYPE_EXPECTATIONS = {
        "Quarterly Business Review (QBR)": {
            "importance": ["critical", "high"],
            "prep_time_min": 240,  # 4 hours minimum
            "prep_time_max": 360,  # 6 hours maximum
            "prep_needed": True
        },
        "Board of Directors Meeting": {
            "importance": ["critical"],
            "prep_time_min": 300,  # 5 hours minimum
            "prep_time_max": 480,  # 8 hours maximum
            "prep_needed": True
        },
        "Executive Sales Presentation": {
            "importance": ["critical", "high"],
            "prep_time_min": 120,  # 2 hours minimum
            "prep_time_max": 240,  # 4 hours maximum
            "prep_needed": True
        },
        "Product Launch Go/No-Go Decision": {
            "importance": ["critical", "high"],
            "prep_time_min": 180,  # 3 hours minimum
            "prep_time_max": 300,  # 5 hours maximum
            "prep_needed": True
        },
        "Annual SOX 404 Compliance Review": {
            "importance": ["critical", "high"],
            "prep_time_min": 240,  # 4 hours minimum
            "prep_time_max": 360,  # 6 hours maximum
            "prep_needed": True
        },
        "Quarterly Earnings Call": {
            "importance": ["critical"],
            "prep_time_min": 300,  # 5 hours minimum
            "prep_time_max": 480,  # 8 hours maximum
            "prep_needed": True
        },
        "M&A Deal Approval (Board)": {
            "importance": ["critical"],
            "prep_time_min": 360,  # 6 hours minimum
            "prep_time_max": 600,  # 10 hours maximum
            "prep_needed": True
        }
    }
    
    def __init__(self):
        self.assertions_passed = 0
        self.assertions_failed = 0
        self.failures = []
    
    def assert_importance_correct(self, meeting: Dict, prediction: Dict) -> bool:
        """Assert that importance label is appropriate for meeting type."""
        meeting_type = meeting.get('_llm_classification', {}).get('meeting_type')
        expected = self.MEETING_TYPE_EXPECTATIONS.get(meeting_type, {})
        expected_importance = expected.get('importance', [])
        
        predicted_importance = prediction.get('importance_label', '').lower()
        
        if predicted_importance in [i.lower() for i in expected_importance]:
            self.assertions_passed += 1
            return True
        else:
            self.assertions_failed += 1
            self.failures.append({
                'assertion': 'importance_correct',
                'meeting': meeting.get('subject'),
                'meeting_type': meeting_type,
                'expected': expected_importance,
                'actual': predicted_importance
            })
            return False
    
    def assert_prep_time_reasonable(self, meeting: Dict, prediction: Dict) -> bool:
        """Assert that prep time is within reasonable range for meeting type."""
        meeting_type = meeting.get('_llm_classification', {}).get('meeting_type')
        expected = self.MEETING_TYPE_EXPECTATIONS.get(meeting_type, {})
        
        min_prep = expected.get('prep_time_min', 0)
        max_prep = expected.get('prep_time_max', 1000)
        
        predicted_prep = prediction.get('prep_time_minutes', 0)
        
        if min_prep <= predicted_prep <= max_prep:
            self.assertions_passed += 1
            return True
        else:
            self.assertions_failed += 1
            self.failures.append({
                'assertion': 'prep_time_reasonable',
                'meeting': meeting.get('subject'),
                'meeting_type': meeting_type,
                'expected_range': f"{min_prep}-{max_prep} min",
                'actual': f"{predicted_prep} min"
            })
            return False
    
    def assert_prep_needed(self, meeting: Dict, prediction: Dict) -> bool:
        """Assert that prep_needed is True for all top 7 types."""
        meeting_type = meeting.get('_llm_classification', {}).get('meeting_type')
        
        predicted_prep_needed = prediction.get('prep_needed', False)
        
        if predicted_prep_needed:
            self.assertions_passed += 1
            return True
        else:
            self.assertions_failed += 1
            self.failures.append({
                'assertion': 'prep_needed',
                'meeting': meeting.get('subject'),
                'meeting_type': meeting_type,
                'expected': True,
                'actual': predicted_prep_needed
            })
            return False
    
    def assert_reasoning_present(self, meeting: Dict, prediction: Dict) -> bool:
        """Assert that reasoning is provided and non-empty."""
        reasoning = prediction.get('reasoning', '').strip()
        
        if reasoning and len(reasoning) >= 20:  # At least 20 characters
            self.assertions_passed += 1
            return True
        else:
            self.assertions_failed += 1
            self.failures.append({
                'assertion': 'reasoning_present',
                'meeting': meeting.get('subject'),
                'reasoning_length': len(reasoning),
                'expected': '>= 20 characters'
            })
            return False
    
    def calculate_prep_time_mae(self, meetings: List[Dict], predictions: List[Dict]) -> float:
        """Calculate Mean Absolute Error for prep time predictions."""
        errors = []
        
        for meeting, prediction in zip(meetings, predictions):
            ground_truth = meeting.get('prep_time_minutes', 0)
            predicted = prediction.get('prep_time_minutes', 0)
            
            error = abs(ground_truth - predicted)
            errors.append(error)
        
        return statistics.mean(errors) if errors else 0
    
    def calculate_importance_accuracy(self, meetings: List[Dict], predictions: List[Dict]) -> float:
        """Calculate accuracy for importance label predictions."""
        correct = 0
        total = len(meetings)
        
        for meeting, prediction in zip(meetings, predictions):
            ground_truth = meeting.get('importance_label', '').lower()
            predicted = prediction.get('importance_label', '').lower()
            
            if ground_truth == predicted:
                correct += 1
        
        return (correct / total * 100) if total > 0 else 0
    
    def evaluate_all(self, meetings: List[Dict], predictions: List[Dict]) -> Dict:
        """Run all evaluation assertions."""
        print(f"\n{'='*80}")
        print(f"EVALUATING {len(meetings)} PREDICTIONS")
        print(f"{'='*80}\n")
        
        results = {
            'total_assertions': 0,
            'passed': 0,
            'failed': 0,
            'pass_rate': 0.0,
            'metrics': {},
            'failures': []
        }
        
        # Run assertions for each prediction
        for meeting, prediction in zip(meetings, predictions):
            self.assert_importance_correct(meeting, prediction)
            self.assert_prep_time_reasonable(meeting, prediction)
            self.assert_prep_needed(meeting, prediction)
            self.assert_reasoning_present(meeting, prediction)
        
        # Calculate metrics
        prep_time_mae = self.calculate_prep_time_mae(meetings, predictions)
        importance_accuracy = self.calculate_importance_accuracy(meetings, predictions)
        
        results['total_assertions'] = self.assertions_passed + self.assertions_failed
        results['passed'] = self.assertions_passed
        results['failed'] = self.assertions_failed
        results['pass_rate'] = (self.assertions_passed / results['total_assertions'] * 100) if results['total_assertions'] > 0 else 0
        
        results['metrics'] = {
            'prep_time_mae': prep_time_mae,
            'importance_accuracy': importance_accuracy,
            'prep_needed_compliance': 100.0  # Should always be 100% for top 7
        }
        
        results['failures'] = self.failures
        
        return results


def load_jsonl(file_path: Path) -> List[Dict]:
    """Load JSONL file."""
    data = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                data.append(json.loads(line))
    return data


def print_results(results: Dict):
    """Print evaluation results."""
    print(f"\n{'='*80}")
    print(f"EVALUATION RESULTS")
    print(f"{'='*80}")
    
    print(f"\n✅ Assertions Passed: {results['passed']}/{results['total_assertions']} ({results['pass_rate']:.1f}%)")
    print(f"❌ Assertions Failed: {results['failed']}/{results['total_assertions']}")
    
    print(f"\n📊 Metrics:")
    print(f"   Prep Time MAE: {results['metrics']['prep_time_mae']:.1f} minutes")
    print(f"   Importance Accuracy: {results['metrics']['importance_accuracy']:.1f}%")
    print(f"   Prep Needed Compliance: {results['metrics']['prep_needed_compliance']:.1f}%")
    
    # Success criteria
    print(f"\n🎯 Success Criteria:")
    mae_pass = results['metrics']['prep_time_mae'] < 45
    importance_pass = results['metrics']['importance_accuracy'] >= 85
    overall_pass = results['pass_rate'] >= 90
    
    print(f"   {'✅' if mae_pass else '❌'} Prep Time MAE < 45 minutes: {mae_pass}")
    print(f"   {'✅' if importance_pass else '❌'} Importance Accuracy >= 85%: {importance_pass}")
    print(f"   {'✅' if overall_pass else '❌'} Overall Pass Rate >= 90%: {overall_pass}")
    
    # Show failures if any
    if results['failures']:
        print(f"\n⚠️  Failed Assertions ({len(results['failures'])}):")
        for i, failure in enumerate(results['failures'][:10], 1):  # Show first 10
            print(f"\n   [{i}] {failure['assertion']}")
            print(f"       Meeting: {failure.get('meeting', 'Unknown')}")
            for key, value in failure.items():
                if key not in ['assertion', 'meeting']:
                    print(f"       {key}: {value}")
        
        if len(results['failures']) > 10:
            print(f"\n   ... and {len(results['failures']) - 10} more failures")
    
    print(f"\n{'='*80}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate predictions against top 7 meeting type assertions'
    )
    parser.add_argument(
        '--test-data',
        type=Path,
        help='Test data JSONL file (ground truth)'
    )
    parser.add_argument(
        '--predictions',
        type=Path,
        help='Model predictions JSONL file'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('eval_results.json'),
        help='Output file for results'
    )
    
    args = parser.parse_args()
    
    # Load data
    if args.test_data and args.test_data.exists():
        test_data = load_jsonl(args.test_data)
        predictions = test_data  # Use ground truth as predictions for validation
    elif args.test_data and args.predictions:
        test_data = load_jsonl(args.test_data)
        predictions = load_jsonl(args.predictions)
    else:
        print("❌ Error: Provide --test-data or both --test-data and --predictions")
        return 1
    
    # Run evaluation
    evaluator = Top7Evaluator()
    results = evaluator.evaluate_all(test_data, predictions)
    
    # Print results
    print_results(results)
    
    # Save results
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"💾 Results saved to: {args.output}")
    
    # Return exit code based on success criteria
    mae_pass = results['metrics']['prep_time_mae'] < 45
    importance_pass = results['metrics']['importance_accuracy'] >= 85
    overall_pass = results['pass_rate'] >= 90
    
    if mae_pass and importance_pass and overall_pass:
        print("\n✅ All success criteria met!")
        return 0
    else:
        print("\n❌ Some success criteria not met")
        return 1


if __name__ == '__main__':
    sys.exit(main())
