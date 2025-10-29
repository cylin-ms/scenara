"""
Meeting Classification Validation Web App - Single Model Version
=================================================================

A Flask-based web application for human validation of AI meeting classifications.
This version evaluates ONE model's classification at a time.

Features:
- Display meetings with AI classifications from selected model
- Rate classifications (correct/incorrect)
- Select correct type from full taxonomy
- Track validation progress
- Export validation results
- Calculate accuracy metrics

Author: Scenara 2.0 Project
Date: October 29, 2025
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

app = Flask(__name__)

# Configuration - will be set via command line argument
TARGET_DATE = None
MODEL_NAME = None  # e.g., "gpt5", "copilot", "gpt4o"
DATA_DIR = Path(__file__).parent / "data" / "meetings"
EXPERIMENTS_DIR = None
VALIDATION_FILE = None

def configure_app(target_date: str, model_name: str):
    """Configure app with specific date and model."""
    global TARGET_DATE, MODEL_NAME, EXPERIMENTS_DIR, VALIDATION_FILE
    TARGET_DATE = target_date
    MODEL_NAME = model_name
    EXPERIMENTS_DIR = Path(__file__).parent / "experiments" / TARGET_DATE
    VALIDATION_FILE = EXPERIMENTS_DIR / f"human_validation_{model_name}.json"

# Meeting taxonomy
TAXONOMY = {
    "Internal Recurring Meetings (Cadence)": [
        "Team Status Update Meetings",
        "Progress Review Meetings",
        "One-on-One Meetings",
        "Action Review Meetings",
        "Governance & Strategy Cadence"
    ],
    "Strategic Planning & Decision Meetings": [
        "Planning Sessions",
        "Decision-Making Meetings",
        "Problem-Solving / Incident Resolution Meetings",
        "Brainstorming / Innovation Meetings",
        "Workshops & Design Sessions"
    ],
    "External & Client-Facing Meetings": [
        "Sales & Client Meetings",
        "Vendor/Supplier Meetings",
        "Partnership/Business Development Meetings",
        "Interviews and Recruiting Meetings",
        "Client Training or Onboarding"
    ],
    "Informational & Broadcast Meetings": [
        "All-Hands / Town Hall Meetings",
        "Informational Briefings",
        "Training & Education Sessions",
        "Webinars and Broadcasts"
    ],
    "Team-Building & Culture Meetings": [
        "Team-Building Activities",
        "Recognition & Social Events",
        "Communities of Practice & Networking Meets"
    ]
}

# Model display names and metadata
MODEL_INFO = {
    "gpt5": {
        "display_name": "GPT-5",
        "icon": "🤖",
        "color": "#8b5cf6",
        "bg_color": "#f5f3ff"
    },
    "copilot": {
        "display_name": "GitHub Copilot",
        "icon": "🤖",
        "color": "#3b82f6",
        "bg_color": "#eff6ff"
    },
    "gpt4o": {
        "display_name": "GPT-4o",
        "icon": "🤖",
        "color": "#10b981",
        "bg_color": "#f0fdf4"
    },
    "claude": {
        "display_name": "Claude",
        "icon": "🤖",
        "color": "#f59e0b",
        "bg_color": "#fffbeb"
    }
}

def load_meetings() -> List[Dict[str, Any]]:
    """Load meetings from data file."""
    meetings_file = DATA_DIR / f"meetings_{TARGET_DATE}.json"
    with open(meetings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['meetings']

def load_classifications() -> Dict[int, Dict[str, Any]]:
    """Load classification results for the selected model."""
    # Map model names to file names
    file_mapping = {
        "gpt5": "meeting_classification_gpt5.json",
        "copilot": "meeting_classification_github_copilot.json",
        "gpt4o": "meeting_classification_gpt4o.json",
        "claude": "meeting_classification_claude.json"
    }
    
    file_name = file_mapping.get(MODEL_NAME)
    if not file_name:
        raise ValueError(f"Unknown model: {MODEL_NAME}")
    
    file_path = EXPERIMENTS_DIR / file_name
    
    # Return empty dict if file doesn't exist
    if not file_path.exists():
        print(f"Warning: Classification file not found: {file_path}")
        return {}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create lookup by meeting index
    classifications = {}
    for i, meeting in enumerate(data.get('meetings', [])):
        classifications[i] = meeting.get('classification', {})
    
    return classifications

def load_validation_results() -> Dict[str, Any]:
    """Load existing validation results or create empty structure."""
    if VALIDATION_FILE.exists():
        with open(VALIDATION_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    return {
        "validation_date": datetime.now().isoformat(),
        "validator": "Human Expert",
        "model": MODEL_NAME,
        "model_display_name": MODEL_INFO.get(MODEL_NAME, {}).get("display_name", MODEL_NAME),
        "total_meetings": 0,
        "validated_count": 0,
        "validations": {}
    }

def save_validation_results(results: Dict[str, Any]):
    """Save validation results to file."""
    VALIDATION_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(VALIDATION_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, indent=2, fp=f)

@app.route('/')
def index():
    """Main validation interface."""
    print(f"DEBUG: TARGET_DATE = {TARGET_DATE}")
    print(f"DEBUG: MODEL_NAME = {MODEL_NAME}")
    print(f"DEBUG: EXPERIMENTS_DIR = {EXPERIMENTS_DIR}")
    print(f"DEBUG: Loading meetings file: data/meetings/meetings_{TARGET_DATE}.json")
    
    meetings = load_meetings()
    print(f"DEBUG: Loaded {len(meetings)} meetings")
    if meetings:
        print(f"DEBUG: First meeting: {meetings[0].get('subject')}")
    
    classifications = load_classifications()
    validation_results = load_validation_results()
    model_info = MODEL_INFO.get(MODEL_NAME, {
        "display_name": MODEL_NAME,
        "icon": "🤖",
        "color": "#667eea",
        "bg_color": "#f5f3ff"
    })
    
    # Combine data
    combined_meetings = []
    for i, meeting in enumerate(meetings):
        meeting_id = meeting['id']
        combined_meetings.append({
            'id': meeting_id,
            'subject': meeting['subject'],
            'bodyPreview': meeting.get('bodyPreview', ''),
            'start': meeting['start']['dateTime'],
            'end': meeting['end']['dateTime'],
            'attendees': len(meeting.get('attendees', [])),
            'classification': classifications.get(i, {}),
            'validation': validation_results['validations'].get(meeting_id, {})
        })
    
    return render_template('validation_single.html', 
                         meetings=combined_meetings,
                         taxonomy=TAXONOMY,
                         model_info=model_info,
                         target_date=TARGET_DATE,
                         validation_stats={
                             'total': len(meetings),
                             'validated': validation_results['validated_count']
                         })

@app.route('/api/validate', methods=['POST'])
def validate_meeting():
    """Save validation for a meeting."""
    data = request.json
    validation_results = load_validation_results()
    
    meeting_id = data['meeting_id']
    validation_results['validations'][meeting_id] = {
        'timestamp': datetime.now().isoformat(),
        'is_correct': data.get('is_correct'),
        'correct_type': data.get('correct_type'),
        'correct_category': data.get('correct_category'),
        'notes': data.get('notes', ''),
        'difficulty': data.get('difficulty', 'medium')
    }
    
    # Update counts
    validation_results['validated_count'] = len(validation_results['validations'])
    validation_results['total_meetings'] = data.get('total_meetings', len(validation_results['validations']))
    
    save_validation_results(validation_results)
    
    return jsonify({'success': True, 'validated_count': validation_results['validated_count']})

@app.route('/api/stats')
def get_stats():
    """Get validation statistics."""
    validation_results = load_validation_results()
    
    if not validation_results['validations']:
        return jsonify({
            'total': 0,
            'validated': 0,
            'accuracy': 0,
            'progress': 0
        })
    
    validations = validation_results['validations']
    correct_count = sum(1 for v in validations.values() if v.get('is_correct'))
    total = len(validations)
    
    return jsonify({
        'total': validation_results['total_meetings'],
        'validated': total,
        'accuracy': round(correct_count / total * 100, 1) if total > 0 else 0,
        'progress': round(total / validation_results['total_meetings'] * 100, 1) if validation_results['total_meetings'] > 0 else 0
    })

@app.route('/api/export')
def export_results():
    """Export validation results as JSON."""
    return send_file(VALIDATION_FILE, as_attachment=True, 
                    download_name=f'validation_{MODEL_NAME}_{TARGET_DATE}.json')

@app.route('/api/report')
def generate_report():
    """Generate detailed validation report."""
    validation_results = load_validation_results()
    meetings = load_meetings()
    classifications = load_classifications()
    
    validations = validation_results['validations']
    
    # Calculate metrics
    correct_classifications = []
    errors = []
    
    for i, meeting in enumerate(meetings):
        meeting_id = meeting['id']
        validation = validations.get(meeting_id)
        
        if not validation:
            continue
            
        if validation.get('is_correct'):
            correct_classifications.append(meeting_id)
        else:
            classification = classifications.get(i, {})
            errors.append({
                'subject': meeting['subject'],
                'ai_type': classification.get('specific_type', 'Unknown'),
                'correct_type': validation.get('correct_type', 'Unknown'),
                'confidence': classification.get('confidence', 0),
                'difficulty': validation.get('difficulty', 'medium'),
                'notes': validation.get('notes', '')
            })
    
    total = len(validations)
    
    report = {
        'summary': {
            'model': MODEL_NAME,
            'model_display_name': MODEL_INFO.get(MODEL_NAME, {}).get("display_name", MODEL_NAME),
            'target_date': TARGET_DATE,
            'total_meetings': validation_results['total_meetings'],
            'validated_meetings': total,
            'accuracy': round(len(correct_classifications) / total * 100, 1) if total > 0 else 0,
            'correct_count': len(correct_classifications),
            'error_count': len(errors)
        },
        'errors': errors,
        'validation_date': validation_results['validation_date'],
        'validator': validation_results['validator']
    }
    
    return jsonify(report)

if __name__ == '__main__':
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("\n❌ ERROR: Model name required")
        print("\nUsage: python validation_app_single.py <model> [date]")
        print("\nExamples:")
        print("  python validation_app_single.py gpt5")
        print("  python validation_app_single.py copilot 2025-10-29")
        print("\nAvailable models: gpt5, copilot, gpt4o, claude")
        sys.exit(1)
    
    model_name = sys.argv[1]
    
    if len(sys.argv) > 2:
        target_date = sys.argv[2]
    else:
        target_date = datetime.now().strftime('%Y-%m-%d')
    
    # Configure app with target date and model
    configure_app(target_date, model_name)
    
    model_display = MODEL_INFO.get(model_name, {}).get("display_name", model_name)
    
    print("\n" + "="*70)
    print(f"  MEETING CLASSIFICATION VALIDATION - {model_display}")
    print("="*70)
    print(f"\n📅 Target Date: {TARGET_DATE}")
    print(f"🤖 Model: {model_display}")
    print("\nStarting validation server...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Experiments directory: {EXPERIMENTS_DIR}")
    print(f"Validation results: {VALIDATION_FILE}")
    print("\nOpen your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
