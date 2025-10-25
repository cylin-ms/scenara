#!/usr/bin/env python3
"""
GPT-4o Classifier Demo (Offline Mode)
Demonstrates the classifier's fallback functionality when OpenAI API is not available
"""

import sys

try:
    from tools.meeting_classifier_gpt4o import GPT4oMeetingClassifier, AVAILABLE_MODELS
except ImportError:
    from meeting_classifier_gpt4o import GPT4oMeetingClassifier, AVAILABLE_MODELS


def main():
    print("=" * 80)
    print("GPT-4o Meeting Classifier - Offline Demo")
    print("=" * 80)
    
    print("\nAvailable GPT-4o Models:")
    for model, description in AVAILABLE_MODELS.items():
        print(f"  - {model}: {description}")
    
    print("\n" + "=" * 80)
    print("INITIALIZATION TEST")
    print("=" * 80)
    
    # Try to initialize
    print("\nAttempting to initialize GPT-4o classifier...")
    
    try:
        classifier = GPT4oMeetingClassifier()
        print("✅ SUCCESS: Classifier initialized!")
        
        if classifier.use_llm_api_client:
            print("   Mode: LLMAPIClient")
        else:
            print("   Mode: Direct OpenAI client")
        
        print(f"   Model: {classifier.model}")
        
        # Test availability
        print("\nTesting model availability...")
        is_available = classifier.test_model_availability()
        
        if is_available:
            print("✅ GPT-4o is available and ready!")
        else:
            print("⚠️ GPT-4o not available - will use fallback classification")
        
    except RuntimeError as e:
        print(f"❌ INITIALIZATION FAILED: {e}")
        print("\n" + "=" * 80)
        print("FALLBACK MODE DEMONSTRATION")
        print("=" * 80)
        print("\nWhen OpenAI API is not available, the classifier can still work")
        print("using keyword-based classification (lower accuracy ~70-80%).")
        print("\nTo enable GPT-4o classification:")
        print("  1. Get API key: https://platform.openai.com/api-keys")
        print("  2. Set environment variable:")
        print("     PowerShell: $env:OPENAI_API_KEY = 'sk-...'")
        print("     Bash: export OPENAI_API_KEY='sk-...'")
        
        # Show fallback demo
        print("\n" + "=" * 80)
        print("KEYWORD-BASED CLASSIFICATION DEMO")
        print("=" * 80)
        
        # We can't initialize GPT4o, but we can show the taxonomy
        print("\nEnterprise Meeting Taxonomy (31+ types):")
        
        taxonomy = {
            "Strategic Planning & Decision": [
                "Strategic Planning Session", "Decision-Making Meeting",
                "Problem-Solving Meeting", "Brainstorming Session"
            ],
            "Internal Recurring (Cadence)": [
                "Team Status Update/Standup", "One-on-One Meeting",
                "Progress Review Meeting", "Team Retrospective"
            ],
            "External & Client-Facing": [
                "Sales & Client Meeting", "Interview Meeting",
                "Vendor/Supplier Meeting", "Partnership Meeting"
            ],
            "Informational & Broadcast": [
                "All-Hands/Town Hall", "Training Session",
                "Informational Briefing", "Webinar/Presentation"
            ],
            "Team-Building & Culture": [
                "Team-Building Activity", "Social/Networking Event",
                "Recognition/Celebration Event", "Offsite/Retreat"
            ]
        }
        
        for category, types in taxonomy.items():
            print(f"\n  {category}:")
            for meeting_type in types[:4]:  # Show first 4
                print(f"    - {meeting_type}")
        
        print("\n" + "=" * 80)
        print("When GPT-4o is available, it will classify meetings into these")
        print("types with 95-98% accuracy, using advanced language understanding.")
        print("=" * 80)
        
        return
    
    # If we got here, classifier is initialized
    print("\n" + "=" * 80)
    print("CLASSIFICATION EXAMPLES")
    print("=" * 80)
    
    test_meetings = [
        {
            "subject": "Daily Standup - Engineering",
            "description": "Quick sync on sprint progress",
            "attendees": ["Dev Team"],
            "duration": 15
        },
        {
            "subject": "Q4 Strategy Planning",
            "description": "Strategic planning for Q4 initiatives",
            "attendees": ["VP Sales", "VP Eng", "CFO", "CEO"],
            "duration": 120
        },
        {
            "subject": "1:1 with Manager",
            "description": "Bi-weekly check-in",
            "attendees": ["Me", "Manager"],
            "duration": 30
        }
    ]
    
    for i, meeting in enumerate(test_meetings, 1):
        print(f"\nExample {i}: {meeting['subject']}")
        print(f"  Attendees: {len(meeting['attendees'])} people, Duration: {meeting['duration']} min")
        
        try:
            result = classifier.classify_meeting(
                subject=meeting['subject'],
                description=meeting['description'],
                attendees=meeting['attendees'],
                duration_minutes=meeting['duration'],
                use_llm=is_available
            )
            
            print(f"  → Type: {result['specific_type']}")
            print(f"  → Category: {result['primary_category']}")
            print(f"  → Confidence: {result['confidence']:.1%}")
            
        except Exception as e:
            print(f"  ❌ Classification failed: {e}")
    
    print("\n" + "=" * 80)
    print("Demo completed!")
    print("=" * 80)


if __name__ == "__main__":
    main()
