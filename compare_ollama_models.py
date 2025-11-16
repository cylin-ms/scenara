#!/usr/bin/env python3
"""
Compare Ollama Models: gpt-oss:20b (localhost) vs gpt-oss:120b (remote)

Tests workback planning generation with both models using the same context
from CXA Newsletter example to compare quality and performance.
"""

import json
import sys
import os
import time
from typing import Dict, Any

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

from src.workback_planning import generate_plan
from tools.llm_api import LLMAPIClient


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


def analyze_structured_output(structured: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze the quality of structured output."""
    metrics = {
        "has_summary": bool(structured.get('summary')),
        "task_count": len(structured.get('tasks', [])),
        "deliverable_count": len(structured.get('deliverables', [])),
        "participant_count": len(structured.get('participants', [])),
        "tasks_with_dependencies": 0,
        "tasks_with_participants": 0,
        "tasks_with_artifacts": 0,
        "avg_task_description_length": 0,
    }
    
    tasks = structured.get('tasks', [])
    if tasks:
        task_desc_lengths = []
        for task in tasks:
            if task.get('depends_on'):
                metrics["tasks_with_dependencies"] += 1
            if task.get('participants'):
                metrics["tasks_with_participants"] += 1
            if task.get('artifacts'):
                metrics["tasks_with_artifacts"] += 1
            desc = task.get('description', '')
            if desc:
                task_desc_lengths.append(len(desc))
        
        if task_desc_lengths:
            metrics["avg_task_description_length"] = sum(task_desc_lengths) // len(task_desc_lengths)
    
    return metrics


def test_model(
    model_name: str,
    base_url: str,
    context: str,
    test_number: int
) -> Dict[str, Any]:
    """Test a single model configuration."""
    
    print_section(f"Test {test_number}: {model_name}")
    print(f"Base URL: {base_url}")
    print(f"Model: {model_name}")
    
    # Configure model
    model_config = {
        "provider": "ollama",
        "model": model_name,
        "temperature": 0.3,  # Slightly higher for creativity
        "base_url": base_url
    }
    
    print("\n🚀 Starting two-stage generation...")
    print("   Stage 1: Analysis (hierarchical breakdown)")
    print("   Stage 2: Structuring (convert to JSON)")
    
    start_time = time.time()
    
    try:
        result = generate_plan(
            context,
            analysis_model_override=model_config,
            structure_model_override=model_config
        )
        
        elapsed = time.time() - start_time
        
        # Analyze results
        analysis_length = len(result.get('analysis', ''))
        structured_json = json.dumps(result.get('structured', {}), indent=2)
        structured_length = len(structured_json)
        
        metrics = analyze_structured_output(result.get('structured', {}))
        
        # Print results
        print(f"\n✅ Generation completed in {format_duration(elapsed)}")
        print(f"\n📊 Output Metrics:")
        print(f"   • Analysis length: {analysis_length:,} chars")
        print(f"   • Structured JSON: {structured_length:,} chars")
        print(f"   • Tasks generated: {metrics['task_count']}")
        print(f"   • Deliverables: {metrics['deliverable_count']}")
        print(f"   • Participants: {metrics['participant_count']}")
        print(f"   • Tasks with dependencies: {metrics['tasks_with_dependencies']}")
        print(f"   • Tasks with participants: {metrics['tasks_with_participants']}")
        print(f"   • Avg task description: {metrics['avg_task_description_length']} chars")
        
        # Preview analysis
        print(f"\n📝 Analysis Preview (first 400 chars):")
        print("-" * 80)
        analysis_preview = result['analysis'][:400]
        print(analysis_preview)
        if len(result['analysis']) > 400:
            print("...")
        
        # Preview structured output
        print(f"\n🏗️  Structured Output Preview:")
        print("-" * 80)
        structured_preview = structured_json[:600]
        print(structured_preview)
        if len(structured_json) > 600:
            print("...")
        
        return {
            "success": True,
            "model": model_name,
            "base_url": base_url,
            "elapsed": elapsed,
            "analysis_length": analysis_length,
            "structured_length": structured_length,
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
            "model": model_name,
            "base_url": base_url,
            "elapsed": elapsed,
            "error": str(e)
        }


def compare_results(result1: Dict[str, Any], result2: Dict[str, Any]):
    """Print comparison of two model results."""
    
    print_section("COMPARISON SUMMARY")
    
    if not result1['success'] or not result2['success']:
        print("\n⚠️  Cannot compare - one or both models failed")
        return
    
    # Speed comparison
    print("\n⚡ Performance:")
    print(f"   • {result1['model']:20s}: {format_duration(result1['elapsed']):>10s}")
    print(f"   • {result2['model']:20s}: {format_duration(result2['elapsed']):>10s}")
    
    speed_ratio = result1['elapsed'] / result2['elapsed']
    if speed_ratio > 1.2:
        print(f"   → {result2['model']} is {speed_ratio:.1f}x faster")
    elif speed_ratio < 0.8:
        print(f"   → {result1['model']} is {1/speed_ratio:.1f}x faster")
    else:
        print(f"   → Similar performance")
    
    # Output size comparison
    print("\n📏 Output Size:")
    print(f"   • Analysis length:")
    print(f"     - {result1['model']:18s}: {result1['analysis_length']:>8,} chars")
    print(f"     - {result2['model']:18s}: {result2['analysis_length']:>8,} chars")
    print(f"   • Structured JSON:")
    print(f"     - {result1['model']:18s}: {result1['structured_length']:>8,} chars")
    print(f"     - {result2['model']:18s}: {result2['structured_length']:>8,} chars")
    
    # Quality metrics comparison
    print("\n🎯 Quality Metrics:")
    m1 = result1['metrics']
    m2 = result2['metrics']
    
    print(f"   • Tasks generated:")
    print(f"     - {result1['model']:18s}: {m1['task_count']:>3}")
    print(f"     - {result2['model']:18s}: {m2['task_count']:>3}")
    
    print(f"   • Tasks with dependencies:")
    print(f"     - {result1['model']:18s}: {m1['tasks_with_dependencies']:>3} ({m1['tasks_with_dependencies']/m1['task_count']*100 if m1['task_count'] else 0:.0f}%)")
    print(f"     - {result2['model']:18s}: {m2['tasks_with_dependencies']:>3} ({m2['tasks_with_dependencies']/m2['task_count']*100 if m2['task_count'] else 0:.0f}%)")
    
    print(f"   • Tasks with participants:")
    print(f"     - {result1['model']:18s}: {m1['tasks_with_participants']:>3} ({m1['tasks_with_participants']/m1['task_count']*100 if m1['task_count'] else 0:.0f}%)")
    print(f"     - {result2['model']:18s}: {m2['tasks_with_participants']:>3} ({m2['tasks_with_participants']/m2['task_count']*100 if m2['task_count'] else 0:.0f}%)")
    
    print(f"   • Deliverables:")
    print(f"     - {result1['model']:18s}: {m1['deliverable_count']:>3}")
    print(f"     - {result2['model']:18s}: {m2['deliverable_count']:>3}")
    
    print(f"   • Participants:")
    print(f"     - {result1['model']:18s}: {m1['participant_count']:>3}")
    print(f"     - {result2['model']:18s}: {m2['participant_count']:>3}")
    
    # Overall assessment
    print("\n🏆 Winner Assessment:")
    
    scores = {result1['model']: 0, result2['model']: 0}
    
    # Speed (favor faster, but not too heavily)
    if speed_ratio > 1.1:
        scores[result2['model']] += 1
        print(f"   • Speed: {result2['model']} ✓")
    elif speed_ratio < 0.9:
        scores[result1['model']] += 1
        print(f"   • Speed: {result1['model']} ✓")
    else:
        print(f"   • Speed: Tie")
    
    # Task count (more tasks = better breakdown)
    if m1['task_count'] > m2['task_count']:
        scores[result1['model']] += 2
        print(f"   • Task breakdown: {result1['model']} ✓✓")
    elif m2['task_count'] > m1['task_count']:
        scores[result2['model']] += 2
        print(f"   • Task breakdown: {result2['model']} ✓✓")
    else:
        print(f"   • Task breakdown: Tie")
    
    # Dependencies (shows understanding of relationships)
    if m1['tasks_with_dependencies'] > m2['tasks_with_dependencies']:
        scores[result1['model']] += 2
        print(f"   • Task dependencies: {result1['model']} ✓✓")
    elif m2['tasks_with_dependencies'] > m1['tasks_with_dependencies']:
        scores[result2['model']] += 2
        print(f"   • Task dependencies: {result2['model']} ✓✓")
    else:
        print(f"   • Task dependencies: Tie")
    
    # Detail level (avg description length)
    if m1['avg_task_description_length'] > m2['avg_task_description_length'] * 1.2:
        scores[result1['model']] += 1
        print(f"   • Detail level: {result1['model']} ✓")
    elif m2['avg_task_description_length'] > m1['avg_task_description_length'] * 1.2:
        scores[result2['model']] += 1
        print(f"   • Detail level: {result2['model']} ✓")
    else:
        print(f"   • Detail level: Tie")
    
    print(f"\n   Final Score:")
    print(f"   • {result1['model']:20s}: {scores[result1['model']]} points")
    print(f"   • {result2['model']:20s}: {scores[result2['model']]} points")
    
    if scores[result1['model']] > scores[result2['model']]:
        print(f"\n   🏆 Overall Winner: {result1['model']}")
    elif scores[result2['model']] > scores[result1['model']]:
        print(f"\n   🏆 Overall Winner: {result2['model']}")
    else:
        print(f"\n   🤝 Tie - both models performed similarly")


def main():
    """Run comparison test."""
    
    # Newsletter workback context from CXA example
    context = """
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
"""
    
    print_section("MODEL COMPARISON: WORKBACK PLANNING", 80)
    print("\n📋 Test Scenario: Newsletter Launch Workback Plan")
    print("   Based on CXA slide07 example")
    print("   Timeline: 4 weeks (T-4w → T-0)")
    print("   Complexity: Multi-stakeholder approval workflow")
    print("\n" + "=" * 80)
    
    # Test localhost gpt-oss:20b
    result_20b = test_model(
        model_name="gpt-oss:20b",
        base_url="http://localhost:11434",
        context=context,
        test_number=1
    )
    
    print("\n" + "=" * 80)
    input("\n⏸️  Press Enter to continue with remote 120b model test...")
    
    # Test remote gpt-oss:120b
    result_120b = test_model(
        model_name="gpt-oss:120b",
        base_url="http://192.168.2.204:11434",
        context=context,
        test_number=2
    )
    
    # Compare results
    compare_results(result_20b, result_120b)
    
    # Save detailed results
    output_file = "ollama_comparison_results.json"
    comparison_data = {
        "test_date": "2025-11-16",
        "test_scenario": "Newsletter Launch Workback Plan (CXA slide07)",
        "context": context,
        "results": {
            "gpt-oss:20b": {
                "success": result_20b['success'],
                "elapsed": result_20b['elapsed'],
                "metrics": result_20b.get('metrics', {}),
                "analysis_length": result_20b.get('analysis_length', 0),
                "structured_length": result_20b.get('structured_length', 0)
            },
            "gpt-oss:120b": {
                "success": result_120b['success'],
                "elapsed": result_120b['elapsed'],
                "metrics": result_120b.get('metrics', {}),
                "analysis_length": result_120b.get('analysis_length', 0),
                "structured_length": result_120b.get('structured_length', 0)
            }
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(comparison_data, f, indent=2)
    
    print_section("RESULTS SAVED")
    print(f"\n📁 Detailed results saved to: {output_file}")
    print("\n💡 Next Steps:")
    print("   1. Review full analysis and structured output for both models")
    print("   2. Consider using 120b for production workback planning")
    print("   3. Test with more complex CXA examples (project launch, QBR)")
    print("   4. Integrate winner into meeting_intelligence.py pipeline")
    print("\n" + "=" * 80)
    
    return 0 if result_20b['success'] and result_120b['success'] else 1


if __name__ == "__main__":
    exit(main())
