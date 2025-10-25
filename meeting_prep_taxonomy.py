# Meeting Type Taxonomy for PromptCoT Meeting Preparation Data Generation

MEETING_TAXONOMY = {
    "internal_cadence": {
        "types": [
            {
                "name": "Team Status Update",
                "purpose": "share progress, blockers",
                "participants": ["team members", "team lead"],
                "frequency": "weekly standup",
                "stakes": "low/medium"
            },
            {
                "name": "One-on-One",
                "purpose": "coaching & performance feedback",
                "participants": ["manager", "direct report"],
                "frequency": "bi-weekly or monthly",
                "stakes": "medium-high for employee growth"
            },
            {
                "name": "Sprint Planning",
                "purpose": "plan upcoming sprint work",
                "participants": ["development team", "product owner", "scrum master"],
                "frequency": "start of each sprint",
                "stakes": "medium"
            },
            {
                "name": "Sprint Retrospective", 
                "purpose": "learn from completed sprint",
                "participants": ["development team", "scrum master"],
                "frequency": "end of each sprint",
                "stakes": "low-medium"
            }
        ]
    },
    "strategic_planning": {
        "types": [
            {
                "name": "Project Kickoff",
                "purpose": "align on project plan and roles",
                "participants": ["cross-functional project team", "stakeholders"],
                "frequency": "one-time at start",
                "stakes": "medium, sets project trajectory"
            },
            {
                "name": "Design Review",
                "purpose": "evaluate proposed design or solution",
                "participants": ["design leads", "engineering leads", "product manager"],
                "frequency": "scheduled at milestones",
                "stakes": "medium-high, approval needed to proceed"
            },
            {
                "name": "Strategic Planning Session",
                "purpose": "define long-term strategy and goals",
                "participants": ["leadership team", "key stakeholders"],
                "frequency": "quarterly or annually",
                "stakes": "high, sets organizational direction"
            },
            {
                "name": "Budget Planning",
                "purpose": "allocate resources and budget",
                "participants": ["finance team", "department heads"],
                "frequency": "annually or quarterly",
                "stakes": "high, impacts all operations"
            }
        ]
    },
    "performance_evaluation": {
        "types": [
            {
                "name": "Performance Review",
                "purpose": "review employee performance and set goals",
                "participants": ["manager", "employee", "sometimes HR"],
                "frequency": "semi-annual/annual",
                "stakes": "high for individual's career"
            },
            {
                "name": "Promotion Committee",
                "purpose": "evaluate promotion candidates",
                "participants": ["senior leadership", "HR", "relevant managers"],
                "frequency": "quarterly or as needed",
                "stakes": "extremely high for candidates"
            },
            {
                "name": "360 Feedback Session",
                "purpose": "comprehensive performance feedback",
                "participants": ["employee", "peers", "direct reports", "manager"],
                "frequency": "annually",
                "stakes": "high for development"
            }
        ]
    },
    "external_client": {
        "types": [
            {
                "name": "Client Pitch",
                "purpose": "win new business",
                "participants": ["sales team", "client stakeholders"],
                "frequency": "as needed",
                "stakes": "high - could make or break deal"
            },
            {
                "name": "Quarterly Business Review",
                "purpose": "update client on progress and results",
                "participants": ["account team", "client executives"],
                "frequency": "quarterly",
                "stakes": "high - relationship and renewal impact"
            },
            {
                "name": "Vendor Negotiation",
                "purpose": "manage supplier relationship or contract",
                "participants": ["procurement leads", "vendor representatives"],
                "frequency": "as needed",
                "stakes": "medium, impacts costs and supply"
            },
            {
                "name": "Partnership Meeting",
                "purpose": "establish or manage strategic partnerships",
                "participants": ["business development", "partner representatives"],
                "frequency": "as needed",
                "stakes": "medium-high, strategic implications"
            }
        ]
    },
    "informational_broadcast": {
        "types": [
            {
                "name": "All-Hands/Town Hall",
                "purpose": "inform and inspire large group",
                "participants": ["organization-wide", "led by leadership"],
                "frequency": "quarterly or ad-hoc",
                "stakes": "medium - important for morale and alignment"
            },
            {
                "name": "Training Session",
                "purpose": "transfer knowledge or skills",
                "participants": ["instructor", "employees"],
                "frequency": "as needed",
                "stakes": "low individually, important for compliance"
            },
            {
                "name": "Product Launch",
                "purpose": "announce new product or feature",
                "participants": ["product team", "stakeholders", "customers"],
                "frequency": "as needed",
                "stakes": "high - market impact"
            }
        ]
    },
    "team_building": {
        "types": [
            {
                "name": "Team Retrospective",
                "purpose": "learn from completed project",
                "participants": ["project team"],
                "frequency": "end of project/sprint",
                "stakes": "low-medium, improves future process"
            },
            {
                "name": "Recognition Event",
                "purpose": "boost morale and recognize achievements",
                "participants": ["team or organization"],
                "frequency": "as needed",
                "stakes": "low business impact, high cultural impact"
            },
            {
                "name": "Team Offsite",
                "purpose": "build relationships and alignment",
                "participants": ["team members"],
                "frequency": "annually or semi-annually",
                "stakes": "medium - team cohesion impact"
            }
        ]
    },
    "governance_executive": {
        "types": [
            {
                "name": "Board Meeting",
                "purpose": "review business performance and strategy",
                "participants": ["C-level executives", "board members"],
                "frequency": "quarterly",
                "stakes": "extremely high - company direction"
            },
            {
                "name": "Executive Committee",
                "purpose": "make high-level strategic decisions",
                "participants": ["C-level executives"],
                "frequency": "monthly",
                "stakes": "extremely high - organizational impact"
            },
            {
                "name": "Audit Committee",
                "purpose": "oversee financial reporting and compliance",
                "participants": ["board members", "auditors", "CFO"],
                "frequency": "quarterly",
                "stakes": "extremely high - regulatory compliance"
            }
        ]
    }
}

# Common challenges/complications to add to scenarios
MEETING_CHALLENGES = [
    "skeptical stakeholders",
    "limited data availability",
    "tight time constraints",
    "conflicting priorities among attendees",
    "remote/hybrid meeting format",
    "technical difficulties expected",
    "sensitive/confidential information",
    "previous meeting went poorly",
    "new team members unfamiliar with context",
    "competing vendor presentations",
    "budget constraints",
    "regulatory compliance requirements",
    "cultural differences among participants",
    "language barriers",
    "urgent deadline pressure",
    "incomplete project deliverables",
    "stakeholder fatigue",
    "conflicting schedules",
    "missing key decision makers",
    "unclear success criteria"
]

# Context elements that can be available for preparation
AVAILABLE_CONTEXT = [
    "previous meeting notes",
    "project status reports", 
    "financial data",
    "competitor analysis",
    "customer feedback",
    "team performance metrics",
    "industry benchmarks",
    "regulatory guidelines",
    "organizational chart",
    "budget information",
    "timeline constraints",
    "technical specifications",
    "stakeholder profiles",
    "risk assessments",
    "market research",
    "user research data",
    "vendor proposals",
    "audit reports",
    "compliance documentation",
    "strategic plans"
]

def get_random_meeting_scenario():
    """Generate a random meeting scenario from the taxonomy"""
    import random
    
    # Select random category and meeting type
    category = random.choice(list(MEETING_TAXONOMY.keys()))
    meeting_type = random.choice(MEETING_TAXONOMY[category]["types"])
    
    # Add 1-3 random challenges
    num_challenges = random.randint(1, 3)
    challenges = random.sample(MEETING_CHALLENGES, num_challenges)
    
    # Add 1-4 available context elements
    num_context = random.randint(1, 4)
    context = random.sample(AVAILABLE_CONTEXT, num_context)
    
    return {
        "category": category,
        "meeting_type": meeting_type,
        "challenges": challenges,
        "available_context": context
    }

def format_scenario_description(scenario):
    """Format a scenario into a natural language description"""
    meeting = scenario["meeting_type"]
    challenges_str = ", ".join(scenario["challenges"])
    context_str = ", ".join(scenario["available_context"])
    
    description = f"""
A {meeting["name"]} meeting where the purpose is to {meeting["purpose"]}. 
The participants include: {", ".join(meeting["participants"])}.
This meeting typically occurs {meeting["frequency"]} and has {meeting["stakes"]} stakes.

Complicating factors for this meeting:
- {challenges_str}

Available information for preparation:
- {context_str}
""".strip()
    
    return description