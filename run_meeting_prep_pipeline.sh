#!/bin/bash

# Meeting Preparation Data Generation Pipeline using adapted PromptCoT 2.0
# Based on the meeting prep adaptation document

# Configuration
MODEL_PATH="Qwen/Qwen3-32B-Instruct"
N_GPUS=4
SEED=42
TEMPERATURE=0.8
OUTPUT_DIR="meeting_prep_data"

# Create output directory
mkdir -p $OUTPUT_DIR

echo "=== PromptCoT 2.0 Meeting Preparation Data Generation Pipeline ==="

# Step 1: Generate meeting scenarios
echo "Step 1: Generating meeting scenarios..."
python meeting_scenario_generation.py \
  --model_path $MODEL_PATH \
  --output_path $OUTPUT_DIR/meeting_scenarios.jsonl \
  --num_scenarios 500 \
  --seed $SEED \
  --temperature $TEMPERATURE \
  --n_gpus $N_GPUS \
  --use_chat_template true

# Step 2: Generate initial responses (cold start data)
echo "Step 2: Generating initial meeting preparation responses..."
python meeting_prep_inference.py \
  --data_path $OUTPUT_DIR/meeting_scenarios.jsonl \
  --output_path $OUTPUT_DIR/meeting_scenarios_with_responses.jsonl \
  --model_path $MODEL_PATH \
  --num_responses_per_scenario 4 \
  --batch_size 16 \
  --seed $SEED \
  --temperature 0.7 \
  --n_gpus $N_GPUS \
  --use_chat_template true

# Step 3: Evaluate responses and assign rewards (E-step)
echo "Step 3: Evaluating responses and assigning rewards..."
python meeting_prep_self_play_eval.py \
  --data_path $OUTPUT_DIR/meeting_scenarios_with_responses.jsonl \
  --output_path $OUTPUT_DIR/meeting_scenarios_evaluated.jsonl \
  --pairs_output $OUTPUT_DIR/meeting_prep_training_pairs.jsonl \
  --min_quality_score 0.6

# Step 4: Self-play iterations (EM loop)
echo "Step 4: Starting EM self-training loop..."

for iteration in {1..3}; do
    echo "=== Self-Play Iteration $iteration ==="
    
    # Generate more responses using current model
    echo "Generating responses for iteration $iteration..."
    python meeting_prep_self_play.py \
      --data_path $OUTPUT_DIR/meeting_scenarios.jsonl \
      --output_path $OUTPUT_DIR/meeting_scenarios_selfplay_iter_${iteration}.jsonl \
      --model_path $MODEL_PATH \
      --num_completions 6 \
      --seed $((SEED + iteration)) \
      --temperature 0.8 \
      --n_gpus $N_GPUS \
      --num_splits 2 \
      --use_chat_template true
    
    # Evaluate new responses
    echo "Evaluating responses for iteration $iteration..."
    python meeting_prep_self_play_eval.py \
      --data_path $OUTPUT_DIR/meeting_scenarios_selfplay_iter_${iteration}.jsonl \
      --output_path $OUTPUT_DIR/meeting_scenarios_evaluated_iter_${iteration}.jsonl \
      --pairs_output $OUTPUT_DIR/meeting_prep_training_pairs_iter_${iteration}.jsonl \
      --min_quality_score 0.6
    
    # Filter high-quality responses for next iteration
    echo "Filtering high-quality responses..."
    python meeting_prep_evaluation.py \
      --data_path $OUTPUT_DIR/meeting_scenarios_evaluated_iter_${iteration}.jsonl \
      --output_path $OUTPUT_DIR/meeting_scenarios_filtered_iter_${iteration}.jsonl \
      --action filter \
      --min_score 0.7
done

# Step 5: Prepare final SFT dataset
echo "Step 5: Preparing SFT training dataset..."

# Combine all high-quality responses
cat $OUTPUT_DIR/meeting_scenarios_filtered_iter_*.jsonl > $OUTPUT_DIR/meeting_prep_combined_filtered.jsonl

python prepare_meeting_prep_sft_data.py \
  --data_path $OUTPUT_DIR/meeting_prep_combined_filtered.jsonl \
  --output_path $OUTPUT_DIR/meeting_prep_sft_training.jsonl \
  --tokenizer_path $MODEL_PATH \
  --min_quality_score 0.7 \
  --max_examples 10000 \
  --format chat

# Step 6: Golden prompt evaluation
echo "Step 6: Evaluating against golden prompts..."
python -c "
import json
from meeting_prep_golden_prompts import GOLDEN_PROMPTS
from meeting_prep_inference import meeting_prep_inference

# Generate responses for golden prompts
golden_scenarios = []
for prompt in GOLDEN_PROMPTS:
    scenario = {
        'id': prompt['id'],
        'scenario': prompt['scenario'], 
        'meeting_type': prompt['meeting_type'],
        'participants': prompt['participants'],
        'stakes': prompt['stakes'],
        'challenges': prompt['challenges'],
        'available_context': prompt['available_context'],
        'preparation_question': prompt['prompt'],
        'responses': []
    }
    golden_scenarios.append(scenario)

# Save golden scenarios
with open('$OUTPUT_DIR/golden_prompts_scenarios.jsonl', 'w') as f:
    for scenario in golden_scenarios:
        f.write(json.dumps(scenario) + '\\n')
"

python meeting_prep_inference.py \
  --data_path $OUTPUT_DIR/golden_prompts_scenarios.jsonl \
  --output_path $OUTPUT_DIR/golden_prompts_responses.jsonl \
  --model_path $MODEL_PATH \
  --num_responses_per_scenario 1 \
  --seed $SEED \
  --temperature 0.6 \
  --n_gpus $N_GPUS

python meeting_prep_evaluation.py \
  --data_path $OUTPUT_DIR/golden_prompts_responses.jsonl \
  --output_path $OUTPUT_DIR/golden_prompts_evaluation.json \
  --action evaluate

# Step 7: Generate summary statistics
echo "Step 7: Generating summary statistics..."
python -c "
import json
import os

output_dir = '$OUTPUT_DIR'
print('\\n=== MEETING PREPARATION DATA GENERATION SUMMARY ===')

# Count scenarios
try:
    with open(f'{output_dir}/meeting_scenarios.jsonl', 'r') as f:
        num_scenarios = sum(1 for line in f)
    print(f'Total scenarios generated: {num_scenarios}')
except:
    pass

# Count training examples
try:
    with open(f'{output_dir}/meeting_prep_sft_training.jsonl', 'r') as f:
        num_training = sum(1 for line in f)
    print(f'SFT training examples: {num_training}')
except:
    pass

# Count training pairs
try:
    with open(f'{output_dir}/meeting_prep_training_pairs.jsonl', 'r') as f:
        num_pairs = sum(1 for line in f)
    print(f'Self-play training pairs: {num_pairs}')
except:
    pass

# Golden prompt performance
try:
    with open(f'{output_dir}/golden_prompts_evaluation.json', 'r') as f:
        golden_results = json.load(f)
    
    if golden_results:
        scores = []
        for result in golden_results:
            for eval_data in result.get('response_evaluations', []):
                scores.append(eval_data.get('overall_score', 0))
        
        if scores:
            avg_golden_score = sum(scores) / len(scores)
            print(f'Average golden prompt score: {avg_golden_score:.3f}')
except:
    pass

print(f'\\nAll outputs saved to: {output_dir}/')
"

echo ""
echo "=== Pipeline Complete! ==="
echo "Generated datasets:"
echo "  - meeting_prep_sft_training.jsonl (for supervised fine-tuning)"  
echo "  - meeting_prep_training_pairs.jsonl (for self-play training)"
echo "  - golden_prompts_evaluation.json (evaluation results)"
echo ""
echo "To train a model:"
echo "  1. Use meeting_prep_sft_training.jsonl for initial SFT"
echo "  2. Use meeting_prep_training_pairs.jsonl for self-play/DPO training"
echo "  3. Evaluate using golden prompts for quality assessment"