#!/usr/bin/env python3
"""
Analyze Single Model Validation Results
========================================

Analyze accuracy and error patterns from human validation of a single model.

Usage:
    python analyze_single_model_validation.py <model> <date>

Example:
    python analyze_single_model_validation.py gpt5 2025-10-29
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

def load_validation_results(model: str, date: str) -> Dict[str, Any]:
    """Load validation results for a specific model and date."""
    validation_file = Path(f"experiments/{date}/human_validation_{model}.json")
    
    if not validation_file.exists():
        print(f"❌ ERROR: Validation file not found: {validation_file}")
        sys.exit(1)
    
    with open(validation_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_meetings(date: str) -> List[Dict[str, Any]]:
    """Load meetings data."""
    meetings_file = Path(f"data/meetings/meetings_{date}.json")
    
    if not meetings_file.exists():
        print(f"❌ ERROR: Meetings file not found: {meetings_file}")
        sys.exit(1)
    
    with open(meetings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['meetings']

def load_classifications(model: str, date: str) -> Dict[int, Dict[str, Any]]:
    """Load classification results."""
    file_mapping = {
        "gpt5": "meeting_classification_gpt5.json",
        "copilot": "meeting_classification_github_copilot.json",
        "gpt4o": "meeting_classification_gpt4o.json",
        "claude": "meeting_classification_claude.json"
    }
    
    file_name = file_mapping.get(model)
    if not file_name:
        print(f"❌ ERROR: Unknown model: {model}")
        sys.exit(1)
    
    file_path = Path(f"experiments/{date}/{file_name}")
    
    if not file_path.exists():
        print(f"❌ ERROR: Classification file not found: {file_path}")
        sys.exit(1)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create lookup by meeting index
    classifications = {}
    for i, meeting in enumerate(data.get('meetings', [])):
        classifications[i] = meeting.get('classification', {})
    
    return classifications

def analyze_validation(validation_results: Dict[str, Any], 
                       meetings: List[Dict[str, Any]], 
                       classifications: Dict[int, Dict[str, Any]],
                       model: str) -> Dict[str, Any]:
    """Analyze validation results and generate detailed report."""
    
    validations = validation_results['validations']
    
    # Calculate basic metrics
    total_validated = len(validations)
    correct_count = sum(1 for v in validations.values() if v.get('is_correct'))
    incorrect_count = total_validated - correct_count
    accuracy = (correct_count / total_validated * 100) if total_validated > 0 else 0
    
    # Analyze by difficulty
    difficulty_stats = {'easy': {'total': 0, 'correct': 0}, 
                       'medium': {'total': 0, 'correct': 0}, 
                       'hard': {'total': 0, 'correct': 0}}
    
    for validation in validations.values():
        diff = validation.get('difficulty', 'medium')
        difficulty_stats[diff]['total'] += 1
        if validation.get('is_correct'):
            difficulty_stats[diff]['correct'] += 1
    
    # Collect errors with details
    errors = []
    for i, meeting in enumerate(meetings):
        meeting_id = meeting['id']
        validation = validations.get(meeting_id)
        
        if not validation:
            continue
        
        if not validation.get('is_correct'):
            classification = classifications.get(i, {})
            error_detail = {
                'meeting_number': i + 1,
                'subject': meeting['subject'],
                'ai_type': classification.get('specific_type', 'Unknown'),
                'ai_category': classification.get('primary_category', 'Unknown'),
                'correct_type': validation.get('correct_type', 'Unknown'),
                'correct_category': validation.get('correct_category', 'Unknown'),
                'confidence': classification.get('confidence', 0),
                'difficulty': validation.get('difficulty', 'medium'),
                'notes': validation.get('notes', ''),
                'reasoning': classification.get('reasoning', '')
            }
            errors.append(error_detail)
    
    # Category-level analysis
    category_errors = {}
    for error in errors:
        ai_cat = error['ai_category']
        correct_cat = error['correct_category']
        
        if ai_cat != 'Unknown':
            if ai_cat not in category_errors:
                category_errors[ai_cat] = {'misclassified_as': ai_cat, 'should_be': [], 'count': 0}
            category_errors[ai_cat]['should_be'].append(correct_cat)
            category_errors[ai_cat]['count'] += 1
    
    return {
        'summary': {
            'model': model,
            'model_display_name': validation_results.get('model_display_name', model.upper()),
            'validation_date': validation_results.get('validation_date'),
            'target_date': validation_results.get('target_date'),
            'total_meetings': validation_results.get('total_meetings', 0),
            'validated_count': total_validated,
            'correct_count': correct_count,
            'incorrect_count': incorrect_count,
            'accuracy': round(accuracy, 1),
            'error_rate': round(100 - accuracy, 1)
        },
        'difficulty_breakdown': {
            diff: {
                'total': stats['total'],
                'correct': stats['correct'],
                'accuracy': round(stats['correct'] / stats['total'] * 100, 1) if stats['total'] > 0 else 0
            }
            for diff, stats in difficulty_stats.items() if stats['total'] > 0
        },
        'errors': errors,
        'category_errors': category_errors,
        'validator': validation_results.get('validator', 'Human Expert')
    }

def print_report(analysis: Dict[str, Any]):
    """Print formatted analysis report."""
    summary = analysis['summary']
    
    print("\n" + "="*80)
    print(f"  VALIDATION ANALYSIS REPORT - {summary['model_display_name']}")
    print("="*80)
    
    print(f"\n📅 Target Date: {summary.get('target_date', 'N/A')}")
    print(f"👤 Validator: {analysis['validator']}")
    print(f"🕐 Validation Date: {summary['validation_date'][:19]}")
    
    print("\n" + "-"*80)
    print("  OVERALL ACCURACY")
    print("-"*80)
    
    print(f"\nTotal Meetings:     {summary['total_meetings']}")
    print(f"Validated:          {summary['validated_count']}")
    print(f"Correct:            {summary['correct_count']} ✓")
    print(f"Incorrect:          {summary['incorrect_count']} ✗")
    print(f"\n{'🎯 ACCURACY:':<20} {summary['accuracy']}%")
    print(f"{'Error Rate:':<20} {summary['error_rate']}%")
    
    # Difficulty breakdown
    if analysis['difficulty_breakdown']:
        print("\n" + "-"*80)
        print("  ACCURACY BY DIFFICULTY")
        print("-"*80)
        
        for diff, stats in analysis['difficulty_breakdown'].items():
            emoji = '😊' if diff == 'easy' else '🤔' if diff == 'medium' else '😰'
            print(f"\n{emoji} {diff.upper():<10} {stats['correct']}/{stats['total']} correct ({stats['accuracy']}%)")
    
    # Errors
    if analysis['errors']:
        print("\n" + "-"*80)
        print(f"  CLASSIFICATION ERRORS ({len(analysis['errors'])} total)")
        print("-"*80)
        
        for i, error in enumerate(analysis['errors'], 1):
            print(f"\n{i}. {error['subject']}")
            print(f"   Meeting #{error['meeting_number']}")
            print(f"   ❌ AI Classification: {error['ai_type']}")
            print(f"      Category: {error['ai_category']}")
            print(f"      Confidence: {error['confidence']*100:.0f}%")
            print(f"   ✓  Correct Type: {error['correct_type']}")
            print(f"      Category: {error['correct_category']}")
            print(f"   Difficulty: {error['difficulty']}")
            if error['notes']:
                print(f"   Notes: {error['notes']}")
            if error['reasoning']:
                print(f"   AI Reasoning: {error['reasoning']}")
    else:
        print("\n🎉 NO ERRORS! Perfect classification!")
    
    # Category errors
    if analysis['category_errors']:
        print("\n" + "-"*80)
        print("  ERROR PATTERNS BY CATEGORY")
        print("-"*80)
        
        for cat, details in analysis['category_errors'].items():
            print(f"\n{cat}:")
            print(f"  Misclassifications: {details['count']}")
            print(f"  Should be: {', '.join(set(details['should_be']))}")
    
    print("\n" + "="*80)
    
    # Comparison with threshold
    threshold = 80.0
    if summary['accuracy'] >= threshold:
        print(f"\n✅ PRODUCTION READY: Accuracy {summary['accuracy']}% meets {threshold}% threshold")
    else:
        gap = threshold - summary['accuracy']
        print(f"\n⚠️  BELOW THRESHOLD: Accuracy {summary['accuracy']}% is {gap:.1f}% below {threshold}% threshold")
        print(f"   Need to improve {summary['incorrect_count']} more classifications")
    
    print("\n" + "="*80 + "\n")

def save_report(analysis: Dict[str, Any], model: str, date: str):
    """Save analysis report as JSON."""
    output_file = Path(f"experiments/{date}/validation_analysis_{model}.json")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    print(f"📄 Detailed report saved to: {output_file}")

def main():
    if len(sys.argv) < 3:
        print("\n❌ ERROR: Model and date required")
        print("\nUsage: python analyze_single_model_validation.py <model> <date>")
        print("\nExample: python analyze_single_model_validation.py gpt5 2025-10-29")
        sys.exit(1)
    
    model = sys.argv[1]
    date = sys.argv[2]
    
    print(f"\n🔍 Loading validation results for {model.upper()} on {date}...")
    
    validation_results = load_validation_results(model, date)
    meetings = load_meetings(date)
    classifications = load_classifications(model, date)
    
    print(f"✅ Loaded {len(validation_results['validations'])} validations")
    
    print(f"\n📊 Analyzing results...")
    analysis = analyze_validation(validation_results, meetings, classifications, model)
    
    print_report(analysis)
    save_report(analysis, model, date)

if __name__ == "__main__":
    main()
