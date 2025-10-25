#!/usr/bin/env python3
"""
Meeting Data Enhancer - Generate diverse meeting scenarios from existing MEvals data
No IT approval required - works with existing data
"""

import json
import random
import os
from typing import List, Dict, Any
from datetime import datetime, timedelta

class MeetingDataEnhancer:
    def __init__(self):
        self.base_scenarios = []
        self.meeting_types = [
            "Technical Design Review",
            "Quarterly Business Review", 
            "Product Strategy Session",
            "Cross-team Collaboration",
            "Customer Discovery Call",
            "Team Retrospective",
            "Budget Planning Meeting",
            "Vendor Evaluation Session",
            "Sprint Planning",
            "Architecture Review",
            "Performance Analysis",
            "Security Assessment",
            "User Research Session",
            "Competitive Analysis",
            "Partnership Discussion",
            "Training Session"
        ]
        
        self.attendee_roles = [
            "Product Manager", "Engineering Lead", "Designer", 
            "Data Scientist", "Marketing Manager", "Sales Director",
            "Customer Success", "DevOps Engineer", "QA Lead",
            "Business Analyst", "Research Manager", "VP Engineering"
        ]
        
        self.complexity_factors = [
            "cross-functional dependencies",
            "technical constraints",
            "budget considerations", 
            "timeline pressure",
            "stakeholder alignment",
            "regulatory requirements",
            "customer impact",
            "competitive landscape"
        ]

    def load_existing_data(self) -> List[Dict]:
        """Load existing MEvals training data"""
        data_files = [
            "meeting_prep_data/mevals_training_scenarios.json",
            "meeting_prep_test/test_scenarios.jsonl"
        ]
        
        scenarios = []
        for file_path in data_files:
            if os.path.exists(file_path):
                try:
                    if file_path.endswith('.json'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                scenarios.extend(data)
                            else:
                                scenarios.append(data)
                    elif file_path.endswith('.jsonl'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            for line in f:
                                if line.strip():
                                    scenarios.append(json.loads(line))
                except Exception as e:
                    print(f"Warning: Could not load {file_path}: {e}")
        
        print(f"Loaded {len(scenarios)} base scenarios")
        return scenarios

    def generate_meeting_variations(self, base_scenario: Dict, count: int = 5) -> List[Dict]:
        """Generate variations of a base meeting scenario"""
        variations = []
        
        for i in range(count):
            variation = base_scenario.copy()
            
            # Vary meeting type
            variation['meeting_type'] = random.choice(self.meeting_types)
            
            # Vary attendee count (3-12 people)
            attendee_count = random.randint(3, 12)
            variation['attendee_count'] = attendee_count
            variation['attendees'] = random.sample(self.attendee_roles, min(attendee_count, len(self.attendee_roles)))
            
            # Vary complexity
            complexity_level = random.choice(['low', 'medium', 'high', 'critical'])
            variation['complexity'] = complexity_level
            variation['complexity_factors'] = random.sample(
                self.complexity_factors, 
                random.randint(1, 4)
            )
            
            # Vary duration (30min to 3 hours)
            duration_options = [30, 45, 60, 90, 120, 180]
            variation['duration_minutes'] = random.choice(duration_options)
            
            # Generate preparation requirements based on complexity
            variation['preparation_requirements'] = self.generate_prep_requirements(
                variation['meeting_type'],
                complexity_level,
                attendee_count
            )
            
            # Generate context-specific details
            variation['context'] = self.generate_meeting_context(variation)
            
            variations.append(variation)
        
        return variations

    def generate_prep_requirements(self, meeting_type: str, complexity: str, attendee_count: int) -> List[str]:
        """Generate realistic preparation requirements"""
        base_requirements = [
            "Review agenda and objectives",
            "Prepare status updates",
            "Gather relevant documents"
        ]
        
        complexity_requirements = {
            'low': [
                "Quick team sync preparation",
                "Review last week's action items"
            ],
            'medium': [
                "Prepare presentation slides",
                "Research competitive landscape",
                "Gather stakeholder feedback"
            ],
            'high': [
                "Conduct thorough analysis",
                "Prepare multiple scenarios",
                "Coordinate with external teams",
                "Review legal/compliance requirements"
            ],
            'critical': [
                "Executive briefing preparation",
                "Risk assessment analysis",
                "Prepare contingency plans",
                "Coordinate crisis communication",
                "Schedule follow-up decision meetings"
            ]
        }
        
        type_specific = {
            'Technical Design Review': [
                "Review system architecture",
                "Prepare technical diagrams",
                "Analyze performance metrics"
            ],
            'Customer Discovery Call': [
                "Research customer background",
                "Prepare interview questions",
                "Review previous interactions"
            ],
            'Budget Planning Meeting': [
                "Gather financial reports",
                "Prepare budget proposals",
                "Research cost optimization"
            ]
        }
        
        requirements = base_requirements.copy()
        requirements.extend(complexity_requirements.get(complexity, []))
        requirements.extend(type_specific.get(meeting_type, []))
        
        # Add more requirements for larger meetings
        if attendee_count > 8:
            requirements.extend([
                "Coordinate schedules across teams",
                "Prepare executive summary",
                "Set up recording/notes system"
            ])
        
        return list(set(requirements))  # Remove duplicates

    def generate_meeting_context(self, scenario: Dict) -> Dict:
        """Generate realistic meeting context"""
        return {
            'subject': f"{scenario['meeting_type']} - {self.generate_subject_suffix()}",
            'description': self.generate_description(scenario),
            'urgency': random.choice(['low', 'medium', 'high', 'urgent']),
            'expected_outcome': self.generate_expected_outcome(scenario['meeting_type']),
            'key_decisions': self.generate_key_decisions(scenario['meeting_type']),
            'follow_up_required': random.choice([True, False]),
            'external_stakeholders': random.choice([True, False])
        }

    def generate_subject_suffix(self) -> str:
        """Generate realistic meeting subject suffixes"""
        suffixes = [
            "Q4 Planning", "Sprint Review", "Architecture Discussion",
            "Performance Analysis", "Strategy Alignment", "Risk Assessment",
            "User Feedback Review", "Technical Deep Dive", "Process Optimization",
            "Roadmap Planning", "Stakeholder Sync", "Implementation Review"
        ]
        return random.choice(suffixes)

    def generate_description(self, scenario: Dict) -> str:
        """Generate realistic meeting descriptions"""
        templates = [
            f"Discuss {scenario['meeting_type'].lower()} objectives and align on next steps with {scenario['attendee_count']} team members.",
            f"Review progress on key initiatives and address {random.choice(scenario.get('complexity_factors', ['various challenges']))}.",
            f"Strategic session to evaluate options and make decisions on {scenario['meeting_type'].lower()}.",
            f"Cross-functional collaboration meeting to ensure alignment across {scenario['attendee_count']} stakeholders."
        ]
        return random.choice(templates)

    def generate_expected_outcome(self, meeting_type: str) -> str:
        """Generate expected outcomes based on meeting type"""
        outcomes = {
            'Technical Design Review': "Technical approach approved and implementation plan finalized",
            'Product Strategy Session': "Product roadmap priorities confirmed and resource allocation decided",
            'Budget Planning Meeting': "Budget allocations approved and spending guidelines established",
            'Team Retrospective': "Process improvements identified and action items assigned"
        }
        
        default_outcomes = [
            "Clear action items and ownership assigned",
            "Key decisions documented and communicated",
            "Next steps and timeline confirmed",
            "Stakeholder alignment achieved"
        ]
        
        return outcomes.get(meeting_type, random.choice(default_outcomes))

    def generate_key_decisions(self, meeting_type: str) -> List[str]:
        """Generate key decisions that need to be made"""
        decision_types = {
            'Technical Design Review': [
                "Architecture approach selection",
                "Technology stack decisions",
                "Performance requirements approval"
            ],
            'Budget Planning Meeting': [
                "Resource allocation decisions",
                "Budget approval levels",
                "Cost optimization priorities"
            ],
            'Product Strategy Session': [
                "Feature prioritization",
                "Market positioning decisions",
                "Release timeline approval"
            ]
        }
        
        default_decisions = [
            "Priority level assignment",
            "Resource requirement approval",
            "Timeline confirmation",
            "Risk mitigation approach"
        ]
        
        return decision_types.get(meeting_type, random.sample(default_decisions, random.randint(2, 4)))

    def generate_enhanced_dataset(self, target_count: int = 200) -> List[Dict]:
        """Generate enhanced dataset with target number of scenarios"""
        print("Loading existing data...")
        base_scenarios = self.load_existing_data()
        
        if not base_scenarios:
            print("No base scenarios found, generating from templates...")
            base_scenarios = self.create_template_scenarios(20)
        
        print(f"Generating {target_count} enhanced scenarios...")
        enhanced_scenarios = []
        
        variations_per_base = max(1, target_count // len(base_scenarios))
        
        for base in base_scenarios:
            variations = self.generate_meeting_variations(base, variations_per_base)
            enhanced_scenarios.extend(variations)
            
            if len(enhanced_scenarios) >= target_count:
                break
        
        # Trim to exact target count
        enhanced_scenarios = enhanced_scenarios[:target_count]
        
        print(f"Generated {len(enhanced_scenarios)} enhanced scenarios")
        return enhanced_scenarios

    def create_template_scenarios(self, count: int) -> List[Dict]:
        """Create basic template scenarios if no existing data found"""
        templates = []
        
        for i in range(count):
            template = {
                'id': f'template_{i+1}',
                'meeting_type': random.choice(self.meeting_types),
                'original_context': f"Template scenario {i+1} for {random.choice(self.meeting_types)}",
                'quality_score': random.uniform(7.0, 9.5),
                'created_date': datetime.now().isoformat()
            }
            templates.append(template)
        
        return templates

    def save_enhanced_data(self, scenarios: List[Dict], output_path: str = "meeting_prep_data/enhanced_scenarios.json"):
        """Save enhanced scenarios to file"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(scenarios, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(scenarios)} enhanced scenarios to {output_path}")

def main():
    """Main execution function"""
    print("🚀 Meeting PromptCoT Data Enhancer")
    print("Generating enhanced meeting scenarios (no IT approval needed)")
    print("-" * 60)
    
    enhancer = MeetingDataEnhancer()
    
    # Generate enhanced dataset
    enhanced_scenarios = enhancer.generate_enhanced_dataset(target_count=200)
    
    # Save to file
    enhancer.save_enhanced_data(enhanced_scenarios)
    
    # Generate summary statistics
    meeting_types = {}
    complexity_levels = {}
    
    for scenario in enhanced_scenarios:
        meeting_type = scenario.get('meeting_type', 'Unknown')
        complexity = scenario.get('complexity', 'Unknown')
        
        meeting_types[meeting_type] = meeting_types.get(meeting_type, 0) + 1
        complexity_levels[complexity] = complexity_levels.get(complexity, 0) + 1
    
    print("\n📊 Dataset Summary:")
    print(f"Total scenarios: {len(enhanced_scenarios)}")
    print(f"Meeting types: {len(meeting_types)}")
    print(f"Complexity levels: {len(complexity_levels)}")
    
    print("\n🎯 Ready for Meeting PromptCoT training!")
    print("Next steps:")
    print("1. Run: python update_training_data.py")
    print("2. Launch: streamlit run meeting_data_explorer.py")
    print("3. Access: http://localhost:8501")

if __name__ == "__main__":
    main()