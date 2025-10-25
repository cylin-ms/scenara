#!/usr/bin/env bash

# Meeting Preparation Data Generation Pipeline using adapted PromptCoT 2.0
# macOS Compatible Version
# Based on the meeting prep adaptation document

set -e  # Exit on any error
set -u  # Exit on undefined variable

# Configuration
MODEL_PATH="${MODEL_PATH:-Qwen/Qwen3-32B-Instruct}"
N_GPUS="${N_GPUS:-1}"  # Default to 1 GPU for macOS (often single GPU setups)
SEED="${SEED:-42}"
TEMPERATURE="${TEMPERATURE:-0.8}"
OUTPUT_DIR="${OUTPUT_DIR:-meeting_prep_data}"

# Colors for output (macOS terminal compatible)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}=== $1 ===${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to check if command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        print_error "Command '$1' not found. Please install it first."
        exit 1
    fi
}

# Function to check if Python module is available
check_python_module() {
    if ! python -c "import $1" &> /dev/null; then
        print_error "Python module '$1' not found. Please install it with: pip install $1"
        exit 1
    fi
}

# Pre-flight checks
print_step "Pre-flight checks"
check_command "python"
check_command "pip"

# Check for required Python modules
echo "Checking Python dependencies..."
required_modules=("torch" "transformers" "vllm" "json" "argparse")
for module in "${required_modules[@]}"; do
    if [[ "$module" == "json" || "$module" == "argparse" ]]; then
        # These are built-in modules, skip check
        continue
    fi
    check_python_module "$module"
done

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    print_warning "This script is optimized for macOS. You may encounter issues on other systems."
fi

# Check available disk space (macOS specific)
available_space=$(df -h . | tail -1 | awk '{print $4}')
print_success "Available disk space: $available_space"

# Create output directory with proper permissions
if [[ ! -d "$OUTPUT_DIR" ]]; then
    mkdir -p "$OUTPUT_DIR"
    print_success "Created output directory: $OUTPUT_DIR"
else
    print_success "Using existing output directory: $OUTPUT_DIR"
fi

# Check if output directory is writable
if [[ ! -w "$OUTPUT_DIR" ]]; then
    print_error "Output directory $OUTPUT_DIR is not writable"
    exit 1
fi

print_step "PromptCoT 2.0 Meeting Preparation Data Generation Pipeline (macOS)"
echo "Model: $MODEL_PATH"
echo "GPUs: $N_GPUS"
echo "Output: $OUTPUT_DIR"
echo "Seed: $SEED"
echo ""

# Step 1: Generate meeting scenarios
print_step "Step 1: Generating meeting scenarios"
python meeting_scenario_generation.py \
  --model_path "$MODEL_PATH" \
  --output_path "$OUTPUT_DIR/meeting_scenarios.jsonl" \
  --num_scenarios 500 \
  --seed "$SEED" \
  --temperature "$TEMPERATURE" \
  --n_gpus "$N_GPUS" \
  --use_chat_template true

if [[ -f "$OUTPUT_DIR/meeting_scenarios.jsonl" ]]; then
    scenario_count=$(wc -l < "$OUTPUT_DIR/meeting_scenarios.jsonl" | tr -d ' ')
    print_success "Generated $scenario_count scenarios"
else
    print_error "Failed to generate scenarios"
    exit 1
fi

# Step 2: Generate initial responses (cold start data)
print_step "Step 2: Generating initial meeting preparation responses"
python meeting_prep_inference.py \
  --data_path "$OUTPUT_DIR/meeting_scenarios.jsonl" \
  --output_path "$OUTPUT_DIR/meeting_scenarios_with_responses.jsonl" \
  --model_path "$MODEL_PATH" \
  --num_responses_per_scenario 4 \
  --batch_size 16 \
  --seed "$SEED" \
  --temperature 0.7 \
  --n_gpus "$N_GPUS" \
  --use_chat_template true

if [[ -f "$OUTPUT_DIR/meeting_scenarios_with_responses.jsonl" ]]; then
    print_success "Generated initial responses"
else
    print_error "Failed to generate initial responses"
    exit 1
fi

# Step 3: Evaluate responses and assign rewards (E-step)
print_step "Step 3: Evaluating responses and assigning rewards"
python meeting_prep_self_play_eval.py \
  --data_path "$OUTPUT_DIR/meeting_scenarios_with_responses.jsonl" \
  --output_path "$OUTPUT_DIR/meeting_scenarios_evaluated.jsonl" \
  --pairs_output "$OUTPUT_DIR/meeting_prep_training_pairs.jsonl" \
  --min_quality_score 0.6

if [[ -f "$OUTPUT_DIR/meeting_scenarios_evaluated.jsonl" ]]; then
    print_success "Completed initial evaluation"
else
    print_error "Failed to evaluate responses"
    exit 1
fi

# Step 4: Self-play iterations (EM loop)
print_step "Step 4: Starting EM self-training loop"

for iteration in {1..3}; do
    print_step "Self-Play Iteration $iteration"
    
    # Generate more responses using current model
    echo "Generating responses for iteration $iteration..."
    python meeting_prep_self_play.py \
      --data_path "$OUTPUT_DIR/meeting_scenarios.jsonl" \
      --output_path "$OUTPUT_DIR/meeting_scenarios_selfplay_iter_${iteration}.jsonl" \
      --model_path "$MODEL_PATH" \
      --num_completions 6 \
      --seed $((SEED + iteration)) \
      --temperature 0.8 \
      --n_gpus "$N_GPUS" \
      --num_splits 2 \
      --use_chat_template true
    
    # Evaluate new responses
    echo "Evaluating responses for iteration $iteration..."
    python meeting_prep_self_play_eval.py \
      --data_path "$OUTPUT_DIR/meeting_scenarios_selfplay_iter_${iteration}.jsonl" \
      --output_path "$OUTPUT_DIR/meeting_scenarios_evaluated_iter_${iteration}.jsonl" \
      --pairs_output "$OUTPUT_DIR/meeting_prep_training_pairs_iter_${iteration}.jsonl" \
      --min_quality_score 0.6
    
    # Filter high-quality responses for next iteration
    echo "Filtering high-quality responses..."
    python meeting_prep_evaluation.py \
      --data_path "$OUTPUT_DIR/meeting_scenarios_evaluated_iter_${iteration}.jsonl" \
      --output_path "$OUTPUT_DIR/meeting_scenarios_filtered_iter_${iteration}.jsonl" \
      --action filter \
      --min_score 0.7
    
    if [[ -f "$OUTPUT_DIR/meeting_scenarios_filtered_iter_${iteration}.jsonl" ]]; then
        filtered_count=$(wc -l < "$OUTPUT_DIR/meeting_scenarios_filtered_iter_${iteration}.jsonl" | tr -d ' ')
        print_success "Iteration $iteration: Filtered $filtered_count high-quality responses"
    else
        print_warning "Iteration $iteration: No filtered responses generated"
    fi
done

# Step 5: Prepare final SFT dataset
print_step "Step 5: Preparing SFT training dataset"

# Combine all high-quality responses (macOS compatible)
if ls "$OUTPUT_DIR"/meeting_scenarios_filtered_iter_*.jsonl 1> /dev/null 2>&1; then
    cat "$OUTPUT_DIR"/meeting_scenarios_filtered_iter_*.jsonl > "$OUTPUT_DIR/meeting_prep_combined_filtered.jsonl"
    print_success "Combined filtered responses"
else
    print_warning "No filtered responses found to combine"
    touch "$OUTPUT_DIR/meeting_prep_combined_filtered.jsonl"
fi

python prepare_meeting_prep_sft_data.py \
  --data_path "$OUTPUT_DIR/meeting_prep_combined_filtered.jsonl" \
  --output_path "$OUTPUT_DIR/meeting_prep_sft_training.jsonl" \
  --tokenizer_path "$MODEL_PATH" \
  --min_quality_score 0.7 \
  --max_examples 10000 \
  --format chat

# Step 6: Golden prompt evaluation
print_step "Step 6: Evaluating against golden prompts"

# Create golden prompts scenarios file
python3 << 'EOF'
import json
import sys
import os

# Add current directory to path for imports
sys.path.append('.')

try:
    from meeting_prep_golden_prompts import GOLDEN_PROMPTS
    
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
    output_dir = os.environ.get('OUTPUT_DIR', 'meeting_prep_data')
    with open(f'{output_dir}/golden_prompts_scenarios.jsonl', 'w') as f:
        for scenario in golden_scenarios:
            f.write(json.dumps(scenario) + '\n')
    
    print(f"Created {len(golden_scenarios)} golden prompt scenarios")
    
except ImportError as e:
    print(f"Warning: Could not import golden prompts: {e}")
    # Create empty file to continue pipeline
    output_dir = os.environ.get('OUTPUT_DIR', 'meeting_prep_data')
    with open(f'{output_dir}/golden_prompts_scenarios.jsonl', 'w') as f:
        pass
except Exception as e:
    print(f"Error creating golden prompts: {e}")
    sys.exit(1)
EOF

if [[ -f "$OUTPUT_DIR/golden_prompts_scenarios.jsonl" && -s "$OUTPUT_DIR/golden_prompts_scenarios.jsonl" ]]; then
    python meeting_prep_inference.py \
      --data_path "$OUTPUT_DIR/golden_prompts_scenarios.jsonl" \
      --output_path "$OUTPUT_DIR/golden_prompts_responses.jsonl" \
      --model_path "$MODEL_PATH" \
      --num_responses_per_scenario 1 \
      --seed "$SEED" \
      --temperature 0.6 \
      --n_gpus "$N_GPUS"

    python meeting_prep_evaluation.py \
      --data_path "$OUTPUT_DIR/golden_prompts_responses.jsonl" \
      --output_path "$OUTPUT_DIR/golden_prompts_evaluation.json" \
      --action evaluate
    
    print_success "Completed golden prompt evaluation"
else
    print_warning "Skipping golden prompt evaluation (no scenarios created)"
fi

# Step 7: Generate summary statistics
print_step "Step 7: Generating summary statistics"

python3 << EOF
import json
import os

output_dir = '$OUTPUT_DIR'
print()
print('=' * 60)
print('MEETING PREPARATION DATA GENERATION SUMMARY')
print('=' * 60)

# Count scenarios
try:
    with open(f'{output_dir}/meeting_scenarios.jsonl', 'r') as f:
        num_scenarios = sum(1 for line in f)
    print(f'📋 Total scenarios generated: {num_scenarios}')
except:
    print('📋 Total scenarios generated: N/A')

# Count training examples
try:
    with open(f'{output_dir}/meeting_prep_sft_training.jsonl', 'r') as f:
        num_training = sum(1 for line in f)
    print(f'🎯 SFT training examples: {num_training}')
except:
    print('🎯 SFT training examples: N/A')

# Count training pairs
try:
    with open(f'{output_dir}/meeting_prep_training_pairs.jsonl', 'r') as f:
        num_pairs = sum(1 for line in f)
    print(f'🔄 Self-play training pairs: {num_pairs}')
except:
    print('🔄 Self-play training pairs: N/A')

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
            print(f'⭐ Average golden prompt score: {avg_golden_score:.3f}')
        else:
            print('⭐ Average golden prompt score: N/A')
    else:
        print('⭐ Average golden prompt score: N/A')
except:
    print('⭐ Average golden prompt score: N/A')

print()
print(f'📁 All outputs saved to: {output_dir}/')
print()
EOF

# Final success message
print_success "Pipeline Complete!"
echo ""
echo "📦 Generated datasets:"
echo "  • meeting_prep_sft_training.jsonl (for supervised fine-tuning)"  
echo "  • meeting_prep_training_pairs.jsonl (for self-play training)"
echo "  • golden_prompts_evaluation.json (evaluation results)"
echo ""
echo "🚀 To train a model:"
echo "  1. Use meeting_prep_sft_training.jsonl for initial SFT"
echo "  2. Use meeting_prep_training_pairs.jsonl for self-play/DPO training"
echo "  3. Evaluate using golden prompts for quality assessment"
echo ""
echo "💡 Tip: Set environment variables to customize:"
echo "   export MODEL_PATH='your/model/path'"
echo "   export N_GPUS=2"
echo "   export OUTPUT_DIR='custom/output/dir'"
echo ""