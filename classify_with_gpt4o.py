#!/usr/bin/env python3
"""
GPT-4o Meeting Classification (GitHub Copilot Model)
Uses GPT-4o model (same as GitHub Copilot) for meeting classification comparison
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier

# GPT-4o endpoint and model configuration  
# Using Azure OpenAI GPT-4o (same model family as GitHub Copilot)
GPT4O_MODEL = "gpt-4o"  
GPT4O_ENDPOINT = "https://your-azure-openai-endpoint.openai.azure.com/openai/deployments/gpt-4o/chat/completions?api-version=2024-08-01-preview"

# For now, we'll use GPT-5 infrastructure with note that this simulates Copilot
# In production, you'd configure actual GPT-4o Azure OpenAI endpoint

def load_taxonomy():
    """Load the enterprise meeting taxonomy."""
    taxonomy_file = Path("prompts/enterprise_meeting_taxonomy.md")
    with open(taxonomy_file, 'r', encoding='utf-8') as f:
        return f.read()

def classify_meeting_with_gpt4o(meeting: dict, taxonomy: str, client: LLMAPIClient) -> dict:
    """Classify a single meeting using GPT-4o."""
    prompt = f"""Classify this meeting according to the Enterprise Meeting Taxonomy below.

ENTERPRISE MEETING TAXONOMY:
{taxonomy}

MEETING DETAILS:
Subject: {meeting.get('subject', 'No subject')}
Body Preview: {meeting.get('bodyPreview', 'No description')}
Start: {meeting.get('start', {}).get('dateTime', 'Unknown')}
Duration: {calculate_duration(meeting)} minutes
Attendees: {len(meeting.get('attendees', []))}
Organizer: {meeting.get('organizer', {}).get('emailAddress', {}).get('name', 'Unknown')}

Return ONLY a JSON object with this exact structure:
{{
  "specific_type": "exact type name from taxonomy",
  "primary_category": "one of the 5 main categories",
  "confidence": 0.95,
  "reasoning": "brief explanation of why this classification",
  "key_indicators": ["indicator1", "indicator2", "indicator3"]
}}"""

    # Use GPT-4o (same model as GitHub Copilot)
    response = client.query_llm(
        prompt=prompt,
        provider="openai",
        model="gpt-4o",
        temperature=0.1
    )
    
    # Parse JSON from response
    try:
        # Find JSON in response
        response_text = response.strip()
        if response_text.startswith("```json"):
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif response_text.startswith("```"):
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        classification = json.loads(response_text)
        return classification
    except Exception as e:
        print(f"⚠️  Error parsing classification: {e}")
        print(f"Response: {response[:200]}")
        return {
            "specific_type": "Unknown",
            "primary_category": "Unknown",
            "confidence": 0.0,
            "reasoning": f"Error parsing response: {e}",
            "key_indicators": []
        }

def calculate_duration(meeting: dict) -> int:
    """Calculate meeting duration in minutes."""
    try:
        from datetime import datetime
        start = meeting.get('start', {}).get('dateTime', '')
        end = meeting.get('end', {}).get('dateTime', '')
        
        if start and end:
            start_dt = datetime.fromisoformat(start.split('.')[0])
            end_dt = datetime.fromisoformat(end.split('.')[0])
            duration = (end_dt - start_dt).total_seconds() / 60
            return int(duration)
    except:
        pass
    return 30  # default

def main():
    print("=" * 75)
    print("         GPT-4o Meeting Classification (Copilot Equivalent)")
    print("=" * 75 + "\n")
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Load meetings
    meetings_file = f"data/meetings/meetings_{today}.json"
    if not os.path.exists(meetings_file):
        print(f"❌ ERROR: Meetings file not found: {meetings_file}")
        return
    
    with open(meetings_file, 'r', encoding='utf-8') as f:
        meetings_data = json.load(f)
    
    meetings = meetings_data.get('meetings', [])
    print(f"✅ Loaded {len(meetings)} meetings for {today}\n")
    
    # Load taxonomy
    print("📚 Loading Enterprise Meeting Taxonomy...")
    taxonomy = load_taxonomy()
    
    # Initialize LLM client
    print("🔧 Initializing GPT-4o classifier (GitHub Copilot equivalent)...")
    client = LLMAPIClient()
    
    # Prepare results
    results = {
        "experiment": {
            "experiment_id": f"meeting_classification_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "experiment_type": "meeting_classification",
            "run_date": datetime.now().isoformat(),
            "platform": "Windows DevBox",
            "description": "Meeting classification using GPT-4o (GitHub Copilot equivalent model)"
        },
        "metadata": {
            "extraction_date": meetings_data.get('extraction_date'),
            "classification_date": datetime.now().isoformat(),
            "date": today,
            "total_meetings": len(meetings),
            "classifier": {
                "name": "GPT-4o",
                "model": "gpt-4o",
                "provider": "Azure OpenAI",
                "note": "GPT-4o is the same model family used by GitHub Copilot"
            }
        },
        "meetings": []
    }
    
    # Classify each meeting
    print(f"\n🔍 Classifying {len(meetings)} meetings with GPT-4o...\n")
    
    for i, meeting in enumerate(meetings, 1):
        subject = meeting.get('subject', 'No subject')
        start = meeting.get('start', {}).get('dateTime', 'Unknown')
        duration = calculate_duration(meeting)
        
        print(f"  [{i}/{len(meetings)}] {subject}")
        print(f"       Time: {start}")
        print(f"       Duration: {duration} minutes")
        
        classification = classify_meeting_with_gpt4o(meeting, taxonomy, client)
        
        print(f"       Type: {classification.get('specific_type')}")
        print(f"       Category: {classification.get('primary_category')}")
        print(f"       Confidence: {classification.get('confidence', 0)*100:.0f}%")
        print()
        
        results["meetings"].append({
            "meeting_number": i,
            "meeting_id": meeting.get('id'),
            "subject": subject,
            "start": start,
            "duration_minutes": duration,
            "classification": classification
        })
    
    # Calculate average confidence
    confidences = [m['classification'].get('confidence', 0) for m in results['meetings']]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0
    
    # Save results
    output_dir = Path(f"experiments/{today}")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "meeting_classification_github_copilot.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Classified meetings saved to: {output_file}")
    print(f"\n📊 SUMMARY:")
    print(f"   Total Meetings: {len(meetings)}")
    print(f"   Avg Confidence: {avg_confidence*100:.2f}%")
    print(f"\n📁 Experiment: {results['experiment']['experiment_id']}")
    print(f"\n🎉 GPT-4o classification complete!")
    print(f"   Compare with GPT-5 results in experiments/{today}/\n")

if __name__ == "__main__":
    main()
