#!/usr/bin/env python3
"""
LLM-Based GUTT Framework Evaluation using Ollama
Implements ACRUE evaluation methodology with gpt-oss:20b
"""

import ollama
import json
import re
from typing import Dict, Any, List, Optional
import logging

class GUTTFrameworkEvaluator:
    def __init__(self, model_name: str = "gpt-oss:20b"):
        self.model_name = model_name
        self.client = ollama.Client()
        
        # GUTT v4.0 ACRUE Framework definitions
        self.acrue_definitions = {
            "Accurate": {
                "description": "Factually correct capability execution with evidence documentation",
                "criteria": [
                    "Meeting details are correctly extracted and represented",
                    "Business context is accurately analyzed",
                    "Preparation requirements are technically sound",
                    "No factual errors or misrepresentations"
                ]
            },
            "Complete": {
                "description": "Comprehensive coverage with context intelligence and series analysis",
                "criteria": [
                    "All relevant meeting aspects are covered",
                    "Stakeholder considerations are included",
                    "Preparation requirements are thorough",
                    "Context intelligence provides full picture"
                ]
            },
            "Relevant": {
                "description": "Business context alignment and meeting type appropriateness",
                "criteria": [
                    "Preparation aligns with meeting objectives",
                    "Requirements match meeting type and complexity",
                    "Business context is appropriately considered",
                    "Recommendations are situationally appropriate"
                ]
            },
            "Useful": {
                "description": "Goal achievement utility and practical implementation value",
                "criteria": [
                    "Preparation requirements are actionable",
                    "Clear implementation guidance provided",
                    "Practical value for meeting success",
                    "Enables effective goal achievement"
                ]
            },
            "Exceptional": {
                "description": "Competitive advantage and superior capability performance",
                "criteria": [
                    "Goes beyond basic requirements",
                    "Provides strategic insights",
                    "Demonstrates advanced understanding",
                    "Creates competitive advantage"
                ]
            }
        }
        
        # GUTT Unit Tasks for evaluation context
        self.gutt_tasks = {
            "GUTT.02": "Identify [key themes] from [discussion/content]",
            "GUTT.03": "Summarize [content] for [specific purpose]",
            "GUTT.07": "Create [timeframe] plan for [goal/project]",
            "GUTT.08": "Balance [plan/schedule] with [priorities]",
            "GUTT.12": "Extract [key information] from [data source]",
            "GUTT.13": "Schedule time to [action] for [entity]",
            "GUTT.14": "Identify [stakeholders] for [initiative/decision]",
            "GUTT.17": "Find content of [artifact] for [event]",
            "GUTT.20": "Summarize [meeting objectives] into [specific goals]",
            "GUTT.21": "Monitor [metrics/indicators] for [objective]",
            "GUTT.22": "Predict [outcome] based on [data/trends]",
            "GUTT.23": "Communicate [message] to [audience]",
            "GUTT.24": "Negotiate [agreement] between [parties]"
        }
    
    def evaluate_meeting_scenario(self, scenario: Dict[str, Any]) -> Dict[str, float]:
        """Evaluate a meeting scenario using GUTT ACRUE framework with LLM"""
        
        try:
            # Extract scenario components
            context = scenario.get('context', {})
            preparation_requirements = scenario.get('preparation_requirements', [])
            meeting_classification = scenario.get('meeting_classification', {})
            
            # Create evaluation context
            evaluation_context = self._prepare_evaluation_context(scenario)
            
            # Evaluate each ACRUE dimension
            acrue_scores = {}
            
            for dimension, definition in self.acrue_definitions.items():
                score = self._evaluate_acrue_dimension(
                    dimension, definition, evaluation_context
                )
                acrue_scores[dimension.lower()] = score
            
            return acrue_scores
            
        except Exception as e:
            logging.error(f"LLM evaluation failed: {e}")
            # Fallback to rule-based evaluation
            return self._fallback_evaluation(scenario)
    
    def _prepare_evaluation_context(self, scenario: Dict[str, Any]) -> str:
        """Prepare comprehensive evaluation context for LLM"""
        
        context = scenario.get('context', {})
        classification = scenario.get('meeting_classification', {})
        prep_requirements = scenario.get('preparation_requirements', [])
        
        context_parts = [
            "MEETING SCENARIO EVALUATION:",
            f"Title: {context.get('subject', 'N/A')}",
            f"Description: {context.get('description', 'N/A')}",
            f"Meeting Type: {classification.get('specific_type', 'N/A')}",
            f"Category: {classification.get('primary_category', 'N/A')}",
            f"Attendees: {context.get('attendee_count', 0)} participants",
            f"Duration: {context.get('duration_minutes', 60)} minutes",
            f"Complexity: {scenario.get('complexity', 'medium')}",
            "",
            "PREPARATION REQUIREMENTS:",
        ]
        
        for i, req in enumerate(prep_requirements, 1):
            context_parts.append(f"{i}. {req}")
        
        # Add GUTT task context if available
        gutt_tasks = classification.get('gutt_recommendations', [])
        if gutt_tasks:
            context_parts.extend([
                "",
                "RECOMMENDED GUTT TASKS:",
                ", ".join(gutt_tasks)
            ])
        
        return "\n".join(context_parts)
    
    def _evaluate_acrue_dimension(self, dimension: str, definition: Dict, context: str) -> float:
        """Evaluate a specific ACRUE dimension using LLM"""
        
        criteria_text = "\n".join([f"- {criterion}" for criterion in definition["criteria"]])
        
        prompt = f"""
You are an expert business analyst evaluating meeting preparation quality using the GUTT v4.0 ACRUE framework.

EVALUATION CONTEXT:
{context}

ACRUE DIMENSION: {dimension}
DEFINITION: {definition["description"]}

EVALUATION CRITERIA:
{criteria_text}

SCORING GUIDELINES:
- Score 1-3: Poor/Inadequate - Major deficiencies, fails to meet basic standards
- Score 4-5: Fair/Below Average - Some issues, partially meets requirements
- Score 6-7: Good/Average - Meets most requirements with minor gaps
- Score 8-9: Excellent/Above Average - Exceeds requirements, high quality
- Score 10: Outstanding/Exceptional - Perfect execution, sets new standards

Please evaluate this meeting preparation scenario on the {dimension} dimension and provide:

1. A score from 1-10 (use decimals for precision, e.g., 8.5)
2. Specific reasoning for your score
3. Areas of strength
4. Areas for improvement (if any)

RESPONSE FORMAT:
Score: [X.X]
Reasoning: [Detailed explanation of why this score was assigned]
Strengths: [Specific strong points observed]
Improvements: [Specific areas that could be enhanced, or "None identified" if score is 9-10]
"""
        
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a precise business evaluation expert using the GUTT framework. Provide accurate numerical scores with detailed reasoning."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                options={
                    "temperature": 0.1,  # Low temperature for consistent evaluation
                    "top_p": 0.9,
                    "num_ctx": 4096
                }
            )
            
            llm_output = response['message']['content']
            score = self._extract_score_from_response(llm_output)
            
            # Log detailed evaluation for debugging
            logging.info(f"{dimension} evaluation: {score}/10.0")
            logging.debug(f"{dimension} details: {llm_output}")
            
            return score
            
        except Exception as e:
            logging.error(f"LLM evaluation failed for {dimension}: {e}")
            # Return middle score as fallback
            return 6.0
    
    def _extract_score_from_response(self, llm_output: str) -> float:
        """Extract numerical score from LLM response"""
        
        # Look for "Score: X.X" pattern
        score_match = re.search(r'Score:\s*([0-9.]+)', llm_output, re.IGNORECASE)
        if score_match:
            try:
                score = float(score_match.group(1))
                # Validate score is in valid range
                if 1.0 <= score <= 10.0:
                    return score
            except ValueError:
                pass
        
        # Fallback: look for any number that could be a score
        numbers = re.findall(r'\b([0-9.]+)\b', llm_output)
        for num_str in numbers:
            try:
                num = float(num_str)
                if 1.0 <= num <= 10.0:
                    return num
            except ValueError:
                continue
        
        # If no valid score found, return middle value
        logging.warning(f"Could not extract score from: {llm_output[:100]}...")
        return 6.0
    
    def _fallback_evaluation(self, scenario: Dict[str, Any]) -> Dict[str, float]:
        """Fallback rule-based evaluation when LLM is not available"""
        
        context = scenario.get('context', {})
        preparation_requirements = scenario.get('preparation_requirements', [])
        classification = scenario.get('meeting_classification', {})
        
        # Base scoring logic (enhanced version of current approach)
        accurate_score = 8.0  # High base for real calendar data
        complete_score = 6.5
        relevant_score = 7.5
        useful_score = 7.0
        exceptional_score = 5.5
        
        # Context-based adjustments
        attendee_count = context.get('attendee_count', 0)
        duration = context.get('duration_minutes', 60)
        importance = context.get('importance', 'normal')
        confidence = classification.get('confidence', 0.5)
        
        # Accurate: Based on classification confidence and data completeness
        accurate_score += confidence * 1.5
        if context.get('subject') and context.get('description'):
            accurate_score += 0.5
        
        # Complete: Based on preparation thoroughness
        prep_count = len(preparation_requirements)
        complete_score += min(prep_count * 0.3, 2.0)
        if attendee_count > 5:
            complete_score += 0.5
        
        # Relevant: Based on meeting context alignment
        if confidence > 0.8:
            relevant_score += 1.0
        if duration > 60:
            relevant_score += 0.5
        
        # Useful: Based on actionability
        if prep_count > 4:
            useful_score += 1.0
        if importance == 'high':
            useful_score += 0.5
        
        # Exceptional: Based on advanced features
        if attendee_count > 15:
            exceptional_score += 1.5
        if prep_count > 6:
            exceptional_score += 1.0
        if confidence > 0.9:
            exceptional_score += 0.5
        
        # Cap scores at 10.0
        return {
            "accurate": min(accurate_score, 10.0),
            "complete": min(complete_score, 10.0),
            "relevant": min(relevant_score, 10.0),
            "useful": min(useful_score, 10.0),
            "exceptional": min(exceptional_score, 10.0)
        }
    
    def test_model_availability(self) -> bool:
        """Test if the evaluation model is available"""
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{"role": "user", "content": "Test"}],
                options={"num_ctx": 100}
            )
            return True
        except Exception as e:
            logging.error(f"Evaluation model {self.model_name} not available: {e}")
            return False
    
    def evaluate_with_detailed_feedback(self, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate scenario and provide detailed feedback"""
        
        scores = self.evaluate_meeting_scenario(scenario)
        overall_score = sum(scores.values()) / len(scores)
        
        return {
            "acrue_scores": scores,
            "overall_score": overall_score,
            "evaluation_method": "GUTT_v4.0_LLM" if self.test_model_availability() else "GUTT_v4.0_fallback",
            "framework_version": "4.0_ACRUE_Enhanced"
        }

def test_gutt_evaluator():
    """Test the GUTT framework evaluator"""
    
    evaluator = GUTTFrameworkEvaluator()
    
    if not evaluator.test_model_availability():
        print("❌ LLM evaluation model not available")
        print("To enable LLM evaluation:")
        print("1. Start Ollama: ollama serve")
        print("2. Install model: ollama pull gpt-oss:20b")
        return
    
    # Test scenario
    test_scenario = {
        "context": {
            "subject": "Q3 Product Strategy Review",
            "description": "Comprehensive review of product roadmap and strategic initiatives for Q3",
            "attendee_count": 8,
            "duration_minutes": 120,
            "importance": "high"
        },
        "meeting_classification": {
            "primary_category": "Strategic Planning & Decision",
            "specific_type": "Strategic Planning Session",
            "confidence": 0.95,
            "gutt_recommendations": ["GUTT.07", "GUTT.14", "GUTT.21", "GUTT.22"]
        },
        "preparation_requirements": [
            "Review Q2 performance metrics and outcomes",
            "Analyze competitive landscape and market trends",
            "Prepare strategic options and recommendations",
            "Identify key stakeholders and decision criteria",
            "Develop risk assessment and mitigation strategies",
            "Create implementation timeline and resource requirements"
        ],
        "complexity": "high"
    }
    
    print("🧠 Testing GUTT Framework LLM Evaluator")
    print("=" * 50)
    
    result = evaluator.evaluate_with_detailed_feedback(test_scenario)
    
    print(f"Overall ACRUE Score: {result['overall_score']:.2f}/10.0")
    print(f"Evaluation Method: {result['evaluation_method']}")
    print("\nACRUE Dimension Scores:")
    
    for dimension, score in result['acrue_scores'].items():
        print(f"  - {dimension.title()}: {score:.2f}/10.0")

if __name__ == "__main__":
    test_gutt_evaluator()