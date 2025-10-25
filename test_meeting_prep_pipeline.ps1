# Simple test script for meeting prep pipeline
# Tests basic functionality before running the full pipeline

param(
    [string]$ModelPath = "microsoft/phi-2",
    [string]$OutputDir = "meeting_prep_test"
)

Write-Host "=== Testing Meeting Prep Pipeline Components ===" -ForegroundColor Green

# Create test output directory
if (-not (Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

# Test 1: Basic model access
Write-Host "Test 1: Testing model access..." -ForegroundColor Yellow
python test_model_access.py --model_path $ModelPath

if ($LASTEXITCODE -ne 0) {
    Write-Error "Model access test failed"
    exit 1
}

# Test 2: Generate a small number of scenarios
Write-Host "Test 2: Generating 5 test scenarios..." -ForegroundColor Yellow
python meeting_scenario_generation_transformers.py `
  --model_path $ModelPath `
  --output_path "$OutputDir/test_scenarios.jsonl" `
  --num_scenarios 5 `
  --seed 42 `
  --temperature 0.8 `
  --use_chat_template

if ($LASTEXITCODE -ne 0) {
    Write-Error "Scenario generation test failed"
    exit 1
}

# Test 3: Generate responses for the scenarios
Write-Host "Test 3: Generating responses for test scenarios..." -ForegroundColor Yellow
python meeting_prep_inference_transformers.py `
  --data_path "$OutputDir/test_scenarios.jsonl" `
  --output_path "$OutputDir/test_responses.jsonl" `
  --model_path $ModelPath `
  --num_responses_per_scenario 2 `
  --seed 42 `
  --temperature 0.7 `
  --use_chat_template

if ($LASTEXITCODE -ne 0) {
    Write-Error "Response generation test failed"
    exit 1
}

# Test 4: Evaluate responses
Write-Host "Test 4: Evaluating responses..." -ForegroundColor Yellow
python meeting_prep_self_play_eval.py `
  --data_path "$OutputDir/test_responses.jsonl" `
  --output_path "$OutputDir/test_evaluated.jsonl" `
  --min_quality_score 0.5

if ($LASTEXITCODE -ne 0) {
    Write-Error "Evaluation test failed"
    exit 1
}

# Test 5: Check outputs
Write-Host "Test 5: Checking generated outputs..." -ForegroundColor Yellow
python -c @"
import json
import os

output_dir = '$OutputDir'
print('=== TEST RESULTS ===')

# Check scenarios
scenarios_file = f'{output_dir}/test_scenarios.jsonl'
if os.path.exists(scenarios_file):
    with open(scenarios_file, 'r', encoding='utf-8') as f:
        scenarios = [json.loads(line) for line in f]
    print(f'✓ Generated {len(scenarios)} scenarios')
    
    if scenarios:
        print(f'  Sample scenario: {scenarios[0].get("meeting_type", "Unknown")}')
else:
    print('✗ No scenarios file found')

# Check responses
responses_file = f'{output_dir}/test_responses.jsonl'
if os.path.exists(responses_file):
    with open(responses_file, 'r', encoding='utf-8') as f:
        responses = [json.loads(line) for line in f]
    print(f'✓ Generated responses for {len(responses)} scenarios')
    
    total_responses = sum(len(item.get('responses', [])) for item in responses)
    print(f'  Total responses: {total_responses}')
else:
    print('✗ No responses file found')

# Check evaluations
eval_file = f'{output_dir}/test_evaluated.jsonl'
if os.path.exists(eval_file):
    with open(eval_file, 'r', encoding='utf-8') as f:
        evaluations = [json.loads(line) for line in f]
    print(f'✓ Evaluated {len(evaluations)} scenarios')
    
    # Calculate average quality score
    all_scores = []
    for item in evaluations:
        for response in item.get('responses', []):
            score = response.get('quality_score', 0)
            if score > 0:
                all_scores.append(score)
    
    if all_scores:
        avg_score = sum(all_scores) / len(all_scores)
        print(f'  Average quality score: {avg_score:.3f}')
    else:
        print('  No quality scores found')
else:
    print('✗ No evaluation file found')

print(f'\nTest files saved to: {output_dir}/')
"@

Write-Host ""
Write-Host "=== Test Complete! ===" -ForegroundColor Green

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All tests passed! You can now run the full pipeline with:" -ForegroundColor Green
    Write-Host "  .\run_meeting_prep_pipeline.ps1 -ModelPath $ModelPath" -ForegroundColor White
} else {
    Write-Host "✗ Some tests failed. Check the error messages above." -ForegroundColor Red
}