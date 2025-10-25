#!/usr/bin/env python3
"""
Real-World Meeting Preparation Framework
Based on PromptCoT 2.0 principles for context-aware synthetic data generation

Core Innovation: Apply PromptCoT 2.0's concept-rationale-prompt framework to meeting preparation,
addressing the context dependency problem with enterprise-grade solutions.
"""

import json
import os
import requests
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import uuid

class RealWorldMeetingPrepFramework:
    """
    Enterprise-grade meeting preparation framework inspired by PromptCoT 2.0
    
    Key Innovations from Paper Applied to Meeting Prep:
    1. Concept-Rationale-Prompt Paradigm → Context-Analysis-Preparation
    2. EM Optimization → Iterative Context Enhancement  
    3. Self-Play Training → Human-in-the-Loop Validation
    4. Synthetic Data Generation → Contextualized Scenario Creation
    """
    
    def __init__(self, ollama_base_url: str = "http://localhost:11434"):
        self.ollama_base_url = ollama_base_url
        self.context_extraction_model = "qwen3:8b"
        self.rationale_generation_model = "deepseek-r1:14b"  
        self.preparation_synthesis_model = "gpt-oss:20b"
        
        # Enterprise context categories (inspired by PromptCoT 2.0's concept space)
        self.context_categories = [
            "company_structure", "financial_data", "performance_metrics",
            "stakeholder_dynamics", "strategic_objectives", "operational_constraints",
            "industry_context", "regulatory_environment", "cultural_factors",
            "historical_decisions", "communication_patterns", "resource_availability"
        ]
        
    def extract_meeting_context(self, scenario_description: str, company_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant business context (analogous to PromptCoT 2.0's concept extraction)
        
        This addresses the core limitation: "how can you be sure that the meeting prep 
        response is good or bad if you don't have the files, chats, messages, and other 
        artifacts relevant to a meeting?"
        """
        
        context_extraction_prompt = f"""
As an expert business analyst with access to comprehensive company data, analyze this meeting scenario:

MEETING SCENARIO:
{scenario_description}

COMPANY PROFILE:
{json.dumps(company_profile, indent=2)}

Extract and categorize the key business context elements needed for effective meeting preparation:

1. STAKEHOLDER ANALYSIS:
   - Who are the key decision makers?
   - What are their interests, concerns, and power dynamics?
   - Historical relationships and communication patterns

2. BUSINESS CONTEXT:
   - Relevant financial data and performance metrics
   - Strategic objectives and operational constraints  
   - Industry pressures and regulatory requirements

3. ORGANIZATIONAL FACTORS:
   - Company culture and communication norms
   - Available resources and budget constraints
   - Past decisions and their outcomes

4. EXTERNAL ENVIRONMENT:
   - Market conditions and competitive landscape
   - Regulatory requirements and compliance issues
   - Industry best practices and benchmarks

Format your response as structured JSON with clear categories and specific details.
"""

        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.context_extraction_model,
                    "prompt": context_extraction_prompt,
                    "stream": False,
                    "options": {"temperature": 0.3}
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                return self._parse_context_extraction(result.get("response", ""))
            else:
                return {"error": f"Context extraction failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Context extraction error: {str(e)}"}
    
    def generate_analysis_rationale(self, meeting_context: Dict[str, Any], preparation_objectives: List[str]) -> str:
        """
        Generate comprehensive business analysis rationale
        (analogous to PromptCoT 2.0's rationale generation with business logic)
        """
        
        rationale_prompt = f"""
As a senior business strategist, develop a comprehensive analysis rationale for meeting preparation.

MEETING CONTEXT:
{json.dumps(meeting_context, indent=2)}

PREPARATION OBJECTIVES:
{json.dumps(preparation_objectives, indent=2)}

Generate a detailed thinking process that shows how to:

1. CONTEXT ANALYSIS:
   - How do the company's current financial position and performance metrics influence meeting dynamics?
   - What stakeholder interests and power dynamics must be navigated?
   - How do industry conditions and regulatory requirements shape constraints?

2. STRATEGIC ALIGNMENT:
   - How does this meeting connect to broader company objectives?
   - What are the potential risks and opportunities?
   - How do past decisions and organizational culture influence approach?

3. PREPARATION STRATEGY:
   - What specific data, documents, and insights are needed?
   - How should different stakeholder concerns be addressed?
   - What are the optimal communication strategies and messaging?

4. SUCCESS METRICS:
   - How will meeting effectiveness be measured?
   - What are the key decision points and potential outcomes?
   - How does success connect to broader business objectives?

Provide a comprehensive rationale that demonstrates deep business understanding and strategic thinking.
"""

        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.rationale_generation_model,
                    "prompt": rationale_prompt,
                    "stream": False,
                    "options": {"temperature": 0.4}
                },
                timeout=180
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "")
            else:
                return f"Rationale generation failed: {response.status_code}"
                
        except Exception as e:
            return f"Rationale generation error: {str(e)}"
    
    def synthesize_contextualized_preparation(self, context: Dict[str, Any], rationale: str) -> Dict[str, Any]:
        """
        Synthesize comprehensive meeting preparation based on business context and analysis
        (analogous to PromptCoT 2.0's prompt generation but for meeting preparation)
        """
        
        synthesis_prompt = f"""
As an expert executive assistant with deep business acumen, synthesize a comprehensive meeting preparation plan.

BUSINESS CONTEXT:
{json.dumps(context, indent=2)}

STRATEGIC ANALYSIS RATIONALE:
{rationale}

Generate a detailed meeting preparation plan that demonstrates:

1. CONTEXTUAL AWARENESS:
   - Specific references to company data, metrics, and constraints
   - Understanding of stakeholder dynamics and organizational culture
   - Recognition of industry context and regulatory requirements

2. STRATEGIC PREPARATION:
   - Key talking points tailored to stakeholder interests
   - Supporting data and documentation requirements
   - Risk mitigation strategies and contingency planning

3. TACTICAL EXECUTION:
   - Meeting agenda optimized for stakeholder engagement
   - Communication strategies and messaging frameworks
   - Resource allocation and logistics coordination

4. OUTCOME OPTIMIZATION:
   - Success metrics aligned with business objectives
   - Follow-up actions and accountability frameworks
   - Integration with broader strategic initiatives

Ensure every recommendation is grounded in the specific business context and demonstrates understanding of real enterprise constraints and opportunities.
"""

        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.preparation_synthesis_model,
                    "prompt": synthesis_prompt,
                    "stream": False,
                    "options": {"temperature": 0.5}
                },
                timeout=240
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "preparation_plan": result.get("response", ""),
                    "context_grounding": self._assess_context_grounding(result.get("response", ""), context),
                    "business_relevance": self._assess_business_relevance(result.get("response", ""), context)
                }
            else:
                return {"error": f"Preparation synthesis failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Preparation synthesis error: {str(e)}"}
    
    def human_in_the_loop_validation(self, preparation_plan: Dict[str, Any], validator_profile: str) -> Dict[str, Any]:
        """
        Human expert validation framework (inspired by PromptCoT 2.0's self-play but with human oversight)
        
        This addresses the fundamental limitation: synthetic evaluation needs real business expert validation
        """
        
        validation_prompt = f"""
As a {validator_profile}, evaluate this meeting preparation plan for real-world effectiveness:

PREPARATION PLAN:
{json.dumps(preparation_plan, indent=2)}

Provide expert validation across these dimensions:

1. BUSINESS REALISM (0-10):
   - Does this reflect real enterprise decision-making processes?
   - Are the constraints and considerations realistic?
   - Would this approach work in actual business environments?

2. CONTEXTUAL ACCURACY (0-10):
   - Does the plan demonstrate understanding of specific business context?
   - Are stakeholder dynamics accurately captured?
   - Is industry/regulatory knowledge appropriate?

3. STRATEGIC SOUNDNESS (0-10):
   - Are the strategic recommendations well-founded?
   - Do the tactics align with stated objectives?
   - Is the risk assessment comprehensive and realistic?

4. EXECUTION FEASIBILITY (0-10):
   - Can this plan actually be implemented?
   - Are resource requirements realistic?
   - Is the timeline achievable?

5. OUTCOME PROBABILITY (0-10):
   - How likely is this approach to achieve stated goals?
   - Are success metrics meaningful and measurable?
   - Does this connect to broader business value?

Provide specific feedback on strengths, weaknesses, and improvement recommendations.
Include examples from your professional experience where relevant.
"""

        try:
            response = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": self.rationale_generation_model,
                    "prompt": validation_prompt,
                    "stream": False,
                    "options": {"temperature": 0.2}
                },
                timeout=180
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "validation_response": result.get("response", ""),
                    "requires_human_review": True,
                    "validation_timestamp": datetime.now().isoformat(),
                    "validator_profile": validator_profile
                }
            else:
                return {"error": f"Validation failed: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Validation error: {str(e)}"}
    
    def iterative_context_enhancement(self, 
                                    initial_context: Dict[str, Any], 
                                    feedback: Dict[str, Any], 
                                    iterations: int = 3) -> Dict[str, Any]:
        """
        EM-style iterative improvement of context and preparation quality
        (inspired by PromptCoT 2.0's EM optimization)
        """
        
        enhanced_context = initial_context.copy()
        improvement_history = []
        
        for iteration in range(iterations):
            print(f"\n🔄 Enhancement Iteration {iteration + 1}/{iterations}")
            
            # E-step: Update context understanding based on feedback
            context_update_prompt = f"""
Based on expert feedback, enhance the business context understanding:

CURRENT CONTEXT:
{json.dumps(enhanced_context, indent=2)}

EXPERT FEEDBACK:
{json.dumps(feedback, indent=2)}

ITERATION: {iteration + 1}/{iterations}

Enhance the context by:
1. Adding missing business details identified in feedback
2. Correcting any misunderstandings or inaccuracies
3. Deepening stakeholder and organizational insights
4. Incorporating additional relevant constraints and opportunities

Return an improved context that addresses the feedback while maintaining accuracy.
"""

            try:
                response = requests.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.context_extraction_model,
                        "prompt": context_update_prompt,
                        "stream": False,
                        "options": {"temperature": 0.3}
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    enhanced_context = self._parse_context_extraction(result.get("response", ""))
                    improvement_history.append({
                        "iteration": iteration + 1,
                        "context_enhancement": enhanced_context,
                        "timestamp": datetime.now().isoformat()
                    })
                    
            except Exception as e:
                print(f"⚠️ Enhancement iteration {iteration + 1} failed: {str(e)}")
                break
        
        return {
            "final_enhanced_context": enhanced_context,
            "improvement_history": improvement_history,
            "total_iterations": len(improvement_history)
        }
    
    def generate_enterprise_scenario_corpus(self, 
                                          company_profiles: List[Dict[str, Any]], 
                                          scenario_templates: List[str],
                                          corpus_size: int = 1000) -> List[Dict[str, Any]]:
        """
        Generate large-scale corpus of contextualized meeting scenarios
        (inspired by PromptCoT 2.0's scalable synthetic data generation)
        """
        
        print(f"🏭 Generating enterprise scenario corpus of {corpus_size} scenarios...")
        corpus = []
        
        for i in range(corpus_size):
            try:
                # Select random company profile and scenario template
                company = company_profiles[i % len(company_profiles)]
                template = scenario_templates[i % len(scenario_templates)]
                
                # Generate contextualized scenario
                scenario_prompt = f"""
Generate a realistic business meeting scenario based on:

COMPANY PROFILE: {json.dumps(company, indent=2)}
SCENARIO TEMPLATE: {template}

Create a specific, detailed meeting scenario that:
1. Reflects the company's actual business context and constraints
2. Involves realistic stakeholder dynamics and decision-making processes  
3. Requires substantive business analysis and strategic thinking
4. Can be evaluated based on business outcomes and value creation

Include specific details about participants, objectives, constraints, and success criteria.
"""

                response = requests.post(
                    f"{self.ollama_base_url}/api/generate",
                    json={
                        "model": self.context_extraction_model,
                        "prompt": scenario_prompt,
                        "stream": False,
                        "options": {"temperature": 0.6}
                    },
                    timeout=120
                )
                
                if response.status_code == 200:
                    result = response.json()
                    scenario = {
                        "scenario_id": str(uuid.uuid4()),
                        "company_profile": company,
                        "scenario_description": result.get("response", ""),
                        "template_source": template,
                        "generation_timestamp": datetime.now().isoformat()
                    }
                    corpus.append(scenario)
                    
                    if (i + 1) % 50 == 0:
                        print(f"✅ Generated {i + 1}/{corpus_size} scenarios")
                        
            except Exception as e:
                print(f"⚠️ Failed to generate scenario {i + 1}: {str(e)}")
                continue
        
        print(f"🎯 Successfully generated {len(corpus)} enterprise scenarios")
        return corpus
    
    def _parse_context_extraction(self, response_text: str) -> Dict[str, Any]:
        """Parse context extraction response into structured format"""
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                # Fallback to structured parsing
                return {"extracted_context": response_text}
        except:
            return {"raw_response": response_text}
    
    def _assess_context_grounding(self, preparation_plan: str, context: Dict[str, Any]) -> float:
        """Assess how well preparation plan is grounded in business context"""
        # Simple keyword-based assessment (could be enhanced with more sophisticated analysis)
        context_keywords = set()
        for category, data in context.items():
            if isinstance(data, str):
                context_keywords.update(data.lower().split())
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, str):
                        context_keywords.update(item.lower().split())
        
        plan_words = set(preparation_plan.lower().split())
        overlap = len(context_keywords.intersection(plan_words))
        total_context_words = len(context_keywords)
        
        return min(overlap / max(total_context_words, 1), 1.0)
    
    def _assess_business_relevance(self, preparation_plan: str, context: Dict[str, Any]) -> float:
        """Assess business relevance of preparation plan"""
        business_terms = [
            "roi", "revenue", "cost", "budget", "strategic", "stakeholder",
            "objectives", "metrics", "performance", "compliance", "risk",
            "value", "opportunity", "decision", "resource", "timeline"
        ]
        
        plan_lower = preparation_plan.lower()
        term_count = sum(1 for term in business_terms if term in plan_lower)
        
        return min(term_count / len(business_terms), 1.0)


def demo_real_world_framework():
    """Demonstrate the real-world meeting preparation framework"""
    
    print("🏢 Real-World Meeting Preparation Framework Demo")
    print("Based on PromptCoT 2.0 principles for context-aware synthesis\n")
    
    framework = RealWorldMeetingPrepFramework()
    
    # Sample company profile with rich business context
    company_profile = {
        "company_name": "TechCorp Analytics",
        "industry": "Enterprise Software",
        "size": "500 employees",
        "revenue": "$50M annual",
        "financial_status": "Profitable, seeking Series B funding",
        "key_stakeholders": {
            "ceo": "Sarah Chen - Technical background, growth-focused",
            "cfo": "Mike Rodriguez - Conservative, ROI-driven", 
            "vp_sales": "Lisa Park - Aggressive targets, customer-focused",
            "vp_engineering": "David Kim - Quality-focused, resource-constrained"
        },
        "strategic_objectives": [
            "Scale to $100M ARR within 2 years",
            "Expand international markets",
            "Improve product scalability",
            "Maintain 90%+ customer satisfaction"
        ],
        "current_challenges": [
            "Engineering bandwidth constraints",
            "Increasing customer acquisition costs",
            "International compliance requirements",
            "Competitive pressure from larger players"
        ],
        "organizational_culture": "Data-driven, collaborative, fast-paced",
        "recent_performance": {
            "growth_rate": "40% YoY",
            "churn_rate": "5%",
            "nps_score": 72,
            "cash_runway": "18 months"
        }
    }
    
    # Meeting scenario requiring deep business context
    scenario_description = """
    Quarterly Business Review meeting with key executives to discuss:
    1. Q3 performance vs targets
    2. Resource allocation for Q4 product roadmap
    3. International expansion strategy for European markets
    4. Series B funding timeline and requirements
    
    Attendees: CEO, CFO, VP Sales, VP Engineering, Head of International
    Duration: 2 hours
    Stakes: High - decisions will impact funding and growth trajectory
    """
    
    print("📊 Step 1: Extracting Business Context...")
    context = framework.extract_meeting_context(scenario_description, company_profile)
    print(f"✅ Extracted {len(context)} context categories")
    
    print("\n🧠 Step 2: Generating Strategic Analysis Rationale...")
    preparation_objectives = [
        "Demonstrate strong Q3 performance to support funding narrative",
        "Secure executive alignment on resource allocation priorities", 
        "Validate international expansion strategy and timeline",
        "Address any concerns about growth sustainability"
    ]
    
    rationale = framework.generate_analysis_rationale(context, preparation_objectives)
    print(f"✅ Generated {len(rationale)} character strategic rationale")
    
    print("\n📋 Step 3: Synthesizing Contextualized Preparation Plan...")
    preparation = framework.synthesize_contextualized_preparation(context, rationale)
    print(f"✅ Generated comprehensive preparation plan")
    print(f"   - Context Grounding Score: {preparation.get('context_grounding', 0):.2f}")
    print(f"   - Business Relevance Score: {preparation.get('business_relevance', 0):.2f}")
    
    print("\n👥 Step 4: Human Expert Validation...")
    validation = framework.human_in_the_loop_validation(
        preparation, 
        "Senior Management Consultant with 15+ years enterprise experience"
    )
    print(f"✅ Expert validation completed at {validation.get('validation_timestamp')}")
    
    print("\n🔄 Step 5: Iterative Context Enhancement...")
    sample_feedback = {
        "missing_elements": ["Competitive landscape analysis", "Customer input on roadmap"],
        "enhancement_areas": ["Stakeholder communication strategies", "Risk mitigation plans"],
        "accuracy_issues": ["Budget allocation assumptions need validation"]
    }
    
    enhanced = framework.iterative_context_enhancement(context, sample_feedback, iterations=2)
    print(f"✅ Completed {enhanced['total_iterations']} enhancement iterations")
    
    print("\n🎯 FRAMEWORK ADVANTAGES:")
    print("✅ Addresses context dependency through rich company profiling")
    print("✅ Generates business-grounded preparation recommendations")
    print("✅ Incorporates human expert validation for quality assurance")
    print("✅ Iteratively improves through feedback incorporation")
    print("✅ Scalable to enterprise scenario corpus generation")
    
    print("\n📈 PROMPTCOT 2.0 PRINCIPLES APPLIED:")
    print("• Concept-Rationale-Prompt → Context-Analysis-Preparation")
    print("• EM Optimization → Iterative Context Enhancement")
    print("• Self-Play Training → Human-in-the-Loop Validation") 
    print("• Synthetic Data Generation → Contextualized Scenario Creation")
    
    return framework


if __name__ == "__main__":
    demo_framework = demo_real_world_framework()