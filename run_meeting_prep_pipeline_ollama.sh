#!/usr/bin/env bash

# Meeting Preparation Data Generation Pipeline using Ollama
# macOS Compatible Version with Local Ollama Models
# Based on the PromptCoT 2.0 meeting prep adaptation

set -e  # Exit on any error
set -u  # Exit on undefined variable

# Configuration - using local Ollama models
OLLAMA_MODEL="${OLLAMA_MODEL:-qwen3:8b}"  # Default model, can be overridden
OLLAMA_HOST="${OLLAMA_HOST:-http://localhost:11434}"
SEED="${SEED:-42}"
TEMPERATURE="${TEMPERATURE:-0.8}"
OUTPUT_DIR="${OUTPUT_DIR:-meeting_prep_data_ollama}"
NUM_SCENARIOS="${NUM_SCENARIOS:-100}"  # Reduced for local processing
MAX_EXAMPLES="${MAX_EXAMPLES:-5000}"   # Reduced for local processing

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_info() {
    echo -e "${PURPLE}ℹ $1${NC}"
}

# Function to check if Ollama is running
check_ollama() {
    if ! curl -s "$OLLAMA_HOST/api/tags" > /dev/null 2>&1; then
        print_error "Ollama is not running or not accessible at $OLLAMA_HOST"
        echo "Please start Ollama with: ollama serve"
        exit 1
    fi
}

# Function to check if model is available
check_model() {
    local model=$1
    if ! ollama list | grep -q "^$model"; then
        print_error "Model '$model' not found in Ollama"
        echo "Available models:"
        ollama list
        echo ""
        echo "To pull the model: ollama pull $model"
        exit 1
    fi
}

# Function to test model with a simple prompt
test_model() {
    local model=$1
    print_info "Testing model $model..."
    
    local test_response=$(ollama generate "$model" "Hello! Please respond with 'Model working' if you can understand this." --format json 2>/dev/null | jq -r '.response' 2>/dev/null || echo "")
    
    if [[ -n "$test_response" ]]; then
        print_success "Model $model is responding correctly"
    else
        print_warning "Model $model test unclear, but proceeding..."
    fi
}

# Pre-flight checks
print_step "Pre-flight checks for Ollama Pipeline"

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    print_error "Ollama not found. Please install it from https://ollama.ai"
    exit 1
fi

print_success "Ollama is installed"

# Check if Ollama is running
check_ollama
print_success "Ollama service is running"

# Check if the specified model is available
check_model "$OLLAMA_MODEL"
print_success "Model $OLLAMA_MODEL is available"

# Test the model
test_model "$OLLAMA_MODEL"

# Check for required Python modules
if ! python -c "import requests, json" &> /dev/null; then
    print_error "Required Python modules not found. Install with: pip install requests"
    exit 1
fi

print_success "Python dependencies available"

# Check available disk space
available_space=$(df -h . | tail -1 | awk '{print $4}')
print_success "Available disk space: $available_space"

# Create output directory
if [[ ! -d "$OUTPUT_DIR" ]]; then
    mkdir -p "$OUTPUT_DIR"
    print_success "Created output directory: $OUTPUT_DIR"
else
    print_success "Using existing output directory: $OUTPUT_DIR"
fi

print_step "PromptCoT 2.0 Meeting Preparation Pipeline (Ollama)"
echo "Model: $OLLAMA_MODEL"
echo "Host: $OLLAMA_HOST"
echo "Output: $OUTPUT_DIR"
echo "Scenarios: $NUM_SCENARIOS"
echo "Seed: $SEED"
echo ""

# Step 1: Generate meeting scenarios using Ollama
print_step "Step 1: Generating meeting scenarios with Ollama"

python3 << 'EOF'
import requests
import json
import os
import random
import sys

# Configuration from environment
ollama_host = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
model = os.environ.get('OLLAMA_MODEL', 'qwen3:8b')
output_dir = os.environ.get('OUTPUT_DIR', 'meeting_prep_data_ollama')
num_scenarios = int(os.environ.get('NUM_SCENARIOS', '100'))
seed = int(os.environ.get('SEED', '42'))
temperature = float(os.environ.get('TEMPERATURE', '0.8'))

random.seed(seed)

def call_ollama(prompt, model, temperature=0.8):
    """Call Ollama API for text generation"""
    url = f"{ollama_host}/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 1024
        }
    }
    
    try:
        response = requests.post(url, json=data, timeout=120)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return ""

# Meeting types and contexts for scenario generation
meeting_types = [
    "Internal Cadence", "Strategic Planning", "Performance Evaluation",
    "External/Client", "Informational Broadcast", "Team Building",
    "Governance/Executive", "Project Kickoff", "Crisis Management",
    "Product Review", "Budget Planning", "Quarterly Business Review"
]

def generate_scenario_prompt():
    meeting_type = random.choice(meeting_types)
    
    prompt = f"""Generate a realistic enterprise meeting scenario for a {meeting_type} meeting.

Please provide a JSON response with the following structure:
{{
    "meeting_type": "{meeting_type}",
    "scenario": "Brief description of the meeting context and purpose",
    "participants": ["List of participant roles"],
    "stakes": "What's at risk or important about this meeting",
    "challenges": ["List of potential challenges or complexities"],
    "available_context": ["List of available information or resources"],
    "preparation_question": "A specific question someone might ask to prepare for this meeting"
}}

Make it realistic and specific to enterprise environments. Focus on practical business situations."""

    return prompt

print(f"Generating {num_scenarios} meeting scenarios...")

scenarios = []
for i in range(num_scenarios):
    if i % 10 == 0:
        print(f"Progress: {i}/{num_scenarios}")
    
    prompt = generate_scenario_prompt()
    response = call_ollama(prompt, model, temperature)
    
    try:
        # Try to extract JSON from response
        if '```json' in response:
            json_str = response.split('```json')[1].split('```')[0].strip()
        elif '{' in response:
            start = response.find('{')
            end = response.rfind('}') + 1
            json_str = response[start:end]
        else:
            continue
            
        scenario_data = json.loads(json_str)
        scenario_data['id'] = f"scenario_{i+1:04d}"
        scenarios.append(scenario_data)
        
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"Failed to parse scenario {i+1}: {e}")
        continue

print(f"Successfully generated {len(scenarios)} scenarios")

# Save scenarios
output_file = f"{output_dir}/meeting_scenarios.jsonl"
with open(output_file, 'w') as f:
    for scenario in scenarios:
        f.write(json.dumps(scenario) + '\n')

print(f"Scenarios saved to {output_file}")
EOF

if [[ -f "$OUTPUT_DIR/meeting_scenarios.jsonl" ]]; then
    scenario_count=$(wc -l < "$OUTPUT_DIR/meeting_scenarios.jsonl" | tr -d ' ')
    print_success "Generated $scenario_count scenarios"
else
    print_error "Failed to generate scenarios"
    exit 1
fi

# Step 2: Generate meeting preparation responses
print_step "Step 2: Generating meeting preparation responses"

python3 << 'EOF'
import requests
import json
import os
import random

# Configuration
ollama_host = os.environ.get('OLLAMA_HOST', 'http://localhost:11434')
model = os.environ.get('OLLAMA_MODEL', 'qwen3:8b')
output_dir = os.environ.get('OUTPUT_DIR', 'meeting_prep_data_ollama')
temperature = float(os.environ.get('TEMPERATURE', '0.7'))

def call_ollama(prompt, model, temperature=0.7):
    """Call Ollama API for text generation"""
    url = f"{ollama_host}/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": 2048
        }
    }
    
    try:
        response = requests.post(url, json=data, timeout=180)
        response.raise_for_status()
        return response.json()['response']
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        return ""

def create_meeting_prep_prompt(scenario):
    prompt = f"""You are an expert executive assistant helping someone prepare for an important meeting.

MEETING DETAILS:
Type: {scenario['meeting_type']}
Scenario: {scenario['scenario']}
Participants: {', '.join(scenario['participants'])}
Stakes: {scenario['stakes']}
Challenges: {', '.join(scenario['challenges'])}
Available Context: {', '.join(scenario['available_context'])}

PREPARATION QUESTION: {scenario['preparation_question']}

Please provide a comprehensive meeting preparation response that includes:

1. OBJECTIVES CLARITY
   - Clear statement of meeting goals
   - Key outcomes expected

2. AGENDA STRUCTURE
   - Recommended agenda items
   - Time allocation suggestions

3. STAKEHOLDER ANALYSIS
   - Key participants and their interests
   - Potential concerns or objections

4. CONTENT PREPARATION
   - Key talking points
   - Supporting data/materials needed
   - Potential questions to expect

5. RISK MITIGATION
   - Potential challenges and how to address them
   - Contingency plans

6. ACTIONABILITY
   - Specific next steps
   - Decision points

7. FOLLOW-UP PLANNING
   - Post-meeting actions
   - Communication plans

Provide practical, actionable advice that demonstrates deep understanding of enterprise meeting dynamics."""

    return prompt

# Load scenarios
scenarios_file = f"{output_dir}/meeting_scenarios.jsonl"
scenarios = []
with open(scenarios_file, 'r') as f:
    for line in f:
        scenarios.append(json.loads(line.strip()))

print(f"Processing {len(scenarios)} scenarios for response generation...")

# Generate responses for each scenario
processed_scenarios = []
for i, scenario in enumerate(scenarios):
    if i % 5 == 0:
        print(f"Progress: {i}/{len(scenarios)}")
    
    # Generate multiple responses per scenario
    scenario_with_responses = scenario.copy()
    scenario_with_responses['responses'] = []
    
    for response_idx in range(2):  # Generate 2 responses per scenario
        prompt = create_meeting_prep_prompt(scenario)
        response_text = call_ollama(prompt, model, temperature + (response_idx * 0.1))
        
        if response_text:
            response_data = {
                'response_id': f"{scenario['id']}_response_{response_idx+1}",
                'response_text': response_text,
                'model': model,
                'temperature': temperature + (response_idx * 0.1)
            }
            scenario_with_responses['responses'].append(response_data)
    
    if scenario_with_responses['responses']:
        processed_scenarios.append(scenario_with_responses)

print(f"Generated responses for {len(processed_scenarios)} scenarios")

# Save scenarios with responses
output_file = f"{output_dir}/meeting_scenarios_with_responses.jsonl"
with open(output_file, 'w') as f:
    for scenario in processed_scenarios:
        f.write(json.dumps(scenario) + '\n')

print(f"Scenarios with responses saved to {output_file}")
EOF

if [[ -f "$OUTPUT_DIR/meeting_scenarios_with_responses.jsonl" ]]; then
    print_success "Generated meeting preparation responses"
else
    print_error "Failed to generate responses"
    exit 1
fi

# Step 3: Basic evaluation and filtering
print_step "Step 3: Evaluating and filtering responses"

python3 << 'EOF'
import json
import os
import re
import random

# Configuration
output_dir = os.environ.get('OUTPUT_DIR', 'meeting_prep_data_ollama')

def evaluate_response_quality(response_text):
    """Simple quality evaluation based on content structure and completeness"""
    score = 0.0
    max_score = 7.0  # 7 categories
    
    # Check for key sections
    sections = [
        'objectives', 'agenda', 'stakeholder', 'content', 
        'risk', 'action', 'follow'
    ]
    
    text_lower = response_text.lower()
    
    for section in sections:
        if section in text_lower:
            score += 1.0
    
    # Bonus for structure and detail
    if len(response_text) > 500:
        score += 0.5
    if len(response_text.split('\n')) > 10:
        score += 0.5
    
    # Normalize score
    return min(score / max_score, 1.0)

# Load scenarios with responses
input_file = f"{output_dir}/meeting_scenarios_with_responses.jsonl"
scenarios = []
with open(input_file, 'r') as f:
    for line in f:
        scenarios.append(json.loads(line.strip()))

print(f"Evaluating {len(scenarios)} scenarios...")

# Evaluate and create training pairs
evaluated_scenarios = []
training_pairs = []

for scenario in scenarios:
    scenario_eval = scenario.copy()
    scenario_eval['response_evaluations'] = []
    
    for response in scenario['responses']:
        quality_score = evaluate_response_quality(response['response_text'])
        
        response_eval = response.copy()
        response_eval['quality_score'] = quality_score
        response_eval['evaluation'] = {
            'overall_score': quality_score,
            'length': len(response['response_text']),
            'structure_score': min(len(response['response_text'].split('\n')) / 20.0, 1.0)
        }
        
        scenario_eval['response_evaluations'].append(response_eval)
    
    # Sort responses by quality
    scenario_eval['response_evaluations'].sort(key=lambda x: x['quality_score'], reverse=True)
    
    # Create training pairs (best vs worst if we have multiple responses)
    if len(scenario_eval['response_evaluations']) >= 2:
        best_response = scenario_eval['response_evaluations'][0]
        worst_response = scenario_eval['response_evaluations'][-1]
        
        if best_response['quality_score'] > worst_response['quality_score']:
            training_pair = {
                'scenario': scenario,
                'chosen': best_response,
                'rejected': worst_response,
                'score_difference': best_response['quality_score'] - worst_response['quality_score']
            }
            training_pairs.append(training_pair)
    
    evaluated_scenarios.append(scenario_eval)

print(f"Created {len(training_pairs)} training pairs")

# Save evaluated scenarios
eval_file = f"{output_dir}/meeting_scenarios_evaluated.jsonl"
with open(eval_file, 'w') as f:
    for scenario in evaluated_scenarios:
        f.write(json.dumps(scenario) + '\n')

# Save training pairs
pairs_file = f"{output_dir}/meeting_prep_training_pairs.jsonl"
with open(pairs_file, 'w') as f:
    for pair in training_pairs:
        f.write(json.dumps(pair) + '\n')

print(f"Evaluation complete. Files saved:")
print(f"  - {eval_file}")
print(f"  - {pairs_file}")
EOF

# Step 4: Prepare final training dataset
print_step "Step 4: Preparing final training dataset"

python3 << 'EOF'
import json
import os

# Configuration
output_dir = os.environ.get('OUTPUT_DIR', 'meeting_prep_data_ollama')
max_examples = int(os.environ.get('MAX_EXAMPLES', '5000'))

# Load evaluated scenarios
eval_file = f"{output_dir}/meeting_scenarios_evaluated.jsonl"
scenarios = []
with open(eval_file, 'r') as f:
    for line in f:
        scenarios.append(json.loads(line.strip()))

# Collect high-quality responses for SFT
sft_examples = []
min_quality_threshold = 0.6

for scenario in scenarios:
    for response_eval in scenario['response_evaluations']:
        if response_eval['quality_score'] >= min_quality_threshold:
            # Create chat format for SFT
            prompt = f"""You are an expert executive assistant helping someone prepare for an important meeting.

MEETING DETAILS:
Type: {scenario['meeting_type']}
Scenario: {scenario['scenario']}
Participants: {', '.join(scenario['participants'])}
Stakes: {scenario['stakes']}
Challenges: {', '.join(scenario['challenges'])}
Available Context: {', '.join(scenario['available_context'])}

PREPARATION QUESTION: {scenario['preparation_question']}

Please provide a comprehensive meeting preparation response."""

            sft_example = {
                'messages': [
                    {'role': 'user', 'content': prompt},
                    {'role': 'assistant', 'content': response_eval['response_text']}
                ],
                'quality_score': response_eval['quality_score'],
                'scenario_id': scenario['id'],
                'response_id': response_eval['response_id']
            }
            sft_examples.append(sft_example)

# Sort by quality and limit examples
sft_examples.sort(key=lambda x: x['quality_score'], reverse=True)
sft_examples = sft_examples[:max_examples]

print(f"Prepared {len(sft_examples)} SFT training examples")

# Save SFT dataset
sft_file = f"{output_dir}/meeting_prep_sft_training.jsonl"
with open(sft_file, 'w') as f:
    for example in sft_examples:
        f.write(json.dumps(example) + '\n')

print(f"SFT training data saved to {sft_file}")
EOF

# Step 5: Generate summary statistics
print_step "Step 5: Generating summary statistics"

python3 << 'EOF'
import json
import os

output_dir = os.environ.get('OUTPUT_DIR', 'meeting_prep_data_ollama')

print()
print('=' * 70)
print('OLLAMA MEETING PREPARATION DATA GENERATION SUMMARY')
print('=' * 70)

# Count scenarios
try:
    with open(f'{output_dir}/meeting_scenarios.jsonl', 'r') as f:
        scenarios = [json.loads(line) for line in f]
    print(f'📋 Total scenarios generated: {len(scenarios)}')
    
    # Meeting type distribution
    meeting_types = {}
    for scenario in scenarios:
        mt = scenario.get('meeting_type', 'Unknown')
        meeting_types[mt] = meeting_types.get(mt, 0) + 1
    
    print('\n📊 Meeting Type Distribution:')
    for mt, count in sorted(meeting_types.items()):
        print(f'   {mt}: {count}')
        
except Exception as e:
    print(f'📋 Total scenarios generated: Error - {e}')

# Count training examples
try:
    with open(f'{output_dir}/meeting_prep_sft_training.jsonl', 'r') as f:
        training_examples = [json.loads(line) for line in f]
    print(f'\n🎯 SFT training examples: {len(training_examples)}')
    
    # Quality distribution
    quality_scores = [ex['quality_score'] for ex in training_examples]
    avg_quality = sum(quality_scores) / len(quality_scores)
    print(f'📈 Average quality score: {avg_quality:.3f}')
    print(f'📈 Quality range: {min(quality_scores):.3f} - {max(quality_scores):.3f}')
    
except Exception as e:
    print(f'🎯 SFT training examples: Error - {e}')

# Count training pairs
try:
    with open(f'{output_dir}/meeting_prep_training_pairs.jsonl', 'r') as f:
        training_pairs = [json.loads(line) for line in f]
    print(f'🔄 Self-play training pairs: {len(training_pairs)}')
    
    if training_pairs:
        score_diffs = [pair['score_difference'] for pair in training_pairs]
        avg_diff = sum(score_diffs) / len(score_diffs)
        print(f'📊 Average score difference: {avg_diff:.3f}')
        
except Exception as e:
    print(f'🔄 Self-play training pairs: Error - {e}')

print(f'\n📁 All outputs saved to: {output_dir}/')
print()
EOF

# Final success message
print_success "Ollama Pipeline Complete!"
echo ""
echo "🎉 Generated datasets using local Ollama model: $OLLAMA_MODEL"
echo ""
echo "📦 Generated files:"
echo "  • meeting_scenarios.jsonl - Generated meeting scenarios"
echo "  • meeting_scenarios_with_responses.jsonl - Scenarios with responses"  
echo "  • meeting_scenarios_evaluated.jsonl - Evaluated responses"
echo "  • meeting_prep_sft_training.jsonl - For supervised fine-tuning"
echo "  • meeting_prep_training_pairs.jsonl - For preference learning"
echo ""
echo "🚀 Next steps:"
echo "  1. Review the generated data quality"
echo "  2. Use meeting_prep_sft_training.jsonl for fine-tuning"
echo "  3. Use training_pairs.jsonl for DPO/preference learning"
echo ""
echo "💡 To use a different model:"
echo "   export OLLAMA_MODEL='gpt-oss:20b'  # or any other available model"
echo "   ./run_meeting_prep_pipeline_ollama.sh"
echo ""
echo "🔧 To generate more data:"
echo "   export NUM_SCENARIOS=500"
echo "   export MAX_EXAMPLES=10000"
echo "   ./run_meeting_prep_pipeline_ollama.sh"
echo ""