import argparse
import json
import torch
from vllm import LLM, SamplingParams
from transformers import AutoTokenizer
from str2bool import str2bool
import os
from meeting_scenario_generation import meeting_preparation_response_prompt

def meeting_prep_inference(args):
    """Generate meeting preparation responses for given scenarios"""
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)
    
    # Load model
    model = LLM(
        model=args.model_path,
        tokenizer=args.model_path,
        tokenizer_mode="slow",
        dtype=args.dtype,
        tensor_parallel_size=args.n_gpus,
        seed=args.seed,
        enforce_eager=True,
        disable_custom_all_reduce=True,
        trust_remote_code=args.trust_remote_code,
    )
    
    # Setup sampling parameters
    sampling_params = SamplingParams(
        temperature=args.temperature,
        top_p=args.top_p,
        max_tokens=args.max_len,
    )
    
    # Load scenarios
    scenarios = []
    with open(args.data_path, 'r') as f:
        for line in f:
            scenarios.append(json.loads(line.strip()))
    
    print(f"Loaded {len(scenarios)} scenarios from {args.data_path}")
    
    # Process scenarios that need responses
    results = []
    prompts_to_generate = []
    scenario_indices = []
    
    for i, scenario in enumerate(scenarios):
        # Check if we need to generate responses for this scenario
        if "responses" not in scenario:
            scenario["responses"] = []
        
        if len(scenario["responses"]) < args.num_responses_per_scenario:
            # Generate prompt for this scenario
            response_prompt = meeting_preparation_response_prompt(scenario)
            
            if args.use_chat_template:
                messages = [{"role": "user", "content": response_prompt}]
                formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            else:
                formatted_prompt = response_prompt
            
            # Add multiple copies for multiple responses
            responses_needed = args.num_responses_per_scenario - len(scenario["responses"])
            for _ in range(responses_needed):
                prompts_to_generate.append(formatted_prompt)
                scenario_indices.append(i)
    
    print(f"Generating {len(prompts_to_generate)} responses...")
    
    if prompts_to_generate:
        # Generate responses in batches
        batch_size = args.batch_size
        for batch_start in range(0, len(prompts_to_generate), batch_size):
            batch_end = min(batch_start + batch_size, len(prompts_to_generate))
            batch_prompts = prompts_to_generate[batch_start:batch_end]
            batch_indices = scenario_indices[batch_start:batch_end]
            
            print(f"Processing batch {batch_start//batch_size + 1}/{(len(prompts_to_generate) + batch_size - 1)//batch_size}")
            
            outputs = model.generate(batch_prompts, sampling_params)
            
            for output, scenario_idx in zip(outputs, batch_indices):
                generated_text = output.outputs[0].text.strip()
                
                # Add response to scenario
                response_data = {
                    "response": generated_text,
                    "model": args.model_path,
                    "temperature": args.temperature,
                    "generated_at": None  # Could add timestamp if needed
                }
                
                scenarios[scenario_idx]["responses"].append(response_data)
    
    # Save results
    with open(args.output_path, 'w') as f:
        for scenario in scenarios:
            f.write(json.dumps(scenario) + '\n')
    
    print(f"Saved results to {args.output_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate meeting preparation responses")
    parser.add_argument("--data_path", type=str, required=True, help="Path to scenarios JSONL file")
    parser.add_argument("--output_path", type=str, required=True, help="Output path for scenarios with responses")
    parser.add_argument("--model_path", type=str, required=True, help="Model path")
    parser.add_argument("--num_responses_per_scenario", type=int, default=1, help="Number of responses per scenario")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size for generation")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--max_len", type=int, default=4096)
    parser.add_argument("--n_gpus", type=int, default=1)
    parser.add_argument("--dtype", type=str, default="bfloat16")
    parser.add_argument("--trust_remote_code", type=str2bool, default=False)
    parser.add_argument("--use_chat_template", type=str2bool, default=True)
    
    args = parser.parse_args()
    
    meeting_prep_inference(args)

if __name__ == "__main__":
    main()