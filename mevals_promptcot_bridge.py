#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MEvals to Meeting PromptCoT Data Bridge
Converts real Microsoft meeting data to Meeting PromptCoT training format
"""

import json
import csv
import re
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MEValsPromptCoTBridge:
    """
    Bridge between MEvals real meeting data and Meeting PromptCoT training
    Converts authentic Microsoft meeting scenarios to synthetic training data
    """
    
    def __init__(self, mevals_data_dir: str, promptcot_output_dir: str):
        self.mevals_data_dir = Path(mevals_data_dir)
        self.promptcot_output_dir = Path(promptcot_output_dir)
        self.promptcot_output_dir.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Initialized bridge: {self.mevals_data_dir} -> {self.promptcot_output_dir}")
    
    def extract_training_scenarios(self) -> List[Dict[str, Any]]:
        """Extract real meeting scenarios for Meeting PromptCoT training"""
        scenarios = []
        
        # Check if MEvals data directory exists
        if not self.mevals_data_dir.exists():
            logger.error(f"MEvals data directory not found: {self.mevals_data_dir}")
            return scenarios
        
        # Look for meeting prep samples
        sample_pattern = "sample_*"
        sample_dirs = list(self.mevals_data_dir.glob(sample_pattern))
        
        logger.info(f"Found {len(sample_dirs)} meeting samples to process")
        
        for sample_dir in sample_dirs:
            try:
                scenario = self._process_meeting_sample(sample_dir)
                if scenario:
                    scenarios.append(scenario)
                    logger.debug(f"Processed: {sample_dir.name}")
            except Exception as e:
                logger.error(f"Error processing {sample_dir.name}: {e}")
        
        logger.info(f"Successfully extracted {len(scenarios)} training scenarios")
        return scenarios
    
    def _process_meeting_sample(self, sample_dir: Path) -> Optional[Dict[str, Any]]:
        """Process a single meeting sample"""
        # Read evaluation summary
        seval_summary = sample_dir / "seval.summary.md"
        if not seval_summary.exists():
            logger.warning(f"No seval.summary.md found in {sample_dir.name}")
            return None
        
        # Extract meeting context and evaluation
        context = self._extract_meeting_context(sample_dir)
        evaluation = self._extract_evaluation_scores(seval_summary)
        
        # Only include high-quality scenarios
        if not self._is_high_quality_scenario(evaluation):
            logger.debug(f"Skipping low-quality scenario: {sample_dir.name}")
            return None
        
        # Create Meeting PromptCoT compatible scenario
        scenario = {
            "scenario_id": sample_dir.name,
            "meeting_context": context,
            "real_world_data": True,
            "evaluation_scores": evaluation,
            "source": "MEvals",
            "extraction_timestamp": datetime.now().isoformat(),
            "quality_score": self._calculate_quality_score(evaluation)
        }
        
        return scenario
    
    def _extract_meeting_context(self, sample_dir: Path) -> Dict[str, Any]:
        """Extract business context from meeting sample"""
        context = {}
        
        # Extract from directory name (contains rich information)
        dir_name = sample_dir.name
        context.update(self._parse_directory_name(dir_name))
        
        # Extract from input files if available
        input_dir = sample_dir / "input"
        if input_dir.exists():
            for file in input_dir.glob("*.json"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        context.update(data)
                except Exception as e:
                    logger.warning(f"Could not read {file}: {e}")
        
        # Extract from seval files
        seval_files = list(sample_dir.glob("*seval*.md"))
        for seval_file in seval_files:
            try:
                with open(seval_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    context["meeting_content"] = content[:1000]  # First 1000 chars
                    break
            except Exception as e:
                logger.warning(f"Could not read {seval_file}: {e}")
        
        return context
    
    def _parse_directory_name(self, dir_name: str) -> Dict[str, Any]:
        """Parse rich information from MEvals directory naming convention"""
        # Example: sample_#001_Gary_Zhu_[AI_School_China_FY25]_Generative_AI_Hands-on_Practice___3rd_Class_2025-05-15
        
        parts = dir_name.split('_')
        context = {}
        
        if len(parts) >= 4:
            # Extract sample number
            sample_match = re.search(r'#(\d+)', parts[1])
            if sample_match:
                context["sample_number"] = int(sample_match.group(1))
            
            # Extract organizer (usually parts 2-3)
            if len(parts) >= 4:
                context["organizer"] = f"{parts[2]}_{parts[3]}"
            
            # Extract meeting subject (everything between organizer and date)
            subject_parts = []
            date_part = None
            
            for i, part in enumerate(parts[4:], 4):
                # Check if this looks like a date
                if re.match(r'\d{4}-\d{2}-\d{2}$', part):
                    date_part = part
                    break
                subject_parts.append(part)
            
            if subject_parts:
                context["meeting_subject"] = "_".join(subject_parts)
            
            if date_part:
                context["meeting_date"] = date_part
        
        return context
    
    def _extract_evaluation_scores(self, seval_file: Path) -> Dict[str, float]:
        """Extract evaluation scores from seval summary"""
        scores = {}
        
        try:
            with open(seval_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Could not read {seval_file}: {e}")
            return scores
        
        # Parse evaluation table - look for score patterns
        score_patterns = [
            (r'Contextual Relevance.*?(\d+)', 'contextual_relevance'),
            (r'Comprehension.*?(\d+)', 'comprehension'),
            (r'Sufficiency.*?(\d+)', 'sufficiency'),
            (r'Page Quality.*?(\d+)', 'page_quality')
        ]
        
        for pattern, key in score_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                try:
                    score = float(match.group(1)) / 100.0  # Convert to 0-1 scale
                    scores[key] = score
                except ValueError:
                    pass
        
        # Look for overall score patterns
        overall_patterns = [
            r'Overall.*?(\d+)',
            r'Score.*?(\d+)',
            r'Rating.*?(\d+)'
        ]
        
        for pattern in overall_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match and 'overall_score' not in scores:
                try:
                    score = float(match.group(1)) / 100.0
                    scores['overall_score'] = score
                    break
                except ValueError:
                    pass
        
        return scores
    
    def _is_high_quality_scenario(self, evaluation: Dict[str, float]) -> bool:
        """Filter for high-quality scenarios only"""
        if not evaluation:
            return False
        
        # Require minimum scores for training data quality
        min_scores = {
            'contextual_relevance': 0.85,  # 85%
            'comprehension': 0.80,         # 80%
            'sufficiency': 0.80,           # 80%
        }
        
        for criterion, min_score in min_scores.items():
            if criterion in evaluation and evaluation[criterion] < min_score:
                return False
        
        return True
    
    def _calculate_quality_score(self, evaluation: Dict[str, float]) -> float:
        """Calculate overall quality score"""
        if not evaluation:
            return 0.0
        
        # Weight different criteria
        weights = {
            'contextual_relevance': 0.3,
            'comprehension': 0.25,
            'sufficiency': 0.25,
            'page_quality': 0.2
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for criterion, weight in weights.items():
            if criterion in evaluation:
                weighted_sum += evaluation[criterion] * weight
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def convert_to_promptcot_format(self, scenarios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert MEvals data to Meeting PromptCoT training format"""
        promptcot_scenarios = []
        
        for scenario in scenarios:
            # Create rich company profile from meeting context
            company_profile = self._infer_company_profile(scenario["meeting_context"])
            
            # Generate Meeting PromptCoT compatible scenario
            promptcot_scenario = {
                "scenario_description": self._generate_scenario_description(scenario),
                "company_profile": company_profile,
                "meeting_objectives": self._extract_meeting_objectives(scenario),
                "stakeholder_dynamics": self._infer_stakeholder_dynamics(scenario),
                "business_context": self._extract_business_context(scenario),
                "success_metrics": scenario["evaluation_scores"],
                "quality_score": scenario["quality_score"],
                "source_data": {
                    "mevals_sample": scenario["scenario_id"],
                    "real_meeting": True,
                    "extraction_timestamp": scenario["extraction_timestamp"]
                }
            }
            
            promptcot_scenarios.append(promptcot_scenario)
        
        logger.info(f"Converted {len(promptcot_scenarios)} scenarios to Meeting PromptCoT format")
        return promptcot_scenarios
    
    def _infer_company_profile(self, meeting_context: Dict[str, Any]) -> Dict[str, Any]:
        """Infer company profile from meeting context"""
        organizer = meeting_context.get("organizer", "")
        subject = meeting_context.get("meeting_subject", "")
        
        # Basic Microsoft profile (since this is MEvals data)
        company_profile = {
            "company_name": "Microsoft Corporation",
            "industry": "Technology Software",
            "size": "Large Enterprise (>100,000 employees)",
            "stage": "Public (Fortune 500)",
            "revenue": ">$200B annual",
            "growth_rate": "Stable enterprise growth",
            "key_challenges": self._infer_challenges_from_subject(subject),
            "strategic_priorities": self._infer_priorities_from_subject(subject),
            "organizational_culture": "Data-driven, collaborative, customer-focused",
            "meeting_patterns": self._analyze_meeting_patterns(meeting_context)
        }
        
        return company_profile
    
    def _generate_scenario_description(self, scenario: Dict[str, Any]) -> str:
        """Generate detailed scenario description"""
        context = scenario["meeting_context"]
        
        organizer = context.get("organizer", "Team Lead")
        subject = context.get("meeting_subject", "Strategic Planning Meeting")
        date = context.get("meeting_date", "upcoming")
        
        description = f"""
Business meeting scenario: {subject.replace('_', ' ')}

Meeting Details:
- Organizer: {organizer.replace('_', ' ')}
- Date: {date}
- Type: Strategic business meeting requiring comprehensive preparation

This meeting involves key stakeholders discussing important business decisions 
that will impact team objectives, resource allocation, and strategic direction.
Preparation requires understanding of business context, stakeholder interests, 
and potential outcomes.
        """.strip()
        
        return description
    
    def _extract_meeting_objectives(self, scenario: Dict[str, Any]) -> List[str]:
        """Extract meeting objectives from scenario"""
        subject = scenario["meeting_context"].get("meeting_subject", "")
        
        # Infer objectives based on meeting subject keywords
        objectives = []
        
        subject_lower = subject.lower()
        if "sync" in subject_lower:
            objectives.append("Align team on current priorities and progress")
        if "review" in subject_lower:
            objectives.append("Review performance and identify improvement areas")
        if "planning" in subject_lower:
            objectives.append("Develop strategic plans and resource allocation")
        if "1_1" in subject or "1-1" in subject:
            objectives.append("Individual performance and career development discussion")
        
        # Default objectives if none inferred
        if not objectives:
            objectives = [
                "Align stakeholders on key business decisions",
                "Review current performance and challenges",
                "Plan next steps and resource allocation"
            ]
        
        return objectives
    
    def _infer_stakeholder_dynamics(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Infer stakeholder dynamics from meeting context"""
        organizer = scenario["meeting_context"].get("organizer", "")
        subject = scenario["meeting_context"].get("meeting_subject", "")
        
        dynamics = {
            "primary_stakeholder": organizer.replace('_', ' '),
            "stakeholder_interests": self._infer_stakeholder_interests(subject),
            "power_dynamics": "Collaborative decision-making with clear ownership",
            "communication_style": "Professional, data-driven, action-oriented"
        }
        
        return dynamics
    
    def _extract_business_context(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Extract business context elements"""
        context = scenario["meeting_context"]
        subject = context.get("meeting_subject", "")
        
        business_context = {
            "meeting_type": self._classify_meeting_type(subject),
            "business_function": self._infer_business_function(subject),
            "decision_level": self._infer_decision_level(subject),
            "urgency": "Medium",  # Default for training data
            "complexity": "High" if "design" in subject.lower() or "strategy" in subject.lower() else "Medium"
        }
        
        return business_context
    
    def _infer_challenges_from_subject(self, subject: str) -> List[str]:
        """Infer business challenges from meeting subject"""
        challenges = []
        subject_lower = subject.lower()
        
        if "ai" in subject_lower or "ml" in subject_lower:
            challenges.append("AI/ML technology integration and scaling")
        if "compliance" in subject_lower or "security" in subject_lower:
            challenges.append("Regulatory compliance and security requirements")
        if "design" in subject_lower:
            challenges.append("Technical design and architecture decisions")
        
        return challenges or ["Scaling operations efficiently", "Competitive market pressures"]
    
    def _infer_priorities_from_subject(self, subject: str) -> List[str]:
        """Infer strategic priorities from meeting subject"""
        priorities = []
        subject_lower = subject.lower()
        
        if "ai" in subject_lower or "ml" in subject_lower:
            priorities.append("AI/ML technology advancement and adoption")
        if "strategy" in subject_lower or "planning" in subject_lower:
            priorities.append("Strategic planning and execution excellence")
        if "performance" in subject_lower or "review" in subject_lower:
            priorities.append("Performance optimization and continuous improvement")
        if "sync" in subject_lower or "alignment" in subject_lower:
            priorities.append("Team alignment and operational efficiency")
        if "growth" in subject_lower or "scale" in subject_lower:
            priorities.append("Sustainable growth and scalability")
        
        return priorities or ["Customer satisfaction", "Operational excellence", "Innovation leadership"]
    
    def _analyze_meeting_patterns(self, meeting_context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze meeting patterns from context"""
        organizer = meeting_context.get("organizer", "")
        subject = meeting_context.get("meeting_subject", "")
        date = meeting_context.get("meeting_date", "")
        
        patterns = {
            "meeting_frequency": "Weekly" if "weekly" in subject.lower() else "Ad-hoc",
            "meeting_type": self._classify_meeting_type(subject),
            "organizer_role": "Technical Lead" if any(tech in organizer.lower() for tech in ["dev", "eng", "tech"]) else "Business Lead",
            "recurring": "1_1" in subject or "sync" in subject.lower(),
            "cross_functional": "stakeholder" in subject.lower() or "review" in subject.lower()
        }
        
        return patterns
    
    def _classify_meeting_type(self, subject: str) -> str:
        """Classify meeting type from subject"""
        subject_lower = subject.lower()
        
        if "1_1" in subject or "1-1" in subject:
            return "One-on-One"
        elif "sync" in subject_lower:
            return "Team Sync"
        elif "review" in subject_lower:
            return "Review Meeting"
        elif "planning" in subject_lower or "strategy" in subject_lower:
            return "Planning Meeting"
        elif "standup" in subject_lower or "daily" in subject_lower:
            return "Standup"
        elif "retro" in subject_lower or "retrospective" in subject_lower:
            return "Retrospective"
        else:
            return "Business Meeting"
    
    def _infer_stakeholder_interests(self, subject: str) -> List[str]:
        """Infer stakeholder interests from meeting subject"""
        interests = []
        subject_lower = subject.lower()
        
        if "strategy" in subject_lower:
            interests.append("Strategic direction and market positioning")
        if "performance" in subject_lower:
            interests.append("Performance metrics and KPI achievement")
        if "budget" in subject_lower or "cost" in subject_lower:
            interests.append("Budget optimization and cost management")
        if "team" in subject_lower or "people" in subject_lower:
            interests.append("Team development and resource allocation")
        
        return interests or ["Business outcomes", "Operational efficiency", "Risk management"]
    
    def _infer_business_function(self, subject: str) -> str:
        """Infer business function from meeting subject"""
        subject_lower = subject.lower()
        
        if "engineering" in subject_lower or "dev" in subject_lower or "tech" in subject_lower:
            return "Engineering"
        elif "product" in subject_lower:
            return "Product Management"
        elif "sales" in subject_lower or "revenue" in subject_lower:
            return "Sales"
        elif "marketing" in subject_lower:
            return "Marketing"
        elif "hr" in subject_lower or "people" in subject_lower:
            return "Human Resources"
        elif "finance" in subject_lower or "budget" in subject_lower:
            return "Finance"
        else:
            return "General Business"
    
    def _infer_decision_level(self, subject: str) -> str:
        """Infer decision level from meeting subject"""
        subject_lower = subject.lower()
        
        if "strategy" in subject_lower or "vision" in subject_lower:
            return "Strategic"
        elif "budget" in subject_lower or "investment" in subject_lower:
            return "Executive"
        elif "planning" in subject_lower or "roadmap" in subject_lower:
            return "Tactical"
        else:
            return "Operational"
    
    def save_training_data(self, scenarios: List[Dict[str, Any]], filename: str = "mevals_training_data.jsonl"):
        """Save converted scenarios as JSONL for Meeting PromptCoT training"""
        output_file = self.promptcot_output_dir / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            for scenario in scenarios:
                f.write(json.dumps(scenario, ensure_ascii=False) + '\n')
        
        logger.info(f"Saved {len(scenarios)} training scenarios to {output_file}")
        return output_file
    
    def generate_summary_report(self, scenarios: List[Dict[str, Any]]) -> str:
        """Generate summary report of extracted data"""
        if not scenarios:
            return "No scenarios extracted"
        
        # Calculate statistics
        total_scenarios = len(scenarios)
        avg_quality = sum(s["quality_score"] for s in scenarios) / total_scenarios
        
        # Count by organizers
        organizers = {}
        for s in scenarios:
            org = s["meeting_context"].get("organizer", "Unknown")
            organizers[org] = organizers.get(org, 0) + 1
        
        # Count by meeting types
        meeting_types = {}
        for s in scenarios:
            subject = s["meeting_context"].get("meeting_subject", "unknown")
            if "sync" in subject.lower():
                meeting_types["Sync"] = meeting_types.get("Sync", 0) + 1
            elif "review" in subject.lower():
                meeting_types["Review"] = meeting_types.get("Review", 0) + 1
            elif "1_1" in subject or "1-1" in subject:
                meeting_types["1:1"] = meeting_types.get("1:1", 0) + 1
            else:
                meeting_types["Other"] = meeting_types.get("Other", 0) + 1
        
        report = f"""
MEvals to Meeting PromptCoT Data Extraction Summary
=================================================

📊 Extraction Statistics:
- Total scenarios extracted: {total_scenarios}
- Average quality score: {avg_quality:.2f}
- High-quality scenarios (>0.8): {sum(1 for s in scenarios if s['quality_score'] > 0.8)}

👥 Top Organizers:
{chr(10).join(f"- {org}: {count} meetings" for org, count in sorted(organizers.items(), key=lambda x: x[1], reverse=True)[:5])}

📅 Meeting Types:
{chr(10).join(f"- {type_}: {count}" for type_, count in meeting_types.items())}

🎯 Quality Assessment:
- Contextual Relevance: Available for {sum(1 for s in scenarios if 'contextual_relevance' in s['evaluation_scores'])} scenarios
- Comprehension: Available for {sum(1 for s in scenarios if 'comprehension' in s['evaluation_scores'])} scenarios
- Sufficiency: Available for {sum(1 for s in scenarios if 'sufficiency' in s['evaluation_scores'])} scenarios

✅ Data ready for Meeting PromptCoT training pipeline
        """.strip()
        
        return report


def main():
    """Main function for testing the bridge"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Convert MEvals data to Meeting PromptCoT format")
    parser.add_argument("--mevals-data", default="MEvals/data/meeting_prep.prompt.samples",
                      help="Path to MEvals data directory")
    parser.add_argument("--output", default="meeting_prep_data_real",
                      help="Output directory for Meeting PromptCoT data")
    parser.add_argument("--min-quality", type=float, default=0.8,
                      help="Minimum quality score for inclusion")
    
    args = parser.parse_args()
    
    print("🌉 MEvals to Meeting PromptCoT Data Bridge")
    print("========================================")
    
    # Initialize bridge
    bridge = MEValsPromptCoTBridge(args.mevals_data, args.output)
    
    # Extract scenarios
    print("📊 Extracting real meeting scenarios...")
    scenarios = bridge.extract_training_scenarios()
    
    if not scenarios:
        print("❌ No scenarios extracted. Check MEvals data directory.")
        return 1
    
    # Filter by quality
    high_quality_scenarios = [s for s in scenarios if s["quality_score"] >= args.min_quality]
    print(f"✅ Found {len(high_quality_scenarios)} high-quality scenarios (>= {args.min_quality})")
    
    # Convert to Meeting PromptCoT format
    print("🔄 Converting to Meeting PromptCoT format...")
    promptcot_scenarios = bridge.convert_to_promptcot_format(high_quality_scenarios)
    
    # Save training data
    print("💾 Saving training data...")
    output_file = bridge.save_training_data(promptcot_scenarios)
    
    # Generate and save summary report
    report = bridge.generate_summary_report(high_quality_scenarios)
    print("\n" + report)
    
    # Save report
    report_file = Path(args.output) / "extraction_report.md"
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n🎉 Data extraction complete!")
    print(f"📁 Training data: {output_file}")
    print(f"📋 Report: {report_file}")
    
    return 0


if __name__ == "__main__":
    exit(main())