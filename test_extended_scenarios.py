#!/usr/bin/env python3
"""
Extended Model Testing: Complex CXA Scenarios

Tests gpt-oss:120b with three complex workback planning scenarios:
1. Project Launch (6-week timeline)
2. QBR Planning (quarterly cycle)
3. Strategic Initiatives Review (2-week cycle)
"""

import json
import sys
import os
import time
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.workback_planning import generate_plan


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 60:
        return f"{seconds:.1f}s"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}m {secs}s"


def print_section(title: str, width: int = 80):
    """Print a formatted section header."""
    print("\n" + "=" * width)
    print(f"{title:^{width}}")
    print("=" * width)


def analyze_result(result: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze workback planning result."""
    structured = result.get('structured', {})
    analysis = result.get('analysis', '')
    
    metrics = {
        "success": True,
        "analysis_length": len(analysis),
        "structured_json_length": len(json.dumps(structured, indent=2)),
        "has_summary": bool(structured.get('summary')),
        "task_count": len(structured.get('tasks', [])),
        "deliverable_count": len(structured.get('deliverables', [])),
        "participant_count": len(structured.get('participants', [])),
        "reference_count": len(structured.get('references', [])),
        "tasks_with_dependencies": 0,
        "tasks_with_participants": 0,
        "tasks_with_artifacts": 0,
        "milestones_identified": 0,
    }
    
    # Analyze tasks
    for task in structured.get('tasks', []):
        if task.get('depends_on'):
            metrics["tasks_with_dependencies"] += 1
        if task.get('participants'):
            metrics["tasks_with_participants"] += 1
        if task.get('artifacts'):
            metrics["tasks_with_artifacts"] += 1
        if task.get('is_milestone'):
            metrics["milestones_identified"] += 1
    
    return metrics


def test_scenario(
    scenario_name: str,
    context: str,
    model: str = "gpt-oss:120b",
    base_url: str = "http://192.168.2.204:11434"
) -> Dict[str, Any]:
    """Test a single scenario."""
    
    print_section(f"Scenario: {scenario_name}")
    print(f"Model: {model}")
    print(f"Server: {base_url}")
    
    # Configure model
    model_config = {
        "provider": "ollama",
        "model": model,
        "temperature": 0.3,
        "base_url": base_url,
        "timeout": 300.0
    }
    
    print("\n🚀 Generating workback plan...")
    print("   Stage 1: Deep analysis with hierarchical breakdown")
    print("   Stage 2: Convert to structured JSON with full metadata")
    
    start_time = time.time()
    
    try:
        result = generate_plan(
            context,
            analysis_model_override=model_config,
            structure_model_override=model_config
        )
        
        elapsed = time.time() - start_time
        
        # Analyze results
        metrics = analyze_result(result)
        metrics["elapsed"] = elapsed
        metrics["scenario"] = scenario_name
        
        # Print results
        print(f"\n✅ Generation completed in {format_duration(elapsed)}")
        print(f"\n📊 Quality Metrics:")
        print(f"   • Analysis length: {metrics['analysis_length']:,} chars")
        print(f"   • Structured JSON: {metrics['structured_json_length']:,} chars")
        print(f"   • Summary present: {'✅' if metrics['has_summary'] else '❌'}")
        print(f"   • Tasks: {metrics['task_count']}")
        print(f"   • Deliverables: {metrics['deliverable_count']}")
        print(f"   • Participants: {metrics['participant_count']}")
        print(f"   • References: {metrics['reference_count']}")
        print(f"   • Milestones: {metrics['milestones_identified']}")
        print(f"   • Tasks with dependencies: {metrics['tasks_with_dependencies']} ({metrics['tasks_with_dependencies']/metrics['task_count']*100 if metrics['task_count'] else 0:.0f}%)")
        print(f"   • Tasks with participants: {metrics['tasks_with_participants']} ({metrics['tasks_with_participants']/metrics['task_count']*100 if metrics['task_count'] else 0:.0f}%)")
        
        # Preview analysis
        analysis = result.get('analysis', '')
        print(f"\n📝 Analysis Preview (first 500 chars):")
        print("-" * 80)
        print(analysis[:500] + ("..." if len(analysis) > 500 else ""))
        
        # Preview key structured elements
        structured = result.get('structured', {})
        print(f"\n🏗️  Structured Elements:")
        print("-" * 80)
        
        if structured.get('participants'):
            print(f"\n👥 Participants ({len(structured['participants'])}):")
            for p in structured['participants'][:3]:
                print(f"   • {p.get('name', 'Unknown')} ({p.get('email', 'N/A')})")
            if len(structured['participants']) > 3:
                print(f"   ... and {len(structured['participants']) - 3} more")
        
        if structured.get('deliverables'):
            print(f"\n📦 Deliverables ({len(structured['deliverables'])}):")
            for d in structured['deliverables'][:3]:
                print(f"   • {d.get('name', 'Unknown')}")
            if len(structured['deliverables']) > 3:
                print(f"   ... and {len(structured['deliverables']) - 3} more")
        
        if structured.get('tasks'):
            print(f"\n✓ Sample Tasks (showing first 3 of {len(structured['tasks'])}):")
            for t in structured['tasks'][:3]:
                print(f"   • {t.get('name', 'Unknown')}")
                if t.get('depends_on'):
                    print(f"     ↳ Depends on: {', '.join(t['depends_on'])}")
        
        return {
            "success": True,
            "metrics": metrics,
            "result": result
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"\n❌ Generation failed after {format_duration(elapsed)}")
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "success": False,
            "scenario": scenario_name,
            "elapsed": elapsed,
            "error": str(e)
        }


def main():
    """Run all three scenario tests."""
    
    print_section("EXTENDED WORKBACK PLANNING TESTING", 80)
    print("\n📋 Testing Scenarios:")
    print("   1. Newsletter Launch (baseline - already tested)")
    print("   2. Project Launch (6-week timeline, multiple phases)")
    print("   3. QBR Planning (quarterly cycle, executive stakeholders)")
    print("   4. Strategic Initiatives Review (2-week cycle, high-level strategy)")
    print("\n🎯 Model: gpt-oss:120b on 192.168.2.204:11434")
    print("=" * 80)
    
    # Load baseline Newsletter test results
    baseline_result = None
    try:
        with open('ollama_comparison_results.json', 'r') as f:
            comparison_data = json.load(f)
            baseline_metrics = comparison_data['results']['gpt-oss:120b']
            baseline_result = {
                "success": True,
                "metrics": {
                    "scenario": "Newsletter Launch",
                    "elapsed": baseline_metrics['elapsed'],
                    "analysis_length": baseline_metrics['analysis_length'],
                    "structured_json_length": baseline_metrics['structured_length'],
                    "has_summary": baseline_metrics['metrics']['has_summary'],
                    "task_count": baseline_metrics['metrics']['task_count'],
                    "deliverable_count": baseline_metrics['metrics']['deliverable_count'],
                    "participant_count": baseline_metrics['metrics']['participant_count'],
                    "reference_count": 0,
                    "tasks_with_dependencies": baseline_metrics['metrics']['tasks_with_dependencies'],
                    "tasks_with_participants": baseline_metrics['metrics']['tasks_with_participants'],
                    "tasks_with_artifacts": baseline_metrics['metrics']['tasks_with_artifacts'],
                    "milestones_identified": 0,
                }
            }
            print("\n✅ Loaded baseline Newsletter Launch results (2m 58s)")
    except Exception as e:
        print(f"\n⚠️  Could not load baseline results: {e}")
        print("   Continuing with new scenarios only...")
    
    # Define test scenarios
    scenarios = []
    
    # Scenario 1: Project Launch
    scenarios.append({
        "name": "Project Launch",
        "context": """
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
"""
    })
    
    # Scenario 2: QBR Planning
    scenarios.append({
        "name": "QBR Planning",
        "context": """
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
"""
    })
    
    # Scenario 3: Strategic Initiatives Review
    scenarios.append({
        "name": "Strategic Initiatives Review",
        "context": """
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
    })
    
    # Run all tests
    results = []
    
    # Add baseline if available
    if baseline_result:
        results.append(baseline_result)
        print("\n" + "=" * 80)
        print("BASELINE TEST (from previous comparison)")
        print("=" * 80)
        print(f"✅ Newsletter Launch: {format_duration(baseline_result['metrics']['elapsed'])}")
        print(f"   • Tasks: {baseline_result['metrics']['task_count']}")
        print(f"   • Deliverables: {baseline_result['metrics']['deliverable_count']}")
        print(f"   • Participants: {baseline_result['metrics']['participant_count']}")
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i + (1 if baseline_result else 0)} of {len(scenarios) + (1 if baseline_result else 0)}")
        print(f"{'='*80}")
        
        result = test_scenario(
            scenario_name=scenario["name"],
            context=scenario["context"]
        )
        results.append(result)
    
    # Summary comparison
    print_section("COMPREHENSIVE SUMMARY: ALL SCENARIOS")
    
    total_scenarios = len(results)
    successful_tests = sum(1 for r in results if r['success'])
    
    print(f"\n📊 Test Completion: {successful_tests}/{total_scenarios} scenarios passed")
    
    # Create comparison table
    print("\n📊 Comparative Metrics:")
    print("-" * 80)
    print(f"{'Scenario':<30} {'Time':<12} {'Tasks':<8} {'Deliv':<8} {'Parts':<8} {'Status':<10}")
    print("-" * 80)
    
    for result in results:
        if result['success']:
            m = result['metrics']
            print(f"{m['scenario']:<30} {format_duration(m['elapsed']):<12} {m['task_count']:<8} {m['deliverable_count']:<8} {m['participant_count']:<8} {'✅ Pass':<10}")
        else:
            print(f"{result['scenario']:<30} {format_duration(result['elapsed']):<12} {'N/A':<8} {'N/A':<8} {'N/A':<8} {'❌ Fail':<10}")
    
    print("-" * 80)
    
    # Detailed metrics
    if all(r['success'] for r in results):
        print("\n📈 Detailed Analysis:")
        print("-" * 80)
        
        for result in results:
            m = result['metrics']
            print(f"\n{m['scenario']}:")
            print(f"   • Total time: {format_duration(m['elapsed'])}")
            print(f"   • Analysis: {m['analysis_length']:,} chars")
            print(f"   • Structured JSON: {m['structured_json_length']:,} chars")
            print(f"   • Tasks: {m['task_count']} ({m['tasks_with_dependencies']} with deps)")
            print(f"   • Deliverables: {m['deliverable_count']}")
            print(f"   • Participants: {m['participant_count']}")
            print(f"   • Milestones: {m['milestones_identified']}")
        
        # Quality assessment
        print("\n🎯 Quality Assessment:")
        print("-" * 80)
        
        avg_tasks = sum(r['metrics']['task_count'] for r in results) / len(results)
        avg_deliverables = sum(r['metrics']['deliverable_count'] for r in results) / len(results)
        avg_participants = sum(r['metrics']['participant_count'] for r in results) / len(results)
        avg_time = sum(r['metrics']['elapsed'] for r in results) / len(results)
        
        print(f"   • Average tasks per scenario: {avg_tasks:.1f}")
        print(f"   • Average deliverables per scenario: {avg_deliverables:.1f}")
        print(f"   • Average participants per scenario: {avg_participants:.1f}")
        print(f"   • Average generation time: {format_duration(avg_time)}")
        
        # Success criteria check
        print("\n✅ Success Criteria Check:")
        print("-" * 80)
        all_have_participants = all(r['metrics']['participant_count'] > 0 for r in results)
        all_have_deliverables = all(r['metrics']['deliverable_count'] > 0 for r in results)
        all_under_5min = all(r['metrics']['elapsed'] < 300 for r in results)
        
        print(f"   • All scenarios extracted participants: {'✅ PASS' if all_have_participants else '❌ FAIL'}")
        print(f"   • All scenarios identified deliverables: {'✅ PASS' if all_have_deliverables else '❌ FAIL'}")
        print(f"   • All scenarios completed <5 minutes: {'✅ PASS' if all_under_5min else '❌ FAIL'}")
        
        if all_have_participants and all_have_deliverables and all_under_5min:
            print("\n🏆 OVERALL: ALL TESTS PASSED ✅")
            print("   gpt-oss:120b is ready for production deployment!")
        else:
            print("\n⚠️  OVERALL: SOME CRITERIA NOT MET")
    
    # Save results
    output_file = "extended_scenario_testing_results.json"
    test_data = {
        "test_date": "2025-11-16",
        "model": "gpt-oss:120b",
        "server": "http://192.168.2.204:11434",
        "scenarios": []
    }
    
    for result in results:
        if result['success']:
            test_data['scenarios'].append({
                "name": result['metrics']['scenario'],
                "elapsed": result['metrics']['elapsed'],
                "metrics": {
                    k: v for k, v in result['metrics'].items() 
                    if k not in ['scenario']
                }
            })
        else:
            test_data['scenarios'].append({
                "name": result['scenario'],
                "success": False,
                "error": result['error']
            })
    
    with open(output_file, 'w') as f:
        json.dump(test_data, f, indent=2)
    
    print(f"\n📁 Results saved to: {output_file}")
    print("\n" + "=" * 80)
    
    return 0 if all(r['success'] for r in results) else 1


if __name__ == "__main__":
    exit(main())
