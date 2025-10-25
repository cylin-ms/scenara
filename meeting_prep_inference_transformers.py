import argparse
import json
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from meeting_scenario_generation_transformers import meeting_preparation_response_prompt

def meeting_prep_inference_transformers(args):
    """Generate meeting preparation responses using Transformers pipeline"""
    
    print(f"Loading model: {args.model_path}")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    
    # Set pad token if not exists
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        args.model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
        trust_remote_code=args.trust_remote_code
    )
    
    # Create text generation pipeline
    generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        device_map="auto" if torch.cuda.is_available() else None,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    
    # Load scenarios
    scenarios = []
    with open(args.data_path, 'r', encoding='utf-8') as f:
        for line in f:
            scenarios.append(json.loads(line.strip()))
    
    print(f"Loaded {len(scenarios)} scenarios from {args.data_path}")
    
    # Process scenarios that need responses
    for i, scenario in enumerate(scenarios):
        # Check if we need to generate responses for this scenario
        if "responses" not in scenario:
            scenario["responses"] = []
        
        if len(scenario["responses"]) < args.num_responses_per_scenario:
            print(f"Generating responses for scenario {i+1}/{len(scenarios)}")
            
            # Generate prompt for this scenario
            response_prompt = meeting_preparation_response_prompt(scenario)
            
            # Generate responses
            responses_needed = args.num_responses_per_scenario - len(scenario["responses"])
            
            for j in range(responses_needed):
                try:
                    if args.use_chat_template and hasattr(tokenizer, 'apply_chat_template') and tokenizer.chat_template is not None:
                        try:
                            messages = [{"role": "user", "content": response_prompt}]
                            formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                        except:
                            # Fallback to plain prompt if chat template fails
                            formatted_prompt = f"User: {response_prompt}\n\nAssistant: "
                    else:
                        formatted_prompt = f"User: {response_prompt}\n\nAssistant: "
                    
                    # Generate response
                    outputs = generator(
                        formatted_prompt,
                        max_new_tokens=args.max_len,
                        temperature=args.temperature,
                        top_p=args.top_p,
                        do_sample=True,
                        pad_token_id=tokenizer.eos_token_id,
                        eos_token_id=tokenizer.eos_token_id,
                        return_full_text=False
                    )
                    
                    generated_text = outputs[0]['generated_text'].strip()
                    
                    # Add response to scenario
                    response_data = {
                        "response": generated_text,
                        "model": args.model_path,
                        "temperature": args.temperature,
                        "response_index": j
                    }
                    
                    scenario["responses"].append(response_data)
                    print(f"  Generated response {j+1}/{responses_needed}")
                    
                except Exception as e:
                    print(f"  Error generating response {j+1}: {e}")
    
    # Save results
    with open(args.output_path, 'w', encoding='utf-8') as f:
        for scenario in scenarios:
            f.write(json.dumps(scenario, ensure_ascii=False) + '\n')
    
    print(f"Saved results to {args.output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate meeting preparation responses using Transformers")
    parser.add_argument("--data_path", type=str, required=True, help="Path to scenarios JSONL file")
    parser.add_argument("--output_path", type=str, required=True, help="Output path for scenarios with responses")
    parser.add_argument("--model_path", type=str, required=True, help="Model path")
    parser.add_argument("--num_responses_per_scenario", type=int, default=1, help="Number of responses per scenario")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--max_len", type=int, default=4096)
    parser.add_argument("--trust_remote_code", action="store_true", default=False)
    parser.add_argument("--use_chat_template", action="store_true", default=True)
    
    args = parser.parse_args()
    
    # Set random seed
    torch.manual_seed(args.seed)
    
    meeting_prep_inference_transformers(args)

if __name__ == "__main__":
    main()