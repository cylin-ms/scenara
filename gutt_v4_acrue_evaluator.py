#!/usr/bin/env python3
"""
Enhanced GUTT v4.0 ACRUE-Integrated LLM Evaluator
Implements the full GUTT v4.0 framework with multiplicative GUTTScore methodology
Based on: ContextFlow/docs/cyl/GUTT_v4.0_ACRUE_Integrated_Evaluation_Prompt.md
"""

import ollama
import json
import re
from typing import Dict, Any, List, Optional, Tuple
import logging
from datetime import datetime

class GUTTv4ACRUEEvaluator:
    def __init__(self, model_name: str = "gpt-oss:20b"):
        self.model_name = model_name
        self.client = ollama.Client()
        
        # GUTT v4.0 ACRUE Framework with enhanced definitions
        self.acrue_definitions = {
            "Accurate": {
                "description": "Factually correct capability execution with evidence documentation",
                "weight": 1.0,
                "levels": {
                    4: "All GUTT execution completely accurate, perfect factual correctness, verifiable evidence",
                    3: "Mostly accurate GUTT performance with minor non-critical inaccuracies that don't affect user trust",
                    2: "Generally accurate but contains notable errors affecting user confidence in capability reliability",
                    1: "Significant accuracy issues in GUTT execution that would compromise user trust and adoption"
                }
            },
            "Complete": {
                "description": "Comprehensive coverage with context intelligence and series analysis",
                "weight": 1.1,
                "levels": {
                    4: "Fully comprehensive GUTT execution addressing all aspects with advanced context expansion awareness",
                    3: "Good GUTT coverage with minor information gaps, some pattern recognition and context intelligence",
                    2: "Adequate GUTT execution but missing important context opportunities or series analysis potential",
                    1: "Incomplete GUTT coverage with significant gaps affecting user satisfaction and goal achievement"
                }
            },
            "Relevant": {
                "description": "Business context alignment and meeting type appropriateness",
                "weight": 1.0,
                "levels": {
                    4: "Perfect alignment of GUTT execution with enterprise context and meeting type requirements",
                    3: "Strong business context alignment with GUTT outputs appropriate for user role and meeting type",
                    2: "Generally relevant GUTT execution but some misalignment with business context or user needs",
                    1: "Poor alignment of GUTT capabilities with enterprise needs, meeting type, or user objectives"
                }
            },
            "Useful": {
                "description": "Goal achievement utility and practical implementation value",
                "weight": 1.2,
                "levels": {
                    4: "GUTT capabilities provide exceptional utility in helping users achieve meeting preparation and productivity goals",
                    3: "Strong utility with GUTT outputs enabling effective goal achievement with minor implementation friction",
                    2: "Generally useful GUTT performance but with notable limitations affecting goal achievement efficiency",
                    1: "Limited utility with GUTT capabilities providing minimal help in achieving user objectives"
                }
            },
            "Exceptional": {
                "description": "Competitive advantage and superior capability performance",
                "weight": 0.9,
                "levels": {
                    4: "GUTT capabilities provide exceptional value significantly superior to alternative approaches or manual methods",
                    3: "Strong competitive advantage with GUTT performance notably better than available alternatives",
                    2: "Some competitive advantage but GUTT capabilities only marginally better than alternative approaches",
                    1: "Limited differentiation with GUTT performance comparable to or worse than alternative methods"
                }
            }
        }
        
        # Enhanced GUTT Tasks by Categories with Business Value Multipliers
        self.gutt_categories = {
            "Enterprise Information Integration": {
                "weight": 1.2,  # Critical Path GUTTs
                "tasks": {
                    "GUTT.01": "Access [enterprise data] from [internal systems]",
                    "GUTT.02": "Identify [key themes] from [discussion/content]",
                    "GUTT.03": "Summarize [complex information] for [specific audience]",
                    "GUTT.04": "Extract [actionable items] from [meeting content]",
                    "GUTT.05": "Connect [current discussion] to [relevant business context]"
                }
            },
            "Meeting & Calendar Intelligence": {
                "weight": 1.2,  # Critical Path GUTTs
                "tasks": {
                    "GUTT.06": "Analyze [calendar data] for [scheduling optimization]",
                    "GUTT.07": "Identify [meeting stakeholders] with [appropriate roles]",
                    "GUTT.08": "Coordinate [multiple calendars] with [constraint satisfaction]",
                    "GUTT.09": "Generate [meeting proposals] based on [availability patterns]",
                    "GUTT.10": "Resolve [scheduling conflicts] through [intelligent negotiation]"
                }
            },
            "Communication & Synthesis": {
                "weight": 1.1,  # High Value GUTTs
                "tasks": {
                    "GUTT.11": "Translate [technical content] for [business stakeholders]",
                    "GUTT.12": "Synthesize [multiple perspectives] into [unified recommendations]",
                    "GUTT.13": "Generate [executive summaries] from [detailed discussions]",
                    "GUTT.14": "Create [action-oriented communications] for [specific recipients]",
                    "GUTT.15": "Format [information] according to [organizational standards]"
                }
            },
            "Decision Support & Analysis": {
                "weight": 1.1,  # High Value GUTTs
                "tasks": {
                    "GUTT.16": "Compare [alternative options] across [evaluation criteria]",
                    "GUTT.17": "Assess [risks and implications] for [proposed decisions]",
                    "GUTT.18": "Recommend [optimal solutions] based on [business constraints]",
                    "GUTT.19": "Prioritize [action items] by [business impact and urgency]",
                    "GUTT.20": "Validate [proposals] against [organizational policies]"
                }
            },
            "Context & Relationship Management": {
                "weight": 1.0,  # Standard GUTTs
                "tasks": {
                    "GUTT.21": "Track [project dependencies] across [organizational boundaries]",
                    "GUTT.22": "Maintain [relationship context] between [stakeholder interactions]",
                    "GUTT.23": "Monitor [progress indicators] against [established metrics]",
                    "GUTT.24": "Archive [meeting outcomes] with [searchable metadata]",
                    "GUTT.25": "Link [current activities] to [strategic objectives]"
                }
            },
            "Multi-Turn Conversation Intelligence": {
                "weight": 1.1,  # High Value GUTTs
                "tasks": {
                    "GUTT.26": "Maintain [context coherence] across [conversation turns]",
                    "GUTT.27": "Integrate [new information] with [established context]",
                    "GUTT.28": "Preserve [user constraints] throughout [extended interaction]",
                    "GUTT.29": "Adapt [strategy/approach] based on [conversation evolution]",
                    "GUTT.30": "Resolve [conversation objective] through [multi-turn coordination]"
                }
            },
            "Universal System Intelligence": {
                "weight": 1.0,  # Standard GUTTs
                "tasks": {
                    "GUTT.31": "Select [appropriate system mode] for [query complexity]"
                }
            }
        }
    
    def evaluate_meeting_scenario_v4(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a meeting scenario using full GUTT v4.0 ACRUE framework
        Returns comprehensive evaluation with multiplicative GUTTScore
        """
        
        try:
            # Step 1: Analyze user query and identify required GUTTs
            required_gutts = self._identify_required_gutts(scenario)
            
            # Step 2: Calculate Track 1 - GUTT Trigger Assessment (0.0-1.0)
            track1_score = self._calculate_track1_score(scenario, required_gutts)
            
            # Step 3: Calculate Track 2 - ACRUE Quality Assessment (1.0-4.0)
            track2_score, acrue_details = self._calculate_track2_score(scenario, required_gutts)
            
            # Step 4: Calculate Final GUTTScore (Multiplicative)
            gutt_score = track1_score * track2_score
            
            # Step 5: Generate comprehensive evaluation report
            evaluation_report = self._generate_v4_evaluation_report(
                scenario, required_gutts, track1_score, track2_score, 
                gutt_score, acrue_details
            )
            
            return {
                "framework_version": "4.0_ACRUE_Integration",
                "evaluation_date": datetime.now().isoformat(),
                "scenario_id": scenario.get('id', 'unknown'),
                "user_query_analysis": self._analyze_user_query(scenario),
                "required_gutts": required_gutts,
                "track1_score": track1_score,
                "track2_score": track2_score,
                "gutt_score": gutt_score,
                "performance_level": self._classify_performance_level(gutt_score),
                "acrue_details": acrue_details,
                "user_quality_prediction": self._predict_user_quality(gutt_score, acrue_details),
                "competitive_analysis": self._analyze_competitive_advantage(acrue_details),
                "evaluation_report": evaluation_report
            }
            
        except Exception as e:
            logging.error(f"Error in GUTT v4.0 evaluation: {e}")
            return self._create_error_response(scenario, str(e))
    
    def _identify_required_gutts(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Use LLM to identify which GUTT capabilities are required for the scenario"""
        
        context = scenario.get('context', {})
        meeting_type = scenario.get('meeting_type', 'General Business Meeting')
        
        prompt = f"""
# GUTT v4.0 Capability Identification

You are an expert at analyzing meeting scenarios and identifying which GUTT (Granular Unit Task Template) capabilities are required.

## Meeting Scenario:
- **Subject**: {context.get('subject', 'N/A')}
- **Meeting Type**: {meeting_type}
- **Description**: {context.get('description', 'N/A')}
- **Attendees**: {context.get('attendee_count', 'N/A')} people
- **Duration**: {context.get('duration_minutes', 'N/A')} minutes

## Available GUTT Categories and Tasks:
{self._format_gutt_categories_for_prompt()}

## Task:
Analyze the meeting scenario and identify which GUTT capabilities would be required for optimal meeting preparation and execution. For each required GUTT:

1. **Template Display**: Show the GUTT template with placeholders
2. **Slot Mapping**: Map specific values from the scenario
3. **Materialized GUTT**: Show the fully populated template
4. **Business Value**: Explain why this GUTT is critical for this meeting

Respond in JSON format:
{{
    "required_gutts": [
        {{
            "gutt_id": "GUTT.XX",
            "category": "category_name",
            "template": "template with [placeholders]",
            "slot_mapping": {{"placeholder": "mapped_value"}},
            "materialized": "fully populated template",
            "business_value": "explanation of why this GUTT is critical",
            "weight": 1.0
        }}
    ],
    "complexity_assessment": "single-turn|multi-turn",
    "primary_objectives": ["objective1", "objective2"],
    "success_criteria": ["criteria1", "criteria2"]
}}
"""

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.3}
            )
            
            response_text = response['message']['content']
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback to basic GUTT identification
                return self._fallback_gutt_identification(scenario)
                
        except Exception as e:
            logging.error(f"Error in GUTT identification: {e}")
            return self._fallback_gutt_identification(scenario)
    
    def _calculate_track1_score(self, scenario: Dict[str, Any], required_gutts: Dict[str, Any]) -> float:
        """
        Calculate Track 1 Score: GUTT Trigger Assessment (0.0-1.0)
        Evaluates how well the system identified and triggered required capabilities
        """
        
        if not required_gutts.get('required_gutts'):
            return 0.0
        
        prompt = f"""
# Track 1: GUTT Trigger Assessment

Evaluate how well the system identified and would trigger the required GUTT capabilities for this meeting scenario.

## Scenario Context:
{json.dumps(scenario.get('context', {}), indent=2)}

## Required GUTTs Identified:
{json.dumps(required_gutts.get('required_gutts', []), indent=2)}

## Assessment Criteria:
For each required GUTT, evaluate:
- **Precision**: Is this GUTT actually needed for the scenario?
- **Recall**: Are we missing any critical GUTTs for this scenario?
- **Template Accuracy**: Are the template slot mappings correct?

## Scoring:
- **1.0**: All required GUTTs correctly identified, perfect template mapping
- **0.8-0.9**: Most GUTTs correct, minor template mapping issues
- **0.6-0.7**: Good GUTT identification but some gaps or inaccuracies
- **0.4-0.5**: Partial GUTT identification with notable issues
- **0.2-0.3**: Poor GUTT identification, major gaps
- **0.0**: Complete failure to identify required capabilities

Respond with a score between 0.0 and 1.0 and brief justification:
{{
    "track1_score": 0.85,
    "precision": 0.9,
    "recall": 0.8,
    "template_accuracy": 0.85,
    "justification": "explanation of the score"
}}
"""

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.2}
            )
            
            response_text = response['message']['content']
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return float(result.get('track1_score', 0.7))
            else:
                return 0.7  # Default reasonable score
                
        except Exception as e:
            logging.error(f"Error in Track 1 calculation: {e}")
            return 0.7
    
    def _calculate_track2_score(self, scenario: Dict[str, Any], required_gutts: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
        """
        Calculate Track 2 Score: ACRUE Quality Assessment (1.0-4.0)
        Evaluates the quality of GUTT execution using ACRUE dimensions
        """
        
        acrue_scores = {}
        
        for dimension, definition in self.acrue_definitions.items():
            score = self._evaluate_acrue_dimension_v4(scenario, required_gutts, dimension, definition)
            acrue_scores[dimension] = score
        
        # Calculate weighted ACRUE score
        weighted_score = 0.0
        total_weight = 0.0
        
        for dimension, score in acrue_scores.items():
            weight = self.acrue_definitions[dimension]['weight']
            weighted_score += score * weight
            total_weight += weight
        
        # Normalize to 1.0-4.0 range
        track2_score = (weighted_score / total_weight)
        
        return track2_score, acrue_scores
    
    def _evaluate_acrue_dimension_v4(self, scenario: Dict[str, Any], required_gutts: Dict[str, Any], 
                                   dimension: str, definition: Dict[str, Any]) -> float:
        """Evaluate a specific ACRUE dimension using LLM with v4.0 criteria"""
        
        prompt = f"""
# ACRUE Dimension Evaluation: {dimension}

## Definition:
{definition['description']}

## Evaluation Levels:
{json.dumps(definition['levels'], indent=2)}

## Meeting Scenario:
{json.dumps(scenario.get('context', {}), indent=2)}

## Meeting Preparation Requirements:
{json.dumps(scenario.get('preparation_requirements', [])[:5], indent=2)}

## Required GUTTs for this Scenario:
{json.dumps(required_gutts.get('required_gutts', []), indent=2)}

## Assessment Task:
Evaluate how well the meeting preparation and GUTT execution would perform on the **{dimension}** dimension.

Consider:
- Quality of information extraction and analysis
- Appropriateness of preparation requirements
- Business context understanding
- User goal achievement potential
- Competitive advantage vs manual preparation

Rate on scale 1-4 based on the levels above and provide detailed justification.

Respond in JSON:
{{
    "score": 3.2,
    "level": 3,
    "justification": "detailed explanation of why this score was assigned",
    "evidence": ["specific evidence point 1", "evidence point 2"],
    "improvement_areas": ["area 1", "area 2"]
}}
"""

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.3}
            )
            
            response_text = response['message']['content']
            
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                return float(result.get('score', 2.5))
            else:
                return 2.5  # Default score
                
        except Exception as e:
            logging.error(f"Error evaluating {dimension}: {e}")
            return 2.5
    
    def _classify_performance_level(self, gutt_score: float) -> Dict[str, Any]:
        """Classify performance level based on GUTTScore"""
        
        if gutt_score == 0.0:
            return {
                "level": 0,
                "name": "Complete Failure",
                "description": "System failed to identify and trigger any required GUTT capabilities",
                "user_impact": "Complete user experience failure with no functional value delivery"
            }
        elif 0.1 <= gutt_score <= 1.0:
            return {
                "level": 1,
                "name": "Poor Performance",
                "description": "Weak GUTT performance with significant capability identification failures",
                "user_impact": "Poor user experience likelihood with low competitive positioning"
            }
        elif 1.1 <= gutt_score <= 2.0:
            return {
                "level": 2,
                "name": "Adequate Performance",
                "description": "Basic GUTT execution meeting user needs but missing key capabilities",
                "user_impact": "Adequate user experience with notable improvement potential"
            }
        elif 2.1 <= gutt_score <= 3.0:
            return {
                "level": 3,
                "name": "Strong Performance",
                "description": "Solid GUTT execution with clear user value and goal achievement support",
                "user_impact": "Good user quality prediction with strong business value"
            }
        else:  # 3.1-4.0
            return {
                "level": 4,
                "name": "Exceptional Performance",
                "description": "World-class GUTT execution with superior performance vs alternatives",
                "user_impact": "High user trust and retention confidence"
            }
    
    def _predict_user_quality(self, gutt_score: float, acrue_details: Dict[str, Any]) -> Dict[str, Any]:
        """Predict user-perceived quality outcomes based on GUTT performance"""
        
        return {
            "overall_prediction": "High" if gutt_score >= 3.0 else "Medium" if gutt_score >= 2.0 else "Low",
            "user_trust_confidence": gutt_score / 4.0,
            "goal_achievement_likelihood": acrue_details.get('Useful', 2.5) / 4.0,
            "competitive_advantage": acrue_details.get('Exceptional', 2.0) / 4.0,
            "retention_probability": min(1.0, gutt_score / 3.5)
        }
    
    def _analyze_competitive_advantage(self, acrue_details: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze competitive positioning based on ACRUE scores"""
        
        exceptional_score = acrue_details.get('Exceptional', 2.0)
        useful_score = acrue_details.get('Useful', 2.5)
        
        return {
            "vs_manual_preparation": "Superior" if exceptional_score >= 3.0 else "Comparable" if exceptional_score >= 2.0 else "Inferior",
            "market_differentiation": "Strong" if exceptional_score >= 3.5 else "Moderate" if exceptional_score >= 2.5 else "Weak",
            "practical_utility": "High" if useful_score >= 3.0 else "Medium" if useful_score >= 2.0 else "Low",
            "strategic_value": (exceptional_score + useful_score) / 2.0
        }
    
    def _format_gutt_categories_for_prompt(self) -> str:
        """Format GUTT categories and tasks for LLM prompt"""
        
        formatted = ""
        for category, details in self.gutt_categories.items():
            formatted += f"\n### {category} (Weight: {details['weight']}x)\n"
            for gutt_id, template in details['tasks'].items():
                formatted += f"- **{gutt_id}**: {template}\n"
        
        return formatted
    
    def _fallback_gutt_identification(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback GUTT identification when LLM fails"""
        
        # Basic fallback based on meeting type and context
        return {
            "required_gutts": [
                {
                    "gutt_id": "GUTT.02",
                    "category": "Enterprise Information Integration",
                    "template": "Identify [key themes] from [discussion/content]",
                    "slot_mapping": {"key themes": "meeting objectives", "discussion/content": "meeting context"},
                    "materialized": "Identify meeting objectives from meeting context",
                    "business_value": "Essential for meeting preparation",
                    "weight": 1.2
                }
            ],
            "complexity_assessment": "single-turn",
            "primary_objectives": ["meeting preparation"],
            "success_criteria": ["effective preparation"]
        }
    
    def _analyze_user_query(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the user query for context and complexity"""
        
        context = scenario.get('context', {})
        
        return {
            "query_type": "meeting_preparation",
            "complexity": "medium",
            "enterprise_context": True if context.get('attendee_count', 0) > 2 else False,
            "multi_turn_potential": True if context.get('duration_minutes', 0) > 60 else False
        }
    
    def _generate_v4_evaluation_report(self, scenario, required_gutts, track1_score, 
                                     track2_score, gutt_score, acrue_details) -> str:
        """Generate comprehensive GUTT v4.0 evaluation report"""
        
        context = scenario.get('context', {})
        performance = self._classify_performance_level(gutt_score)
        
        report = f"""
# GUTT v4.0 ACRUE-Integrated Evaluation Report

**Framework Version**: 4.0 (ACRUE Integration for User Quality Alignment)
**Evaluation Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Scenario ID**: {scenario.get('id', 'unknown')}

## User Query Analysis
- **Meeting Subject**: {context.get('subject', 'N/A')}
- **Meeting Type**: {scenario.get('meeting_type', 'N/A')}
- **Complexity**: {required_gutts.get('complexity_assessment', 'medium')}
- **Attendees**: {context.get('attendee_count', 'N/A')}
- **Duration**: {context.get('duration_minutes', 'N/A')} minutes

## GUTT Capability Assessment
**Required GUTTs Identified**: {len(required_gutts.get('required_gutts', []))}

### Track 1: GUTT Trigger Assessment
- **Score**: {track1_score:.2f}/1.0
- **Interpretation**: {"Excellent" if track1_score >= 0.9 else "Good" if track1_score >= 0.7 else "Needs Improvement"}

### Track 2: ACRUE Quality Assessment  
- **Score**: {track2_score:.2f}/4.0
- **ACRUE Breakdown**:
  - Accurate: {acrue_details.get('Accurate', 0):.2f}/4.0
  - Complete: {acrue_details.get('Complete', 0):.2f}/4.0
  - Relevant: {acrue_details.get('Relevant', 0):.2f}/4.0
  - Useful: {acrue_details.get('Useful', 0):.2f}/4.0
  - Exceptional: {acrue_details.get('Exceptional', 0):.2f}/4.0

## Final GUTTScore (Multiplicative)
- **GUTTScore**: {gutt_score:.2f}/4.0
- **Performance Level**: {performance['name']} (Level {performance['level']})
- **User Impact**: {performance['user_impact']}

## User Quality Prediction
- **Overall Quality Prediction**: {"High" if gutt_score >= 3.0 else "Medium" if gutt_score >= 2.0 else "Low"}
- **User Trust Confidence**: {(gutt_score/4.0)*100:.1f}%
- **Goal Achievement Likelihood**: {(acrue_details.get('Useful', 2.5)/4.0)*100:.1f}%

## Competitive Analysis
- **vs Manual Preparation**: {"Superior" if acrue_details.get('Exceptional', 2.0) >= 3.0 else "Comparable"}
- **Market Differentiation**: {"Strong" if acrue_details.get('Exceptional', 2.0) >= 3.5 else "Moderate"}
- **Strategic Value**: {((acrue_details.get('Exceptional', 2.0) + acrue_details.get('Useful', 2.5))/2.0):.2f}/4.0
"""
        
        return report
    
    def _create_error_response(self, scenario: Dict[str, Any], error_msg: str) -> Dict[str, Any]:
        """Create error response for failed evaluations"""
        
        return {
            "framework_version": "4.0_ACRUE_Integration",
            "evaluation_date": datetime.now().isoformat(),
            "scenario_id": scenario.get('id', 'unknown'),
            "error": True,
            "error_message": error_msg,
            "track1_score": 0.0,
            "track2_score": 1.0,
            "gutt_score": 0.0,
            "performance_level": {
                "level": 0,
                "name": "Evaluation Failed",
                "description": "Could not complete GUTT v4.0 evaluation"
            }
        }


def test_enhanced_gutt_evaluator():
    """Test the enhanced GUTT v4.0 evaluator"""
    
    evaluator = GUTTv4ACRUEEvaluator()
    
    # Test scenario
    test_scenario = {
        'id': 'test_enhanced_gutt_v4',
        'context': {
            'subject': 'Q4 Strategic Planning Session',
            'description': 'Cross-functional planning meeting to set Q4 objectives and align on key initiatives',
            'attendee_count': 8,
            'duration_minutes': 120,
            'is_online_meeting': True
        },
        'meeting_type': 'Strategic Planning Meeting',
        'preparation_requirements': [
            'Review Q3 performance metrics and identify improvement areas',
            'Prepare SWOT analysis for current market position',
            'Gather input from department heads on resource requirements',
            'Draft preliminary Q4 OKRs with measurable targets'
        ]
    }
    
    print("🧪 Testing Enhanced GUTT v4.0 ACRUE Evaluator")
    print("=" * 60)
    
    result = evaluator.evaluate_meeting_scenario_v4(test_scenario)
    
    print(f"📊 GUTTScore: {result['gutt_score']:.2f}/4.0")
    print(f"🎯 Track 1 (Trigger): {result['track1_score']:.2f}/1.0")
    print(f"📈 Track 2 (ACRUE): {result['track2_score']:.2f}/4.0")
    print(f"🏆 Performance: {result['performance_level']['name']}")
    print(f"👥 User Quality: {result['user_quality_prediction']['overall_prediction']}")
    
    print(f"\n📋 ACRUE Breakdown:")
    for dimension, score in result['acrue_details'].items():
        print(f"  {dimension}: {score:.2f}/4.0")
    
    print(f"\n📄 Full Evaluation Report:")
    print(result['evaluation_report'])
    
    return result


if __name__ == "__main__":
    test_enhanced_gutt_evaluator()