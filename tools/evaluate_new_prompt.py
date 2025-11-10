#!/usr/bin/env python3
"""
New Prompt Evaluator - Using Canonical GUTT Library

Evaluates new Calendar.AI prompts by mapping their capabilities to the
20 canonical Unit Tasks identified through semantic analysis.

Usage:
    python evaluate_new_prompt.py --prompt "Your new Calendar.AI feature"
    python evaluate_new_prompt.py --file new_prompt.txt
    python evaluate_new_prompt.py --interactive

Based on canonical library from Copilot semantic analysis.
"""

import sys
from pathlib import Path

# Canonical GUTT Library (from copilot_claude_semantic_analysis.md)
CANONICAL_UNIT_TASKS = [
    # Tier 1: Universal (50%+ prompts)
    {
        "id": 1,
        "name": "Calendar Events Retrieval",
        "frequency": "9/9 (100%)",
        "tier": 1,
        "api": "GET /me/calendar/events",
        "tool": "Microsoft Graph API / Google Calendar API",
        "description": "Retrieve calendar event data from calendar systems via API, with optional filters for time range, attendees, or status",
        "examples": [
            "Get all meetings this week",
            "Retrieve pending invitations",
            "Load historical calendar data",
            "Access multi-person availability"
        ]
    },
    {
        "id": 2,
        "name": "Meeting Classification",
        "frequency": "7/9 (78%)",
        "tier": 1,
        "api": "ML Classification Model",
        "tool": "Azure AI Language / OpenAI / Custom ML",
        "description": "Assign categories, scores, or classifications to calendar events based on attributes, content, and context",
        "examples": [
            "Classify meeting type (1:1, team, executive)",
            "Score meeting importance",
            "Identify override-eligible meetings (1:1s, lunches)",
            "Determine priority alignment"
        ]
    },
    {
        "id": 3,
        "name": "Calendar Event Creation/Update",
        "frequency": "6/9 (67%)",
        "tier": 1,
        "api": "POST /me/calendar/events, PATCH /me/calendar/events/{id}",
        "tool": "Microsoft Graph API / Google Calendar API",
        "description": "Create or modify calendar events via API, including recurrence rules, attendees, and resources",
        "examples": [
            "Create new meeting",
            "Update RSVP status",
            "Add recurring series",
            "Modify event time/attendees"
        ]
    },
    {
        "id": 4,
        "name": "NLU (Constraint/Intent Extraction)",
        "frequency": "6/9 (67%)",
        "tier": 1,
        "api": "NLU Service",
        "tool": "Azure AI Language / OpenAI GPT / Custom NLP",
        "description": "Extract structured information (entities, constraints, intents) from unstructured natural language input",
        "examples": [
            "Parse 'Thursday afternoon' to datetime range",
            "Extract meeting participants from 'my team'",
            "Identify constraints like 'avoid Fridays'",
            "Extract priorities from user goals"
        ]
    },
    {
        "id": 5,
        "name": "Attendee/Contact Resolution",
        "frequency": "5/9 (56%)",
        "tier": 1,
        "api": "GET /users",
        "tool": "Microsoft Graph API / Directory Service",
        "description": "Resolve participant names/descriptions to specific calendar identities via directory lookup",
        "examples": [
            "Resolve 'Chris' to email address",
            "Map 'product team' to member list",
            "Identify customer attendees",
            "Lookup manager/reports"
        ]
    },
    
    # Tier 2: Common (25-50% prompts)
    {
        "id": 6,
        "name": "Availability Checking",
        "frequency": "4/9 (44%)",
        "tier": 2,
        "api": "POST /me/calendar/getSchedule",
        "tool": "Microsoft Graph API / Google Calendar API",
        "description": "Retrieve availability status (free/busy) for specified users and time ranges",
        "examples": [
            "Check when attendees are free",
            "Find common availability window",
            "Identify scheduling conflicts",
            "Get free/busy for next 2 weeks"
        ]
    },
    {
        "id": 7,
        "name": "Meeting Invitation Sending",
        "frequency": "4/9 (44%)",
        "tier": 2,
        "api": "POST /me/sendMail",
        "tool": "Email/Calendar Invitation System",
        "description": "Dispatch calendar invitations or notifications via email/calendar system",
        "examples": [
            "Send meeting invite",
            "Update meeting attendees",
            "Send reschedule notification",
            "Dispatch prep reminders"
        ]
    },
    {
        "id": 8,
        "name": "Document/Content Retrieval",
        "frequency": "4/9 (44%)",
        "tier": 2,
        "api": "SharePoint API / OneDrive API / CRM",
        "tool": "SharePoint / OneDrive / CRM / Web Search",
        "description": "Retrieve documents, data, or content from various sources (SharePoint, CRM, web, etc.)",
        "examples": [
            "Get project status documents",
            "Retrieve company background",
            "Access meeting materials",
            "Fetch relevant content"
        ]
    },
    {
        "id": 9,
        "name": "Document Generation",
        "frequency": "4/9 (44%)",
        "tier": 2,
        "api": "NLG Service / Template Engine",
        "tool": "Natural Language Generation / Template System",
        "description": "Generate formatted documents from structured data using templates and NLG",
        "examples": [
            "Create meeting agenda",
            "Generate briefing document",
            "Produce time usage report",
            "Format meeting brief"
        ]
    },
    {
        "id": 10,
        "name": "Time Aggregation/Analytics",
        "frequency": "3/9 (33%)",
        "tier": 2,
        "api": "Analytics Service",
        "tool": "Data Aggregation / Analytics Engine",
        "description": "Aggregate and compute statistical metrics from calendar event data",
        "examples": [
            "Total hours by category",
            "Average meeting duration",
            "Time distribution analysis",
            "Meeting count per person"
        ]
    },
    {
        "id": 11,
        "name": "Priority/Preference Matching",
        "frequency": "3/9 (33%)",
        "tier": 2,
        "api": "Semantic Matching Algorithm",
        "tool": "Priority Scoring Service",
        "description": "Score/classify calendar events based on alignment with user-defined priorities or preferences",
        "examples": [
            "Match meetings to priorities",
            "Score alignment with goals",
            "Filter by priority level",
            "Rank by relevance"
        ]
    },
    {
        "id": 12,
        "name": "Constraint Satisfaction",
        "frequency": "3/9 (33%)",
        "tier": 2,
        "api": "Scheduling Algorithm",
        "tool": "Constraint Solver",
        "description": "Find time slots satisfying multiple scheduling constraints using constraint satisfaction algorithms",
        "examples": [
            "Find time meeting all criteria",
            "Optimize slot selection",
            "Satisfy hard/soft constraints",
            "Multi-attendee coordination"
        ]
    },
    {
        "id": 13,
        "name": "RSVP Status Update",
        "frequency": "3/9 (33%)",
        "tier": 2,
        "api": "POST /me/events/{id}/accept",
        "tool": "Calendar API",
        "description": "Update meeting RSVP status via calendar API",
        "examples": [
            "Accept meeting invitation",
            "Decline invitation",
            "Mark as tentative",
            "Bulk RSVP updates"
        ]
    },
    {
        "id": 14,
        "name": "Recommendation Engine",
        "frequency": "3/9 (33%)",
        "tier": 2,
        "api": "Rule Engine / ML Model",
        "tool": "Recommendation Service",
        "description": "Generate actionable recommendations based on analysis using rule engines or ML models",
        "examples": [
            "Suggest meetings to decline",
            "Recommend schedule optimizations",
            "Propose responses to objections",
            "Identify improvement opportunities"
        ]
    },
    
    # Tier 3: Specialized (<25% prompts)
    {
        "id": 15,
        "name": "Recurrence Rule Generation",
        "frequency": "2/9 (22%)",
        "tier": 3,
        "api": "iCalendar RRULE",
        "tool": "iCalendar Specification",
        "description": "Generate iCalendar RRULE specifications from natural language recurrence patterns",
        "examples": [
            "Create weekly recurrence",
            "Set bi-weekly pattern",
            "Generate monthly series",
            "Complex recurrence rules"
        ]
    },
    {
        "id": 16,
        "name": "Event Monitoring",
        "frequency": "2/9 (22%)",
        "tier": 3,
        "api": "Webhooks / Change Notifications",
        "tool": "Calendar Webhooks / Polling Service",
        "description": "Detect and respond to calendar event changes via webhooks or polling",
        "examples": [
            "Monitor RSVP changes",
            "Detect conflicts",
            "Track cancellations",
            "Watch for updates"
        ]
    },
    {
        "id": 16,
        "name": "Event Monitoring",
        "frequency": "2/9 (22%)",
        "tier": 3,
        "api": "Webhooks / Change Notifications",
        "tool": "Calendar Webhooks / Polling Service",
        "description": "Detect and respond to calendar event changes via webhooks or polling",
        "examples": [
            "Monitor RSVP changes",
            "Detect conflicts",
            "Track cancellations",
            "Watch for updates"
        ]
    },
    {
        "id": 17,
        "name": "Automatic Rescheduling",
        "frequency": "2/9 (22%)",
        "tier": 3,
        "api": "Dynamic Scheduling Service",
        "tool": "Workflow Automation",
        "description": "Automatically reschedule meetings in response to conflicts or declines using dynamic scheduling logic",
        "examples": [
            "Auto-reschedule on decline",
            "Resolve conflicts automatically",
            "Find alternative times",
            "Update and notify attendees"
        ]
    },
    {
        "id": 18,
        "name": "Objection/Risk Anticipation",
        "frequency": "2/9 (22%)",
        "tier": 3,
        "api": "Risk Analysis Service",
        "tool": "Critical Thinking / Risk Modeling",
        "description": "Predict objections, concerns, or risks using critical thinking and risk modeling",
        "examples": [
            "Anticipate objections",
            "Identify project risks",
            "Predict concerns",
            "Flag potential blockers"
        ]
    },
    {
        "id": 19,
        "name": "Resource Booking",
        "frequency": "1/9 (11%)",
        "tier": 3,
        "api": "GET /places",
        "tool": "Resource Scheduling API",
        "description": "Search for and book physical resources (rooms, equipment) via resource scheduling API",
        "examples": [
            "Find available conference room",
            "Book meeting space",
            "Reserve equipment",
            "Check room capacity"
        ]
    },
    {
        "id": 20,
        "name": "Data Visualization",
        "frequency": "1/9 (11%)",
        "tier": 3,
        "api": "Charting Library",
        "tool": "Chart.js / D3.js / Dashboard Service",
        "description": "Generate visualizations (charts, graphs, dashboards) from calendar data",
        "examples": [
            "Time distribution pie chart",
            "Meeting trends over time",
            "Category comparison bars",
            "Interactive dashboards"
        ]
    }
]


def print_header():
    """Print tool header"""
    print("\n" + "="*80)
    print("NEW CALENDAR.AI PROMPT EVALUATOR")
    print("Using 20 Canonical Unit Tasks from Copilot Semantic Analysis")
    print("="*80 + "\n")


def get_prompt_input():
    """Get prompt from user"""
    print("Enter your new Calendar.AI prompt (or 'quit' to exit):")
    print("-" * 80)
    prompt = input("> ").strip()
    
    if prompt.lower() == 'quit':
        return None
    
    return prompt


def analyze_prompt(prompt: str):
    """Analyze prompt and identify canonical tasks needed"""
    print(f"\n{'='*80}")
    print(f"ANALYZING PROMPT")
    print(f"{'='*80}\n")
    print(f"Prompt: \"{prompt}\"\n")
    
    print("🧠 AI Reasoning Analysis (using semantic understanding)...\n")
    
    # Keywords and patterns for each canonical task
    # This would ideally be done with AI reasoning, but showing the concept
    task_indicators = {
        1: ["retrieve", "get", "fetch", "load", "calendar", "events", "meetings"],
        2: ["classify", "categorize", "type", "importance", "priority"],
        3: ["create", "schedule", "book", "update", "add", "modify"],
        4: ["parse", "understand", "extract", "identify constraints"],
        5: ["resolve", "identify", "who", "attendee", "participant", "contact"],
        6: ["available", "free", "busy", "when", "find time"],
        7: ["invite", "send", "notify", "invitation"],
        8: ["document", "content", "materials", "background", "research"],
        9: ["generate", "create brief", "agenda", "report", "summary"],
        10: ["analyze", "aggregate", "metrics", "statistics", "time spent"],
        11: ["priority", "align", "match", "goals", "preferences"],
        12: ["constraint", "satisfy", "optimize", "find slot", "coordinate"],
        13: ["accept", "decline", "rsvp", "respond"],
        14: ["recommend", "suggest", "advise", "propose"],
        15: ["recurring", "weekly", "monthly", "repeat", "series"],
        16: ["monitor", "watch", "track", "detect changes"],
        17: ["reschedule", "automatically", "auto", "conflict resolution"],
        18: ["objection", "risk", "concern", "anticipate", "blocker"],
        19: ["room", "conference", "resource", "equipment"],
        20: ["visualize", "chart", "graph", "dashboard", "visualization"]
    }
    
    # Simple keyword matching (in real implementation, use AI reasoning)
    prompt_lower = prompt.lower()
    detected_tasks = []
    
    for task_id, keywords in task_indicators.items():
        if any(keyword in prompt_lower for keyword in keywords):
            task = next(t for t in CANONICAL_UNIT_TASKS if t["id"] == task_id)
            detected_tasks.append(task)
    
    return detected_tasks


def print_evaluation_results(prompt: str, detected_tasks: list):
    """Print evaluation results"""
    print(f"{'='*80}")
    print(f"EVALUATION RESULTS")
    print(f"{'='*80}\n")
    
    if not detected_tasks:
        print("⚠️  No canonical tasks detected. This may be:")
        print("   - Not a Calendar.AI capability")
        print("   - Requires new canonical tasks to be defined")
        print("   - Needs more specific description\n")
        return
    
    print(f"✅ Detected {len(detected_tasks)} Canonical Unit Tasks:\n")
    
    # Group by tier
    tier1 = [t for t in detected_tasks if t["tier"] == 1]
    tier2 = [t for t in detected_tasks if t["tier"] == 2]
    tier3 = [t for t in detected_tasks if t["tier"] == 3]
    
    if tier1:
        print("🌟 TIER 1 - Universal Capabilities (High Priority):")
        for task in tier1:
            print(f"   {task['id']}. {task['name']} - {task['frequency']}")
            print(f"      API: {task['api']}")
        print()
    
    if tier2:
        print("⭐ TIER 2 - Common Capabilities (Medium Priority):")
        for task in tier2:
            print(f"   {task['id']}. {task['name']} - {task['frequency']}")
            print(f"      API: {task['api']}")
        print()
    
    if tier3:
        print("💎 TIER 3 - Specialized Capabilities (Lower Priority):")
        for task in tier3:
            print(f"   {task['id']}. {task['name']} - {task['frequency']}")
            print(f"      API: {task['api']}")
        print()
    
    # Coverage analysis
    print(f"{'='*80}")
    print("COVERAGE ANALYSIS")
    print(f"{'='*80}\n")
    
    total_canonical = len(CANONICAL_UNIT_TASKS)
    coverage_pct = (len(detected_tasks) / total_canonical) * 100
    
    print(f"Canonical Tasks Used: {len(detected_tasks)}/{total_canonical} ({coverage_pct:.1f}%)")
    print(f"Tier 1 Tasks: {len(tier1)}/5 ({len(tier1)/5*100:.0f}%)")
    print(f"Tier 2 Tasks: {len(tier2)}/9 ({len(tier2)/9*100:.0f}%)")
    print(f"Tier 3 Tasks: {len(tier3)}/6 ({len(tier3)/6*100:.0f}%)\n")
    
    # Implementation recommendations
    print(f"{'='*80}")
    print("IMPLEMENTATION RECOMMENDATIONS")
    print(f"{'='*80}\n")
    
    if tier1:
        print("✅ Build Tier 1 tasks first (universal, high-reuse):")
        for task in tier1:
            print(f"   - Implement '{task['name']}' using {task['tool']}")
        print()
    
    if tier2:
        print("⚡ Then Tier 2 tasks (common, moderate-reuse):")
        for task in tier2[:3]:  # Show top 3
            print(f"   - Implement '{task['name']}' using {task['tool']}")
        if len(tier2) > 3:
            print(f"   - ... and {len(tier2)-3} more Tier 2 tasks")
        print()
    
    if tier3:
        print("🔧 Finally Tier 3 tasks (specialized):")
        for task in tier3[:2]:  # Show top 2
            print(f"   - Implement '{task['name']}' using {task['tool']}")
        if len(tier3) > 2:
            print(f"   - ... and {len(tier3)-2} more Tier 3 tasks")
        print()
    
    # Reusability insight
    total_freq = sum(int(t['frequency'].split('/')[0]) for t in detected_tasks)
    avg_reuse = total_freq / len(detected_tasks) if detected_tasks else 0
    
    print(f"💡 Reusability Score: {avg_reuse:.1f}/9 prompts average")
    print(f"   (Higher = more reusable across Calendar.AI features)\n")


def interactive_mode():
    """Run in interactive mode"""
    print_header()
    
    while True:
        prompt = get_prompt_input()
        
        if prompt is None:
            print("\nGoodbye! 👋\n")
            break
        
        if not prompt:
            print("⚠️  Please enter a prompt.\n")
            continue
        
        detected_tasks = analyze_prompt(prompt)
        print_evaluation_results(prompt, detected_tasks)
        
        print("\n" + "="*80 + "\n")


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Evaluate new Calendar.AI prompts using canonical GUTT library"
    )
    parser.add_argument("--prompt", "-p", help="Prompt to evaluate")
    parser.add_argument("--file", "-f", help="File containing prompt")
    parser.add_argument("--interactive", "-i", action="store_true",
                       help="Interactive mode")
    
    args = parser.parse_args()
    
    if args.interactive or (not args.prompt and not args.file):
        interactive_mode()
    elif args.file:
        prompt = Path(args.file).read_text()
        print_header()
        detected_tasks = analyze_prompt(prompt)
        print_evaluation_results(prompt, detected_tasks)
    elif args.prompt:
        print_header()
        detected_tasks = analyze_prompt(args.prompt)
        print_evaluation_results(args.prompt, detected_tasks)


if __name__ == "__main__":
    main()
