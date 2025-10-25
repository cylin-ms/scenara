import argparse
import json
from transformers import AutoTokenizer
from typing import List, Dict

def prepare_meeting_prep_sft_data(args):
    """
    Prepare meeting preparation data for supervised fine-tuning
    
    Args:
        args: Command line arguments
    """
    
    # Load tokenizer to check token lengths
    tokenizer = AutoTokenizer.from_pretrained(args.tokenizer_path)
    
    # Load evaluated data
    training_examples = []
    
    with open(args.data_path, 'r') as f:
        for line in f:
            item = json.loads(line.strip())
            
            if "responses" not in item:
                continue
            
            # Filter for high-quality responses only
            high_quality_responses = [
                r for r in item["responses"] 
                if r.get("quality_score", 0) >= args.min_quality_score
            ]
            
            if not high_quality_responses:
                continue
            
            # Create training prompt
            scenario_prompt = f"""Please provide comprehensive preparation guidance for the following meeting scenario:

**Meeting Scenario:**
{item.get('scenario', '')}

**Meeting Details:**
- Type: {item.get('meeting_type', '')}
- Participants: {', '.join(item.get('participants', []))}
- Stakes: {item.get('stakes', '')}
- Key Challenges: {', '.join(item.get('challenges', []))}
- Available Resources: {', '.join(item.get('available_context', []))}

**Question:** {item.get('preparation_question', 'How should I prepare for this meeting?')}"""

            # Use the best response(s) as targets
            for response_data in high_quality_responses:
                response_text = response_data["response"]
                
                # Check token length
                if args.max_tokens:
                    prompt_tokens = len(tokenizer.encode(scenario_prompt))
                    response_tokens = len(tokenizer.encode(response_text))
                    total_tokens = prompt_tokens + response_tokens
                    
                    if total_tokens > args.max_tokens:
                        print(f"Skipping example with {total_tokens} tokens (exceeds limit of {args.max_tokens})")
                        continue
                
                # Create training example
                if args.format == "chat":
                    # Chat format for instruction tuning
                    training_example = {
                        "messages": [
                            {"role": "user", "content": scenario_prompt},
                            {"role": "assistant", "content": response_text}
                        ],
                        "quality_score": response_data.get("quality_score", 0),
                        "meeting_type": item.get("meeting_type", ""),
                        "stakes": item.get("stakes", ""),
                        "scenario_id": item.get("id")
                    }
                elif args.format == "completion":
                    # Completion format
                    training_example = {
                        "prompt": scenario_prompt,
                        "completion": response_text,
                        "quality_score": response_data.get("quality_score", 0),
                        "meeting_type": item.get("meeting_type", ""),
                        "stakes": item.get("stakes", ""),
                        "scenario_id": item.get("id")
                    }
                else:
                    # Simple prompt-response format
                    training_example = {
                        "input": scenario_prompt,
                        "output": response_text,
                        "quality_score": response_data.get("quality_score", 0),
                        "meeting_type": item.get("meeting_type", ""),
                        "stakes": item.get("stakes", ""),
                        "scenario_id": item.get("id")
                    }
                
                training_examples.append(training_example)
    
    # Sort by quality score (best first) and optionally limit
    training_examples.sort(key=lambda x: x["quality_score"], reverse=True)
    
    if args.max_examples:
        training_examples = training_examples[:args.max_examples]
    
    # Save training data
    with open(args.output_path, 'w') as f:
        for example in training_examples:
            f.write(json.dumps(example) + '\n')
    
    # Print statistics
    print(f"Created {len(training_examples)} training examples")
    print(f"Saved to {args.output_path}")
    
    if training_examples:
        avg_quality = sum(ex["quality_score"] for ex in training_examples) / len(training_examples)
        print(f"Average quality score: {avg_quality:.3f}")
        
        # Statistics by meeting type
        meeting_types = {}
        stakes_dist = {}
        
        for ex in training_examples:
            mt = ex["meeting_type"]
            stakes = ex["stakes"]
            
            meeting_types[mt] = meeting_types.get(mt, 0) + 1
            stakes_dist[stakes] = stakes_dist.get(stakes, 0) + 1
        
        print("\nDistribution by meeting type:")
        for mt, count in sorted(meeting_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {mt}: {count}")
        
        print("\nDistribution by stakes:")
        for stakes, count in sorted(stakes_dist.items(), key=lambda x: x[1], reverse=True):
            print(f"  {stakes}: {count}")
        
        # Token length statistics if tokenizer provided
        if args.max_tokens:
            token_lengths = []
            for ex in training_examples:
                if args.format == "chat":
                    # Approximate token count for chat format
                    total_text = ex["messages"][0]["content"] + ex["messages"][1]["content"]
                elif args.format == "completion":
                    total_text = ex["prompt"] + ex["completion"]
                else:
                    total_text = ex["input"] + ex["output"]
                
                tokens = len(tokenizer.encode(total_text))
                token_lengths.append(tokens)
            
            if token_lengths:
                avg_tokens = sum(token_lengths) / len(token_lengths)
                max_tokens = max(token_lengths)
                print(f"\nToken statistics:")
                print(f"  Average tokens: {avg_tokens:.0f}")
                print(f"  Max tokens: {max_tokens}")
                print(f"  Examples over {args.max_tokens//2} tokens: {sum(1 for t in token_lengths if t > args.max_tokens//2)}")

def main():
    parser = argparse.ArgumentParser(description="Prepare meeting preparation data for SFT")
    parser.add_argument("--data_path", type=str, required=True, 
                        help="Path to evaluated responses JSONL file")
    parser.add_argument("--output_path", type=str, required=True,
                        help="Path to save SFT training data")
    parser.add_argument("--tokenizer_path", type=str, required=True,
                        help="Path to tokenizer for length checking")
    parser.add_argument("--min_quality_score", type=float, default=0.7,
                        help="Minimum quality score for including responses")
    parser.add_argument("--max_examples", type=int, default=None,
                        help="Maximum number of training examples")
    parser.add_argument("--max_tokens", type=int, default=4096,
                        help="Maximum token length for examples")
    parser.add_argument("--format", type=str, default="chat", 
                        choices=["chat", "completion", "simple"],
                        help="Output format for training data")
    
    args = parser.parse_args()
    
    prepare_meeting_prep_sft_data(args)

if __name__ == "__main__":
    main()