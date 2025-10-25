# Meeting Preparation Data Generation Pipeline using adapted PromptCoT 2.0
# PowerShell version for Windows
# Based on the meeting prep adaptation document

param(
    [string]$ModelPath = "microsoft/phi-2",
    [int]$NGpus = 1,
    [int]$Seed = 42,
    [double]$Temperature = 0.8,
    [string]$OutputDir = "meeting_prep_data"
)

# Create output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

Write-Host "=== PromptCoT 2.0 Meeting Preparation Data Generation Pipeline ===" -ForegroundColor Green

# Step 1: Generate meeting scenarios
Write-Host "Step 1: Generating meeting scenarios..." -ForegroundColor Yellow
python meeting_scenario_generation.py `
  --model_path $ModelPath `
  --output_path "$OutputDir/meeting_scenarios.jsonl" `
  --num_scenarios 500 `
  --seed $Seed `
  --temperature $Temperature `
  --n_gpus $NGpus `
  --use_chat_template true

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to generate meeting scenarios"
    exit 1
}

# Step 2: Generate initial responses (cold start data)
Write-Host "Step 2: Generating initial meeting preparation responses..." -ForegroundColor Yellow
python meeting_prep_inference.py `
  --data_path "$OutputDir/meeting_scenarios.jsonl" `
  --output_path "$OutputDir/meeting_scenarios_with_responses.jsonl" `
  --model_path $ModelPath `
  --num_responses_per_scenario 4 `
  --batch_size 16 `
  --seed $Seed `
  --temperature 0.7 `
  --n_gpus $NGpus `
  --use_chat_template true

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to generate initial responses"
    exit 1
}

# Step 3: Evaluate responses and assign rewards (E-step)
Write-Host "Step 3: Evaluating responses and assigning rewards..." -ForegroundColor Yellow
python meeting_prep_self_play_eval.py `
  --data_path "$OutputDir/meeting_scenarios_with_responses.jsonl" `
  --output_path "$OutputDir/meeting_scenarios_evaluated.jsonl" `
  --pairs_output "$OutputDir/meeting_prep_training_pairs.jsonl" `
  --min_quality_score 0.6

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to evaluate responses"
    exit 1
}

# Step 4: Self-play iterations (EM loop)
Write-Host "Step 4: Starting EM self-training loop..." -ForegroundColor Yellow

for ($iteration = 1; $iteration -le 3; $iteration++) {
    Write-Host "=== Self-Play Iteration $iteration ===" -ForegroundColor Cyan
    
    # Generate more responses using current model
    Write-Host "Generating responses for iteration $iteration..." -ForegroundColor Yellow
    python meeting_prep_self_play.py `
      --data_path "$OutputDir/meeting_scenarios.jsonl" `
      --output_path "$OutputDir/meeting_scenarios_selfplay_iter_$iteration.jsonl" `
      --model_path $ModelPath `
      --num_completions 6 `
      --seed ($Seed + $iteration) `
      --temperature 0.8 `
      --n_gpus $NGpus `
      --num_splits 2 `
      --use_chat_template
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to generate responses for iteration $iteration"
        exit 1
    }
    
    # Evaluate new responses
    Write-Host "Evaluating responses for iteration $iteration..." -ForegroundColor Yellow
    python meeting_prep_self_play_eval.py `
      --data_path "$OutputDir/meeting_scenarios_selfplay_iter_$iteration.jsonl" `
      --output_path "$OutputDir/meeting_scenarios_evaluated_iter_$iteration.jsonl" `
      --pairs_output "$OutputDir/meeting_prep_training_pairs_iter_$iteration.jsonl" `
      --min_quality_score 0.6
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to evaluate responses for iteration $iteration"
        exit 1
    }
    
    # Filter high-quality responses for next iteration
    Write-Host "Filtering high-quality responses..." -ForegroundColor Yellow
    python meeting_prep_evaluation.py `
      --data_path "$OutputDir/meeting_scenarios_evaluated_iter_$iteration.jsonl" `
      --output_path "$OutputDir/meeting_scenarios_filtered_iter_$iteration.jsonl" `
      --action filter `
      --min_score 0.7
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to filter responses for iteration $iteration"
        exit 1
    }
}

# Step 5: Prepare final SFT dataset
Write-Host "Step 5: Preparing SFT training dataset..." -ForegroundColor Yellow

# Combine all high-quality responses
$filteredFiles = Get-ChildItem "$OutputDir/meeting_scenarios_filtered_iter_*.jsonl"
if ($filteredFiles) {
    $filteredFiles | Get-Content | Out-File "$OutputDir/meeting_prep_combined_filtered.jsonl" -Encoding utf8
} else {
    Write-Warning "No filtered files found for combining"
}

python prepare_meeting_prep_sft_data.py `
  --data_path "$OutputDir/meeting_prep_combined_filtered.jsonl" `
  --output_path "$OutputDir/meeting_prep_sft_training.jsonl" `
  --tokenizer_path $ModelPath `
  --min_quality_score 0.7 `
  --max_examples 10000 `
  --format chat

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to prepare SFT training data"
    exit 1
}

# Step 6: Golden prompt evaluation
Write-Host "Step 6: Evaluating against golden prompts..." -ForegroundColor Yellow

# Generate golden prompt scenarios
python -c @"
import json
import sys
sys.path.append('.')
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
with open('$OutputDir/golden_prompts_scenarios.jsonl', 'w', encoding='utf-8') as f:
    for scenario in golden_scenarios:
        f.write(json.dumps(scenario) + '\n')

print(f'Generated {len(golden_scenarios)} golden prompt scenarios')
"@

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to generate golden prompt scenarios"
    exit 1
}

python meeting_prep_inference.py `
  --data_path "$OutputDir/golden_prompts_scenarios.jsonl" `
  --output_path "$OutputDir/golden_prompts_responses.jsonl" `
  --model_path $ModelPath `
  --num_responses_per_scenario 1 `
  --seed $Seed `
  --temperature 0.6 `
  --n_gpus $NGpus

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to generate golden prompt responses"
    exit 1
}

python meeting_prep_evaluation.py `
  --data_path "$OutputDir/golden_prompts_responses.jsonl" `
  --output_path "$OutputDir/golden_prompts_evaluation.json" `
  --action evaluate

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to evaluate golden prompts"
    exit 1
}

# Step 7: Generate summary statistics
Write-Host "Step 7: Generating summary statistics..." -ForegroundColor Yellow

python -c @"
import json
import os

output_dir = '$OutputDir'
print('\n=== MEETING PREPARATION DATA GENERATION SUMMARY ===')

# Count scenarios
try:
    with open(f'{output_dir}/meeting_scenarios.jsonl', 'r', encoding='utf-8') as f:
        num_scenarios = sum(1 for line in f)
    print(f'Total scenarios generated: {num_scenarios}')
except Exception as e:
    print(f'Could not count scenarios: {e}')

# Count training examples
try:
    with open(f'{output_dir}/meeting_prep_sft_training.jsonl', 'r', encoding='utf-8') as f:
        num_training = sum(1 for line in f)
    print(f'SFT training examples: {num_training}')
except Exception as e:
    print(f'Could not count training examples: {e}')

# Count training pairs
try:
    with open(f'{output_dir}/meeting_prep_training_pairs.jsonl', 'r', encoding='utf-8') as f:
        num_pairs = sum(1 for line in f)
    print(f'Self-play training pairs: {num_pairs}')
except Exception as e:
    print(f'Could not count training pairs: {e}')

# Golden prompt performance
try:
    with open(f'{output_dir}/golden_prompts_evaluation.json', 'r', encoding='utf-8') as f:
        golden_results = json.load(f)
    
    if golden_results:
        scores = []
        for result in golden_results:
            for eval_data in result.get('response_evaluations', []):
                scores.append(eval_data.get('overall_score', 0))
        
        if scores:
            avg_golden_score = sum(scores) / len(scores)
            print(f'Average golden prompt score: {avg_golden_score:.3f}')
except Exception as e:
    print(f'Could not evaluate golden prompts: {e}')

print(f'\nAll outputs saved to: {output_dir}/')
"@

Write-Host ""
Write-Host "=== Pipeline Complete! ===" -ForegroundColor Green
Write-Host "Generated datasets:" -ForegroundColor White
Write-Host "  - meeting_prep_sft_training.jsonl (for supervised fine-tuning)" -ForegroundColor White
Write-Host "  - meeting_prep_training_pairs.jsonl (for self-play training)" -ForegroundColor White
Write-Host "  - golden_prompts_evaluation.json (evaluation results)" -ForegroundColor White
Write-Host ""
Write-Host "To train a model:" -ForegroundColor White
Write-Host "  1. Use meeting_prep_sft_training.jsonl for initial SFT" -ForegroundColor White
Write-Host "  2. Use meeting_prep_training_pairs.jsonl for self-play/DPO training" -ForegroundColor White
Write-Host "  3. Evaluate using golden prompts for quality assessment" -ForegroundColor White