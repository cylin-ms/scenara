# Meeting Preparation Golden Prompts
# Based on the GUTT (Generalized Unit Task Template) framework

GOLDEN_PROMPTS = [
    {
        "id": "qbr_missed_targets",
        "category": "governance_executive",
        "meeting_type": "Quarterly Business Review",
        "scenario": "A Quarterly Business Review with the board where you must present Q3 results, but the revenue targets were missed by 15% due to a major client cancellation, and two board members have already expressed concerns about the strategic direction. The meeting is in 2 days and you need to present both the shortfall analysis and a recovery plan.",
        "participants": ["CEO", "board members", "CFO", "VP Sales"],
        "stakes": "extremely high",
        "challenges": ["missed revenue targets", "skeptical board members", "short preparation time", "need recovery plan"],
        "available_context": ["Q3 financial data", "client cancellation details", "previous board feedback", "competitor analysis"],
        "prompt": "How should I prepare for this QBR meeting to address the revenue shortfall while maintaining board confidence?",
        "expected_elements": [
            "Honest acknowledgment of shortfall",
            "Root cause analysis",
            "Recovery plan with specific actions",
            "Risk mitigation strategies",
            "Board-specific concerns addressed",
            "Financial projections for Q4"
        ]
    },
    
    {
        "id": "performance_review_bad_quarter",
        "category": "performance_evaluation",
        "meeting_type": "Performance Review",
        "scenario": "Your annual performance review with your manager where you had a challenging quarter with two project delays and missed your sales quota by 20%, but you also led a successful team initiative and received positive client feedback. Your manager has been supportive but HR requires documentation of performance gaps.",
        "participants": ["manager", "employee", "HR representative"],
        "stakes": "high for individual's career",
        "challenges": ["missed targets", "project delays", "HR documentation requirements", "mixed performance"],
        "available_context": ["project timelines", "sales data", "client feedback", "team initiative results"],
        "prompt": "How should I prepare for my performance review to address the challenges while highlighting my contributions?",
        "expected_elements": [
            "Self-assessment with evidence",
            "Explanation of challenges",
            "Documentation of achievements",
            "Development goals",
            "Action plan for improvement"
        ]
    },
    
    {
        "id": "client_pitch_skeptical_audience",
        "category": "external_client", 
        "meeting_type": "Client Pitch",
        "scenario": "A high-stakes pitch to a Fortune 500 client who has been burned by previous vendors and is extremely skeptical of new technology solutions. The decision committee includes both technical and business stakeholders with different priorities, and you're competing against two established incumbents. The client has budget constraints but urgent needs.",
        "participants": ["sales team", "client CTO", "client CFO", "procurement team", "technical leads"],
        "stakes": "high - could make or break deal",
        "challenges": ["skeptical audience", "competing vendors", "budget constraints", "mixed stakeholder priorities"],
        "available_context": ["client's pain points", "competitor analysis", "previous vendor failures", "budget parameters"],
        "prompt": "How should I prepare for this client pitch to overcome skepticism and win against established competitors?",
        "expected_elements": [
            "Client-specific value proposition",
            "Risk mitigation strategies",
            "Competitive differentiation",
            "Budget justification",
            "Stakeholder-specific messaging"
        ]
    },
    
    {
        "id": "one_on_one_difficult_conversation",
        "category": "internal_cadence",
        "meeting_type": "One-on-One",
        "scenario": "A one-on-one with your direct report who has been struggling with performance issues, missing deadlines, and showing signs of disengagement. Other team members have complained, but the employee was previously a strong performer and is going through personal challenges. You need to address the issues while being supportive.",
        "participants": ["manager", "direct report"],
        "stakes": "medium-high for employee growth", 
        "challenges": ["performance decline", "personal issues", "team impact", "previous strong performance"],
        "available_context": ["performance metrics", "team feedback", "previous achievements", "personal circumstances"],
        "prompt": "How should I prepare for this one-on-one to address performance issues while being supportive and constructive?",
        "expected_elements": [
            "Specific performance examples",
            "Empathetic approach",
            "Support resources offered",
            "Clear expectations set",
            "Follow-up plan"
        ]
    },
    
    {
        "id": "design_review_technical_debt",
        "category": "strategic_planning",
        "meeting_type": "Design Review", 
        "scenario": "A critical design review for a new system architecture where the proposed solution addresses current needs but introduces significant technical debt. The engineering team is split on the approach, product wants to ship quickly, and there are concerns about scalability. You need to get approval to proceed with a clear path forward.",
        "participants": ["engineering leads", "product manager", "architect", "tech lead"],
        "stakes": "medium-high, approval needed to proceed",
        "challenges": ["technical debt concerns", "team disagreement", "time pressure", "scalability questions"],
        "available_context": ["technical specifications", "scalability analysis", "timeline constraints", "alternative approaches"],
        "prompt": "How should I prepare for this design review to get approval while addressing technical debt concerns?",
        "expected_elements": [
            "Technical trade-off analysis",
            "Risk assessment",
            "Timeline implications",
            "Alternative approaches evaluated",
            "Stakeholder concerns addressed"
        ]
    },
    
    {
        "id": "team_retrospective_failed_project",
        "category": "team_building",
        "meeting_type": "Team Retrospective",
        "scenario": "A retrospective for a project that failed to meet its objectives, went significantly over budget, and caused tension within the team. Some team members are defensive, others are frustrated, and there's blame being assigned. You need to conduct a productive retrospective that leads to learning and improvement.",
        "participants": ["project team", "scrum master"],
        "stakes": "low-medium, improves future process",
        "challenges": ["project failure", "team tension", "defensiveness", "blame dynamics"],
        "available_context": ["project timeline", "budget overruns", "team feedback", "failure analysis"],
        "prompt": "How should I prepare for this retrospective to ensure it's productive and focuses on learning rather than blame?",
        "expected_elements": [
            "Blameless culture emphasized",
            "Structured facilitation plan", 
            "Focus on process improvements",
            "Actionable next steps",
            "Team psychological safety"
        ]
    },
    
    {
        "id": "vendor_negotiation_contract_renewal",
        "category": "external_client",
        "meeting_type": "Vendor Negotiation",
        "scenario": "A contract renewal negotiation with a critical vendor who has been underperforming on SLAs but is difficult to replace. They're asking for a 30% price increase while your budget is being cut. You need to either improve terms or find alternatives, but switching vendors would cause significant disruption.",
        "participants": ["procurement team", "vendor account manager", "operations lead"],
        "stakes": "medium, impacts costs and supply",
        "challenges": ["SLA underperformance", "price increase request", "budget cuts", "switching costs"],
        "available_context": ["SLA performance data", "market alternatives", "switching cost analysis", "budget constraints"],
        "prompt": "How should I prepare for this vendor negotiation to improve terms without risking service disruption?",
        "expected_elements": [
            "Performance data analysis",
            "Market leverage points",
            "Alternative options prepared",
            "Negotiation strategy",
            "Risk mitigation plan"
        ]
    },
    
    {
        "id": "all_hands_layoffs_announcement", 
        "category": "informational_broadcast",
        "meeting_type": "All-Hands/Town Hall",
        "scenario": "An all-hands meeting where you need to announce workforce reductions affecting 15% of the company due to economic conditions. Employee morale is already low, there are rumors circulating, and you need to maintain trust while delivering difficult news. The leadership team needs to present a united front.",
        "participants": ["entire organization", "executive team", "HR leadership"],
        "stakes": "medium - important for morale and alignment",
        "challenges": ["difficult news delivery", "low morale", "rumors", "maintaining trust"],
        "available_context": ["business rationale", "affected departments", "support resources", "future outlook"],
        "prompt": "How should I prepare for this all-hands meeting to deliver the layoff news with transparency while maintaining employee trust?",
        "expected_elements": [
            "Clear business rationale",
            "Transparent communication",
            "Support for affected employees",
            "Future stability messaging",
            "Q&A preparation"
        ]
    }
]

# GUTT Templates for generating variations
GUTT_TEMPLATES = {
    "stakeholder_challenge": {
        "template": "A {meeting_type} where you must {objective} but {stakeholder_challenge}. {time_constraint} and you need to {deliverable}.",
        "variables": {
            "stakeholder_challenge": [
                "key stakeholders are skeptical",
                "there's resistance to change", 
                "budget approval is uncertain",
                "technical feasibility is questioned",
                "political dynamics are complex"
            ],
            "time_constraint": [
                "The meeting is tomorrow",
                "You have limited preparation time",
                "Decisions need to be made quickly",
                "There's an urgent deadline"
            ]
        }
    },
    
    "resource_constraint": {
        "template": "A {meeting_type} where you must {objective} but {resource_constraint}. {additional_challenge} and {success_criteria}.",
        "variables": {
            "resource_constraint": [
                "budget has been cut by 25%",
                "key team members are unavailable", 
                "critical data is missing",
                "technology limitations exist",
                "regulatory restrictions apply"
            ],
            "additional_challenge": [
                "stakeholders have conflicting priorities",
                "external factors are changing rapidly",
                "competition is intensifying",
                "customer expectations are rising"
            ]
        }
    },
    
    "crisis_management": {
        "template": "An emergency {meeting_type} where you must address {crisis_situation}. {impact_description} and you need to {action_required}.",
        "variables": {
            "crisis_situation": [
                "a major security breach",
                "significant product defects",
                "PR crisis and negative media",
                "key client threatening to leave",
                "regulatory compliance violation"
            ],
            "impact_description": [
                "Customer trust is at risk",
                "Financial impact is severe", 
                "Reputation damage is likely",
                "Legal consequences are possible",
                "Employee morale is affected"
            ]
        }
    }
}

def generate_golden_prompt_variations(template_name: str, base_prompt: dict, num_variations: int = 3):
    """Generate variations of a golden prompt using GUTT templates"""
    import random
    
    if template_name not in GUTT_TEMPLATES:
        return []
    
    template_data = GUTT_TEMPLATES[template_name]
    variations = []
    
    for i in range(num_variations):
        # Select random values for variables
        scenario_vars = {}
        for var_name, options in template_data["variables"].items():
            scenario_vars[var_name] = random.choice(options)
        
        # Create variation
        variation = base_prompt.copy()
        variation["id"] = f"{base_prompt['id']}_var_{i+1}"
        
        # Modify scenario using template
        if "template" in template_data:
            # This would need more sophisticated template substitution
            # For now, just add the variation info to the scenario
            variation["scenario"] += f" Additional challenge: {list(scenario_vars.values())[0]}"
            variation["challenges"].extend(list(scenario_vars.values())[:2])
        
        variations.append(variation)
    
    return variations

def get_golden_prompts_by_category(category: str = None):
    """Get golden prompts, optionally filtered by category"""
    if category:
        return [p for p in GOLDEN_PROMPTS if p["category"] == category]
    return GOLDEN_PROMPTS

def evaluate_against_golden_prompts(model_responses: dict):
    """Evaluate model responses against golden prompts"""
    results = {}
    
    for golden_prompt in GOLDEN_PROMPTS:
        prompt_id = golden_prompt["id"]
        
        if prompt_id in model_responses:
            response = model_responses[prompt_id]
            expected_elements = golden_prompt["expected_elements"]
            
            # Check coverage of expected elements
            coverage_score = 0
            response_lower = response.lower()
            
            for element in expected_elements:
                # Simple keyword matching - could be made more sophisticated
                element_keywords = element.lower().split()
                if any(keyword in response_lower for keyword in element_keywords):
                    coverage_score += 1
            
            coverage_ratio = coverage_score / len(expected_elements)
            
            results[prompt_id] = {
                "coverage_score": coverage_ratio,
                "expected_elements": expected_elements,
                "covered_elements": coverage_score,
                "total_elements": len(expected_elements),
                "response": response
            }
    
    return results