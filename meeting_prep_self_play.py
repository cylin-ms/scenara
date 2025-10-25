import argparse
import json
import os
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
import math
from typing import List, Dict
import time
from meeting_scenario_generation import meeting_preparation_response_prompt

def get_after_think(text):
    parts = text.split("</think>", 1)
    if len(parts) > 1:
        return parts[1]
    else:
        return text

def process_split_worker(split_id: int, data_split: List[Dict], args_dict: Dict, gpu_ids: List[int]) -> List[Dict]:
    """Worker function for generating meeting preparation responses with self-play"""

    # Set CUDA_VISIBLE_DEVICES BEFORE importing torch/vllm
    os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(map(str, gpu_ids))

    # Now import CUDA-dependent libraries
    import torch
    from vllm import LLM, SamplingParams
    from transformers import AutoTokenizer

    print(f"Split {split_id}: Processing {len(data_split)} items on GPUs {gpu_ids}")
    print(f"Split {split_id}: CUDA_VISIBLE_DEVICES = {os.environ.get('CUDA_VISIBLE_DEVICES')}")
    print(f"Split {split_id}: Available CUDA devices: {torch.cuda.device_count()}")

    # Reconstruct args from dict
    args = argparse.Namespace(**args_dict)

    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model_path)

    # Use all visible GPUs for tensor parallelism
    tensor_parallel_size = len(gpu_ids)

    # Load model
    model = LLM(
        model=args.model_path,
        tokenizer=args.model_path,
        tokenizer_mode="slow",
        dtype=args.dtype,
        tensor_parallel_size=tensor_parallel_size,
        seed=None if args.seed == -1 else args.seed + split_id,
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

    # Filter items that need processing
    remaining_items = []
    remaining_indices = []

    for idx, item in enumerate(data_split):
        # Initialize fields if not present
        if "responses" not in item:
            item["responses"] = []

        # Check if we need more responses
        if len(item["responses"]) < args.num_completions:
            remaining_items.append(item)
            remaining_indices.append(idx)

    print(f"Split {split_id}: {len(remaining_items)} items need responses out of {len(data_split)} total")

    if not remaining_items:
        print(f"Split {split_id}: No items to process")
        return data_split

    # Prepare prompts for items that need processing
    prompts = []
    item_indices = []
    
    for item_idx, item in enumerate(remaining_items):
        responses_needed = args.num_completions - len(item["responses"])
        
        # Generate prompt for meeting preparation
        response_prompt = meeting_preparation_response_prompt(item)
        
        for completion_idx in range(responses_needed):
            if args.use_chat_template:
                messages = [{"role": "user", "content": response_prompt}]
                formatted_prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
            else:
                formatted_prompt = response_prompt
            
            prompts.append(formatted_prompt)
            item_indices.append(item_idx)

    if not prompts:
        print(f"Split {split_id}: No prompts to process")
        return data_split

    print(f"Split {split_id}: Generating {len(prompts)} responses...")

    # Generate responses in batches
    batch_size = min(args.batch_size, len(prompts))
    outputs = []
    
    for i in range(0, len(prompts), batch_size):
        batch_prompts = prompts[i:i + batch_size]
        batch_outputs = model.generate(batch_prompts, sampling_params)
        outputs.extend(batch_outputs)
        
        print(f"Split {split_id}: Completed batch {i//batch_size + 1}/{(len(prompts) + batch_size - 1)//batch_size}")

    # Process outputs and add to items
    for output, item_idx in zip(outputs, item_indices):
        generated_text = output.outputs[0].text.strip()
        
        # Handle thinking tokens if present
        if args.use_thinking:
            generated_text = get_after_think(generated_text)
        
        response_data = {
            "response": generated_text,
            "model": args.model_path,
            "temperature": args.temperature,
            "seed": args.seed + split_id,
            "split_id": split_id
        }
        
        remaining_items[item_idx]["responses"].append(response_data)

    # Update the original data split
    for remaining_idx, original_idx in enumerate(remaining_indices):
        data_split[original_idx] = remaining_items[remaining_idx]

    print(f"Split {split_id}: Completed processing")
    return data_split

def main():
    parser = argparse.ArgumentParser(description="Meeting preparation self-play generation")
    parser.add_argument("--data_path", type=str, required=True, help="Input JSONL file with meeting scenarios")
    parser.add_argument("--output_path", type=str, required=True, help="Output JSONL file") 
    parser.add_argument("--model_path", type=str, required=True, help="Model path")
    parser.add_argument("--trust_remote_code", action="store_true", help="Trust remote code")
    parser.add_argument("--n_gpus", type=int, default=1, help="Number of GPUs to use")
    parser.add_argument("--num_splits", type=int, default=1, help="Number of data splits")
    parser.add_argument("--num_completions", type=int, default=4, help="Number of responses per scenario")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--temperature", type=float, default=0.8, help="Sampling temperature")
    parser.add_argument("--top_p", type=float, default=0.95, help="Top-p sampling")
    parser.add_argument("--max_len", type=int, default=4096, help="Maximum generation length")
    parser.add_argument("--batch_size", type=int, default=16, help="Batch size for generation")
    parser.add_argument("--use_chat_template", action="store_true", help="Use chat template")
    parser.add_argument("--use_thinking", action="store_true", help="Handle thinking tokens")
    parser.add_argument("--dtype", type=str, default="bfloat16", help="Model dtype")

    args = parser.parse_args()

    # Load data
    data = []
    with open(args.data_path, 'r') as f:
        for line in f:
            data.append(json.loads(line.strip()))

    print(f"Loaded {len(data)} scenarios from {args.data_path}")

    # Split data for parallel processing
    if args.num_splits > 1:
        chunk_size = math.ceil(len(data) / args.num_splits)
        data_splits = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
        
        # Assign GPUs to splits
        gpu_assignments = []
        gpus_per_split = max(1, args.n_gpus // args.num_splits)
        
        for split_id in range(len(data_splits)):
            start_gpu = (split_id * gpus_per_split) % args.n_gpus
            end_gpu = min(start_gpu + gpus_per_split, args.n_gpus)
            gpu_ids = list(range(start_gpu, end_gpu))
            gpu_assignments.append(gpu_ids)

        print(f"Processing {len(data_splits)} splits with GPU assignments: {gpu_assignments}")

        # Convert args to dict for multiprocessing
        args_dict = vars(args)

        # Process splits in parallel
        with ProcessPoolExecutor(max_workers=args.num_splits) as executor:
            futures = []
            for split_id, (data_split, gpu_ids) in enumerate(zip(data_splits, gpu_assignments)):
                future = executor.submit(process_split_worker, split_id, data_split, args_dict, gpu_ids)
                futures.append(future)

            # Collect results
            processed_data = []
            for future in as_completed(futures):
                result = future.result()
                processed_data.extend(result)

    else:
        # Single process
        gpu_ids = list(range(args.n_gpus))
        args_dict = vars(args)
        processed_data = process_split_worker(0, data, args_dict, gpu_ids)

    # Save results
    os.makedirs(os.path.dirname(args.output_path), exist_ok=True)
    with open(args.output_path, 'w') as f:
        for item in processed_data:
            f.write(json.dumps(item) + '\n')

    print(f"Saved {len(processed_data)} processed scenarios to {args.output_path}")

    # Print summary
    total_responses = sum(len(item.get("responses", [])) for item in processed_data)
    print(f"Generated {total_responses} total responses")
    print(f"Average {total_responses / len(processed_data):.1f} responses per scenario")

if __name__ == "__main__":
    main()