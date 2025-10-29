#!/usr/bin/env python3
"""
Single Model Validation App Launcher
=====================================

Start validation web app for a specific model and date.

Usage:
    python start_validation_single.py <model> [date]

Examples:
    python start_validation_single.py gpt5
    python start_validation_single.py copilot 2025-10-29
    python start_validation_single.py gpt4o 2025-10-28

Available models:
    - gpt5: GPT-5 classifications
    - copilot: GitHub Copilot classifications
    - gpt4o: GPT-4o classifications
    - claude: Claude classifications
"""

import sys
import subprocess
from datetime import datetime
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("\n" + "="*70)
        print("  SINGLE MODEL VALIDATION APP LAUNCHER")
        print("="*70)
        print("\n❌ ERROR: Model name required")
        print("\nUsage: python start_validation_single.py <model> [date]")
        print("\nExamples:")
        print("  python start_validation_single.py gpt5")
        print("  python start_validation_single.py copilot 2025-10-29")
        print("  python start_validation_single.py gpt4o 2025-10-28")
        print("\nAvailable models:")
        print("  • gpt5      - GPT-5 classifications")
        print("  • copilot   - GitHub Copilot classifications")
        print("  • gpt4o     - GPT-4o classifications")
        print("  • claude    - Claude classifications")
        print("\nIf date is not provided, today's date will be used.")
        print("="*70 + "\n")
        sys.exit(1)
    
    model = sys.argv[1]
    date = sys.argv[2] if len(sys.argv) > 2 else datetime.now().strftime('%Y-%m-%d')
    
    # Validate model
    valid_models = ['gpt5', 'copilot', 'gpt4o', 'claude']
    if model not in valid_models:
        print(f"\n❌ ERROR: Invalid model '{model}'")
        print(f"   Valid models: {', '.join(valid_models)}")
        sys.exit(1)
    
    # Check if data file exists
    data_file = Path(__file__).parent / "data" / "meetings" / f"meetings_{date}.json"
    if not data_file.exists():
        print(f"\n❌ ERROR: Meetings file not found for {date}")
        print(f"   Expected: {data_file}")
        print("\n   Run calendar extraction first:")
        print(f"   python process_todays_meetings.py {date}")
        sys.exit(1)
    
    # Check if classification file exists
    exp_dir = Path(__file__).parent / "experiments" / date
    class_files = {
        'gpt5': 'meeting_classification_gpt5.json',
        'copilot': 'meeting_classification_github_copilot.json',
        'gpt4o': 'meeting_classification_gpt4o.json',
        'claude': 'meeting_classification_claude.json'
    }
    
    class_file = exp_dir / class_files[model]
    if not class_file.exists():
        print(f"\n⚠️  WARNING: Classification file not found")
        print(f"   Expected: {class_file}")
        print(f"\n   Run classification first:")
        print(f"   python classify_with_{model}.py")
        print("\n   Continuing anyway - you can classify later...\n")
    
    # Launch the app
    print(f"\n🚀 Launching validation app for {model.upper()} on {date}...\n")
    subprocess.run([sys.executable, "validation_app_single.py", model, date])

if __name__ == "__main__":
    main()
