#!/usr/bin/env python3
"""
GitHub Copilot Meeting Classification Experiment
Uses GitHub Copilot's LLM directly for classification comparison
"""

import json
import os
from datetime import datetime
from pathlib import Path

def main():
    print("=" * 75)
    print("         GitHub Copilot Meeting Classification Experiment")
    print("=" * 75 + "\n")
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Load meetings from today's extraction
    meetings_file = f"data/meetings/meetings_{today}.json"
    
    if not os.path.exists(meetings_file):
        print(f"❌ ERROR: Meetings file not found: {meetings_file}")
        print("   Please run calendar extraction first.")
        return
    
    with open(meetings_file, 'r', encoding='utf-8') as f:
        meetings_data = json.load(f)
    
    meetings = meetings_data.get('meetings', [])
    meeting_date = meetings_data.get('date', today)
    print(f"✅ Loaded {len(meetings)} meetings for {meeting_date}\n")
    
    # Prepare experiment results
    experiment_results = {
        "experiment": {
            "experiment_id": f"meeting_classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "experiment_type": "meeting_classification",
            "run_date": datetime.now().isoformat(),
            "platform": "Windows DevBox",
            "description": "Meeting classification using GitHub Copilot LLM for comparison"
        },
        "metadata": {
            "extraction_date": meetings_data.get('extraction_date'),
            "classification_date": datetime.now().isoformat(),
            "target_date": meetings_data.get('target_date'),
            "total_meetings": len(meetings),
            "classifier": {
                "name": "GitHub Copilot",
                "model": "GPT-4 Turbo (estimated)",
                "model_version": "gpt-4-1106-preview (estimated)",
                "provider": "Microsoft Azure OpenAI",
                "endpoint": "GitHub Copilot Chat API",
                "authentication": "GitHub account",
                "capabilities": [
                    "Code-aware classification",
                    "Context-rich analysis",
                    "Detailed reasoning",
                    "Key indicator extraction"
                ],
                "note": "GitHub Copilot uses Azure OpenAI GPT-4 Turbo for chat functionality"
            },
            "classification_method": "Manual classification via GitHub Copilot Chat with Enterprise Meeting Taxonomy",
            "taxonomy_version": "Enterprise Meeting Taxonomy v3.0",
            "input_source": meetings_file
        },
        "meetings": []
    }
    
    print("🤖 GitHub Copilot Classification Mode")
    print("=" * 75)
    print("\nINSTRUCTIONS:")
    print("  For each meeting below, I'll show you the meeting details.")
    print("  Please classify using GitHub Copilot Chat with this prompt:\n")
    print('  """')
    print('  Classify this meeting according to Enterprise Meeting Taxonomy:')
    print('  ')
    print('  [Meeting details will be shown]')
    print('  ')
    print('  Return JSON:')
    print('  {')
    print('    "specific_type": "exact type from taxonomy",')
    print('    "primary_category": "one of 5 main categories",')
    print('    "confidence": 0.95,')
    print('    "reasoning": "explanation",')
    print('    "key_indicators": ["signal1", "signal2", "signal3"]')
    print('  }')
    print('  """')
    print("\n" + "=" * 75 + "\n")
    
    # Since GitHub Copilot classification is manual/interactive,
    # we'll prepare a structured document for the user to classify
    classification_guide = {
        "instructions": "Classify each meeting using GitHub Copilot Chat",
        "prompt_template": """Classify this meeting according to Enterprise Meeting Taxonomy:

Meeting: {subject}
Description: {body_preview}
Attendees: {attendee_count} people
Duration: {duration} minutes

Return JSON with:
- specific_type (exact type from taxonomy)
- primary_category (one of 5 categories)
- confidence (0.0-1.0)
- reasoning (2-3 sentences)
- key_indicators (list of signals)
""",
        "meetings": []
    }
    
    for i, meeting in enumerate(meetings, 1):
        subject = meeting.get('subject', 'No subject')
        body = meeting.get('bodyPreview', 'No description')
        
        # Calculate duration
        start = meeting.get('start', {})
        end = meeting.get('end', {})
        duration = 60  # Default
        
        meeting_info = {
            "meeting_number": i,
            "subject": subject,
            "body_preview": body[:200],
            "start_time": start,
            "duration_minutes": duration,
            "prompt": classification_guide["prompt_template"].format(
                subject=subject,
                body_preview=body[:200],
                attendee_count="Unknown",
                duration=duration
            )
        }
        
        classification_guide["meetings"].append(meeting_info)
        
        print(f"Meeting {i}/{len(meetings)}: {subject}")
        print(f"  Time: {start}")
        print(f"  Duration: {duration} min")
        print()
    
    # Save classification guide
    output_dir = Path(f"experiments/{meeting_date}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    guide_file = output_dir / "github_copilot_classification_guide.json"
    with open(guide_file, 'w', encoding='utf-8') as f:
        json.dump(classification_guide, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Classification guide saved to: {guide_file}")
    print("\n" + "=" * 75)
    print("NEXT STEPS:")
    print("  1. Use the prompts above in GitHub Copilot Chat")
    print("  2. Collect classification results")
    print("  3. Compare with GPT-5 results")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    main()
