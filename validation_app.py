"""
Meeting Classification Validation Web App
==========================================

A Flask-based web application for human validation of AI meeting classifications.

Features:
- Display meetings with AI classifications
- Rate classifications (correct/incorrect)
- Select correct type from full taxonomy
- Track validation progress
- Export validation results
- Calculate accuracy metrics

Author: Scenara 2.0 Project
Date: October 28, 2025
"""

from flask import Flask, render_template, request, jsonify, send_file
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

app = Flask(__name__)

# Configuration
DATA_DIR = Path(__file__).parent / "data" / "meetings"
EXPERIMENTS_DIR = Path(__file__).parent / "experiments" / "2025-10-28"
VALIDATION_FILE = EXPERIMENTS_DIR / "human_validation_results.json"

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

def load_meetings() -> List[Dict[str, Any]]:
    """Load meetings from today's data file."""
    meetings_file = DATA_DIR / "meetings_2025-10-28.json"
    with open(meetings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data['meetings']

def load_classifications(model: str) -> Dict[str, Any]:
    """Load classification results for a specific model."""
    if model == "gpt5":
        file = EXPERIMENTS_DIR / "meeting_classification_gpt5.json"
    elif model == "copilot":
        file = EXPERIMENTS_DIR / "meeting_classification_github_copilot.json"
    else:
        raise ValueError(f"Unknown model: {model}")
    
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Create lookup by meeting number (index)
    # GitHub Copilot file uses meeting_number, GPT-5 has full meeting objects with id
    classifications = {}
    for i, meeting in enumerate(data['meetings']):
        # Use index as key for both (0-based)
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
    meetings = load_meetings()
    gpt5_classifications = load_classifications("gpt5")
    copilot_classifications = load_classifications("copilot")
    validation_results = load_validation_results()
    
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
            'gpt5': gpt5_classifications.get(i, {}),
            'copilot': copilot_classifications.get(i, {}),
            'validation': validation_results['validations'].get(meeting_id, {})
        })
    
    return render_template('validation.html', 
                         meetings=combined_meetings,
                         taxonomy=TAXONOMY,
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
        'gpt5_correct': data.get('gpt5_correct'),
        'copilot_correct': data.get('copilot_correct'),
        'correct_type': data.get('correct_type'),
        'correct_category': data.get('correct_category'),
        'notes': data.get('notes', ''),
        'difficulty': data.get('difficulty', 'medium')
    }
    
    # Update counts
    validation_results['validated_count'] = len(validation_results['validations'])
    validation_results['total_meetings'] = data.get('total_meetings', 8)
    
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
            'gpt5_accuracy': 0,
            'copilot_accuracy': 0
        })
    
    validations = validation_results['validations']
    gpt5_correct = sum(1 for v in validations.values() if v.get('gpt5_correct'))
    copilot_correct = sum(1 for v in validations.values() if v.get('copilot_correct'))
    total = len(validations)
    
    return jsonify({
        'total': validation_results['total_meetings'],
        'validated': total,
        'gpt5_accuracy': round(gpt5_correct / total * 100, 1) if total > 0 else 0,
        'copilot_accuracy': round(copilot_correct / total * 100, 1) if total > 0 else 0,
        'progress': round(total / validation_results['total_meetings'] * 100, 1) if validation_results['total_meetings'] > 0 else 0
    })

@app.route('/api/export')
def export_results():
    """Export validation results as JSON."""
    return send_file(VALIDATION_FILE, as_attachment=True, download_name='validation_results.json')

@app.route('/api/report')
def generate_report():
    """Generate detailed validation report."""
    validation_results = load_validation_results()
    meetings = load_meetings()
    gpt5_classifications = load_classifications("gpt5")
    copilot_classifications = load_classifications("copilot")
    
    validations = validation_results['validations']
    
    # Calculate metrics
    gpt5_correct = []
    copilot_correct = []
    errors_gpt5 = []
    errors_copilot = []
    
    for meeting_id, validation in validations.items():
        if validation.get('gpt5_correct'):
            gpt5_correct.append(meeting_id)
        else:
            # Find meeting subject
            meeting = next((m for m in meetings if m['id'] == meeting_id), None)
            if meeting:
                gpt5_class = gpt5_classifications.get(meeting_id, {})
                errors_gpt5.append({
                    'subject': meeting['subject'],
                    'ai_type': gpt5_class.get('specific_type', 'Unknown'),
                    'correct_type': validation.get('correct_type', 'Unknown'),
                    'confidence': gpt5_class.get('confidence', 0)
                })
        
        if validation.get('copilot_correct'):
            copilot_correct.append(meeting_id)
        else:
            meeting = next((m for m in meetings if m['id'] == meeting_id), None)
            if meeting:
                copilot_class = copilot_classifications.get(meeting_id, {})
                errors_copilot.append({
                    'subject': meeting['subject'],
                    'ai_type': copilot_class.get('specific_type', 'Unknown'),
                    'correct_type': validation.get('correct_type', 'Unknown'),
                    'confidence': copilot_class.get('confidence', 0)
                })
    
    total = len(validations)
    
    report = {
        'summary': {
            'total_meetings': validation_results['total_meetings'],
            'validated_meetings': total,
            'gpt5_accuracy': round(len(gpt5_correct) / total * 100, 1) if total > 0 else 0,
            'copilot_accuracy': round(len(copilot_correct) / total * 100, 1) if total > 0 else 0,
            'cross_model_agreement': 87.5,  # From previous analysis
        },
        'gpt5_errors': errors_gpt5,
        'copilot_errors': errors_copilot,
        'validation_date': validation_results['validation_date'],
        'validator': validation_results['validator']
    }
    
    return jsonify(report)

if __name__ == '__main__':
    print("\n" + "="*70)
    print("  MEETING CLASSIFICATION VALIDATION APP")
    print("="*70)
    print("\nStarting validation server...")
    print(f"Data directory: {DATA_DIR}")
    print(f"Experiments directory: {EXPERIMENTS_DIR}")
    print(f"Validation results: {VALIDATION_FILE}")
    print("\nOpen your browser to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
