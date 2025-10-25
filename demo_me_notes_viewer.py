#!/usr/bin/env python3
"""
Demo script for Me Notes Viewer Tool
Shows how to use the Me Notes Viewer programmatically and via CLI
"""

import sys
from pathlib import Path
import subprocess
import webbrowser
from me_notes_viewer import MeNotesViewer

def demo_programmatic_usage():
    """Demonstrate programmatic usage of Me Notes Viewer"""
    
    print("🎯 Me Notes Viewer Demo - Programmatic Usage")
    print("=" * 50)
    
    # Create viewer instance
    viewer = MeNotesViewer()
    
    # Example 1: Full report for a user
    print("\n📊 Example 1: Complete Me Notes report")
    results = viewer.fetch_and_display(
        user_email="john.doe@company.com",
        format_type="both",
        days_back=30
    )
    
    print(f"✅ Generated reports:")
    for format_type, file_path in results.items():
        print(f"   📄 {format_type.upper()}: {file_path}")
    
    # Example 2: Filtered by category
    print("\n📊 Example 2: Work-related notes only")
    work_results = viewer.fetch_and_display(
        user_email="jane.smith@company.com", 
        format_type="html",
        days_back=14,
        category_filter=["WORK_RELATED", "FOLLOW_UPS"]
    )
    
    # Example 3: Recent expertise insights
    print("\n📊 Example 3: Recent expertise and behavioral patterns")
    expertise_results = viewer.fetch_and_display(
        user_email="expert.user@company.com",
        format_type="markdown", 
        days_back=7,
        category_filter=["EXPERTISE", "BEHAVIORAL_PATTERN"]
    )
    
    return results

def demo_cli_usage():
    """Demonstrate CLI usage examples"""
    
    print("\n🖥️ Me Notes Viewer Demo - CLI Usage Examples")
    print("=" * 50)
    
    cli_examples = [
        {
            "description": "Basic usage - get all notes for a user",
            "command": "python me_notes_viewer.py --user john.doe@company.com"
        },
        {
            "description": "HTML only, last 14 days",
            "command": "python me_notes_viewer.py --user jane@company.com --format html --days 14"
        },
        {
            "description": "Work-related notes only",
            "command": "python me_notes_viewer.py --user expert@company.com --category WORK_RELATED"
        },
        {
            "description": "Multiple categories with auto-open",
            "command": "python me_notes_viewer.py --user manager@company.com --category EXPERTISE --category FOLLOW_UPS --open"
        },
        {
            "description": "Markdown only, last 7 days",
            "command": "python me_notes_viewer.py -u analyst@company.com -f markdown -d 7"
        }
    ]
    
    print("Here are example CLI commands you can run:\n")
    
    for i, example in enumerate(cli_examples, 1):
        print(f"{i}. {example['description']}")
        print(f"   Command: {example['command']}")
        print()
    
    print("💡 Tip: Use --help to see all available options:")
    print("   python me_notes_viewer.py --help")
    
    return cli_examples

def interactive_demo():
    """Run an interactive demo"""
    
    print("\n🎮 Interactive Me Notes Viewer Demo")
    print("=" * 40)
    
    # Get user input
    user_email = input("📧 Enter user email (or press Enter for demo@company.com): ").strip()
    if not user_email:
        user_email = "demo@company.com"
    
    print("\n📋 Select format:")
    print("1. Markdown only")
    print("2. HTML only") 
    print("3. Both formats")
    
    format_choice = input("Choose (1-3, default: 3): ").strip()
    format_map = {"1": "markdown", "2": "html", "3": "both"}
    format_type = format_map.get(format_choice, "both")
    
    days_input = input("\n📅 Days back to fetch (default: 30): ").strip()
    days_back = int(days_input) if days_input.isdigit() else 30
    
    print("\n🏷️ Filter by category (optional):")
    print("Available: WORK_RELATED, EXPERTISE, BEHAVIORAL_PATTERN, INTERESTS, FOLLOW_UPS")
    categories_input = input("Enter categories (comma-separated, or press Enter for all): ").strip()
    
    category_filter = None
    if categories_input:
        category_filter = [cat.strip().upper() for cat in categories_input.split(',')]
    
    # Run the viewer
    print(f"\n🚀 Running Me Notes Viewer...")
    viewer = MeNotesViewer()
    
    try:
        results = viewer.fetch_and_display(
            user_email=user_email,
            format_type=format_type,
            days_back=days_back,
            category_filter=category_filter
        )
        
        # Ask if user wants to open results
        if results:
            open_files = input(f"\n🌐 Open generated reports? (y/n, default: y): ").strip().lower()
            if open_files != 'n':
                if 'html' in results:
                    print("🌐 Opening HTML report in browser...")
                    webbrowser.open(f"file://{Path(results['html']).absolute()}")
                
                if 'markdown' in results:
                    print("📝 Markdown report available at:", results['markdown'])
        
        print("\n✅ Interactive demo completed!")
        
    except Exception as e:
        print(f"\n❌ Error running demo: {e}")

def main():
    """Main demo function"""
    
    print("🧠 Me Notes Viewer Tool - Complete Demo")
    print("=" * 60)
    print()
    print("This tool fetches Microsoft Me Notes and generates beautiful reports")
    print("in Markdown and HTML formats with rich insights and visualizations.")
    print()
    
    demo_choice = input("Choose demo type:\n1. Programmatic usage examples\n2. CLI usage examples\n3. Interactive demo\n4. All demos\n\nChoice (1-4, default: 4): ").strip()
    
    if demo_choice in ["1", "4"]:
        results = demo_programmatic_usage()
    
    if demo_choice in ["2", "4"]:
        demo_cli_usage()
    
    if demo_choice in ["3", "4"]:
        interactive_demo()
    
    if demo_choice == "4":
        print("\n🎉 All demos completed!")
        print("\nNext steps:")
        print("1. 📝 Check the generated reports in the 'me_notes_reports/' directory")
        print("2. 🔧 Customize the tool by modifying the MeNotesAPI class")
        print("3. 🌐 Integrate with real Microsoft Me Notes APIs")
        print("4. 📊 Add more visualization and analysis features")

if __name__ == "__main__":
    main()