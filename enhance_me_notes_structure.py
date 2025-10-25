#!/usr/bin/env python3
"""
Enhanced Me Notes Generation Following Official Structure
Since official access methods require missing files, enhance our working system
"""

import json
from datetime import datetime
from typing import Dict, List, Any

def enhance_existing_me_notes():
    """
    Enhance our existing calendar-based Me Notes with official structure
    """
    
    print('🔧 Enhancing Existing Me Notes with Official Structure')
    print('=' * 60)
    
    # Load our existing calendar-based Me Notes
    try:
        with open('real_me_notes_20251022_040030.json', 'r') as f:
            existing_notes = json.load(f)
        print(f'✅ Loaded {len(existing_notes)} existing calendar-based insights')
    except FileNotFoundError:
        print('❌ Previous Me Notes file not found')
        return None
    
    # Convert to official Me Notes structure
    official_me_notes = []
    
    for note in existing_notes:
        # Map to official structure
        official_note = {
            'note': note['insight'],  # The actual insight text
            'category': categorize_insight(note['insight']),  # WORK_RELATED, FOLLOW_UPS, etc.
            'title': generate_title(note['insight']),  # Short description
            'temporal_durability': 'TEMPORAL_SHORT_LIVED',  # Most calendar insights are short-lived
            'source': 'Calendar Analysis (Scenara Enhanced)',
            'confidence': note.get('confidence', 0.8),
            'original_source': note.get('source', 'Calendar events'),
            'timestamp': note.get('timestamp', datetime.now().isoformat())
        }
        
        official_me_notes.append(official_note)
    
    # Save enhanced version
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'enhanced_me_notes_official_structure_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(official_me_notes, f, indent=2)
    
    print(f'💾 Enhanced Me Notes saved to: {filename}')
    
    # Display sample
    print('\n📋 Sample Enhanced Me Notes (Official Structure):')
    for i, note in enumerate(official_me_notes[:3], 1):
        print(f'\n{i}. {note["title"]} ({note["category"]})')
        print(f'   📝 Note: {note["note"][:100]}...')
        print(f'   ⏱️ Temporal: {note["temporal_durability"]}')
    
    return official_me_notes

def categorize_insight(insight_text: str) -> str:
    """
    Categorize insights based on content (matching official categories)
    """
    
    insight_lower = insight_text.lower()
    
    # Based on documentation: FOLLOW_UPS, WORK_RELATED, etc.
    if any(word in insight_lower for word in ['follow up', 'action item', 'todo', 'task']):
        return 'FOLLOW_UPS'
    elif any(word in insight_lower for word in ['project', 'meeting', 'work', 'collaboration']):
        return 'WORK_RELATED'
    elif any(word in insight_lower for word in ['skill', 'expertise', 'knowledge']):
        return 'EXPERTISE'
    elif any(word in insight_lower for word in ['preference', 'style', 'approach']):
        return 'PREFERENCES'
    else:
        return 'WORK_RELATED'  # Default category

def generate_title(insight_text: str) -> str:
    """
    Generate short titles for insights (3-7 words)
    """
    
    # Extract key phrases
    words = insight_text.split()
    
    if len(words) <= 5:
        return insight_text
    
    # Try to find key action or subject
    key_patterns = [
        ('working on', 'Work Focus'),
        ('meeting with', 'Collaboration'),
        ('expert in', 'Expertise'),
        ('responsible for', 'Responsibility'),
        ('interested in', 'Interest'),
        ('prefers', 'Preference')
    ]
    
    for pattern, title_prefix in key_patterns:
        if pattern in insight_text.lower():
            return f"{title_prefix}: {' '.join(words[:4])}"
    
    # Default: first few words
    return ' '.join(words[:4])

def create_me_notes_comparison():
    """
    Create comparison between our enhanced notes and official structure
    """
    
    comparison = {
        'our_approach': {
            'source': 'Microsoft Calendar events',
            'method': 'Local AI inference',
            'structure': 'Enhanced to match official format',
            'benefits': ['Privacy compliant', 'Working immediately', 'Full control'],
            'limitations': ['Single data source', 'Not official Microsoft data']
        },
        'official_approach': {
            'source': 'M365 emails, chats, meeting transcripts',
            'method': 'Microsoft AI extraction',
            'structure': 'Official Me Notes format',
            'benefits': ['Multi-source data', 'Official Microsoft insights', 'Rich context'],
            'limitations': ['Access complexity', 'Missing tools/files', 'Privacy concerns']
        }
    }
    
    print('\n📊 Approach Comparison')
    print('=' * 60)
    
    for approach, details in comparison.items():
        print(f'\n🔧 {approach.replace("_", " ").title()}:')
        print(f'   📥 Source: {details["source"]}')
        print(f'   🛠️ Method: {details["method"]}')
        print(f'   📋 Structure: {details["structure"]}')
        print(f'   ✅ Benefits: {", ".join(details["benefits"])}')
        print(f'   ❌ Limitations: {", ".join(details["limitations"])}')
    
    return comparison

def main():
    """
    Main function to enhance existing approach
    """
    
    print('🔧 Enhanced Me Notes Strategy')
    print('=' * 70)
    print('💡 Since official access requires missing files...')
    print('🚀 Enhancing our working calendar-based system!')
    print()
    
    # Enhance existing notes
    enhanced_notes = enhance_existing_me_notes()
    
    # Create comparison
    comparison = create_me_notes_comparison()
    
    print('\n🎯 RECOMMENDATION:')
    print('   ✅ Use our enhanced system (working now)')
    print('   🔧 Official structure compliance achieved')
    print('   📊 Proper categorization and formatting')
    print('   🚀 Ready for Scenara integration')
    print()
    print('💡 PARALLEL TRACK:')
    print('   📞 Contact Me Notes team for proper access files')
    print('   🔍 Continue exploring SharePoint personalization site')
    print('   🔧 Eventually integrate official data when accessible')

if __name__ == "__main__":
    main()