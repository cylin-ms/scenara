# PromptCoT 2.0 for Meeting Preparation

This directory contains the adapted PromptCoT 2.0 framework for generating training data for meeting preparation AI assistants, based on the comprehensive adaptation plan detailed in the meeting prep document.

## Overview

The meeting preparation adaptation leverages PromptCoT 2.0's self-training framework to automatically generate diverse, high-quality training data for enterprise meeting preparation scenarios. Unlike math or coding problems, meeting prep requires handling open-ended tasks without verifiable solutions, so we use rubric-based evaluation and the GUTT (Generalized Unit Task Template) framework.

## Key Components

### 1. Meeting Taxonomy (`meeting_prep_taxonomy.py`)
- Comprehensive taxonomy covering enterprise meeting types
- Categories: Internal Cadence, Strategic Planning, Performance Evaluation, External/Client, Informational Broadcast, Team Building, Governance/Executive
- Includes meeting challenges and available context for realistic scenario generation

### 2. Scenario Generation (`meeting_scenario_generation.py`)
- Generates realistic meeting scenarios using taxonomy
- Creates detailed contexts with participants, stakes, challenges, and available resources
- Produces specific preparation questions for each scenario

### 3. Response Generation (`meeting_prep_inference.py`, `meeting_prep_self_play.py`)
- Generates comprehensive meeting preparation responses
- Supports both single-shot generation and self-play iterations
- Uses structured prompts to ensure comprehensive coverage

### 4. Evaluation Framework (`meeting_prep_evaluation.py`)
- Rubric-based evaluation system adapted for meeting prep domain
- Evaluates responses on: objectives clarity, agenda structure, stakeholder analysis, content preparation, risk mitigation, actionability, follow-up planning
- Meeting-type-specific rubrics for specialized scenarios (client pitch, performance review, board meeting)

### 5. Self-Play Evaluation (`meeting_prep_self_play_eval.py`)
- Assigns rewards based on quality scores
- Creates chosen vs rejected pairs for preference learning
- Implements the E-step of the EM loop for self-improvement

### 6. Golden Prompts (`meeting_prep_golden_prompts.py`)
- GUTT-based evaluation framework with high-value scenarios
- Golden prompts derived from real user pain points
- Used for benchmarking and quality assessment

### 7. Data Preparation (`prepare_meeting_prep_sft_data.py`)
- Prepares filtered high-quality responses for supervised fine-tuning
- Multiple output formats: chat, completion, simple
- Token length filtering and quality score thresholds

## Usage

### Quick Start

1. Install dependencies:
```bash
pip install -r requirements_meeting_prep.txt
```

2. Run the complete pipeline:
```bash
bash run_meeting_prep_pipeline.sh
```

### Step-by-Step Process

1. **Generate Meeting Scenarios**:
```bash
python meeting_scenario_generation.py \
  --model_path Qwen/Qwen3-32B-Instruct \
  --output_path meeting_scenarios.jsonl \
  --num_scenarios 500 \
  --n_gpus 4
```

2. **Generate Initial Responses**:
```bash
python meeting_prep_inference.py \
  --data_path meeting_scenarios.jsonl \
  --output_path meeting_scenarios_with_responses.jsonl \
  --model_path Qwen/Qwen3-32B-Instruct \
  --num_responses_per_scenario 4
```

3. **Evaluate and Filter**:
```bash
python meeting_prep_self_play_eval.py \
  --data_path meeting_scenarios_with_responses.jsonl \
  --output_path meeting_scenarios_evaluated.jsonl \
  --pairs_output training_pairs.jsonl
```

4. **Self-Play Iterations** (EM Loop):
```bash
python meeting_prep_self_play.py \
  --data_path meeting_scenarios.jsonl \
  --output_path meeting_scenarios_selfplay.jsonl \
  --model_path Qwen/Qwen3-32B-Instruct \
  --num_completions 6
```

5. **Prepare Training Data**:
```bash
python prepare_meeting_prep_sft_data.py \
  --data_path meeting_scenarios_evaluated.jsonl \
  --output_path sft_training.jsonl \
  --tokenizer_path Qwen/Qwen3-32B-Instruct \
  --format chat
```

## Key Adaptations from Original PromptCoT

### 1. Domain-Specific Taxonomy
- Replaced math/code problem types with enterprise meeting categories
- Added contextual factors (stakes, participants, challenges) 
- Incorporated available information/resources for realistic preparation

### 2. Rubric-Based Evaluation
- Replaced binary correctness with multi-dimensional quality rubrics
- Domain-specific evaluation criteria for different meeting types
- Automated scoring combined with structured assessment

### 3. Open-Ended Response Handling
- Modified generation prompts for comprehensive preparation guidance
- Added constraints to avoid generic advice and ensure specificity
- Incorporated enterprise context and safety considerations

### 4. GUTT Framework Integration
- Golden prompts for high-value scenarios
- Template-based prompt generation for coverage
- Continuous evaluation against user-derived benchmarks

## Output Data Formats

### SFT Training Data
```json
{
  "messages": [
    {"role": "user", "content": "Meeting scenario and preparation question"},
    {"role": "assistant", "content": "Comprehensive preparation response"}
  ],
  "quality_score": 0.85,
  "meeting_type": "Quarterly Business Review",
  "stakes": "extremely high"
}
```

### Self-Play Training Pairs
```json
{
  "prompt": "Meeting scenario and preparation question",
  "chosen": "High-quality preparation response",
  "rejected": "Lower-quality preparation response", 
  "chosen_score": 0.85,
  "rejected_score": 0.62,
  "score_difference": 0.23
}
```

## Evaluation Metrics

- **Overall Quality Score**: Weighted average across all rubric dimensions
- **Coverage Score**: Percentage of expected elements included
- **Specificity Score**: Avoidance of generic advice, inclusion of context-specific details
- **Actionability Score**: Presence of concrete, executable steps
- **Golden Prompt Performance**: Evaluation against high-value benchmark scenarios

## Expected Results

Based on the adaptation framework, this approach should produce:

1. **Diverse Training Data**: 500+ realistic meeting scenarios across all enterprise categories
2. **High-Quality Responses**: Filtered dataset with 70%+ quality scores
3. **Self-Improving Loop**: Progressive quality improvement over EM iterations
4. **Enterprise-Ready**: Outputs tailored to real workplace scenarios and constraints

The resulting models should provide meeting preparation advice comparable to expert human assistants, with coverage across the full spectrum of enterprise meeting types and situations.

## Files Overview

- `meeting_prep_taxonomy.py` - Meeting type definitions and scenario components
- `meeting_scenario_generation.py` - Generate realistic meeting scenarios  
- `meeting_prep_inference.py` - Generate preparation responses
- `meeting_prep_self_play.py` - Self-play response generation with multi-processing
- `meeting_prep_evaluation.py` - Rubric-based response evaluation
- `meeting_prep_self_play_eval.py` - Reward assignment and training pair creation
- `prepare_meeting_prep_sft_data.py` - Format data for supervised fine-tuning
- `meeting_prep_golden_prompts.py` - Golden prompts and GUTT framework
- `run_meeting_prep_pipeline.sh` - Complete end-to-end pipeline
- `requirements_meeting_prep.txt` - Additional dependencies needed

This adaptation demonstrates how PromptCoT 2.0's powerful data generation and self-improvement framework can be extended beyond mathematical reasoning to practical business intelligence tasks.