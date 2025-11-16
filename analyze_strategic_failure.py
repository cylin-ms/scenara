#!/usr/bin/env python3
"""
Deep Analysis: Why Strategic Initiatives Failed Deliverable Extraction

Investigates the root cause of 0 deliverables in Strategic Initiatives scenario
compared to successful extraction in other scenarios.
"""

import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.workback_planning import generate_plan


def print_section(title: str, width: int = 100):
    """Print formatted section."""
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def analyze_context_complexity(context: str) -> dict:
    """Analyze the complexity of input context."""
    lines = context.strip().split('\n')
    
    # Count explicit mentions
    deliverable_keywords = ['deliverable', 'output', 'artifact', 'document', 'report', 'summary', 'scorecard', 'proposal', 'roadmap']
    participant_keywords = ['participant', 'owner', 'responsible', 'team', 'lead']
    
    deliverable_mentions = sum(1 for line in lines for kw in deliverable_keywords if kw.lower() in line.lower())
    participant_mentions = sum(1 for line in lines for kw in participant_keywords if kw.lower() in line.lower())
    
    return {
        "total_lines": len(lines),
        "total_chars": len(context),
        "deliverable_mentions": deliverable_mentions,
        "participant_mentions": participant_mentions,
        "has_deliverables_section": "Deliverables:" in context,
        "has_participants_section": "Participants:" in context,
        "explicit_deliverables": context.count("\n- ") if "Deliverables:" in context else 0
    }


def compare_contexts():
    """Compare all scenario contexts to identify differences."""
    
    print_section("CONTEXT COMPARISON ANALYSIS")
    
    scenarios = {
        "Newsletter Launch": """
Meeting: Newsletter Launch Planning
Target Date: 2025-12-15
Duration: 4 weeks

Participants:
- Content Owner (content@cxa.com) - Responsible for initial draft
- Leadership Team (lt@cxa.com) - First review cycle
- Executive Team (exec@cxa.com) - Final approval
- Ops/Marketing (ops@cxa.com) - Publication and distribution

Objectives:
1. Create comprehensive newsletter content
2. Complete multi-level review process (LT → Exec)
3. Prepare and publish newsletter on schedule
4. Ensure quality and alignment with company messaging

Milestones (4-week timeline):
- T-4w: Content Due - Initial draft ready
- T-3w: LT Review - Leadership team review cycle
- T-2w: Exec Review - Executive approval
- T-1w: Publish Prep - Final preparation
- T-0: Go Live - Newsletter sent to audience

Key Constraints:
- Multi-stakeholder approval process
- Fixed 4-week timeline
- Quality standards must be met
- Cross-functional coordination required

Deliverables:
- Newsletter content (draft, reviewed, final)
- Review feedback and revisions
- Publication materials and distribution list
""",
        "Project Launch": """
Meeting: Project Launch Planning
Target Date: 2025-04-12
Duration: 6 weeks

Participants:
- Project Lead (project.lead@cxa.com) - Overall project coordination
- PM/Stakeholders (pm@cxa.com) - Requirements and stakeholder management
- Content Team (content@cxa.com) - Content creation and editing
- Team Leads (leads@cxa.com) - Internal review and feedback
- Ops/Marketing (ops@cxa.com) - Publication and launch preparation

Objectives:
1. Launch new project on schedule (April 12, 2025)
2. Complete requirements gathering with all stakeholders
3. Develop high-quality content through iterative review
4. Ensure smooth launch preparation and execution
5. Coordinate across multiple teams (PM, Content, Ops, Leadership)

Milestones (6-week timeline):
- T-6w (Mar 1): Kickoff - Project initiation
- T-5w (Mar 8): Requirements Gathering - Collect all inputs
- T-4w (Mar 15): Initial Draft - First version ready
- T-3w (Mar 22): Internal Review - Team leads provide feedback
- T-2w (Mar 29): Final Edits - Incorporate all feedback
- T-1w (Apr 5): Publish Prep - Prepare for release
- T-0 (Apr 12): Go Live - Launch the project

Key Constraints:
- Fixed 6-week timeline with hard deadline
- Multiple review cycles requiring coordination
- Cross-functional dependencies (Content → Review → Ops)
- Quality standards must be maintained throughout
- Stakeholder approval required at key milestones

Deliverables:
- Project requirements document
- Content drafts (initial, reviewed, final)
- Review feedback and revision tracking
- Launch materials and preparation checklist
- Go-live documentation
""",
        "QBR Planning": """
Meeting: Quarterly Business Review (QBR) Planning
Next QBR Date: 2026-03-19
Duration: Quarterly cycle (3 months)

Participants:
- Nicolle (nicolle@cxa.com) - QBR Owner and facilitator
- Executive Team (exec@cxa.com) - Senior leadership participants
- Business Unit Leaders (bu.leads@cxa.com) - Functional area representatives
- Analytics Team (analytics@cxa.com) - Data preparation and reporting
- Operations (ops@cxa.com) - Logistics and coordination

Objectives:
1. Conduct comprehensive quarterly business review
2. Review performance metrics and KPIs across all business units
3. Identify strategic initiatives and priorities for next quarter
4. Align leadership on key decisions and resource allocation
5. Document action items and accountability for follow-up

QBR Schedule (Quarterly):
- September 18, 2025: Q3 2025 Review (offline session)
- November 19, 2025: Q4 2025 Review (offline session)
- March 19, 2026: Q1 2026 Review (quarterly review)
- June 18, 2026: Q2 2026 Review (quarterly review)

Key Constraints:
- Quarterly cadence must be maintained
- Executive stakeholder availability (offline sessions)
- Comprehensive data preparation required (2-3 weeks lead time)
- Multiple business units need coordination
- Strategic decisions require follow-up tracking

Deliverables:
- QBR preparation materials (data, reports, presentations)
- Business performance analysis (metrics, trends, insights)
- Strategic recommendations and decision proposals
- QBR session documentation and meeting minutes
- Action item tracking and accountability assignments
- Follow-up reports for implemented decisions
""",
        "Strategic Initiatives Review": """
Meeting: Strategic Initiatives Review
Target Date: 2025-11-12
Duration: 2-week workback cycle

Participants:
- Nicolle (nicolle@cxa.com) - Strategic Initiatives Owner
- Executive Leadership (exec@cxa.com) - Strategic decision makers
- Initiative Leads (initiative.leads@cxa.com) - Program owners
- Strategy Team (strategy@cxa.com) - Analysis and recommendations
- Finance (finance@cxa.com) - Budget and resource allocation

Objectives:
1. Review current strategic initiatives progress and status
2. Evaluate initiative performance against strategic objectives
3. Make go/no-go decisions on initiatives based on data
4. Prioritize initiatives for next planning cycle
5. Align resources and budget to highest-priority initiatives

Strategic Context:
- Part of regular strategic planning process
- 2-week preparation cycle (rapid turnaround)
- High-level executive review (board-level visibility)
- Data-driven decision making required
- Cross-initiative portfolio view needed

Key Constraints:
- Short 2-week cycle demands efficient preparation
- Executive availability limited (must schedule in advance)
- Multiple initiative owners need coordination
- Financial analysis required for budget decisions
- Strategic alignment with company objectives critical

Deliverables:
- Strategic initiatives portfolio summary
- Initiative performance scorecards (status, metrics, ROI)
- Strategic recommendations (continue, pivot, terminate)
- Resource allocation proposals (budget, headcount)
- Executive decision documentation
- Updated strategic roadmap with priorities
"""
    }
    
    print("\n📊 Context Complexity Metrics:")
    print("-" * 100)
    print(f"{'Scenario':<30} {'Lines':<8} {'Chars':<8} {'Has Deliv':<12} {'Deliv Count':<13} {'Deliv Mentions':<15}")
    print("-" * 100)
    
    analyses = {}
    for name, context in scenarios.items():
        analysis = analyze_context_complexity(context)
        analyses[name] = analysis
        
        print(f"{name:<30} {analysis['total_lines']:<8} {analysis['total_chars']:<8} "
              f"{'✅' if analysis['has_deliverables_section'] else '❌':<12} "
              f"{analysis['explicit_deliverables']:<13} {analysis['deliverable_mentions']:<15}")
    
    print("-" * 100)
    
    # Identify key differences
    print_section("KEY OBSERVATIONS")
    
    print("\n🔍 Deliverables Section Analysis:")
    for name, analysis in analyses.items():
        status = "✅ Present" if analysis['has_deliverables_section'] else "❌ Missing"
        count = analysis['explicit_deliverables']
        print(f"   • {name:<30}: {status} ({count} explicit items)")
    
    print("\n🔍 Context Characteristics:")
    si_analysis = analyses["Strategic Initiatives Review"]
    print(f"\nStrategic Initiatives Review:")
    print(f"   • Has 'Deliverables:' section: {'✅ YES' if si_analysis['has_deliverables_section'] else '❌ NO'}")
    print(f"   • Explicit deliverable items: {si_analysis['explicit_deliverables']}")
    print(f"   • Deliverable keyword mentions: {si_analysis['deliverable_mentions']}")
    print(f"   • Total context length: {si_analysis['total_chars']} chars")
    
    # Test with Strategic Initiatives
    print_section("REGENERATING STRATEGIC INITIATIVES WITH DETAILED LOGGING")
    
    context = scenarios["Strategic Initiatives Review"]
    
    model_config = {
        "provider": "ollama",
        "model": "gpt-oss:120b",
        "temperature": 0.3,
        "base_url": "http://192.168.2.204:11434",
        "timeout": 300.0
    }
    
    print("\n🔄 Regenerating to capture full output...")
    print("   (This will take ~4 minutes)")
    
    result = generate_plan(
        context,
        analysis_model_override=model_config,
        structure_model_override=model_config
    )
    
    # Detailed analysis of output
    print_section("DETAILED OUTPUT ANALYSIS")
    
    analysis = result.get('analysis', '')
    structured = result.get('structured', {})
    
    print(f"\n📝 Analysis Stage Output ({len(analysis)} chars):")
    print("-" * 100)
    
    # Search for deliverable mentions in analysis
    deliverable_lines = [line for line in analysis.split('\n') if any(kw in line.lower() for kw in ['deliverable', 'outcome', 'artifact', 'document', 'report'])]
    
    print(f"\n🔍 Lines mentioning deliverables/outcomes ({len(deliverable_lines)} found):")
    for i, line in enumerate(deliverable_lines[:10], 1):
        print(f"{i}. {line.strip()}")
    if len(deliverable_lines) > 10:
        print(f"   ... and {len(deliverable_lines) - 10} more")
    
    # Check if analysis identified deliverables as "Outcomes"
    print(f"\n📦 Analysis Sections:")
    if "# Outcomes" in analysis:
        print("   ✅ Found '# Outcomes' section")
        outcomes_section = analysis.split("# Outcomes")[1].split("#")[0] if "# Outcomes" in analysis else ""
        outcome_count = outcomes_section.count("## ")
        print(f"   • Number of outcomes identified: {outcome_count}")
    else:
        print("   ❌ No '# Outcomes' section found")
    
    # Analyze structured output
    print(f"\n🏗️  Structured Output Analysis:")
    print("-" * 100)
    
    print(f"\nTop-level fields present:")
    for key in structured.keys():
        value = structured[key]
        if isinstance(value, list):
            print(f"   • {key}: {len(value)} items")
        else:
            print(f"   • {key}: {type(value).__name__}")
    
    # Deep dive into deliverables field
    deliverables = structured.get('deliverables', [])
    print(f"\n📦 Deliverables Field: {len(deliverables)} items")
    
    if len(deliverables) == 0:
        print("   ❌ EMPTY - This is the problem!")
        print("\n   Possible causes:")
        print("   1. Analysis stage identified outcomes but didn't label them as deliverables")
        print("   2. Structure stage failed to map outcomes → deliverables")
        print("   3. JSON parsing dropped the deliverables array")
        print("   4. Model interpreted 'deliverables' differently for strategy meetings")
    else:
        print("   ✅ Deliverables found:")
        for d in deliverables[:5]:
            print(f"      • {d.get('name', 'Unknown')}")
    
    # Check if deliverables might be in tasks instead
    tasks = structured.get('tasks', [])
    print(f"\n✓ Tasks Field: {len(tasks)} items")
    
    # Look for task names that match expected deliverables
    expected_deliverables = [
        "portfolio summary",
        "performance scorecards",
        "recommendations",
        "resource allocation",
        "decision documentation",
        "roadmap"
    ]
    
    matching_tasks = []
    for task in tasks:
        task_name = task.get('name', '').lower()
        for expected in expected_deliverables:
            if expected in task_name:
                matching_tasks.append((task.get('name'), expected))
    
    if matching_tasks:
        print(f"\n   🔍 Found {len(matching_tasks)} tasks that might be deliverables:")
        for task_name, keyword in matching_tasks[:5]:
            print(f"      • '{task_name}' (matches '{keyword}')")
        if len(matching_tasks) > 5:
            print(f"      ... and {len(matching_tasks) - 5} more")
    
    # Extract full analysis Outcomes section
    print_section("FULL ANALYSIS OUTCOMES SECTION")
    
    if "# Outcomes" in analysis:
        outcomes_start = analysis.find("# Outcomes")
        # Find next major section or end
        next_section = analysis.find("\n# ", outcomes_start + 1)
        if next_section == -1:
            next_section = len(analysis)
        
        outcomes_text = analysis[outcomes_start:next_section]
        print("\n" + outcomes_text[:2000])
        if len(outcomes_text) > 2000:
            print(f"\n... ({len(outcomes_text) - 2000} more chars)")
    
    # Save full output for manual inspection
    with open('strategic_initiatives_debug.json', 'w') as f:
        json.dump({
            "analysis": analysis,
            "structured": structured,
            "deliverables_found": len(deliverables),
            "tasks_found": len(tasks),
            "participants_found": len(structured.get('participants', []))
        }, f, indent=2)
    
    print_section("ROOT CAUSE ANALYSIS")
    
    print("\n🔍 HYPOTHESIS TESTING:")
    print("-" * 100)
    
    # Hypothesis 1: Analysis stage didn't identify deliverables
    has_outcomes = "# Outcomes" in analysis
    outcome_count = analysis.count("## ") if has_outcomes else 0
    
    print(f"\n1. Analysis Stage Performance:")
    print(f"   • Identified Outcomes section: {'✅ YES' if has_outcomes else '❌ NO'}")
    print(f"   • Number of outcomes: {outcome_count}")
    print(f"   • Verdict: {'✅ Analysis stage worked' if outcome_count >= 5 else '❌ Analysis stage failed'}")
    
    # Hypothesis 2: Structure stage failed to convert outcomes to deliverables
    if outcome_count >= 5 and len(deliverables) == 0:
        print(f"\n2. Structure Stage Performance:")
        print(f"   • Analysis found {outcome_count} outcomes")
        print(f"   • Structured output has {len(deliverables)} deliverables")
        print(f"   • Verdict: ❌ STRUCTURE STAGE FAILED TO CONVERT OUTCOMES → DELIVERABLES")
        print(f"   • This is the PRIMARY ROOT CAUSE")
    
    # Hypothesis 3: Different terminology used
    print(f"\n3. Terminology Analysis:")
    print(f"   • Context uses word 'Deliverables': {'✅ YES' if 'Deliverables:' in context else '❌ NO'}")
    print(f"   • Analysis uses word 'Outcomes': {'✅ YES' if '# Outcomes' in analysis else '❌ NO'}")
    print(f"   • Structured JSON has 'deliverables' field: {'✅ YES' if 'deliverables' in structured else '❌ NO'}")
    print(f"   • Verdict: {'❌ Terminology mismatch may confuse structure stage' if has_outcomes and len(deliverables) == 0 else '✅ Terminology aligned'}")
    
    # Hypothesis 4: Strategic context interpreted differently
    print(f"\n4. Context Interpretation:")
    print(f"   • Meeting type: Strategic Initiatives Review (high-level)")
    print(f"   • Duration: 2 weeks (shortest of all scenarios)")
    print(f"   • Model may interpret strategy meetings as producing decisions, not deliverables")
    print(f"   • Verdict: ⚠️  Possible contributing factor")
    
    print_section("RECOMMENDATIONS")
    
    print("\n💡 Immediate Fixes:")
    print("-" * 100)
    print("\n1. PROMPT ENGINEERING:")
    print("   • Update structure.md prompt to explicitly map 'Outcomes' → 'deliverables'")
    print("   • Add examples showing high-level strategic deliverables")
    print("   • Emphasize that all outcomes should become deliverables")
    
    print("\n2. ANALYSIS PROMPT ENHANCEMENT:")
    print("   • Strengthen 'Outcomes' section instructions in analyze.md")
    print("   • Add explicit guidance: 'Outcomes are deliverables'")
    print("   • Include strategy meeting examples")
    
    print("\n3. POST-PROCESSING:")
    print("   • Add validation: if outcomes > 0 and deliverables == 0, extract from outcomes")
    print("   • Implement fallback logic to convert outcome sections to deliverables")
    
    print("\n4. TESTING:")
    print("   • Re-test Strategic Initiatives with enhanced prompts")
    print("   • Validate on other high-level strategy scenarios")
    
    print("\n" + "=" * 100)
    print("📁 Full debug output saved to: strategic_initiatives_debug.json")
    print("=" * 100)


if __name__ == "__main__":
    compare_contexts()
