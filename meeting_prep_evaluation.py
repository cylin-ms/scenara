import json
import argparse
from typing import Dict, List
import re

# Meeting preparation evaluation rubrics based on the GUTT framework
MEETING_PREP_RUBRICS = {
    "general": {
        "objectives_clarity": {
            "weight": 0.20,
            "description": "Clear meeting goals and success criteria defined",
            "criteria": [
                "Identifies specific meeting objectives",
                "Defines measurable success criteria", 
                "Aligns objectives with meeting type"
            ]
        },
        "agenda_structure": {
            "weight": 0.15,
            "description": "Well-structured agenda with time allocation",
            "criteria": [
                "Provides detailed agenda outline",
                "Includes time allocation for sections",
                "Orders items logically"
            ]
        },
        "stakeholder_analysis": {
            "weight": 0.20,
            "description": "Thorough analysis of participant needs and concerns",
            "criteria": [
                "Identifies participant motivations",
                "Anticipates objections or resistance",
                "Considers different personality types"
            ]
        },
        "content_preparation": {
            "weight": 0.15,
            "description": "Comprehensive material and data preparation",
            "criteria": [
                "Lists specific materials to gather",
                "Identifies key data points needed",
                "Plans visual aids or presentations"
            ]
        },
        "risk_mitigation": {
            "weight": 0.15,
            "description": "Proactive risk and contingency planning",
            "criteria": [
                "Identifies potential issues",
                "Prepares responses to difficult questions",
                "Has backup strategies"
            ]
        },
        "actionability": {
            "weight": 0.10,
            "description": "Concrete, actionable steps provided",
            "criteria": [
                "Provides specific action items",
                "Includes realistic timelines",
                "Considers resource constraints"
            ]
        },
        "follow_up_planning": {
            "weight": 0.05,
            "description": "Plans for post-meeting actions",
            "criteria": [
                "Identifies follow-up tasks",
                "Plans communication strategy",
                "Considers next steps"
            ]
        }
    },
    
    "meeting_type_specific": {
        "client_pitch": {
            "client_tailoring": {
                "weight": 0.25,
                "description": "Tailored to specific client needs and pain points",
                "criteria": [
                    "Addresses client-specific challenges",
                    "References client's industry context",
                    "Personalizes value proposition"
                ]
            },
            "competitive_differentiation": {
                "weight": 0.20,
                "description": "Clear differentiation from competitors",
                "criteria": [
                    "Highlights unique value propositions",
                    "Addresses competitive threats",
                    "Positions solution effectively"
                ]
            }
        },
        
        "performance_review": {
            "evidence_based": {
                "weight": 0.25,
                "description": "Uses concrete evidence and examples",
                "criteria": [
                    "Cites specific achievements",
                    "References measurable outcomes",
                    "Provides supporting documentation"
                ]
            },
            "development_focus": {
                "weight": 0.20,
                "description": "Emphasizes growth and development",
                "criteria": [
                    "Identifies development opportunities",
                    "Sets learning goals",
                    "Plans skill building activities"
                ]
            }
        },
        
        "board_meeting": {
            "executive_readiness": {
                "weight": 0.30,
                "description": "Prepared for executive-level scrutiny",
                "criteria": [
                    "Anticipates board-level questions",
                    "Prepares financial justifications",
                    "Addresses strategic implications"
                ]
            },
            "compliance_awareness": {
                "weight": 0.15,
                "description": "Considers regulatory and compliance issues",
                "criteria": [
                    "Addresses compliance requirements",
                    "Considers regulatory implications",
                    "Ensures proper documentation"
                ]
            }
        }
    }
}

def evaluate_response_quality(response: str, scenario: Dict, rubric_type: str = "general") -> Dict:
    """
    Evaluate a meeting preparation response against rubrics
    
    Args:
        response: The meeting preparation response text
        scenario: The meeting scenario context
        rubric_type: Type of rubric to use ("general" or specific meeting type)
    
    Returns:
        Dictionary with evaluation scores and feedback
    """
    
    # Get appropriate rubric
    if rubric_type in MEETING_PREP_RUBRICS["meeting_type_specific"]:
        rubric = {**MEETING_PREP_RUBRICS["general"], **MEETING_PREP_RUBRICS["meeting_type_specific"][rubric_type]}
    else:
        rubric = MEETING_PREP_RUBRICS["general"]
    
    evaluation = {
        "overall_score": 0.0,
        "dimension_scores": {},
        "missing_elements": [],
        "strengths": [],
        "weaknesses": []
    }
    
    total_weight = 0.0
    weighted_score = 0.0
    
    # Evaluate each dimension
    for dimension, details in rubric.items():
        score = evaluate_dimension(response, dimension, details["criteria"])
        weight = details["weight"]
        
        evaluation["dimension_scores"][dimension] = {
            "score": score,
            "weight": weight,
            "description": details["description"]
        }
        
        weighted_score += score * weight
        total_weight += weight
        
        # Track missing elements
        if score < 0.5:
            evaluation["missing_elements"].append(dimension)
        elif score > 0.8:
            evaluation["strengths"].append(dimension)
        elif score < 0.6:
            evaluation["weaknesses"].append(dimension)
    
    # Calculate overall score
    evaluation["overall_score"] = weighted_score / total_weight if total_weight > 0 else 0.0
    
    return evaluation

def evaluate_dimension(response: str, dimension: str, criteria: List[str]) -> float:
    """
    Evaluate a specific dimension of the response
    
    Args:
        response: The response text
        dimension: The dimension being evaluated
        criteria: List of criteria for this dimension
    
    Returns:
        Score between 0.0 and 1.0
    """
    
    response_lower = response.lower()
    
    # Keyword patterns for different dimensions
    keyword_patterns = {
        "objectives_clarity": [
            r"goal[s]?", r"objective[s]?", r"success", r"outcome[s]?", r"purpose", r"aim[s]?"
        ],
        "agenda_structure": [
            r"agenda", r"schedule", r"timeline", r"minutes", r"time", r"structure", r"order"
        ],
        "stakeholder_analysis": [
            r"stakeholder[s]?", r"participant[s]?", r"concern[s]?", r"motivation[s]?", 
            r"interest[s]?", r"perspective[s]?", r"objection[s]?"
        ],
        "content_preparation": [
            r"material[s]?", r"document[s]?", r"data", r"information", r"report[s]?", 
            r"presentation[s]?", r"slide[s]?", r"visual[s]?"
        ],
        "risk_mitigation": [
            r"risk[s]?", r"contingency", r"backup", r"fallback", r"issue[s]?", 
            r"problem[s]?", r"challenge[s]?", r"difficult"
        ],
        "actionability": [
            r"action", r"step[s]?", r"task[s]?", r"todo", r"checklist", r"deadline[s]?"
        ],
        "follow_up_planning": [
            r"follow.?up", r"next step[s]?", r"after", r"post.?meeting", r"communication"
        ]
    }
    
    # Check for keyword presence
    keyword_score = 0.0
    if dimension in keyword_patterns:
        patterns = keyword_patterns[dimension]
        matches = sum(1 for pattern in patterns if re.search(pattern, response_lower))
        keyword_score = min(matches / len(patterns), 1.0)
    
    # Check for structure indicators
    structure_score = 0.0
    if any(indicator in response_lower for indicator in ["1.", "2.", "•", "-", "##", "**"]):
        structure_score = 0.3
    
    # Check for specificity (avoiding generic advice)
    specificity_score = 0.0
    generic_phrases = [
        "be on time", "be confident", "do your best", "stay positive",
        "be prepared", "listen carefully", "ask questions"
    ]
    
    # Penalty for generic phrases
    generic_count = sum(1 for phrase in generic_phrases if phrase in response_lower)
    specificity_penalty = min(generic_count * 0.2, 0.5)
    
    # Bonus for specific details
    specific_indicators = [
        r"\d+%", r"\$\d+", r"\d+ days?", r"\d+ hours?", r"\d+ minutes?",
        r"q[1-4]", r"quarter", r"fiscal", r"budget", r"revenue"
    ]
    specific_matches = sum(1 for pattern in specific_indicators if re.search(pattern, response_lower))
    specificity_score = min(specific_matches * 0.2, 0.5) - specificity_penalty
    
    # Combine scores
    final_score = (keyword_score * 0.6 + structure_score + specificity_score * 0.4)
    return max(0.0, min(1.0, final_score))

def evaluate_meeting_prep_dataset(data_path: str, output_path: str):
    """
    Evaluate a dataset of meeting preparation responses
    
    Args:
        data_path: Path to JSONL file with scenarios and responses
        output_path: Path to save evaluation results
    """
    
    results = []
    
    with open(data_path, 'r') as f:
        for line_num, line in enumerate(f):
            try:
                item = json.loads(line.strip())
                
                if "responses" not in item:
                    continue
                
                scenario_results = {
                    "scenario_id": item.get("id", line_num),
                    "meeting_type": item.get("meeting_type", "unknown"),
                    "stakes": item.get("stakes", "unknown"),
                    "response_evaluations": []
                }
                
                # Evaluate each response
                for i, response_data in enumerate(item["responses"]):
                    if isinstance(response_data, dict):
                        response_text = response_data.get("response", "")
                    else:
                        response_text = str(response_data)
                    
                    # Determine rubric type based on meeting type
                    meeting_type = item.get("meeting_type", "").lower()
                    rubric_type = "general"
                    
                    if "client" in meeting_type or "pitch" in meeting_type:
                        rubric_type = "client_pitch"
                    elif "performance" in meeting_type or "review" in meeting_type:
                        rubric_type = "performance_review"  
                    elif "board" in meeting_type or "executive" in meeting_type:
                        rubric_type = "board_meeting"
                    
                    evaluation = evaluate_response_quality(response_text, item, rubric_type)
                    evaluation["response_index"] = i
                    evaluation["rubric_type"] = rubric_type
                    
                    scenario_results["response_evaluations"].append(evaluation)
                
                results.append(scenario_results)
                
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
    
    # Save results
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary statistics
    print_evaluation_summary(results)

def print_evaluation_summary(results: List[Dict]):
    """Print summary statistics of the evaluation"""
    
    all_scores = []
    dimension_scores = {}
    meeting_type_scores = {}
    
    for scenario in results:
        meeting_type = scenario["meeting_type"]
        
        for evaluation in scenario["response_evaluations"]:
            overall_score = evaluation["overall_score"]
            all_scores.append(overall_score)
            
            # Track by meeting type
            if meeting_type not in meeting_type_scores:
                meeting_type_scores[meeting_type] = []
            meeting_type_scores[meeting_type].append(overall_score)
            
            # Track dimension scores
            for dim, details in evaluation["dimension_scores"].items():
                if dim not in dimension_scores:
                    dimension_scores[dim] = []
                dimension_scores[dim].append(details["score"])
    
    if all_scores:
        print(f"\n=== EVALUATION SUMMARY ===")
        print(f"Total responses evaluated: {len(all_scores)}")
        print(f"Average overall score: {sum(all_scores) / len(all_scores):.3f}")
        print(f"Score distribution:")
        print(f"  Excellent (>0.8): {sum(1 for s in all_scores if s > 0.8)} ({sum(1 for s in all_scores if s > 0.8)/len(all_scores)*100:.1f}%)")
        print(f"  Good (0.6-0.8): {sum(1 for s in all_scores if 0.6 <= s <= 0.8)} ({sum(1 for s in all_scores if 0.6 <= s <= 0.8)/len(all_scores)*100:.1f}%)")
        print(f"  Fair (0.4-0.6): {sum(1 for s in all_scores if 0.4 <= s < 0.6)} ({sum(1 for s in all_scores if 0.4 <= s < 0.6)/len(all_scores)*100:.1f}%)")
        print(f"  Poor (<0.4): {sum(1 for s in all_scores if s < 0.4)} ({sum(1 for s in all_scores if s < 0.4)/len(all_scores)*100:.1f}%)")
        
        print(f"\n=== DIMENSION SCORES ===")
        for dim, scores in dimension_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                print(f"  {dim}: {avg_score:.3f}")
        
        print(f"\n=== MEETING TYPE PERFORMANCE ===")
        for meeting_type, scores in meeting_type_scores.items():
            if scores:
                avg_score = sum(scores) / len(scores)
                print(f"  {meeting_type}: {avg_score:.3f} (n={len(scores)})")

def filter_high_quality_responses(data_path: str, output_path: str, min_score: float = 0.7):
    """
    Filter dataset to keep only high-quality responses based on evaluation scores
    
    Args:
        data_path: Path to evaluated dataset
        output_path: Path to save filtered dataset
        min_score: Minimum score threshold for keeping responses
    """
    
    filtered_data = []
    
    with open(data_path, 'r') as f:
        evaluation_results = json.load(f)
    
    # Load original data 
    original_data_path = data_path.replace("_evaluated.json", ".jsonl")
    original_data = []
    try:
        with open(original_data_path, 'r') as f:
            for line in f:
                original_data.append(json.loads(line.strip()))
    except FileNotFoundError:
        print(f"Warning: Could not find original data file {original_data_path}")
        return
    
    # Filter responses
    for result, original_item in zip(evaluation_results, original_data):
        if "response_evaluations" not in result:
            continue
        
        # Keep responses that meet quality threshold
        filtered_responses = []
        for eval_data in result["response_evaluations"]:
            response_idx = eval_data["response_index"] 
            if eval_data["overall_score"] >= min_score:
                if response_idx < len(original_item.get("responses", [])):
                    filtered_responses.append(original_item["responses"][response_idx])
        
        # Keep scenario if it has at least one good response
        if filtered_responses:
            filtered_item = original_item.copy()
            filtered_item["responses"] = filtered_responses
            filtered_item["quality_scores"] = [
                eval_data["overall_score"] for eval_data in result["response_evaluations"]
                if eval_data["overall_score"] >= min_score
            ]
            filtered_data.append(filtered_item)
    
    # Save filtered data
    with open(output_path, 'w') as f:
        for item in filtered_data:
            f.write(json.dumps(item) + '\n')
    
    print(f"Filtered {len(filtered_data)} high-quality scenarios from {len(original_data)} original scenarios")
    print(f"Saved to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Evaluate meeting preparation responses")
    parser.add_argument("--data_path", type=str, required=True, help="Path to JSONL file with responses")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save evaluation results")
    parser.add_argument("--filter_output", type=str, help="Path to save filtered high-quality responses")
    parser.add_argument("--min_score", type=float, default=0.7, help="Minimum score for filtering")
    parser.add_argument("--action", type=str, default="evaluate", choices=["evaluate", "filter"], 
                        help="Action to perform: evaluate or filter")
    
    args = parser.parse_args()
    
    if args.action == "evaluate":
        evaluate_meeting_prep_dataset(args.data_path, args.output_path)
    elif args.action == "filter":
        filter_high_quality_responses(args.data_path, args.output_path, args.min_score)

if __name__ == "__main__":
    main()