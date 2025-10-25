#!/usr/bin/env python3
"""
Enhanced Meeting Prep Evaluation System
Addresses the context-dependency problem identified by the user
"""

import json
import re
from typing import Dict, List, Any

class ContextAwareMeetingEvaluator:
    """
    Better evaluation system that considers context and domain expertise
    """
    
    def __init__(self):
        self.evaluation_criteria = {
            'relevance': 0.25,      # How well advice matches scenario specifics
            'feasibility': 0.20,    # Are recommendations actionable?
            'stakeholder_fit': 0.20, # Appropriate for participant roles?
            'business_logic': 0.15,  # Sound business reasoning?
            'completeness': 0.10,    # Covers all required areas?
            'urgency_match': 0.10    # Addresses stated stakes/timeline?
        }
    
    def evaluate_response(self, scenario: Dict, response: str) -> Dict[str, Any]:
        """
        Context-aware evaluation of meeting prep response
        """
        scores = {}
        
        # 1. Relevance to Scenario Specifics
        scores['relevance'] = self._evaluate_relevance(scenario, response)
        
        # 2. Feasibility Assessment  
        scores['feasibility'] = self._evaluate_feasibility(scenario, response)
        
        # 3. Stakeholder Appropriateness
        scores['stakeholder_fit'] = self._evaluate_stakeholder_fit(scenario, response)
        
        # 4. Business Logic Quality
        scores['business_logic'] = self._evaluate_business_logic(scenario, response)
        
        # 5. Completeness (current approach)
        scores['completeness'] = self._evaluate_completeness(response)
        
        # 6. Urgency/Stakes Match
        scores['urgency_match'] = self._evaluate_urgency_match(scenario, response)
        
        # Calculate weighted overall score
        overall_score = sum(
            scores[criterion] * weight 
            for criterion, weight in self.evaluation_criteria.items()
        )
        
        return {
            'overall_score': overall_score,
            'dimension_scores': scores,
            'strengths': self._identify_strengths(scores),
            'weaknesses': self._identify_weaknesses(scores),
            'context_issues': self._identify_context_issues(scenario, response)
        }
    
    def _evaluate_relevance(self, scenario: Dict, response: str) -> float:
        """Check if advice is relevant to specific scenario context"""
        relevance_score = 0.0
        
        # Check if response addresses scenario-specific challenges
        challenges = scenario.get('challenges', [])
        for challenge in challenges:
            if any(keyword in response.lower() for keyword in challenge.lower().split()[:3]):
                relevance_score += 0.2
        
        # Check if response considers available context
        available_context = scenario.get('available_context', [])
        context_mentions = sum(1 for context in available_context 
                             if any(keyword in response.lower() 
                                   for keyword in context.lower().split()[:2]))
        relevance_score += min(context_mentions * 0.1, 0.3)
        
        # Check meeting type specificity
        meeting_type = scenario.get('meeting_type', '').lower()
        if meeting_type in response.lower():
            relevance_score += 0.2
        
        return min(relevance_score, 1.0)
    
    def _evaluate_feasibility(self, scenario: Dict, response: str) -> float:
        """Assess if recommendations are actionable given constraints"""
        feasibility_score = 0.5  # Start with neutral
        
        # Look for specific, actionable steps
        action_patterns = [
            r'form a.*team', r'schedule.*meeting', r'create.*plan',
            r'allocate.*budget', r'assign.*owner', r'set.*deadline'
        ]
        action_count = sum(1 for pattern in action_patterns 
                          if re.search(pattern, response.lower()))
        feasibility_score += min(action_count * 0.1, 0.3)
        
        # Check for unrealistic timelines
        if re.search(r'immediately|urgent|asap', response.lower()) and \
           'strategic' in scenario.get('meeting_type', '').lower():
            feasibility_score -= 0.2  # Strategic meetings need time
        
        # Check for budget considerations
        if 'budget' in response.lower():
            feasibility_score += 0.1
        
        return max(0.0, min(feasibility_score, 1.0))
    
    def _evaluate_stakeholder_fit(self, scenario: Dict, response: str) -> float:
        """Check if advice is appropriate for participant roles"""
        stakeholder_score = 0.0
        
        participants = scenario.get('participants', [])
        
        # Check if response considers different stakeholder perspectives
        executive_roles = ['ceo', 'cfo', 'cto', 'coo']
        mentions_executives = any(role in response.lower() for role in executive_roles)
        if mentions_executives and any(role in ' '.join(participants).lower() for role in executive_roles):
            stakeholder_score += 0.3
        
        # Check for role-specific recommendations
        if len(participants) > 3 and 'different' in response.lower():
            stakeholder_score += 0.2
        
        # Check for conflict resolution mentions (important for multi-stakeholder meetings)
        if len(participants) > 5 and any(word in response.lower() 
                                       for word in ['consensus', 'alignment', 'concerns']):
            stakeholder_score += 0.3
        
        return min(stakeholder_score, 1.0)
    
    def _evaluate_business_logic(self, scenario: Dict, response: str) -> float:
        """Assess soundness of business reasoning"""
        logic_score = 0.5  # Start neutral
        
        # Check for data-driven approaches
        data_keywords = ['metric', 'kpi', 'data', 'analysis', 'benchmark']
        if any(keyword in response.lower() for keyword in data_keywords):
            logic_score += 0.2
        
        # Check for risk consideration
        if 'risk' in response.lower():
            logic_score += 0.1
        
        # Check for ROI/business impact thinking
        business_keywords = ['roi', 'impact', 'revenue', 'cost', 'efficiency']
        if any(keyword in response.lower() for keyword in business_keywords):
            logic_score += 0.2
        
        return min(logic_score, 1.0)
    
    def _evaluate_completeness(self, response: str) -> float:
        """Current structural completeness check"""
        sections = ['objectives', 'agenda', 'stakeholder', 'content', 
                   'risk', 'action', 'follow']
        
        section_score = sum(1 for section in sections 
                           if section in response.lower()) / len(sections)
        
        # Length and structure bonuses
        length_bonus = 0.1 if len(response) > 500 else 0
        structure_bonus = 0.1 if len(response.split('\n')) > 10 else 0
        
        return min(section_score + length_bonus + structure_bonus, 1.0)
    
    def _evaluate_urgency_match(self, scenario: Dict, response: str) -> float:
        """Check if response appropriately addresses urgency and stakes"""
        urgency_score = 0.5  # Start neutral
        
        stakes = scenario.get('stakes', '').lower()
        
        # High stakes should have more detailed risk mitigation
        if any(word in stakes for word in ['critical', 'urgent', 'crisis']):
            if 'contingency' in response.lower() or 'risk' in response.lower():
                urgency_score += 0.3
            else:
                urgency_score -= 0.2
        
        # Check if timeline matches stakes
        if 'delay' in stakes and 'timeline' in response.lower():
            urgency_score += 0.2
        
        return max(0.0, min(urgency_score, 1.0))
    
    def _identify_strengths(self, scores: Dict[str, float]) -> List[str]:
        """Identify what the response does well"""
        strengths = []
        for dimension, score in scores.items():
            if score >= 0.8:
                strengths.append(f"Strong {dimension.replace('_', ' ')}")
        return strengths
    
    def _identify_weaknesses(self, scores: Dict[str, float]) -> List[str]:
        """Identify areas for improvement"""
        weaknesses = []
        for dimension, score in scores.items():
            if score <= 0.4:
                weaknesses.append(f"Weak {dimension.replace('_', ' ')}")
        return weaknesses
    
    def _identify_context_issues(self, scenario: Dict, response: str) -> List[str]:
        """Identify specific context-related problems"""
        issues = []
        
        # Check for generic vs specific advice
        if response.count('should') > 5 and response.count('specific') == 0:
            issues.append("Advice appears too generic for specific scenario")
        
        # Check if available context is ignored
        available_context = scenario.get('available_context', [])
        if len(available_context) > 3:
            context_used = sum(1 for context in available_context 
                             if any(word in response.lower() 
                                   for word in context.lower().split()[:2]))
            if context_used < len(available_context) * 0.3:
                issues.append("Fails to leverage available context documents")
        
        return issues


def demo_enhanced_evaluation():
    """Demonstrate the enhanced evaluation approach"""
    
    # Load a scenario from the demo data
    with open('demo_ollama/meeting_scenarios_with_responses.jsonl', 'r') as f:
        demo_data = json.loads(f.readline())
    
    evaluator = ContextAwareMeetingEvaluator()
    
    print("🎯 ENHANCED EVALUATION DEMO\n")
    print(f"Scenario: {demo_data['meeting_type']}")
    print(f"Stakes: {demo_data['stakes'][:100]}...")
    print()
    
    for i, response in enumerate(demo_data['responses'], 1):
        print(f"📊 Response {i} Enhanced Evaluation:")
        
        evaluation = evaluator.evaluate_response(demo_data, response['response_text'])
        
        print(f"Overall Score: {evaluation['overall_score']:.3f}")
        print("Dimension Breakdown:")
        for dim, score in evaluation['dimension_scores'].items():
            print(f"  {dim.replace('_', ' ').title()}: {score:.3f}")
        
        if evaluation['strengths']:
            print(f"Strengths: {', '.join(evaluation['strengths'])}")
        
        if evaluation['weaknesses']:
            print(f"Weaknesses: {', '.join(evaluation['weaknesses'])}")
        
        if evaluation['context_issues']:
            print(f"Context Issues: {', '.join(evaluation['context_issues'])}")
        
        print("-" * 50)

if __name__ == "__main__":
    demo_enhanced_evaluation()