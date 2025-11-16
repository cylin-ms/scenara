#!/usr/bin/env python3
"""
Workback Scenario Training Data Generator

Generates evaluation and training data from the 7 high-complexity meeting scenarios
for post-training the meeting intelligence system.

These scenarios represent critical enterprise meetings that require sophisticated
workback planning and preparation.

Usage:
    # Generate training data for all 7 scenarios
    python tools/generate_workback_training_data.py --output post_training/data/training/workback_scenarios.jsonl
    
    # Generate with evaluation splits
    python tools/generate_workback_training_data.py --output post_training/data/training/workback_scenarios.jsonl --eval-split 0.2
    
    # Generate variations for data augmentation
    python tools/generate_workback_training_data.py --output post_training/data/training/workback_scenarios.jsonl --variations 3
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4


# 7 Top Meeting Type Scenarios for Post-Training
WORKBACK_SCENARIOS = {
    "quarterly_business_review": {
        "meeting_type": "Quarterly Business Review (QBR)",
        "complexity": "critical",
        "importance_label": "critical",
        "prep_needed": True,
        "prep_time_minutes": 300,  # 5 hours
        "typical_duration_minutes": 120,
        "typical_attendee_count": 20,
        "key_roles": ["CEO", "CFO", "Division Heads", "Key Stakeholders"],
        "preparation_tasks": [
            "Data collection from all divisions",
            "Financial performance analysis",
            "Operational metrics compilation",
            "Executive deck creation",
            "Pre-read distribution",
            "Rehearsal and Q&A prep"
        ],
        "reasoning": "Quarterly business reviews are board-level strategic meetings requiring extensive cross-functional data collection, executive-level synthesis, and comprehensive performance analysis. Typical preparation includes 21+ days of milestone-driven workback planning.",
        "workback_file": "WORKBACK_PLAN_01_QBR.md"
    },
    
    "board_of_directors": {
        "meeting_type": "Board of Directors Meeting",
        "complexity": "critical",
        "importance_label": "critical",
        "prep_needed": True,
        "prep_time_minutes": 360,  # 6 hours
        "typical_duration_minutes": 180,
        "typical_attendee_count": 11,
        "key_roles": ["Board Members", "CEO", "CFO", "General Counsel"],
        "preparation_tasks": [
            "Board package preparation",
            "Fiduciary materials compilation",
            "Legal review and compliance checks",
            "Financial statements finalization",
            "Strategic presentations",
            "Governance documentation"
        ],
        "reasoning": "Board meetings require the highest level of preparation with fiduciary responsibilities, legal compliance, and governance requirements. Materials must be meticulously prepared, reviewed by legal counsel, and distributed well in advance per board bylaws.",
        "workback_file": "WORKBACK_PLAN_02_BOARD_DIRECTORS.md"
    },
    
    "executive_sales_presentation": {
        "meeting_type": "Executive Sales Presentation",
        "complexity": "high",
        "importance_label": "critical",
        "prep_needed": True,
        "prep_time_minutes": 180,  # 3 hours
        "typical_duration_minutes": 90,
        "typical_attendee_count": 6,
        "key_roles": ["Customer CIO", "Customer CFO", "VP Sales", "Solutions Architect"],
        "preparation_tasks": [
            "Customer research and intelligence",
            "ROI model customization",
            "Technical solution design",
            "Competitive analysis",
            "Executive presentation",
            "Demo preparation"
        ],
        "reasoning": "High-stakes sales presentations to C-level executives require deep customer research, customized ROI analysis, technical solution validation, and rehearsed delivery. Success depends on understanding customer pain points and demonstrating concrete business value.",
        "workback_file": "WORKBACK_PLAN_03_SALES_PRESENTATION.md"
    },
    
    "product_launch_decision": {
        "meeting_type": "Product Launch Go/No-Go Decision",
        "complexity": "critical",
        "importance_label": "critical",
        "prep_needed": True,
        "prep_time_minutes": 240,  # 4 hours
        "typical_duration_minutes": 120,
        "typical_attendee_count": 12,
        "key_roles": ["CEO", "CTO", "CMO", "VP Product", "VP Sales"],
        "preparation_tasks": [
            "Launch readiness checklist",
            "Technical quality metrics",
            "Marketing campaign readiness",
            "Sales enablement verification",
            "Customer support readiness",
            "Risk assessment and mitigation"
        ],
        "reasoning": "Product launch decisions are high-risk, high-impact moments requiring comprehensive readiness assessment across engineering, marketing, sales, and support. Go/no-go criteria must be objectively evaluated with clear risk mitigation plans.",
        "workback_file": "WORKBACK_PLAN_04_PRODUCT_LAUNCH.md"
    },
    
    "compliance_review": {
        "meeting_type": "Annual SOX 404 Compliance Review",
        "complexity": "high",
        "importance_label": "critical",
        "prep_needed": True,
        "prep_time_minutes": 300,  # 5 hours
        "typical_duration_minutes": 180,
        "typical_attendee_count": 8,
        "key_roles": ["External Auditors", "CFO", "CTO", "Chief Compliance Officer"],
        "preparation_tasks": [
            "Internal controls testing documentation",
            "Control deficiency analysis",
            "Remediation plans preparation",
            "IT general controls evidence",
            "Management representation letters",
            "Audit committee materials"
        ],
        "reasoning": "SOX 404 compliance reviews are legally mandated with serious consequences for deficiencies. Preparation requires meticulous documentation of internal controls testing, evidence collection, and coordination with external auditors. Any control deficiencies must have formal remediation plans.",
        "workback_file": "WORKBACK_PLAN_05_COMPLIANCE_REVIEW.md"
    },
    
    "earnings_call": {
        "meeting_type": "Quarterly Earnings Call",
        "complexity": "critical",
        "importance_label": "critical",
        "prep_needed": True,
        "prep_time_minutes": 360,  # 6 hours
        "typical_duration_minutes": 90,
        "typical_attendee_count": 500,
        "key_roles": ["CEO", "CFO", "IR Director", "Analysts", "Investors"],
        "preparation_tasks": [
            "Financial results finalization",
            "Earnings script preparation",
            "Guidance modeling",
            "Q&A preparation (anticipated questions)",
            "Legal review (Reg FD compliance)",
            "Analyst feedback incorporation"
        ],
        "reasoning": "Earnings calls are public events with regulatory requirements (Reg FD) and significant market impact. Preparation requires financial accuracy, legal compliance, coordinated messaging, and extensive Q&A rehearsal. Poor preparation can result in stock volatility and investor loss of confidence.",
        "workback_file": "WORKBACK_PLAN_06_INVESTOR_RELATIONS.md"
    },
    
    "ma_deal_approval": {
        "meeting_type": "M&A Deal Approval (Board)",
        "complexity": "critical",
        "importance_label": "critical",
        "prep_needed": True,
        "prep_time_minutes": 480,  # 8 hours
        "typical_duration_minutes": 360,
        "typical_attendee_count": 14,
        "key_roles": ["Board Members", "CEO", "CFO", "M&A Advisors", "Legal Counsel"],
        "preparation_tasks": [
            "Due diligence summary",
            "Financial valuation analysis",
            "Strategic rationale documentation",
            "Integration planning",
            "Risk assessment and mitigation",
            "Legal and regulatory review",
            "Fairness opinion from advisors"
        ],
        "reasoning": "M&A board approvals are among the most complex decisions a company makes, often involving hundreds of millions in capital. Preparation requires comprehensive due diligence, financial modeling, strategic analysis, integration planning, and legal review. Board members need extensive materials for informed decision-making.",
        "workback_file": "WORKBACK_PLAN_07_M&A_DEAL.md"
    }
}


def generate_meeting_object(
    scenario_key: str,
    scenario: Dict[str, Any],
    meeting_json: Dict[str, Any],
    persona_id: str = "executive",
    variation_id: int = 0
) -> Dict[str, Any]:
    """
    Generate a training data object from a workback scenario.
    
    Args:
        scenario_key: Scenario identifier
        scenario: Scenario metadata
        meeting_json: Graph API meeting object
        persona_id: Persona identifier for this training example
        variation_id: Variation number for data augmentation
        
    Returns:
        Training data object with Graph API schema + training fields
    """
    # Start with the Graph API meeting object
    training_data = dict(meeting_json)
    
    # Add training-specific fields
    training_data.update({
        "importance_label": scenario["importance_label"],
        "prep_needed": scenario["prep_needed"],
        "prep_time_minutes": scenario["prep_time_minutes"],
        "reasoning": scenario["reasoning"],
        "persona_id": persona_id,
        "generation_timestamp": datetime.utcnow().isoformat() + "Z",
        "scenario_key": scenario_key,
        "variation_id": variation_id
    })
    
    # Add workback-specific training metadata
    training_data["_training_metadata"] = {
        "source": "workback_scenario",
        "scenario_file": scenario["workback_file"],
        "complexity": scenario["complexity"],
        "meeting_type": scenario["meeting_type"],
        "preparation_tasks": scenario["preparation_tasks"],
        "key_roles": scenario["key_roles"],
        "typical_duration_minutes": scenario["typical_duration_minutes"],
        "typical_attendee_count": scenario["typical_attendee_count"]
    }
    
    return training_data


def create_variations(
    scenario_key: str,
    scenario: Dict[str, Any],
    meeting_json: Dict[str, Any],
    num_variations: int = 1
) -> List[Dict[str, Any]]:
    """
    Create variations of a scenario for data augmentation.
    
    Variations can include:
    - Different personas (executive, individual contributor, manager)
    - Different prep time estimates
    - Different reasoning emphasis
    - Different attendee counts
    
    Args:
        scenario_key: Scenario identifier
        scenario: Scenario metadata
        meeting_json: Graph API meeting object
        num_variations: Number of variations to generate
        
    Returns:
        List of training data variations
    """
    variations = []
    personas = ["executive", "senior-manager", "individual-contributor"]
    
    for i in range(num_variations):
        persona = personas[i % len(personas)]
        
        # Adjust prep time based on persona
        prep_time_adjustment = {
            "executive": 1.2,  # Executives need more prep
            "senior-manager": 1.0,  # Baseline
            "individual-contributor": 0.8  # ICs may need less strategic prep
        }
        
        adjusted_prep_time = int(
            scenario["prep_time_minutes"] * prep_time_adjustment[persona]
        )
        
        # Create variation
        variation = generate_meeting_object(
            scenario_key,
            {**scenario, "prep_time_minutes": adjusted_prep_time},
            meeting_json,
            persona_id=persona,
            variation_id=i
        )
        
        variations.append(variation)
    
    return variations


def load_meeting_json(workback_file: str, workback_dir: Path) -> Optional[Dict[str, Any]]:
    """Load the Graph API meeting JSON for a workback scenario."""
    json_file = workback_dir / f"{workback_file.replace('.md', '_meeting.json')}"
    
    if not json_file.exists():
        print(f"⚠️  Meeting JSON not found: {json_file}")
        return None
    
    with open(json_file, 'r', encoding='utf-8') as f:
        return json.load(f)


def generate_training_data(
    workback_dir: Path,
    output_file: Path,
    num_variations: int = 1,
    eval_split: float = 0.0
) -> Dict[str, Any]:
    """
    Generate training data from all 7 workback scenarios.
    
    Args:
        workback_dir: Directory containing workback plans and meeting JSONs
        output_file: Output JSONL file path
        num_variations: Number of variations per scenario
        eval_split: Fraction of data to reserve for evaluation (0.0-1.0)
        
    Returns:
        Statistics dictionary
    """
    print(f"\n{'=' * 80}")
    print(f"WORKBACK SCENARIO TRAINING DATA GENERATOR")
    print(f"{'=' * 80}")
    print(f"\nInput directory: {workback_dir}")
    print(f"Output file: {output_file}")
    print(f"Variations per scenario: {num_variations}")
    print(f"Evaluation split: {eval_split:.1%}")
    
    training_data = []
    eval_data = []
    
    for scenario_key, scenario in WORKBACK_SCENARIOS.items():
        print(f"\n{'─' * 80}")
        print(f"Processing: {scenario['meeting_type']}")
        print(f"{'─' * 80}")
        
        # Load meeting JSON
        meeting_json = load_meeting_json(scenario["workback_file"], workback_dir)
        
        if not meeting_json:
            print(f"❌ Skipping {scenario_key}: Meeting JSON not found")
            continue
        
        # Generate variations
        variations = create_variations(
            scenario_key,
            scenario,
            meeting_json,
            num_variations
        )
        
        # Split into training and evaluation
        if eval_split > 0:
            eval_count = max(1, int(len(variations) * eval_split))
            eval_data.extend(variations[:eval_count])
            training_data.extend(variations[eval_count:])
            print(f"✅ Generated {len(variations)} variations ({len(variations)-eval_count} train, {eval_count} eval)")
        else:
            training_data.extend(variations)
            print(f"✅ Generated {len(variations)} training examples")
    
    # Write training data
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in training_data:
            f.write(json.dumps(item) + '\n')
    
    print(f"\n{'=' * 80}")
    print(f"✅ Training data written: {output_file}")
    print(f"   Total examples: {len(training_data)}")
    
    # Write evaluation data if split requested
    if eval_data:
        eval_file = output_file.parent / f"{output_file.stem}_eval.jsonl"
        with open(eval_file, 'w', encoding='utf-8') as f:
            for item in eval_data:
                f.write(json.dumps(item) + '\n')
        print(f"✅ Evaluation data written: {eval_file}")
        print(f"   Total examples: {len(eval_data)}")
    
    # Statistics
    stats = {
        "total_training": len(training_data),
        "total_eval": len(eval_data),
        "scenarios_processed": len([s for s in WORKBACK_SCENARIOS.keys() if any(d["scenario_key"] == s for d in training_data)]),
        "variations_per_scenario": num_variations,
        "output_file": str(output_file),
        "eval_file": str(output_file.parent / f"{output_file.stem}_eval.jsonl") if eval_data else None
    }
    
    print(f"\n{'=' * 80}")
    print(f"STATISTICS")
    print(f"{'=' * 80}")
    print(f"Scenarios processed: {stats['scenarios_processed']}/7")
    print(f"Training examples: {stats['total_training']}")
    print(f"Evaluation examples: {stats['total_eval']}")
    print(f"Total examples: {stats['total_training'] + stats['total_eval']}")
    print(f"{'=' * 80}\n")
    
    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Generate training data from workback scenarios'
    )
    parser.add_argument(
        '--workback-dir',
        type=Path,
        default=Path('workback_ado'),
        help='Directory containing workback plans and meeting JSONs'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=Path('post_training/data/training/workback_scenarios.jsonl'),
        help='Output JSONL file path'
    )
    parser.add_argument(
        '--variations',
        type=int,
        default=1,
        help='Number of variations per scenario (default: 1)'
    )
    parser.add_argument(
        '--eval-split',
        type=float,
        default=0.0,
        help='Fraction of data for evaluation (0.0-1.0, default: 0.0)'
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.workback_dir.exists():
        print(f"❌ Workback directory not found: {args.workback_dir}")
        return 1
    
    if not (0.0 <= args.eval_split <= 1.0):
        print(f"❌ Evaluation split must be between 0.0 and 1.0")
        return 1
    
    # Generate training data
    try:
        stats = generate_training_data(
            args.workback_dir,
            args.output,
            args.variations,
            args.eval_split
        )
        
        # Write statistics
        stats_file = args.output.parent / f"{args.output.stem}_stats.json"
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2)
        
        print(f"📊 Statistics written: {stats_file}\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
