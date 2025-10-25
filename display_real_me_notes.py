#!/usr/bin/env python3
"""
Real Me Notes Report Generator
Displays Me Notes generated from actual Microsoft 365 calendar data
"""

import json
import os
from datetime import datetime
from pathlib import Path

def display_real_me_notes(user_email: str = "cyl@microsoft.com"):
    """Display Me Notes generated from real calendar data"""
    
    cache_file = f'me_notes_cache_{user_email.replace("@", "_").replace(".", "_")}.json'
    
    if not os.path.exists(cache_file):
        print(f'❌ No real Me Notes cache found: {cache_file}')
        return False
    
    with open(cache_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print('🧠 Real Me Notes Report - Generated from Microsoft 365 Calendar Data')
    print('=' * 80)
    print()
    
    # Header information
    print(f'👤 User: {data["user_email"]}')
    print(f'📊 Data Source: {data["data_source"]}')
    print(f'🔍 Generation Method: {data["generation_method"]}')
    print(f'🤖 Official Me Notes API: {data.get("official_me_notes_api", "Unknown")}')
    if 'inference_disclaimer' in data:
        print(f'⚠️  Disclaimer: {data["inference_disclaimer"]}')
    print(f'📅 Meetings Analyzed: {data["total_meetings_analyzed"]} real calendar events')
    print(f'📁 Source File: {data["calendar_file_source"]}')
    print(f'🕒 Generated: {data["last_updated"]}')
    print(f'🔐 Data Authenticity: {data["metadata"]["data_authenticity"]}')
    print()
    
    # Metadata summary
    metadata = data['metadata']
    print('📊 Analysis Summary:')
    print(f'   • Total Insights Generated: {metadata["total_insights_generated"]}')
    print(f'   • Confidence Range: {metadata["confidence_range"]}')
    print(f'   • Source Type: {metadata.get("source_type", "UNKNOWN")}')
    print(f'   • Official API Source: {metadata.get("official_api_source", "Unknown")}')
    if 'inference_methods' in metadata:
        print(f'   • Inference Methods: {", ".join(metadata["inference_methods"])}')
    print(f'   • Meeting Subjects Analyzed: {metadata["meeting_subjects_analyzed"]}')
    print(f'   • Unique Collaborators: {metadata["unique_collaborators"]}')
    print(f'   • AI-Related Meetings: {metadata["ai_related_meetings"]}')
    print(f'   • Collaboration Meetings: {metadata["collaboration_meetings"]}')
    print()
    
    # Display insights by category
    me_notes = data['me_notes']
    categories = {}
    for note in me_notes:
        cat = note['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(note)
    
    category_icons = {
        'WORK_RELATED': '💼',
        'COLLABORATION': '🤝',
        'BEHAVIORAL_PATTERN': '🧭',
        'EXPERTISE': '🎯',
        'INTERESTS': '💡',
        'FOLLOW_UPS': '📋'
    }
    
    for category, notes in categories.items():
        icon = category_icons.get(category, '📝')
        print(f'{icon} {category.replace("_", " ").title()} ({len(notes)} insights)')
        print('-' * 60)
        
        for note in notes:
            title = note.get('title', 'Untitled')
            print(f'📌 **{title}**')
            print(f'   {note["note"]}')
            print(f'   🎯 Confidence: {note["confidence"]*100:.0f}%')
            print(f'   ⏳ Durability: {note["durability"]}')
            print(f'   📡 Source: {note["source"]}')
            print(f'   � Source Type: {note.get("source_type", "UNKNOWN")}')
            print(f'   🤖 Official API: {note.get("official_me_notes_api", "Unknown")}')
            if note.get('inference_method'):
                print(f'   🧠 Inference Method: {note["inference_method"]}')
            print(f'   �🔐 Data Auth: {note["data_authenticity"]}')
            if note.get('source_meetings'):
                print(f'   📅 Source Meetings:')
                for meeting in note['source_meetings'][:3]:  # Show up to 3
                    print(f'      • {meeting}')
            print()
    
    # Save formatted report
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_dir = Path('me_notes_reports')
    report_dir.mkdir(exist_ok=True)
    
    # Markdown report
    md_file = report_dir / f'real_me_notes_{user_email.replace("@", "_").replace(".", "_")}_{timestamp}.md'
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f'# 🧠 Real Me Notes Report for {data["user_email"]}\n\n')
        f.write(f'*Generated from actual Microsoft 365 calendar data on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}*\n\n')
        f.write('---\n\n')
        
        f.write('## 📊 Data Source Information\n\n')
        f.write(f'- **Data Source**: {data["data_source"]}\n')
        f.write(f'- **Generation Method**: {data["generation_method"]}\n')
        f.write(f'- **Meetings Analyzed**: {data["total_meetings_analyzed"]} real calendar events\n')
        f.write(f'- **Source File**: `{data["calendar_file_source"]}`\n')
        f.write(f'- **Data Authenticity**: {metadata["data_authenticity"]}\n')
        f.write(f'- **Total Insights**: {metadata["total_insights_generated"]}\n')
        f.write(f'- **Confidence Range**: {metadata["confidence_range"]}\n\n')
        
        f.write('---\n\n')
        
        for category, notes in categories.items():
            icon = category_icons.get(category, '📝')
            f.write(f'## {icon} {category.replace("_", " ").title()}\n\n')
            f.write(f'*{len(notes)} insights from real calendar analysis*\n\n')
            
            for i, note in enumerate(notes, 1):
                title = note.get('title', 'Untitled')
                f.write(f'### {i}. {title}\n\n')
                f.write(f'**{note["note"]}**\n\n')
                f.write(f'- 🎯 **Confidence**: {note["confidence"]*100:.0f}%\n')
                f.write(f'- ⏳ **Durability**: {note["durability"]}\n')
                f.write(f'- 📡 **Source**: {note["source"]}\n')
                f.write(f'- 🔐 **Data Authenticity**: {note["data_authenticity"]}\n')
                
                if note.get('source_meetings'):
                    f.write(f'- 📅 **Source Meetings**:\n')
                    for meeting in note['source_meetings'][:3]:
                        f.write(f'  - {meeting}\n')
                f.write('\n')
    
    print(f'📄 Real Me Notes report saved to: {md_file}')
    print()
    print('✅ Real Me Notes display completed!')
    print(f'🔍 All data sourced from: {data["data_source"]}')
    print(f'🎯 Data authenticity verified as: {metadata["data_authenticity"]}')
    
    return True

def main():
    """Main function"""
    import sys
    
    user_email = "cyl@microsoft.com"
    if len(sys.argv) > 1:
        user_email = sys.argv[1]
    
    display_real_me_notes(user_email)

if __name__ == "__main__":
    main()