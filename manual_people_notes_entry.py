#!/usr/bin/env python3
"""
Manual People Notes Data Entry
If browser automation is complex, use this to manually enter the data
"""

import json
from datetime import datetime

def manual_people_notes_entry():
    """
    Manual entry system for People Notes data
    """
    
    print('📝 Manual People Notes Data Entry')
    print('=' * 60)
    print('📋 Instructions:')
    print('   1. Open the SharePoint People Notes page in browser')
    print('   2. Copy the people and notes information')
    print('   3. Enter it below')
    print()
    
    people_notes = []
    
    while True:
        print('\n👤 Enter person information (or "done" to finish):')
        
        name = input('Name: ').strip()
        if name.lower() == 'done':
            break
            
        email = input('Email: ').strip()
        job_title = input('Job Title: ').strip()
        notes = input('Notes/Insights: ').strip()
        
        person_data = {
            'name': name,
            'email': email,
            'jobTitle': job_title,
            'notes': notes,
            'source': 'manual_entry',
            'timestamp': datetime.now().isoformat()
        }
        
        people_notes.append(person_data)
        print(f'✅ Added {name}')
    
    # Save to file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'people_notes_manual_{timestamp}.json'
    
    with open(filename, 'w') as f:
        json.dump(people_notes, f, indent=2)
    
    print(f'\n💾 Saved {len(people_notes)} entries to: {filename}')
    
    # Convert to Scenara format
    scenara_notes = []
    for person in people_notes:
        if person['notes']:
            scenara_note = {
                'person': person['name'],
                'email': person['email'],
                'insight': person['notes'],
                'source': 'Official Microsoft People Notes (manual)',
                'confidence': 1.0,
                'timestamp': person['timestamp']
            }
            scenara_notes.append(scenara_note)
    
    scenara_filename = f'scenara_people_notes_{timestamp}.json'
    with open(scenara_filename, 'w') as f:
        json.dump(scenara_notes, f, indent=2)
    
    print(f'💾 Converted to Scenara format: {scenara_filename}')
    
    return people_notes

if __name__ == "__main__":
    manual_people_notes_entry()
