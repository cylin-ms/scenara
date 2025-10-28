"""
Human Validation Analysis - Meeting Classification Accuracy Evaluation
======================================================================

This script analyzes human validation results to calculate actual accuracy
of GPT-5 and GitHub Copilot meeting classifications.

Author: Scenara 2.0 Project
Date: October 28, 2025
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

# File paths
EXPERIMENTS_DIR = Path("experiments/2025-10-28")
VALIDATION_FILE = EXPERIMENTS_DIR / "human_validation_results.json"
GPT5_FILE = EXPERIMENTS_DIR / "meeting_classification_gpt5.json"
COPILOT_FILE = EXPERIMENTS_DIR / "meeting_classification_github_copilot.json"
MEETINGS_FILE = Path("data/meetings/meetings_2025-10-28.json")

def load_json(file_path: Path) -> dict:
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_meeting_details(meeting_id: str, meetings_data: dict) -> dict:
    """Get meeting details by ID."""
    for meeting in meetings_data['meetings']:
        if meeting['id'] == meeting_id:
            return meeting
    return {}

def get_classification_by_index(index: int, classifications: dict) -> dict:
    """Get classification for meeting at given index."""
    meetings = classifications['meetings']
    if index < len(meetings):
        return meetings[index].get('classification', {})
    return {}

def analyze_validation_results():
    """Analyze human validation results and calculate accuracy metrics."""
    
    print("\n" + "="*80)
    print("  HUMAN VALIDATION ANALYSIS - GROUND TRUTH ACCURACY")
    print("="*80)
    print()
    
    # Load data
    validation_data = load_json(VALIDATION_FILE)
    gpt5_data = load_json(GPT5_FILE)
    copilot_data = load_json(COPILOT_FILE)
    meetings_data = load_json(MEETINGS_FILE)
    
    validations = validation_data['validations']
    total_meetings = len(validations)
    
    # Calculate accuracies
    gpt5_correct = sum(1 for v in validations.values() if v.get('gpt5_correct'))
    copilot_correct = sum(1 for v in validations.values() if v.get('copilot_correct'))
    both_correct = sum(1 for v in validations.values() if v.get('gpt5_correct') and v.get('copilot_correct'))
    both_wrong = sum(1 for v in validations.values() if not v.get('gpt5_correct') and not v.get('copilot_correct'))
    
    gpt5_accuracy = (gpt5_correct / total_meetings) * 100
    copilot_accuracy = (copilot_correct / total_meetings) * 100
    
    # Print summary
    print("VALIDATION SUMMARY")
    print("-" * 80)
    print(f"Validation Date: {validation_data['validation_date']}")
    print(f"Validator: {validation_data['validator']}")
    print(f"Total Meetings Validated: {total_meetings}")
    print()
    
    print("ACCURACY RESULTS")
    print("-" * 80)
    print(f"GPT-5 Accuracy:           {gpt5_correct}/{total_meetings} = {gpt5_accuracy:.1f}%")
    print(f"GitHub Copilot Accuracy:  {copilot_correct}/{total_meetings} = {copilot_accuracy:.1f}%")
    print()
    print(f"Both Models Correct:      {both_correct}/{total_meetings} = {(both_correct/total_meetings)*100:.1f}%")
    print(f"Both Models Wrong:        {both_wrong}/{total_meetings} = {(both_wrong/total_meetings)*100:.1f}%")
    print()
    
    # Cross-model agreement (from previous analysis)
    cross_model_agreement = 87.5  # 7/8 meetings
    print("COMPARISON TO CROSS-MODEL AGREEMENT")
    print("-" * 80)
    print(f"Cross-Model Agreement:    87.5% (7/8 meetings)")
    print(f"GPT-5 Actual Accuracy:    {gpt5_accuracy:.1f}%")
    print(f"Copilot Actual Accuracy:  {copilot_accuracy:.1f}%")
    print()
    
    if gpt5_accuracy >= cross_model_agreement:
        print(f"✓ GPT-5 accuracy ({gpt5_accuracy:.1f}%) MATCHES cross-model agreement!")
    else:
        print(f"⚠ GPT-5 accuracy ({gpt5_accuracy:.1f}%) is LOWER than cross-model agreement")
    
    if copilot_accuracy >= cross_model_agreement:
        print(f"✓ Copilot accuracy ({copilot_accuracy:.1f}%) MATCHES cross-model agreement!")
    else:
        print(f"⚠ Copilot accuracy ({copilot_accuracy:.1f}%) is LOWER than cross-model agreement")
    print()
    
    # Detailed meeting-by-meeting analysis
    print("MEETING-BY-MEETING ANALYSIS")
    print("-" * 80)
    print(f"{'#':<3} {'Meeting':<40} {'GPT-5':<10} {'Copilot':<10} {'Difficulty':<10}")
    print("-" * 80)
    
    meeting_ids = list(validations.keys())
    errors_gpt5 = []
    errors_copilot = []
    
    for i, meeting_id in enumerate(meeting_ids, 1):
        validation = validations[meeting_id]
        meeting = get_meeting_details(meeting_id, meetings_data)
        subject = meeting.get('subject', 'Unknown')[:40]
        
        gpt5_status = "✓ Correct" if validation.get('gpt5_correct') else "✗ Wrong"
        copilot_status = "✓ Correct" if validation.get('copilot_correct') else "✗ Wrong"
        difficulty = validation.get('difficulty', 'N/A').capitalize()
        
        print(f"{i:<3} {subject:<40} {gpt5_status:<10} {copilot_status:<10} {difficulty:<10}")
        
        # Collect errors
        if not validation.get('gpt5_correct'):
            gpt5_class = get_classification_by_index(i-1, gpt5_data)
            errors_gpt5.append({
                'meeting': subject,
                'ai_type': gpt5_class.get('specific_type', 'Unknown'),
                'correct_type': validation.get('correct_type', 'Unknown'),
                'confidence': gpt5_class.get('confidence', 0)
            })
        
        if not validation.get('copilot_correct'):
            copilot_class = get_classification_by_index(i-1, copilot_data)
            errors_copilot.append({
                'meeting': subject,
                'ai_type': copilot_class.get('specific_type', 'Unknown'),
                'correct_type': validation.get('correct_type', 'Unknown'),
                'confidence': copilot_class.get('confidence', 0)
            })
    
    print()
    
    # Error analysis
    if errors_gpt5:
        print("GPT-5 ERRORS (Detailed)")
        print("-" * 80)
        for i, error in enumerate(errors_gpt5, 1):
            print(f"\nError {i}: {error['meeting']}")
            print(f"  AI Classification:      {error['ai_type']}")
            print(f"  Correct Classification: {error['correct_type']}")
            print(f"  Confidence:             {error['confidence']*100:.0f}%")
        print()
    else:
        print("GPT-5 ERRORS: None! Perfect accuracy!")
        print()
    
    if errors_copilot:
        print("GITHUB COPILOT ERRORS (Detailed)")
        print("-" * 80)
        for i, error in enumerate(errors_copilot, 1):
            print(f"\nError {i}: {error['meeting']}")
            print(f"  AI Classification:      {error['ai_type']}")
            print(f"  Correct Classification: {error['correct_type']}")
            print(f"  Confidence:             {error['confidence']*100:.0f}%")
        print()
    else:
        print("GITHUB COPILOT ERRORS: None! Perfect accuracy!")
        print()
    
    # Error pattern analysis
    print("ERROR PATTERN ANALYSIS")
    print("-" * 80)
    
    # Collect all errors
    all_errors = []
    for error in errors_gpt5:
        all_errors.append({
            'model': 'GPT-5',
            'ai_type': error['ai_type'],
            'correct_type': error['correct_type']
        })
    for error in errors_copilot:
        all_errors.append({
            'model': 'Copilot',
            'ai_type': error['ai_type'],
            'correct_type': error['correct_type']
        })
    
    if all_errors:
        # Count confusion patterns
        confusion_patterns = {}
        for error in all_errors:
            pattern = f"{error['ai_type']} → {error['correct_type']}"
            confusion_patterns[pattern] = confusion_patterns.get(pattern, 0) + 1
        
        print("Most Common Confusion Patterns:")
        for pattern, count in sorted(confusion_patterns.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {pattern} ({count} occurrence{'s' if count > 1 else ''})")
        print()
        
        # Identify if all errors point to same correct type
        correct_types = [e['correct_type'] for e in all_errors]
        if len(set(correct_types)) == 1:
            print(f"⚠ PATTERN DETECTED: All errors should have been '{correct_types[0]}'")
            print("   This suggests a systematic misclassification of this meeting type.")
        print()
    else:
        print("No errors detected - both models achieved perfect accuracy!")
        print()
    
    # Difficulty analysis
    print("DIFFICULTY ANALYSIS")
    print("-" * 80)
    
    difficulty_stats = {'easy': {'total': 0, 'gpt5_correct': 0, 'copilot_correct': 0},
                       'medium': {'total': 0, 'gpt5_correct': 0, 'copilot_correct': 0},
                       'hard': {'total': 0, 'gpt5_correct': 0, 'copilot_correct': 0}}
    
    for validation in validations.values():
        diff = validation.get('difficulty', 'medium')
        difficulty_stats[diff]['total'] += 1
        if validation.get('gpt5_correct'):
            difficulty_stats[diff]['gpt5_correct'] += 1
        if validation.get('copilot_correct'):
            difficulty_stats[diff]['copilot_correct'] += 1
    
    for diff in ['easy', 'medium', 'hard']:
        stats = difficulty_stats[diff]
        if stats['total'] > 0:
            gpt5_acc = (stats['gpt5_correct'] / stats['total']) * 100
            copilot_acc = (stats['copilot_correct'] / stats['total']) * 100
            print(f"{diff.capitalize()} meetings ({stats['total']}):")
            print(f"  GPT-5:   {stats['gpt5_correct']}/{stats['total']} = {gpt5_acc:.1f}%")
            print(f"  Copilot: {stats['copilot_correct']}/{stats['total']} = {copilot_acc:.1f}%")
            print()
    
    # Key findings
    print("KEY FINDINGS")
    print("-" * 80)
    
    # Winner
    if gpt5_accuracy > copilot_accuracy:
        winner = "GPT-5"
        margin = gpt5_accuracy - copilot_accuracy
    elif copilot_accuracy > gpt5_accuracy:
        winner = "GitHub Copilot"
        margin = copilot_accuracy - gpt5_accuracy
    else:
        winner = "TIE"
        margin = 0
    
    if winner != "TIE":
        print(f"1. {winner} performed better by {margin:.1f} percentage points")
    else:
        print(f"1. Both models achieved equal accuracy ({gpt5_accuracy:.1f}%)")
    
    # Agreement vs accuracy
    if both_correct == total_meetings:
        print(f"2. Perfect agreement - both models correct on all {total_meetings} meetings")
    elif both_wrong > 0:
        print(f"2. Both models wrong on {both_wrong} meeting(s) - systematic error pattern")
    else:
        print(f"2. Models disagree on {total_meetings - both_correct} meeting(s)")
    
    # Confidence calibration
    print(f"3. Cross-model agreement (87.5%) vs actual accuracy:")
    print(f"   - GPT-5: {gpt5_accuracy:.1f}% (difference: {abs(gpt5_accuracy - 87.5):.1f}%)")
    print(f"   - Copilot: {copilot_accuracy:.1f}% (difference: {abs(copilot_accuracy - 87.5):.1f}%)")
    
    print()
    
    # Recommendations
    print("RECOMMENDATIONS")
    print("-" * 80)
    
    if gpt5_accuracy >= 80 and copilot_accuracy >= 80:
        print("✓ Both models meet production-ready threshold (≥80% accuracy)")
        print(f"✓ Recommend deploying: {winner if winner != 'TIE' else 'either model'}")
    else:
        print("⚠ Models below production threshold (80%)")
        print("  Recommended actions:")
        print("  1. Analyze error patterns")
        print("  2. Refine prompt for common errors")
        print("  3. Re-run experiments")
    
    if errors_gpt5 or errors_copilot:
        print("\nPrompt Improvement Opportunities:")
        unique_correct_types = set(e['correct_type'] for e in all_errors)
        for correct_type in unique_correct_types:
            print(f"  • Strengthen classification rules for '{correct_type}'")
    
    print()
    print("="*80)
    print()
    
    # Generate summary report
    summary = {
        'validation_date': validation_data['validation_date'],
        'total_meetings': total_meetings,
        'accuracy': {
            'gpt5': {
                'correct': gpt5_correct,
                'total': total_meetings,
                'percentage': round(gpt5_accuracy, 1)
            },
            'copilot': {
                'correct': copilot_correct,
                'total': total_meetings,
                'percentage': round(copilot_accuracy, 1)
            }
        },
        'agreement': {
            'both_correct': both_correct,
            'both_wrong': both_wrong,
            'cross_model_agreement': 87.5
        },
        'errors': {
            'gpt5': errors_gpt5,
            'copilot': errors_copilot
        },
        'difficulty_breakdown': difficulty_stats,
        'winner': winner,
        'production_ready': gpt5_accuracy >= 80 and copilot_accuracy >= 80
    }
    
    # Save summary
    summary_file = EXPERIMENTS_DIR / "validation_accuracy_report.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, indent=2, fp=f)
    
    print(f"📊 Detailed report saved to: {summary_file}")
    print()
    
    return summary

if __name__ == '__main__':
    analyze_validation_results()
