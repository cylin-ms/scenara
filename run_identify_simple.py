#!/usr/bin/env python3
"""
Simple runner for meeting identification - no arguments needed
"""

import sys
from pathlib import Path

# Add tools to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))
sys.path.insert(0, str(Path(__file__).parent))

def run_identification():
    """Run identification with default settings."""
    from tools.llm_api import LLMAPIClient
    import json
    from datetime import datetime, timedelta
    
    # Import the functions we need
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "identify_module",
        Path(__file__).parent / "tools" / "identify_top7_meetings.py"
    )
    identify_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(identify_module)
    
    # Run with default settings
    input_file = Path("my_calendar_events_complete_attendees.json")
    output_file = Path("data/top7_meetings.json")
    
    print(f"\n{'='*80}")
    print(f"TOP 7 MEETING TYPE IDENTIFICATION")
    print(f"{'='*80}")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Using: Ollama gpt-oss:20b")
    print()
    
    # Load calendar data
    calendar_data = identify_module.load_calendar_data(input_file)
    meetings = calendar_data['meetings']
    
    # Filter recent meetings (6 months)
    recent_meetings = identify_module.filter_recent_meetings(meetings, 6)
    
    if not recent_meetings:
        print("❌ No recent meetings found")
        return
    
    # Pre-screen meetings
    candidates = identify_module.pre_screen_meetings(recent_meetings)
    
    if not candidates:
        print("❌ No candidates found matching top 7 types")
        return
    
    # Initialize LLM client
    llm_client = LLMAPIClient()
    
    # Classify with LLM
    matched_meetings = identify_module.batch_classify_meetings(candidates, llm_client, dry_run=False)
    
    if not matched_meetings:
        print("❌ No meetings matched the top 7 types")
        return
    
    # Generate statistics
    stats = identify_module.generate_statistics(matched_meetings)
    
    # Print summary
    identify_module.print_summary(stats)
    
    # Save results
    identify_module.save_results(matched_meetings, stats, output_file)
    
    print(f"✅ Complete! Found {len(matched_meetings)} meetings matching top 7 types")

if __name__ == "__main__":
    try:
        run_identification()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
