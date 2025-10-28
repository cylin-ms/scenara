"""
Classify today's meetings using the meeting type classifier.

This script:
1. Loads today's meetings from data/meetings/
2. Classifies each meeting using the LLM-based classifier
3. Saves results with classifications included
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from tools.meeting_classifier_gpt4o import classify_meeting
    classifier_version = "GPT-4o"
except ImportError:
    try:
        from tools.meeting_classifier import classify_meeting
        classifier_version = "Keyword-based"
    except ImportError:
        print("❌ Error: Could not import meeting classifier")
        print("Available classifiers:")
        print("  - tools.meeting_classifier_gpt4o (preferred)")
        print("  - tools.meeting_classifier (fallback)")
        sys.exit(1)

def load_todays_meetings():
    """Load today's meetings from data/meetings directory."""
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    
    meetings_file = Path("data/meetings") / f"meetings_{today_str}.json"
    
    if not meetings_file.exists():
        print(f"❌ No meetings file found for today: {meetings_file}")
        print(f"Run 'python get_todays_meetings.py' first")
        return None
    
    with open(meetings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def classify_meetings(meetings_data):
    """Classify each meeting in the data."""
    meetings = meetings_data.get('meetings', [])
    
    if not meetings:
        print("ℹ️  No meetings to classify")
        return meetings_data
    
    print(f"🔍 Classifying {len(meetings)} meetings...")
    print(f"   Using classifier: {classifier_version}\n")
    
    classified_meetings = []
    
    for i, meeting in enumerate(meetings, 1):
        subject = meeting.get('subject', 'No subject')
        start_time = meeting.get('start', {}).get('dateTime', 'N/A')
        
        print(f"  [{i}/{len(meetings)}] {subject}")
        print(f"       Time: {start_time}")
        
        # Classify the meeting
        try:
            classification = classify_meeting(meeting)
            meeting['classification'] = classification
            
            meeting_type = classification.get('type', 'Unknown')
            confidence = classification.get('confidence', 0)
            
            print(f"       Type: {meeting_type} (confidence: {confidence:.2f})")
            
        except Exception as e:
            print(f"       ⚠️  Classification failed: {e}")
            meeting['classification'] = {
                'type': 'Unknown',
                'confidence': 0.0,
                'error': str(e)
            }
        
        classified_meetings.append(meeting)
        print()
    
    return classified_meetings

def save_classified_meetings(meetings_data, classified_meetings):
    """Save classified meetings to file."""
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    
    output_file = Path("data/meetings") / f"meetings_{today_str}_classified.json"
    
    # Update metadata
    metadata = meetings_data.get('metadata', {})
    metadata['classification_date'] = datetime.now().isoformat()
    metadata['classifier_version'] = classifier_version
    metadata['total_classified'] = len([m for m in classified_meetings if 'classification' in m])
    metadata['high_confidence'] = len([
        m for m in classified_meetings 
        if m.get('classification', {}).get('confidence', 0) > 0.8
    ])
    
    # Create output structure
    output = {
        'metadata': metadata,
        'meetings': classified_meetings
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved classified meetings to: {output_file}")
    return output_file

def print_summary(classified_meetings):
    """Print classification summary."""
    if not classified_meetings:
        return
    
    print("\n📊 Classification Summary:")
    print(f"   Total meetings: {len(classified_meetings)}")
    
    classified_count = len([m for m in classified_meetings if 'classification' in m])
    print(f"   Successfully classified: {classified_count}")
    
    high_conf = len([
        m for m in classified_meetings 
        if m.get('classification', {}).get('confidence', 0) > 0.8
    ])
    print(f"   High confidence (>0.8): {high_conf}")
    
    # Count by type
    type_counts = {}
    for meeting in classified_meetings:
        meeting_type = meeting.get('classification', {}).get('type', 'Unknown')
        type_counts[meeting_type] = type_counts.get(meeting_type, 0) + 1
    
    if type_counts:
        print("\n   Meeting types:")
        for meeting_type, count in sorted(type_counts.items(), key=lambda x: x[1], reverse=True):
            print(f"     - {meeting_type}: {count}")

def main():
    """Main execution function."""
    print("🎯 Meeting Classification Tool\n")
    
    # Load today's meetings
    meetings_data = load_todays_meetings()
    if not meetings_data:
        return 1
    
    total_meetings = meetings_data.get('metadata', {}).get('total_meetings', 0)
    target_date = meetings_data.get('metadata', {}).get('target_date', 'Unknown')
    
    print(f"📅 Date: {target_date}")
    print(f"📋 Meetings found: {total_meetings}\n")
    
    if total_meetings == 0:
        print("ℹ️  No meetings to classify")
        return 0
    
    # Classify meetings
    classified_meetings = classify_meetings(meetings_data)
    
    # Save results
    output_file = save_classified_meetings(meetings_data, classified_meetings)
    
    # Print summary
    print_summary(classified_meetings)
    
    print(f"\n✅ Classification complete!")
    print(f"📄 Results saved to: {output_file}")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
