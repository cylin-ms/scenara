import argparse
import json
import os
from typing import List, Dict
from meeting_prep_evaluation import evaluate_response_quality

def evaluate_and_assign_rewards(data_path: str, output_path: str, min_quality_score: float = 0.6):
    """
    Evaluate meeting preparation responses and assign rewards for self-play training
    
    Args:
        data_path: Path to JSONL file with scenarios and responses
        output_path: Path to save evaluated data with rewards
        min_quality_score: Minimum score threshold for positive reward
    """
    
    evaluated_data = []
    
    with open(data_path, 'r') as f:
        for line_num, line in enumerate(f):
            try:
                item = json.loads(line.strip())
                
                if "responses" not in item or not item["responses"]:
                    continue
                
                # Evaluate each response
                evaluated_responses = []
                
                for response_data in item["responses"]:
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
                    
                    # Evaluate response quality
                    evaluation = evaluate_response_quality(response_text, item, rubric_type)
                    
                    # Assign reward based on quality score
                    quality_score = evaluation["overall_score"]
                    
                    if quality_score >= 0.8:
                        reward = 1.0  # High quality
                    elif quality_score >= min_quality_score:
                        reward = 0.5  # Acceptable quality
                    else:
                        reward = 0.0  # Poor quality
                    
                    # Create response with evaluation data
                    evaluated_response = {
                        "response": response_text,
                        "quality_score": quality_score,
                        "reward": reward,
                        "evaluation": evaluation,
                        "rubric_type": rubric_type
                    }
                    
                    # Copy over original metadata if it exists
                    if isinstance(response_data, dict):
                        for key, value in response_data.items():
                            if key not in evaluated_response and key != "response":
                                evaluated_response[key] = value
                    
                    evaluated_responses.append(evaluated_response)
                
                # Update item with evaluated responses
                item["responses"] = evaluated_responses
                
                # Add summary statistics
                scores = [r["quality_score"] for r in evaluated_responses]
                rewards = [r["reward"] for r in evaluated_responses]
                
                item["quality_stats"] = {
                    "avg_score": sum(scores) / len(scores) if scores else 0,
                    "max_score": max(scores) if scores else 0,
                    "min_score": min(scores) if scores else 0,
                    "high_quality_count": sum(1 for s in scores if s >= 0.8),
                    "acceptable_count": sum(1 for s in scores if s >= min_quality_score),
                    "poor_count": sum(1 for s in scores if s < min_quality_score),
                    "avg_reward": sum(rewards) / len(rewards) if rewards else 0
                }
                
                evaluated_data.append(item)
                
                if (line_num + 1) % 100 == 0:
                    print(f"Processed {line_num + 1} scenarios...")
                
            except Exception as e:
                print(f"Error processing line {line_num}: {e}")
    
    # Save evaluated data
    with open(output_path, 'w') as f:
        for item in evaluated_data:
            f.write(json.dumps(item) + '\n')
    
    # Print summary statistics
    print_reward_summary(evaluated_data)
    
    return evaluated_data

def print_reward_summary(evaluated_data: List[Dict]):
    """Print summary of reward assignment"""
    
    total_responses = 0
    high_quality = 0
    acceptable = 0
    poor = 0
    all_scores = []
    
    for item in evaluated_data:
        stats = item.get("quality_stats", {})
        total_responses += len(item.get("responses", []))
        high_quality += stats.get("high_quality_count", 0)
        acceptable += stats.get("acceptable_count", 0) 
        poor += stats.get("poor_count", 0)
        
        for response in item.get("responses", []):
            all_scores.append(response.get("quality_score", 0))
    
    if total_responses > 0:
        print(f"\n=== REWARD ASSIGNMENT SUMMARY ===")
        print(f"Total responses: {total_responses}")
        print(f"High quality (>= 0.8): {high_quality} ({high_quality/total_responses*100:.1f}%)")
        print(f"Acceptable (>= 0.6): {acceptable} ({acceptable/total_responses*100:.1f}%)")
        print(f"Poor (< 0.6): {poor} ({poor/total_responses*100:.1f}%)")
        print(f"Average quality score: {sum(all_scores)/len(all_scores):.3f}")

def prepare_self_play_pairs(data_path: str, output_path: str):
    """
    Prepare chosen vs rejected pairs for self-play training from evaluated responses
    
    Args:
        data_path: Path to evaluated JSONL file
        output_path: Path to save training pairs
    """
    
    training_pairs = []
    
    with open(data_path, 'r') as f:
        for line in f:
            item = json.loads(line.strip())
            
            if "responses" not in item or len(item["responses"]) < 2:
                continue
            
            responses = item["responses"]
            
            # Sort responses by quality score
            sorted_responses = sorted(responses, key=lambda r: r.get("quality_score", 0), reverse=True)
            
            # Create pairs: best vs others
            best_response = sorted_responses[0]
            
            # Only create pairs if best response is actually good quality
            if best_response.get("quality_score", 0) >= 0.6:
                
                for rejected_response in sorted_responses[1:]:
                    # Only pair if there's meaningful quality difference
                    if (best_response.get("quality_score", 0) - rejected_response.get("quality_score", 0)) >= 0.2:
                        
                        # Create the training prompt (scenario + question)
                        training_prompt = f"""Meeting Scenario: {item.get('scenario', '')}

Meeting Type: {item.get('meeting_type', '')}
Participants: {', '.join(item.get('participants', []))}
Stakes: {item.get('stakes', '')}
Challenges: {', '.join(item.get('challenges', []))}
Available Resources: {', '.join(item.get('available_context', []))}

Question: {item.get('preparation_question', 'How should I prepare for this meeting?')}"""
                        
                        pair = {
                            "prompt": training_prompt,
                            "chosen": best_response["response"],
                            "rejected": rejected_response["response"],
                            "chosen_score": best_response.get("quality_score", 0),
                            "rejected_score": rejected_response.get("quality_score", 0),
                            "score_difference": best_response.get("quality_score", 0) - rejected_response.get("quality_score", 0),
                            "scenario_id": item.get("id"),
                            "meeting_type": item.get("meeting_type")
                        }
                        
                        training_pairs.append(pair)
    
    # Save training pairs
    with open(output_path, 'w') as f:
        for pair in training_pairs:
            f.write(json.dumps(pair) + '\n')
    
    print(f"Created {len(training_pairs)} training pairs and saved to {output_path}")
    
    # Print pair statistics
    if training_pairs:
        avg_score_diff = sum(p["score_difference"] for p in training_pairs) / len(training_pairs)
        print(f"Average score difference between chosen/rejected: {avg_score_diff:.3f}")
        
        meeting_types = {}
        for pair in training_pairs:
            mt = pair["meeting_type"]
            if mt not in meeting_types:
                meeting_types[mt] = 0
            meeting_types[mt] += 1
        
        print("Pairs by meeting type:")
        for mt, count in sorted(meeting_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {mt}: {count}")

def main():
    parser = argparse.ArgumentParser(description="Evaluate meeting prep responses and assign rewards")
    parser.add_argument("--data_path", type=str, required=True, help="Path to responses JSONL file")
    parser.add_argument("--output_path", type=str, required=True, help="Path to save evaluated data")
    parser.add_argument("--pairs_output", type=str, help="Path to save training pairs")
    parser.add_argument("--min_quality_score", type=float, default=0.6, help="Minimum score for positive reward")
    parser.add_argument("--eval_type", type=str, default="meeting_prep", help="Evaluation type")
    
    args = parser.parse_args()
    
    # Evaluate and assign rewards
    print("Evaluating responses and assigning rewards...")
    evaluated_data = evaluate_and_assign_rewards(args.data_path, args.output_path, args.min_quality_score)
    
    # Create training pairs if requested
    if args.pairs_output:
        print("Creating training pairs...")
        prepare_self_play_pairs(args.output_path, args.pairs_output)

if __name__ == "__main__":
    main()