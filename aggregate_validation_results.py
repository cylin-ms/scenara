"""
Aggregated Validation Analysis - Multi-Day Dataset Builder
===========================================================

This script:
1. Finds all human validation results across multiple days
2. Aggregates accuracy metrics and error patterns
3. Builds a growing training/evaluation dataset
4. Tracks improvement over time as prompt is refined

Author: Scenara 2.0 Project
Date: October 28, 2025
"""

import json
from pathlib import Path
from typing import Dict, List, Tuple, Any
from datetime import datetime
from collections import defaultdict
import re

# Directories
EXPERIMENTS_DIR = Path("experiments")
DATA_DIR = Path("data/meetings")
AGGREGATED_DIR = Path("experiments/aggregated_validation")

# Output files
AGGREGATED_DIR.mkdir(parents=True, exist_ok=True)
TRAINING_DATASET = AGGREGATED_DIR / "training_dataset.json"
EVALUATION_DATASET = AGGREGATED_DIR / "evaluation_dataset.json"
ACCURACY_TRENDS = AGGREGATED_DIR / "accuracy_trends.json"
ERROR_CATALOG = AGGREGATED_DIR / "error_catalog.json"

def find_validation_files() -> List[Tuple[str, Path]]:
    """Find all human validation result files."""
    validation_files = []
    
    # Search all experiment date directories
    for date_dir in EXPERIMENTS_DIR.glob("20*"):
        if date_dir.is_dir():
            validation_file = date_dir / "human_validation_results.json"
            if validation_file.exists():
                date = date_dir.name
                validation_files.append((date, validation_file))
    
    return sorted(validation_files)

def load_json(file_path: Path) -> dict:
    """Load JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(data: dict, file_path: Path):
    """Save JSON file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, indent=2, fp=f)

def get_meeting_by_id(meeting_id: str, date: str) -> Dict[str, Any]:
    """Get meeting details by ID and date."""
    meetings_file = DATA_DIR / f"meetings_{date}.json"
    if not meetings_file.exists():
        return {}
    
    meetings_data = load_json(meetings_file)
    for meeting in meetings_data.get('meetings', []):
        if meeting['id'] == meeting_id:
            return meeting
    return {}

def get_classification_by_meeting_id(meeting_id: str, date: str, model: str) -> Dict[str, Any]:
    """Get classification for a specific meeting."""
    if model == "gpt5":
        class_file = EXPERIMENTS_DIR / date / "meeting_classification_gpt5.json"
    elif model == "copilot":
        class_file = EXPERIMENTS_DIR / date / "meeting_classification_github_copilot.json"
    else:
        return {}
    
    if not class_file.exists():
        return {}
    
    class_data = load_json(class_file)
    
    # Handle different file formats
    for i, meeting in enumerate(class_data.get('meetings', [])):
        # GPT-5 format has full meeting object with id
        if 'id' in meeting and meeting['id'] == meeting_id:
            return meeting.get('classification', {})
        # GitHub Copilot format may not have id - match by index
        # This is a fallback, less reliable
    
    return {}

def extract_keywords(text: str) -> List[str]:
    """Extract meaningful keywords from meeting subject/description."""
    # Common keywords that indicate meeting type
    keywords = []
    text_lower = text.lower()
    
    patterns = [
        r'\b(meeting prep|prep)\b',
        r'\b(sync|synch)\b',
        r'\b(standup|stand-up)\b',
        r'\b(1:1|1-on-1|one-on-one)\b',
        r'\b(planning|plan)\b',
        r'\b(review|checkpoint)\b',
        r'\b(interview|candidate)\b',
        r'\b(brainstorm|ideation)\b',
        r'\b(retrospective|retro)\b',
        r'\b(office hours?)\b',
        r'\b(all-hands|town hall)\b',
        r'\b(training|workshop)\b',
        r'\b(demo|demonstration)\b',
        r'\[async task\]',
        r'\b(weekly|daily|monthly|quarterly)\b'
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text_lower)
        keywords.extend(matches)
    
    return list(set(keywords))

def build_training_example(meeting_id: str, date: str, validation: Dict[str, Any]) -> Dict[str, Any]:
    """Build a training example from validated meeting."""
    meeting = get_meeting_by_id(meeting_id, date)
    
    if not meeting:
        return None
    
    # Extract features
    subject = meeting.get('subject', '')
    body = meeting.get('bodyPreview', '')
    attendees = meeting.get('attendees', [])
    start_time = meeting.get('start', {}).get('dateTime', '')
    end_time = meeting.get('end', {}).get('dateTime', '')
    
    # Calculate duration
    try:
        from datetime import datetime
        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        duration_minutes = (end - start).total_seconds() / 60
    except:
        duration_minutes = 0
    
    # Extract keywords
    keywords = extract_keywords(subject + ' ' + body)
    
    # Build training example
    example = {
        'id': meeting_id,
        'date': date,
        'features': {
            'subject': subject,
            'body_preview': body[:200],  # Truncate for privacy
            'attendee_count': len(attendees),
            'duration_minutes': duration_minutes,
            'keywords': keywords
        },
        'ground_truth': {
            'specific_type': validation.get('correct_type'),
            'primary_category': validation.get('correct_category'),
            'difficulty': validation.get('difficulty', 'medium'),
            'notes': validation.get('notes', '')
        },
        'validation_metadata': {
            'timestamp': validation.get('timestamp'),
            'gpt5_correct': validation.get('gpt5_correct'),
            'copilot_correct': validation.get('copilot_correct')
        }
    }
    
    return example

def build_error_example(meeting_id: str, date: str, validation: Dict[str, Any], model: str) -> Dict[str, Any]:
    """Build an error example for error catalog."""
    meeting = get_meeting_by_id(meeting_id, date)
    classification = get_classification_by_meeting_id(meeting_id, date, model)
    
    if not meeting or not classification:
        return None
    
    error = {
        'id': meeting_id,
        'date': date,
        'model': model,
        'meeting_subject': meeting.get('subject', ''),
        'keywords': extract_keywords(meeting.get('subject', '') + ' ' + meeting.get('bodyPreview', '')),
        'ai_classification': {
            'specific_type': classification.get('specific_type'),
            'primary_category': classification.get('primary_category'),
            'confidence': classification.get('confidence', 0)
        },
        'correct_classification': {
            'specific_type': validation.get('correct_type'),
            'primary_category': validation.get('correct_category')
        },
        'error_pattern': f"{classification.get('specific_type', 'Unknown')} → {validation.get('correct_type', 'Unknown')}",
        'difficulty': validation.get('difficulty', 'medium'),
        'notes': validation.get('notes', '')
    }
    
    return error

def aggregate_validation_results():
    """Main aggregation function."""
    
    print("\n" + "="*80)
    print("  AGGREGATED VALIDATION ANALYSIS - MULTI-DAY DATASET BUILDER")
    print("="*80)
    print()
    
    # Find all validation files
    validation_files = find_validation_files()
    
    if not validation_files:
        print("No validation files found!")
        print(f"   Searched in: {EXPERIMENTS_DIR}")
        return
    
    print(f"Found {len(validation_files)} validation file(s):")
    for date, filepath in validation_files:
        print(f"   - {date}: {filepath}")
    print()
    
    # Aggregated data structures
    all_training_examples = []
    all_error_examples = []
    accuracy_by_date = {}
    overall_stats = {
        'total_meetings_validated': 0,
        'total_gpt5_correct': 0,
        'total_copilot_correct': 0,
        'dates_validated': [],
        'error_patterns': defaultdict(int),
        'difficulty_breakdown': defaultdict(lambda: {'total': 0, 'gpt5_correct': 0, 'copilot_correct': 0})
    }
    
    # Process each validation file
    for date, filepath in validation_files:
        print(f"Processing {date}...")
        
        validation_data = load_json(filepath)
        validations = validation_data.get('validations', {})
        
        if not validations:
            print(f"  X No validations found in {date}")
            continue
        
        # Date-specific stats
        date_stats = {
            'date': date,
            'total_meetings': len(validations),
            'gpt5_correct': 0,
            'copilot_correct': 0,
            'both_correct': 0,
            'both_wrong': 0,
            'errors': []
        }
        
        # Process each validation
        for meeting_id, validation in validations.items():
            # Build training example
            training_example = build_training_example(meeting_id, date, validation)
            if training_example:
                all_training_examples.append(training_example)
            
            # Track stats
            overall_stats['total_meetings_validated'] += 1
            
            if validation.get('gpt5_correct'):
                overall_stats['total_gpt5_correct'] += 1
                date_stats['gpt5_correct'] += 1
            else:
                # Record GPT-5 error
                error = build_error_example(meeting_id, date, validation, 'gpt5')
                if error:
                    all_error_examples.append(error)
                    date_stats['errors'].append(error)
                    overall_stats['error_patterns'][error['error_pattern']] += 1
            
            if validation.get('copilot_correct'):
                overall_stats['total_copilot_correct'] += 1
                date_stats['copilot_correct'] += 1
            else:
                # Record Copilot error
                error = build_error_example(meeting_id, date, validation, 'copilot')
                if error:
                    all_error_examples.append(error)
                    date_stats['errors'].append(error)
                    overall_stats['error_patterns'][error['error_pattern']] += 1
            
            # Track both correct/wrong
            if validation.get('gpt5_correct') and validation.get('copilot_correct'):
                date_stats['both_correct'] += 1
            elif not validation.get('gpt5_correct') and not validation.get('copilot_correct'):
                date_stats['both_wrong'] += 1
            
            # Track difficulty
            difficulty = validation.get('difficulty', 'medium')
            overall_stats['difficulty_breakdown'][difficulty]['total'] += 1
            if validation.get('gpt5_correct'):
                overall_stats['difficulty_breakdown'][difficulty]['gpt5_correct'] += 1
            if validation.get('copilot_correct'):
                overall_stats['difficulty_breakdown'][difficulty]['copilot_correct'] += 1
        
        # Calculate date-specific accuracy
        date_stats['gpt5_accuracy'] = (date_stats['gpt5_correct'] / date_stats['total_meetings'] * 100) if date_stats['total_meetings'] > 0 else 0
        date_stats['copilot_accuracy'] = (date_stats['copilot_correct'] / date_stats['total_meetings'] * 100) if date_stats['total_meetings'] > 0 else 0
        
        accuracy_by_date[date] = date_stats
        overall_stats['dates_validated'].append(date)
        
        print(f"  + {date}: {date_stats['total_meetings']} meetings")
        print(f"    GPT-5: {date_stats['gpt5_accuracy']:.1f}% | Copilot: {date_stats['copilot_accuracy']:.1f}%")
    
    print()
    
    # Calculate overall accuracy
    total_meetings = overall_stats['total_meetings_validated']
    overall_gpt5_accuracy = (overall_stats['total_gpt5_correct'] / total_meetings * 100) if total_meetings > 0 else 0
    overall_copilot_accuracy = (overall_stats['total_copilot_correct'] / total_meetings * 100) if total_meetings > 0 else 0
    
    # Print overall summary
    print("OVERALL STATISTICS")
    print("-" * 80)
    print(f"Total Meetings Validated: {total_meetings}")
    print(f"Validation Dates: {', '.join(overall_stats['dates_validated'])}")
    print()
    print(f"GPT-5 Overall Accuracy:      {overall_gpt5_accuracy:.1f}% ({overall_stats['total_gpt5_correct']}/{total_meetings})")
    print(f"Copilot Overall Accuracy:    {overall_copilot_accuracy:.1f}% ({overall_stats['total_copilot_correct']}/{total_meetings})")
    print()
    
    # Difficulty breakdown
    print("ACCURACY BY DIFFICULTY")
    print("-" * 80)
    for difficulty in ['easy', 'medium', 'hard']:
        stats = overall_stats['difficulty_breakdown'][difficulty]
        if stats['total'] > 0:
            gpt5_acc = (stats['gpt5_correct'] / stats['total']) * 100
            copilot_acc = (stats['copilot_correct'] / stats['total']) * 100
            print(f"{difficulty.capitalize()} ({stats['total']} meetings):")
            print(f"  GPT-5:   {stats['gpt5_correct']}/{stats['total']} = {gpt5_acc:.1f}%")
            print(f"  Copilot: {stats['copilot_correct']}/{stats['total']} = {copilot_acc:.1f}%")
    print()
    
    # Error patterns
    print("TOP ERROR PATTERNS")
    print("-" * 80)
    sorted_errors = sorted(overall_stats['error_patterns'].items(), key=lambda x: x[1], reverse=True)
    for i, (pattern, count) in enumerate(sorted_errors[:10], 1):
        print(f"{i}. {pattern} ({count} occurrences)")
    print()
    
    # Split dataset into training and evaluation
    # Use 80/20 split
    split_index = int(len(all_training_examples) * 0.8)
    training_set = all_training_examples[:split_index]
    evaluation_set = all_training_examples[split_index:]
    
    print("DATASET SPLIT")
    print("-" * 80)
    print(f"Total Examples:      {len(all_training_examples)}")
    print(f"Training Set:        {len(training_set)} (80%)")
    print(f"Evaluation Set:      {len(evaluation_set)} (20%)")
    print(f"Error Examples:      {len(all_error_examples)}")
    print()
    
    # Save datasets
    print("SAVING DATASETS")
    print("-" * 80)
    
    # Training dataset
    training_data = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'total_examples': len(training_set),
            'purpose': 'Training data for meeting classification model fine-tuning',
            'split': 'training (80%)'
        },
        'examples': training_set
    }
    save_json(training_data, TRAINING_DATASET)
    print(f"+ Training dataset saved: {TRAINING_DATASET}")
    
    # Evaluation dataset
    evaluation_data = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'total_examples': len(evaluation_set),
            'purpose': 'Evaluation data for measuring model accuracy',
            'split': 'evaluation (20%)'
        },
        'examples': evaluation_set
    }
    save_json(evaluation_data, EVALUATION_DATASET)
    print(f"+ Evaluation dataset saved: {EVALUATION_DATASET}")
    
    # Accuracy trends
    accuracy_trends = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'dates_analyzed': overall_stats['dates_validated']
        },
        'overall': {
            'total_meetings': total_meetings,
            'gpt5_accuracy': round(overall_gpt5_accuracy, 1),
            'copilot_accuracy': round(overall_copilot_accuracy, 1)
        },
        'by_date': accuracy_by_date,
        'by_difficulty': dict(overall_stats['difficulty_breakdown'])
    }
    save_json(accuracy_trends, ACCURACY_TRENDS)
    print(f"+ Accuracy trends saved: {ACCURACY_TRENDS}")
    
    # Error catalog
    error_catalog = {
        'metadata': {
            'created': datetime.now().isoformat(),
            'total_errors': len(all_error_examples),
            'unique_patterns': len(overall_stats['error_patterns'])
        },
        'error_patterns': dict(overall_stats['error_patterns']),
        'errors': all_error_examples
    }
    save_json(error_catalog, ERROR_CATALOG)
    print(f"+ Error catalog saved: {ERROR_CATALOG}")
    
    print()
    print("="*80)
    print()
    
    # Recommendations
    print("RECOMMENDATIONS")
    print("-" * 80)
    
    if total_meetings < 20:
        print("! Dataset size is small (<20 meetings)")
        print("  - Continue daily validation to grow dataset")
        print("  - Target: 50+ meetings for reliable statistics")
    elif total_meetings < 50:
        print("+ Dataset size is growing (20-50 meetings)")
        print("  - Continue validation to reach 50+ examples")
        print("  - Can start analyzing trends")
    else:
        print("+ Dataset size is substantial (50+ meetings)")
        print("  - Ready for detailed analysis")
        print("  - Can use for prompt refinement")
        print("  - Consider model fine-tuning")
    
    print()
    
    if overall_gpt5_accuracy < 80 or overall_copilot_accuracy < 80:
        print("! Accuracy below 80% threshold")
        print("  - Review top error patterns above")
        print("  - Refine prompt based on systematic errors")
        print("  - Re-run experiments after prompt updates")
    else:
        print("+ Accuracy meets 80% threshold")
        print("  - Models ready for production consideration")
        print("  - Continue monitoring accuracy trends")
    
    print()
    print("="*80)
    print()
    
    return {
        'total_meetings': total_meetings,
        'overall_accuracy': {
            'gpt5': overall_gpt5_accuracy,
            'copilot': overall_copilot_accuracy
        },
        'datasets': {
            'training': len(training_set),
            'evaluation': len(evaluation_set),
            'errors': len(all_error_examples)
        }
    }

if __name__ == '__main__':
    results = aggregate_validation_results()
    
    if results:
        print(f"Summary: {results['total_meetings']} meetings validated")
        print(f"   GPT-5: {results['overall_accuracy']['gpt5']:.1f}%")
        print(f"   Copilot: {results['overall_accuracy']['copilot']:.1f}%")
        print(f"   Training set: {results['datasets']['training']} examples")
        print(f"   Evaluation set: {results['datasets']['evaluation']} examples")
        print()
