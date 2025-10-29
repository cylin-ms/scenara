#!/usr/bin/env python3
"""
Compare Validation Results Across Dates
=========================================

Compare GPT-5 validation results across multiple dates to identify trends.

Usage:
    python compare_validation_across_dates.py <model> <date1> <date2> [date3...]

Example:
    python compare_validation_across_dates.py gpt5 2025-10-28 2025-10-29
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any

def load_analysis(model: str, date: str) -> Dict[str, Any]:
    """Load analysis results for a specific date."""
    analysis_file = Path(f"experiments/{date}/validation_analysis_{model}.json")
    
    if not analysis_file.exists():
        print(f"⚠️  Warning: Analysis not found for {date}, generating it...")
        import subprocess
        result = subprocess.run([
            sys.executable, 
            "analyze_single_model_validation.py", 
            model, 
            date
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"❌ ERROR: Could not generate analysis for {date}")
            return None
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def compare_results(model: str, dates: List[str]):
    """Compare validation results across multiple dates."""
    
    print("\n" + "="*80)
    print(f"  VALIDATION COMPARISON - {model.upper()}")
    print("="*80)
    
    analyses = []
    for date in dates:
        analysis = load_analysis(model, date)
        if analysis:
            analyses.append((date, analysis))
    
    if len(analyses) < 2:
        print("\n❌ ERROR: Need at least 2 dates with validation data")
        return
    
    # Print comparison table
    print(f"\n{'Date':<15} {'Meetings':<10} {'Validated':<10} {'Accuracy':<10} {'Errors':<10}")
    print("-"*80)
    
    total_meetings = 0
    total_correct = 0
    all_errors = []
    
    for date, analysis in analyses:
        summary = analysis['summary']
        print(f"{date:<15} {summary['total_meetings']:<10} {summary['validated_count']:<10} "
              f"{summary['accuracy']:<10}% {summary['incorrect_count']:<10}")
        
        total_meetings += summary['validated_count']
        total_correct += summary['correct_count']
        
        # Collect errors
        for error in analysis.get('errors', []):
            error['date'] = date
            all_errors.append(error)
    
    # Overall stats
    overall_accuracy = (total_correct / total_meetings * 100) if total_meetings > 0 else 0
    
    print("-"*80)
    print(f"{'TOTAL':<15} {total_meetings:<10} {total_meetings:<10} "
          f"{overall_accuracy:<10.1f}% {len(all_errors):<10}")
    
    # Analyze error patterns
    print("\n" + "="*80)
    print("  ERROR ANALYSIS")
    print("="*80)
    
    # Group errors by AI classification type
    error_types = {}
    for error in all_errors:
        ai_type = error['ai_type']
        if ai_type not in error_types:
            error_types[ai_type] = []
        error_types[ai_type].append(error)
    
    print(f"\nMost Common Misclassifications:")
    print("-"*80)
    
    sorted_errors = sorted(error_types.items(), key=lambda x: len(x[1]), reverse=True)
    for ai_type, errors in sorted_errors[:5]:
        print(f"\n{ai_type}:")
        print(f"  Frequency: {len(errors)} times")
        correct_types = [e['correct_type'] for e in errors]
        print(f"  Should be: {', '.join(set(correct_types))}")
        print(f"  Examples:")
        for error in errors[:2]:  # Show first 2 examples
            print(f"    - {error['subject']} ({error['date']})")
    
    # Category confusion matrix
    print("\n" + "="*80)
    print("  CATEGORY CONFUSION")
    print("="*80)
    
    category_confusion = {}
    for error in all_errors:
        ai_cat = error['ai_category']
        correct_cat = error['correct_category']
        key = f"{ai_cat} → {correct_cat}"
        
        if key not in category_confusion:
            category_confusion[key] = []
        category_confusion[key].append(error)
    
    print(f"\nCategory Mismatches:")
    for confusion, errors in sorted(category_confusion.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n{confusion}: {len(errors)} cases")
        for error in errors[:2]:
            print(f"  - {error['subject']} ({error['date']})")
    
    # Recurring error subjects
    print("\n" + "="*80)
    print("  RECURRING ERRORS")
    print("="*80)
    
    # Check if same meeting types appear in errors across dates
    subject_patterns = {}
    for error in all_errors:
        # Extract key words from subject
        subject_lower = error['subject'].lower()
        if 'office hour' in subject_lower:
            pattern = 'Office Hours'
        elif 'sync' in subject_lower:
            pattern = 'Sync Meetings'
        elif 'review' in subject_lower:
            pattern = 'Review Meetings'
        else:
            continue
        
        if pattern not in subject_patterns:
            subject_patterns[pattern] = []
        subject_patterns[pattern].append(error)
    
    if subject_patterns:
        print(f"\nRecurring Error Patterns:")
        for pattern, errors in subject_patterns.items():
            if len(errors) > 1 or len(dates) == 1:
                print(f"\n{pattern}: {len(errors)} errors")
                for error in errors:
                    print(f"  - {error['subject']} ({error['date']})")
                    print(f"    Misclassified as: {error['ai_type']}")
                    print(f"    Should be: {error['correct_type']}")
    else:
        print("\nNo recurring error patterns detected.")
    
    # Trend analysis
    print("\n" + "="*80)
    print("  TREND ANALYSIS")
    print("="*80)
    
    if len(analyses) >= 2:
        first_accuracy = analyses[0][1]['summary']['accuracy']
        last_accuracy = analyses[-1][1]['summary']['accuracy']
        change = last_accuracy - first_accuracy
        
        print(f"\nAccuracy Change:")
        print(f"  {analyses[0][0]}: {first_accuracy}%")
        print(f"  {analyses[-1][0]}: {last_accuracy}%")
        
        if change > 0:
            print(f"  📈 Improvement: +{change:.1f}%")
        elif change < 0:
            print(f"  📉 Decline: {change:.1f}%")
        else:
            print(f"  ➡️  No change")
    
    print("\n" + "="*80 + "\n")

def main():
    if len(sys.argv) < 3:
        print("\n❌ ERROR: Model and at least 2 dates required")
        print("\nUsage: python compare_validation_across_dates.py <model> <date1> <date2> [date3...]")
        print("\nExample: python compare_validation_across_dates.py gpt5 2025-10-28 2025-10-29")
        sys.exit(1)
    
    model = sys.argv[1]
    dates = sys.argv[2:]
    
    compare_results(model, dates)

if __name__ == "__main__":
    main()
