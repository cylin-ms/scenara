#!/usr/bin/env python3
"""
Quick Start: GPT-5 Meeting Classifier
Simple examples to get started immediately
"""

from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier


def example_1_basic_usage():
    """Example 1: Basic classification with fallback"""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Usage (Keyword Fallback)")
    print("=" * 70)
    
    classifier = GPT5MeetingClassifier()
    
    # Test without LLM (uses keyword fallback)
    result = classifier.classify_meeting(
        subject="Daily Standup",
        description="Quick team sync",
        attendees=["Alice", "Bob", "Charlie"],
        duration_minutes=15,
        use_llm=False  # Force fallback mode
    )
    
    print(f"\nMeeting: {result.get('meeting_subject', 'Daily Standup')}")
    print(f"+ Type: {result['specific_type']}")
    print(f"+ Category: {result['primary_category']}")
    print(f"+ Confidence: {result['confidence']:.1%}")
    print(f"+ Reasoning: {result['reasoning']}")


def example_2_llm_classification():
    """Example 2: LLM-based classification (requires auth)"""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: LLM Classification (GPT-5)")
    print("=" * 70)
    
    classifier = GPT5MeetingClassifier()
    
    # Test if GPT-5 is available
    print("\nChecking GPT-5 availability...")
    is_available = classifier.test_model_availability()
    
    if is_available:
        print("✅ GPT-5 is available - will use LLM classification")
        
        result = classifier.classify_meeting(
            subject="Q4 Strategic Planning Session",
            description="Leadership team planning for Q4 2025 priorities, budget allocation, and resource planning",
            attendees=["CEO", "CFO", "VP Sales", "VP Engineering", "VP Product"],
            duration_minutes=180,
            use_llm=True
        )
        
        print(f"\nMeeting: Q4 Strategic Planning Session")
        print(f"+ Type: {result['specific_type']}")
        print(f"+ Category: {result['primary_category']}")
        print(f"+ Confidence: {result['confidence']:.1%}")
        print(f"+ Reasoning: {result['reasoning']}")
    else:
        print("⚠️  GPT-5 not available - using fallback mode")
        print("\nTo enable GPT-5:")
        print("1. Ensure you have Microsoft account access")
        print("2. Run the script - it will prompt for authentication")
        print("3. Complete browser-based login")


def example_3_batch_classification():
    """Example 3: Classify multiple meetings"""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Batch Classification")
    print("=" * 70)
    
    classifier = GPT5MeetingClassifier()
    
    meetings = [
        {
            "subject": "1:1 with Manager",
            "description": "Monthly career development discussion",
            "attendees": ["Me", "Manager"],
            "duration": 30
        },
        {
            "subject": "All-Hands Meeting",
            "description": "Company-wide Q3 results announcement",
            "attendees": ["All Employees"] * 100,
            "duration": 60
        },
        {
            "subject": "Client Demo",
            "description": "Product demo for Acme Corp stakeholders",
            "attendees": ["Sales", "Solutions Architect", "Client Team"],
            "duration": 45
        }
    ]
    
    print(f"\nClassifying {len(meetings)} meetings...\n")
    
    for i, meeting in enumerate(meetings, 1):
        result = classifier.classify_meeting(
            subject=meeting['subject'],
            description=meeting['description'],
            attendees=meeting['attendees'],
            duration_minutes=meeting['duration'],
            use_llm=False  # Use fallback for demo
        )
        
        print(f"{i}. {meeting['subject']}")
        print(f"   → {result['specific_type']}")
        print(f"   Confidence: {result['confidence']:.1%}")
        print()


def example_4_taxonomy_exploration():
    """Example 4: Explore the taxonomy"""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Enterprise Meeting Taxonomy")
    print("=" * 70)
    
    classifier = GPT5MeetingClassifier()
    
    print(f"\nTotal Categories: {len(classifier.enterprise_taxonomy)}")
    print(f"Total Meeting Types: {len(classifier.all_meeting_types)}\n")
    
    for category, types in classifier.enterprise_taxonomy.items():
        print(f"\n[{category}] ({len(types)} types)")
        for meeting_type in types:
            print(f"   * {meeting_type}")


def example_5_comparison():
    """Example 5: Compare different meetings"""
    print("\n" + "=" * 70)
    print("EXAMPLE 5: Classification Comparison")
    print("=" * 70)
    
    classifier = GPT5MeetingClassifier()
    
    # Compare similar-sounding meetings
    meetings = [
        ("Weekly Team Sync", "Status update", 5, 15),
        ("Weekly Planning Meeting", "Plan next week's work", 5, 60),
        ("Weekly Retrospective", "Discuss what went well", 5, 45),
    ]
    
    print("\nClassifying similar meetings to see differences:\n")
    
    for subject, desc, attendees, duration in meetings:
        result = classifier.classify_meeting(
            subject=subject,
            description=desc,
            attendees=["Team"] * attendees,
            duration_minutes=duration,
            use_llm=False
        )
        
        print(f"'{subject}'")
        print(f"  → {result['specific_type']}")
        print(f"  Category: {result['primary_category']}")
        print()


def main():
    """Run all examples"""
    print("=" * 70)
    print("GPT-5 MEETING CLASSIFIER - QUICK START EXAMPLES")
    print("=" * 70)
    
    # Run all examples
    example_1_basic_usage()
    example_2_llm_classification()
    example_3_batch_classification()
    example_4_taxonomy_exploration()
    example_5_comparison()
    
    print("\n" + "=" * 70)
    print("QUICK START COMPLETED")
    print("=" * 70)
    print("\nNext Steps:")
    print("1. Run comparison: python compare_classifiers.py")
    print("2. Read guide: GPT5_CLASSIFIER_GUIDE.md")
    print("3. Check summary: GPT5_CLASSIFIER_SUMMARY.md")
    print("4. Integrate into collaborator_discovery.py")
    print()


if __name__ == "__main__":
    main()
