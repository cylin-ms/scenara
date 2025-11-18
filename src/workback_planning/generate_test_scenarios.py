#!/usr/bin/env python3
"""
Generate Test Scenarios for Workback Plan Evaluation

This script generates 33 test scenarios (3 per meeting type) with realistic
"movie set" prompts, then creates 3 workback plans per scenario (low, medium, high quality)
using gpt-oss:120b for evaluation testing.

Total output: 33 scenarios × 3 quality levels = 99 workback plans

Usage:
    python src/workback_planning/generate_test_scenarios.py
    python src/workback_planning/generate_test_scenarios.py --meeting-type "Squad Mission"
    python src/workback_planning/generate_test_scenarios.py --scenario-only
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.llm_api import LLMAPIClient
from src.workback_planning.generator.plan_generator import generate_plan


# 11 Meeting Types with Scenario Generation Prompts
MEETING_TYPES = {
    "1_weekly_newsletter": {
        "name": "Weekly Team Newsletter",
        "horizon": "T-7",
        "complexity": "Low",
        "scenario_prompt": """Create a realistic scenario for a weekly team newsletter. Include:
- Team name and department
- Newsletter purpose and audience
- Typical content sections (3-4)
- Key stakeholders (content creator, reviewer, approver)
- Specific deadline (day of week and time)
- Any special requirements or constraints

Make it feel like a real company scenario with specific names and details."""
    },
    
    "2_sprint_planning": {
        "name": "Sprint Planning Meeting",
        "horizon": "T-14",
        "complexity": "Medium",
        "scenario_prompt": """Create a realistic scenario for a 2-week sprint planning meeting. Include:
- Team name and product area
- Sprint number and duration
- Key features or stories planned for sprint
- Team composition (engineers, PM, designer, QA)
- Sprint goals and success metrics
- Any dependencies or blockers
- Meeting date and time

Make it feel like a real agile team with specific details."""
    },
    
    "3_monthly_business_review": {
        "name": "Monthly Business Review",
        "horizon": "T-30",
        "complexity": "High",
        "scenario_prompt": """Create a realistic scenario for a monthly business review with executives. Include:
- Company/division name
- Department presenting (Sales, Marketing, Product, Engineering, etc.)
- Key metrics to report (revenue, growth, KPIs)
- Executive audience (VPs, SVPs, C-suite)
- Specific business challenges or opportunities to address
- Data sources needed
- Meeting date and time
- Presentation duration

Make it feel like a real enterprise MBR with specific business context."""
    },
    
    "4_feature_launch": {
        "name": "Product Feature Launch",
        "horizon": "T-30",
        "complexity": "High",
        "scenario_prompt": """Create a realistic scenario for a product feature launch. Include:
- Product name and feature description
- Target customers and value proposition
- Launch date and time
- Cross-functional team (Product, Engineering, Marketing, Sales, Support)
- Key deliverables (docs, training, marketing materials)
- Success metrics
- Launch channels (email, blog, in-app, etc.)
- Any dependencies or risks

Make it feel like a real SaaS/tech product launch with specific details."""
    },
    
    "5_squad_mission": {
        "name": "Squad Mission Planning",
        "horizon": "T-42 to T-56",
        "complexity": "Medium-High",
        "scenario_prompt": """Create a realistic scenario for a Squad Mission (6-8 week cycle). Include:
- Squad name and mission statement
- Mission duration (6 or 8 weeks)
- DRI (Directly Responsible Individual) and squad members
- Key milestones (every 2 weeks)
- Success metrics (quantitative and measurable)
- Cross-functional team roles (PM, Engineers, UX, Data Science)
- Expected deliverables
- How mission ties to company strategy

Make it feel like a real Microsoft/tech company squad with MMM framework."""
    },
    
    "6_quarterly_business_review": {
        "name": "Quarterly Business Review",
        "horizon": "T-60",
        "complexity": "Very High",
        "scenario_prompt": """Create a realistic scenario for a quarterly business review. Include:
- Company name and industry
- Quarter being reviewed (Q1, Q2, Q3, Q4 and year)
- Board composition (board members, executives)
- Key topics (financial results, strategy, market position)
- Multiple department presentations
- Strategic decisions to be made
- Pre-reads and board materials needed
- Meeting date, time, and duration (half-day or full-day)

Make it feel like a real enterprise QBR with board-level stakes."""
    },
    
    "7_annual_kickoff": {
        "name": "Annual Kickoff Meeting",
        "horizon": "T-60",
        "complexity": "High",
        "scenario_prompt": """Create a realistic scenario for an annual team kickoff event. Include:
- Team/organization name and size
- Event dates (2-3 days)
- Venue location
- Event theme and objectives
- Key presentations and speakers
- Team activities and agenda
- Logistics requirements (venue, catering, AV, swag)
- Expected outcomes

Make it feel like a real annual kickoff with specific event details."""
    },
    
    "8_major_product_launch": {
        "name": "Major Product Launch",
        "horizon": "T-90",
        "complexity": "Very High",
        "scenario_prompt": """Create a realistic scenario for a major product launch (90-day horizon). Include:
- Product name and version
- Market opportunity and competitive positioning
- Launch date and launch event details
- Large cross-functional team (10-20 people)
- Beta program and release candidate milestones
- Go-to-market strategy
- Partner and customer enablement
- Legal, pricing, and compliance considerations
- Post-launch monitoring plan

Make it feel like a real major product launch with enterprise scale."""
    },
    
    "9_strategic_offsite": {
        "name": "Strategic Planning Offsite",
        "horizon": "T-90",
        "complexity": "Very High",
        "scenario_prompt": """Create a realistic scenario for a strategic planning offsite. Include:
- Company name and industry
- Executive team composition
- Offsite dates (2-3 days) and location
- Strategic topics (market trends, competition, vision, OKRs)
- Pre-work requirements (market research, financial analysis)
- External facilitator
- Key decisions to be made
- Post-offsite communication plan

Make it feel like a real executive strategic planning session."""
    },
    
    "10_board_meeting": {
        "name": "Board Meeting (Annual Planning)",
        "horizon": "T-90",
        "complexity": "Very High",
        "scenario_prompt": """Create a realistic scenario for a board meeting with annual planning focus. Include:
- Company name, industry, and stage (Series B, public, etc.)
- Board composition (investors, independents, executives)
- Meeting date and duration
- Agenda topics (financials, strategy, budget, governance)
- CFO and CEO presentations
- Audit and committee reports
- Board materials and pre-reads timeline
- Key approvals needed

Make it feel like a real board meeting with governance requirements."""
    },
    
    "11_ma_integration": {
        "name": "M&A Integration Planning",
        "horizon": "T-90+",
        "complexity": "Extreme",
        "scenario_prompt": """Create a realistic scenario for M&A integration planning. Include:
- Acquiring company name and industry
- Target company name, size, and revenue
- Legal close date
- Integration kickoff date
- Integration team composition (15-30 people)
- Key workstreams (HR, IT, Finance, Product, Sales, Operations)
- Day 1 priorities and 100-day plan focus
- Cultural considerations
- Synergy targets
- Communication strategy

Make it feel like a real M&A integration with complexity and scale."""
    }
}


class ScenarioGenerator:
    """Generate realistic test scenarios for workback plan evaluation."""
    
    def __init__(self, model: str = "gpt-oss:120b", ollama_host: str = "http://192.168.2.204:11434"):
        self.llm_client = LLMAPIClient()
        self.model = model
        self.ollama_host = ollama_host
        self.output_dir = Path("data/workback_scenarios")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"🔧 Initialized ScenarioGenerator")
        print(f"   Model: {self.model}")
        print(f"   Ollama Host: {self.ollama_host}")
        print(f"   Output: {self.output_dir}")
        print()
        
    def generate_scenario(self, meeting_type_key: str, scenario_num: int) -> Dict[str, Any]:
        """Generate a single realistic scenario for a meeting type."""
        meeting_type = MEETING_TYPES[meeting_type_key]
        
        print(f"\n{'='*80}")
        print(f"Generating Scenario {scenario_num} for {meeting_type['name']}")
        print(f"  Horizon: {meeting_type['horizon']} | Complexity: {meeting_type['complexity']}")
        print(f"{'='*80}")
        print(f"📝 Calling LLM to generate realistic scenario context...")
        
        # Generate realistic scenario using LLM
        scenario_prompt = f"""You are creating a realistic test scenario for workback plan evaluation.

Meeting Type: {meeting_type['name']}
Planning Horizon: {meeting_type['horizon']}
Complexity: {meeting_type['complexity']}

{meeting_type['scenario_prompt']}

Generate a detailed, realistic scenario with:
1. **Company/Team Context**: Specific names, industry, team structure
2. **Meeting/Event Details**: Exact date, time, duration, location
3. **Stakeholders**: Specific people with names, roles, and responsibilities
4. **Deliverables**: Concrete outputs expected
5. **Success Criteria**: Measurable outcomes
6. **Constraints**: Time, budget, dependencies, or special requirements

Output as JSON with this structure:
{{
    "scenario_name": "Brief descriptive name",
    "company_context": "Company/team/product details",
    "meeting_event_details": "Date, time, duration, location specifics",
    "stakeholders": ["List of specific people with roles"],
    "deliverables": ["Concrete outputs expected"],
    "success_criteria": ["Measurable outcomes"],
    "constraints": ["Time, budget, or special requirements"],
    "workback_prompt": "The exact prompt to generate a workback plan for this scenario"
}}

Make it feel like a real company scenario with authentic details."""
        
        try:
            print(f"⚙️  Querying {self.model} at {self.ollama_host}...")
            response = self.llm_client.query_llm(
                scenario_prompt,
                provider="ollama",
                model=self.model,
                base_url=self.ollama_host
            )
            
            print(f"📄 Parsing JSON response...")
            # Strip markdown code blocks if present
            json_str = response.strip()
            if json_str.startswith("```"):
                # Remove ```json or ``` prefix
                json_str = json_str.split("\n", 1)[1] if "\n" in json_str else json_str[3:]
                # Remove trailing ```
                if json_str.endswith("```"):
                    json_str = json_str.rsplit("```", 1)[0]
                json_str = json_str.strip()
            
            # Parse JSON response
            scenario_data = json.loads(json_str)
            
            # Add metadata
            scenario_data["meeting_type"] = meeting_type["name"]
            scenario_data["meeting_type_key"] = meeting_type_key
            scenario_data["scenario_number"] = scenario_num
            scenario_data["horizon"] = meeting_type["horizon"]
            scenario_data["complexity"] = meeting_type["complexity"]
            scenario_data["generated_at"] = datetime.now().isoformat()
            
            print(f"✅ Scenario generated: {scenario_data['scenario_name']}")
            print(f"   Company: {scenario_data['company_context'][:80]}...")
            print(f"   Stakeholders: {len(scenario_data.get('stakeholders', []))}")
            print(f"   Deliverables: {len(scenario_data.get('deliverables', []))}")
            
            return scenario_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse JSON response: {e}")
            print(f"Response preview: {json_str[:500] if 'json_str' in locals() else response[:500]}")
            return None
        except Exception as e:
            print(f"❌ Error generating scenario: {e}")
            return None
    
    def generate_workback_plan(
        self,
        scenario: Dict[str, Any],
        quality_level: str
    ) -> Dict[str, Any]:
        """Generate a workback plan for a scenario at specified quality level."""
        
        # Quality level instructions
        quality_instructions = {
            "low": """Generate a LOW QUALITY workback plan with these characteristics:
- Missing key tasks or phases
- Vague task descriptions
- Few or no dependencies defined
- Missing stakeholder assignments
- No milestones or poorly defined milestones
- Unrealistic timelines
- No risk consideration
- Minimal deliverables identified""",
            
            "medium": """Generate a MEDIUM QUALITY workback plan with these characteristics:
- Most major tasks present but some gaps
- Reasonable task descriptions
- Some dependencies defined
- Most tasks have owners
- Milestones present but may lack detail
- Generally realistic timelines
- Some consideration of risks
- Key deliverables identified""",
            
            "high": """Generate a HIGH QUALITY workback plan with these characteristics:
- Comprehensive task coverage
- Clear, actionable task descriptions
- Well-defined dependencies
- All tasks assigned to specific owners
- Clear milestones with completion criteria
- Realistic timelines with buffers
- Proactive risk management
- Complete deliverable list"""
        }
        
        # Construct prompt
        workback_prompt = f"""{scenario['workback_prompt']}

{quality_instructions[quality_level]}

IMPORTANT: Generate a plan that naturally exhibits {quality_level.upper()} quality characteristics.
Do not explicitly label the plan as "{quality_level} quality" - let the quality emerge from the content."""
        
        print(f"  🔄 Generating {quality_level.upper()} quality plan...")
        print(f"     Model: {self.model} at {self.ollama_host}")
        
        try:
            # Generate plan using generate_plan function
            print(f"     Stage 1: Analysis with reasoning model...")
            
            # Create a custom client with the remote Ollama host
            custom_client = LLMAPIClient()
            
            result = generate_plan(
                context=workback_prompt,
                client=custom_client
            )
            
            print(f"     Stage 2: Structuring to JSON...")
            
            # Add metadata
            plan_data = {
                "scenario_name": scenario["scenario_name"],
                "scenario_number": scenario["scenario_number"],
                "meeting_type": scenario["meeting_type"],
                "quality_level": quality_level,
                "workback_prompt": workback_prompt,
                "generated_at": datetime.now().isoformat(),
                "analysis": result["analysis"],
                "plan": result["structured"]
            }
            
            print(f"  ✅ {quality_level.upper()} plan complete")
            if result["structured"]:
                print(f"     Tasks: {len(result['structured'].get('tasks', []))}")
                print(f"     Milestones: {len(result['structured'].get('milestones', []))}")
                print(f"     Participants: {len(result['structured'].get('participants', []))}")
            
            return plan_data
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            import traceback
            print(f"     Traceback: {traceback.format_exc()[:500]}")
            return None
    
    def generate_all_scenarios(
        self,
        meeting_types: List[str] = None,
        scenarios_per_type: int = 3,
        generate_plans: bool = True
    ):
        """Generate all test scenarios and workback plans."""
        
        types_to_generate = meeting_types or list(MEETING_TYPES.keys())
        
        print(f"\n{'='*80}")
        print(f"WORKBACK PLAN TEST SCENARIO GENERATION")
        print(f"{'='*80}")
        print(f"Meeting types: {len(types_to_generate)}")
        print(f"Scenarios per type: {scenarios_per_type}")
        print(f"Total scenarios: {len(types_to_generate) * scenarios_per_type}")
        if generate_plans:
            print(f"Plans per scenario: 3 (low, medium, high)")
            print(f"Total plans: {len(types_to_generate) * scenarios_per_type * 3}")
        print(f"Model: {self.model}")
        print(f"Output directory: {self.output_dir}")
        
        all_scenarios = []
        all_plans = []
        
        for meeting_type_key in types_to_generate:
            meeting_type = MEETING_TYPES[meeting_type_key]
            
            print(f"\n{'='*80}")
            print(f"Meeting Type: {meeting_type['name']}")
            print(f"Horizon: {meeting_type['horizon']} | Complexity: {meeting_type['complexity']}")
            print(f"{'='*80}")
            
            type_scenarios = []
            
            for scenario_num in range(1, scenarios_per_type + 1):
                # Generate scenario
                print(f"\n{'─'*80}")
                print(f"📋 Scenario {scenario_num} of {scenarios_per_type}")
                print(f"{'─'*80}")
                
                scenario = self.generate_scenario(meeting_type_key, scenario_num)
                
                if scenario:
                    type_scenarios.append(scenario)
                    all_scenarios.append(scenario)
                    
                    # Save scenario
                    scenario_file = self.output_dir / f"{meeting_type_key}_scenario_{scenario_num}.json"
                    with open(scenario_file, 'w') as f:
                        json.dump(scenario, f, indent=2)
                    print(f"💾 Saved scenario to: {scenario_file.name}")
                    
                    # Generate workback plans if requested
                    if generate_plans:
                        print(f"\n  🎯 Generating 3 workback plans (low, medium, high quality):")
                        
                        for quality_level in ["low", "medium", "high"]:
                            plan = self.generate_workback_plan(scenario, quality_level)
                            
                            if plan:
                                all_plans.append(plan)
                                
                                # Save plan
                                plan_file = self.output_dir / f"{meeting_type_key}_scenario_{scenario_num}_{quality_level}.json"
                                with open(plan_file, 'w') as f:
                                    json.dump(plan, f, indent=2)
                                print(f"     💾 Saved: {plan_file.name}")
            
            # Save all scenarios for this type
            type_file = self.output_dir / f"{meeting_type_key}_all_scenarios.json"
            with open(type_file, 'w') as f:
                json.dump(type_scenarios, f, indent=2)
            print(f"\n📦 Saved all {len(type_scenarios)} scenarios for {meeting_type['name']}")
            print(f"   File: {type_file.name}\n")
        
        # Save master index
        master_index = {
            "generated_at": datetime.now().isoformat(),
            "model": self.model,
            "meeting_types": len(types_to_generate),
            "scenarios_per_type": scenarios_per_type,
            "total_scenarios": len(all_scenarios),
            "total_plans": len(all_plans) if generate_plans else 0,
            "scenarios": all_scenarios,
            "summary_by_type": {}
        }
        
        for meeting_type_key in types_to_generate:
            meeting_type = MEETING_TYPES[meeting_type_key]
            type_scenarios = [s for s in all_scenarios if s["meeting_type_key"] == meeting_type_key]
            master_index["summary_by_type"][meeting_type_key] = {
                "name": meeting_type["name"],
                "horizon": meeting_type["horizon"],
                "complexity": meeting_type["complexity"],
                "scenarios": len(type_scenarios),
                "plans": len(type_scenarios) * 3 if generate_plans else 0
            }
        
        master_file = self.output_dir / "master_index.json"
        with open(master_file, 'w') as f:
            json.dump(master_index, f, indent=2)
        
        print(f"\n{'='*80}")
        print(f"GENERATION COMPLETE")
        print(f"{'='*80}")
        print(f"Total scenarios generated: {len(all_scenarios)}")
        if generate_plans:
            print(f"Total plans generated: {len(all_plans)}")
        print(f"Master index: {master_file}")
        print(f"Output directory: {self.output_dir}")
        
        return master_index


def main():
    parser = argparse.ArgumentParser(
        description="Generate test scenarios and workback plans for evaluation"
    )
    parser.add_argument(
        "--meeting-type",
        type=str,
        help="Generate scenarios for specific meeting type only (e.g., '1_weekly_newsletter')"
    )
    parser.add_argument(
        "--scenarios",
        type=int,
        default=3,
        help="Number of scenarios per meeting type (default: 3)"
    )
    parser.add_argument(
        "--scenario-only",
        action="store_true",
        help="Generate scenarios only, skip workback plan generation"
    )
    parser.add_argument(
        "--model",
        type=str,
        default="gpt-oss:120b",
        help="LLM model to use (default: gpt-oss:120b)"
    )
    parser.add_argument(
        "--ollama-host",
        type=str,
        default="http://192.168.2.204:11434",
        help="Ollama server host (default: http://192.168.2.204:11434)"
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = ScenarioGenerator(model=args.model, ollama_host=args.ollama_host)
    
    # Determine which meeting types to generate
    meeting_types = None
    if args.meeting_type:
        if args.meeting_type not in MEETING_TYPES:
            print(f"Error: Invalid meeting type '{args.meeting_type}'")
            print(f"Valid types: {', '.join(MEETING_TYPES.keys())}")
            sys.exit(1)
        meeting_types = [args.meeting_type]
    
    # Generate scenarios and plans
    generator.generate_all_scenarios(
        meeting_types=meeting_types,
        scenarios_per_type=args.scenarios,
        generate_plans=not args.scenario_only
    )


if __name__ == "__main__":
    main()
