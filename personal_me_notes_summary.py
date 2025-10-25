#!/usr/bin/env python3
"""
Personal Me Notes Summary - Your Data Only
Complete summary of YOUR Me Notes from all available sources
"""

import json
from datetime import datetime
from typing import Dict, List, Any

def load_personal_me_notes():
    """
    Load your personal Me Notes from calendar analysis
    """
    
    print('📋 Loading Your Personal Me Notes')
    print('=' * 60)
    
    try:
        # Load the generated Me Notes
        with open('real_me_notes_data.json', 'r') as f:
            me_notes = json.load(f)
        
        print(f'✅ Loaded {len(me_notes)} personal insights')
        return me_notes
        
    except FileNotFoundError:
        print('❌ Me Notes file not found')
        return []

def format_for_official_structure(me_notes):
    """
    Format your personal insights to match official Me Notes structure
    """
    
    official_me_notes = []
    
    category_mapping = {
        'WORK_RELATED': 'WORK_RELATED',
        'COLLABORATION': 'WORK_RELATED', 
        'BEHAVIORAL_PATTERN': 'PREFERENCES',
        'EXPERTISE': 'EXPERTISE',
        'INTERESTS': 'INTERESTS',
        'FOLLOW_UPS': 'FOLLOW_UPS'
    }
    
    for note in me_notes:
        # Handle different data structures
        note_text = note.get('note', note.get('insight', ''))
        context = note.get('category', note.get('context', 'WORK_RELATED'))
        
        official_note = {
            'note': note_text,
            'category': category_mapping.get(context, 'WORK_RELATED'),
            'title': generate_title_from_insight(note_text),
            'temporal_durability': note.get('temporal_durability', 'TEMPORAL_SHORT_LIVED'),
            'source': note.get('source', 'Personal Calendar Analysis'),
            'confidence': note.get('confidence', 0.85),
            'timestamp': note.get('timestamp', datetime.now().isoformat()),
            'user': 'cyl@microsoft.com'  # Your data only
        }
        
        official_me_notes.append(official_note)
    
    return official_me_notes

def generate_title_from_insight(insight_text):
    """
    Generate concise titles from insight text
    """
    
    # Common patterns and their titles
    patterns = [
        ('active in', 'Work Focus'),
        ('collaborates with', 'Collaboration Pattern'),
        ('prefers', 'Work Preference'),
        ('demonstrates', 'Professional Capability'),
        ('interest in', 'Professional Interest'),
        ('maintains', 'Work Habit')
    ]
    
    insight_lower = insight_text.lower()
    
    for pattern, title in patterns:
        if pattern in insight_lower:
            return title
    
    # Default: first few words
    words = insight_text.split()
    return ' '.join(words[:3])

def create_personal_insights_summary(official_notes):
    """
    Create a comprehensive summary of your personal insights
    """
    
    print('\n📊 Your Personal Me Notes Summary')
    print('=' * 60)
    
    # Count by category
    categories = {}
    for note in official_notes:
        cat = note['category']
        categories[cat] = categories.get(cat, 0) + 1
    
    print('📈 Insights by Category:')
    for category, count in categories.items():
        print(f'   • {category}: {count} insights')
    
    # Show confidence levels
    confidences = [note['confidence'] for note in official_notes]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    print(f'\n🎯 Average Confidence: {avg_confidence:.1%}')
    print(f'📊 Total Personal Insights: {len(official_notes)}')
    
    # Display formatted insights
    print(f'\n📋 Your Me Notes (Official Format):')
    for i, note in enumerate(official_notes, 1):
        print(f'\n{i}. 📌 {note["title"]} ({note["category"]})')
        print(f'   📝 {note["note"]}')
        print(f'   ⏱️ Temporal: {note["temporal_durability"]}')
        print(f'   🎯 Confidence: {note["confidence"]:.0%}')
    
    return {
        'total_insights': len(official_notes),
        'categories': categories,
        'average_confidence': avg_confidence,
        'user': 'cyl@microsoft.com'
    }

def save_official_format(official_notes):
    """
    Save your Me Notes in official format
    """
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'personal_me_notes_official_format_{timestamp}.json'
    
    output = {
        'user': 'cyl@microsoft.com',
        'generated_at': datetime.now().isoformat(),
        'total_notes': len(official_notes),
        'source': 'Personal Calendar Analysis (Scenara)',
        'format': 'Official Me Notes Structure',
        'notes': official_notes
    }
    
    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f'\n💾 Official format saved to: {filename}')
    return filename

def suggest_graph_explorer_tests():
    """
    Suggest specific Graph Explorer tests for your personal data
    """
    
    print(f'\n🔍 Graph Explorer Tests for Your Personal Data')
    print('=' * 60)
    print('🌐 Graph Explorer is open - try these endpoints for YOUR data:')
    
    personal_tests = [
        {
            'endpoint': 'GET /me',
            'purpose': 'Your basic profile information',
            'look_for': 'aboutMe, jobTitle, department fields'
        },
        {
            'endpoint': 'GET /me/profile',
            'purpose': 'Extended profile with potential notes',
            'look_for': 'Any notes or insights fields'
        },
        {
            'endpoint': 'GET /beta/me/profile',
            'purpose': 'Beta profile features',
            'look_for': 'Enhanced profile data with insights'
        },
        {
            'endpoint': 'GET /me/mailboxSettings',
            'purpose': 'Email settings and preferences',
            'look_for': 'Personal preferences and settings'
        },
        {
            'endpoint': 'GET /me/insights/trending',
            'purpose': 'Documents trending for you',
            'look_for': 'Your document interaction patterns'
        }
    ]
    
    for i, test in enumerate(personal_tests, 1):
        print(f'\n{i}. {test["endpoint"]}')
        print(f'   🎯 Purpose: {test["purpose"]}')
        print(f'   👀 Look for: {test["look_for"]}')

def main():
    """
    Main function for personal Me Notes summary
    """
    
    print('🎯 Your Personal Me Notes - Complete Summary')
    print('=' * 70)
    print('👤 User: cyl@microsoft.com')
    print('📊 Source: Real Microsoft 365 Calendar Data')
    print('🔧 Format: Official Me Notes Structure')
    print()
    
    # Load your Me Notes
    me_notes = load_personal_me_notes()
    
    if not me_notes:
        print('❌ No Me Notes found. Please run generate_real_me_notes.py first.')
        return
    
    # Format to official structure
    official_notes = format_for_official_structure(me_notes)
    
    # Create summary
    summary = create_personal_insights_summary(official_notes)
    
    # Save official format
    filename = save_official_format(official_notes)
    
    # Suggest additional tests
    suggest_graph_explorer_tests()
    
    print(f'\n🏆 SUCCESS: Your Personal Me Notes Ready!')
    print(f'   👤 User: cyl@microsoft.com')
    print(f'   📊 Insights: {summary["total_insights"]} personal notes')
    print(f'   🎯 Confidence: {summary["average_confidence"]:.1%} average')
    print(f'   💾 File: {filename}')
    print(f'   🔧 Format: Official Me Notes structure')
    print(f'\n💡 These are YOUR insights only - no other people\'s data!')

if __name__ == "__main__":
    main()