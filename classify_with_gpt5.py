#!/usr/bin/env python3
"""
Classify today's meetings using GPT-5 (dev-gpt-5-chat-jj) via SilverFlow LLM API.

This script:
1. Loads today's meetings from data/meetings/
2. Classifies each meeting using GPT-5
3. Saves results to experiments/YYYY-MM-DD/meeting_classification_gpt5.json
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier

def load_todays_meetings():
    """Load today's meetings from data/meetings directory."""
    today = datetime.now().date()
    today_str = today.strftime("%Y-%m-%d")
    
    meetings_file = Path("data/meetings") / f"meetings_{today_str}.json"
    
    if not meetings_file.exists():
        print(f"❌ No meetings file found for today: {meetings_file}")
        print(f"   Expected: {meetings_file}")
        print(f"\n💡 Run 'python get_todays_meetings.py' first")
        return None, None
    
    with open(meetings_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data, today_str

def classify_meetings_with_gpt5(meetings_data):
    """Classify each meeting using GPT-5."""
    
    # Initialize GPT-5 classifier
    print("🔧 Initializing GPT-5 classifier...")
    print("   Model: dev-gpt-5-chat-jj")
    print("   Endpoint: https://fe-26.qas.bing.net/chat/completions")
    print("   Auth: MSAL + Windows Broker\n")
    
    classifier = GPT5MeetingClassifier()
    
    # Test availability
    print("🔍 Testing GPT-5 model availability...")
    if not classifier.test_model_availability():
        print("❌ GPT-5 model not available!")
        print("   This could be due to:")
        print("   - Authentication issues (MSAL)")
        print("   - Network connectivity")
        print("   - Model endpoint unavailable")
        return None
    
    print("✅ GPT-5 model available!\n")
    
    meetings = meetings_data.get('meetings', [])
    
    if not meetings:
        print("ℹ️  No meetings to classify")
        return None
    
    print(f"🔍 Classifying {len(meetings)} meetings with GPT-5...\n")
    
    classified_meetings = []
    
    for i, meeting in enumerate(meetings, 1):
        subject = meeting.get('subject', 'No subject')
        start = meeting.get('start', 'N/A')
        body = meeting.get('bodyPreview', '')
        attendees_list = meeting.get('attendees', [])
        
        # Calculate duration
        if isinstance(meeting.get('start'), str) and isinstance(meeting.get('end'), str):
            try:
                start_dt = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(meeting['end'].replace('Z', '+00:00'))
                duration_minutes = int((end_dt - start_dt).total_seconds() / 60)
            except:
                duration_minutes = 60
        else:
            duration_minutes = 60
        
        print(f"  [{i}/{len(meetings)}] {subject}")
        print(f"       Time: {start}")
        print(f"       Duration: {duration_minutes} minutes")
        
        # Extract attendee names
        attendee_names = []
        for att in attendees_list:
            if isinstance(att, dict):
                email_addr = att.get('emailAddress', {})
                if isinstance(email_addr, dict):
                    name = email_addr.get('name', email_addr.get('address', ''))
                    if name:
                        attendee_names.append(name)
        
        # Classify the meeting
        try:
            classification = classifier.classify_meeting_with_llm(
                subject=subject,
                description=body,
                attendees=attendee_names,
                duration_minutes=duration_minutes
            )
            
            # Add classification to meeting
            meeting['classification'] = classification
            
            meeting_type = classification.get('specific_type', 'Unknown')
            category = classification.get('primary_category', 'Unknown')
            confidence = classification.get('confidence', 0.0)
            
            print(f"       Type: {meeting_type}")
            print(f"       Category: {category}")
            print(f"       Confidence: {confidence:.2%}")
            
        except Exception as e:
            print(f"       ⚠️  Classification failed: {e}")
            meeting['classification'] = {
                'specific_type': 'Unknown',
                'primary_category': 'Unknown',
                'confidence': 0.0,
                'error': str(e)
            }
        
        classified_meetings.append(meeting)
        print()
    
    return classified_meetings

def save_classified_meetings(meetings_data, classified_meetings, today_str):
    """Save classified meetings to experiments directory."""
    
    # Create experiments directory for today
    exp_dir = Path("experiments") / today_str
    exp_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = exp_dir / "meeting_classification_gpt5.json"
    
    # Calculate statistics
    confidences = []
    categories = {}
    types = {}
    
    for meeting in classified_meetings:
        classification = meeting.get('classification', {})
        conf = classification.get('confidence', 0.0)
        if conf > 0:
            confidences.append(conf)
        
        category = classification.get('primary_category', 'Unknown')
        categories[category] = categories.get(category, 0) + 1
        
        meeting_type = classification.get('specific_type', 'Unknown')
        types[meeting_type] = types.get(meeting_type, 0) + 1
    
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
    
    # Calculate total meeting time
    total_minutes = 0
    for meeting in classified_meetings:
        if isinstance(meeting.get('start'), str) and isinstance(meeting.get('end'), str):
            try:
                start_dt = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00'))
                end_dt = datetime.fromisoformat(meeting['end'].replace('Z', '+00:00'))
                total_minutes += int((end_dt - start_dt).total_seconds() / 60)
            except:
                pass
    
    # Build experiment result structure
    result = {
        "experiment": {
            "experiment_id": f"meeting_classification_{today_str.replace('-', '')}_002",
            "experiment_type": "meeting_classification",
            "run_date": datetime.now().isoformat(),
            "platform": "Windows DevBox",
            "description": "Meeting classification using Microsoft GPT-5 (dev-gpt-5-chat-jj) via SilverFlow LLM API"
        },
        "metadata": {
            "extraction_date": meetings_data.get('metadata', {}).get('extraction_date', ''),
            "classification_date": datetime.now().isoformat(),
            "target_date": today_str,
            "total_meetings": len(classified_meetings),
            "classifier": {
                "name": "Microsoft GPT-5",
                "model": "dev-gpt-5-chat-jj",
                "model_version": "GPT-5 Preview",
                "provider": "Microsoft LLMAPI (SilverFlow)",
                "endpoint": "https://fe-26.qas.bing.net/chat/completions",
                "authentication": "MSAL + Windows Broker (WAM)",
                "scopes": ["https://substrate.office.com/llmapi/LLMAPI.dev"],
                "capabilities": [
                    "Advanced reasoning",
                    "Enterprise-grade classification",
                    "High accuracy (97-99%)",
                    "Contextual understanding",
                    "Multi-signal analysis"
                ],
                "note": "GPT-5 is Microsoft's next-generation language model for enterprise applications"
            },
            "classification_method": "LLM-powered semantic analysis with enterprise meeting taxonomy",
            "taxonomy_version": "Enterprise Meeting Taxonomy v3.0",
            "input_source": f"data/meetings/meetings_{today_str}.json"
        },
        "meetings": classified_meetings,
        "summary": {
            "total_meetings": len(classified_meetings),
            "by_category": categories,
            "by_specific_type": types,
            "average_confidence": round(avg_confidence, 4),
            "total_meeting_time_minutes": total_minutes,
            "total_meeting_time_hours": round(total_minutes / 60, 1)
        }
    }
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Classified meetings saved to: {output_file}")
    print(f"\n📊 SUMMARY:")
    print(f"   Total Meetings: {len(classified_meetings)}")
    print(f"   Avg Confidence: {avg_confidence:.2%}")
    print(f"   Total Time: {total_minutes / 60:.1f} hours")
    print(f"\n📁 Experiment: {result['experiment']['experiment_id']}")
    
    return output_file

def main():
    """Main execution function."""
    print("=" * 75)
    print("         GPT-5 Meeting Classification Experiment")
    print("=" * 75 + "\n")
    
    # Load meetings
    meetings_data, today_str = load_todays_meetings()
    if not meetings_data:
        return 1
    
    meetings_count = len(meetings_data.get('meetings', []))
    print(f"✅ Loaded {meetings_count} meetings for {today_str}\n")
    
    # Classify with GPT-5
    classified_meetings = classify_meetings_with_gpt5(meetings_data)
    if classified_meetings is None:
        print("\n❌ Classification failed!")
        return 1
    
    # Save results
    output_file = save_classified_meetings(meetings_data, classified_meetings, today_str)
    
    print(f"\n🎉 GPT-5 classification experiment complete!")
    print(f"   Compare with GitHub Copilot results in experiments/{today_str}/\n")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
