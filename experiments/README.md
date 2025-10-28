# Meeting Classification Experiments

## Experiment Structure

All classification experiments are organized by date in this directory structure:

```
experiments/
└── YYYY-MM-DD/           # Date when experiment was conducted
    ├── meeting_classification_[model_name].json    # Classification results
    └── experiment_notes.md                         # Optional notes
```

## Experiment Naming Convention

Classification result files follow this pattern:
```
meeting_classification_[classifier]_[model].json
```

Examples:
- `meeting_classification_github_copilot_gpt4.json` - GitHub Copilot (GPT-4 Turbo)
- `meeting_classification_gpt5.json` - Microsoft GPT-5 (dev-gpt-5-chat-jj)
- `meeting_classification_ollama_gptoss20b.json` - Ollama local (gpt-oss:20b)
- `meeting_classification_gpt4o.json` - Azure OpenAI GPT-4o

## Experiment Metadata

Each experiment file contains:

### Experiment Section
- `experiment_id`: Unique identifier (e.g., meeting_classification_20251028_001)
- `experiment_type`: Type of experiment (meeting_classification)
- `run_date`: When the experiment was conducted
- `platform`: Platform used (Windows DevBox, macOS, etc.)
- `description`: Brief description of the experiment

### Classifier Details
- `name`: Classifier name (GitHub Copilot, GPT-5, etc.)
- `model`: Specific model used (GPT-4 Turbo, dev-gpt-5-chat-jj, etc.)
- `model_version`: Version information
- `provider`: Service provider (Microsoft Azure OpenAI, etc.)
- `deployment`: Deployment type
- `capabilities`: List of classifier capabilities

## Current Experiments

### 2025-10-28

#### Experiment 001: GitHub Copilot GPT-4 Classification
- **File**: `meeting_classification_github_copilot_gpt4.json`
- **Classifier**: GitHub Copilot (GPT-4 Turbo)
- **Meetings Classified**: 8 meetings
- **Average Confidence**: 93%
- **Key Finding**: GitHub Copilot provides high-quality classifications without requiring external API authentication
- **Advantages**:
  - No authentication overhead (MSAL, tokens, etc.)
  - Direct context access to full meeting data
  - Consistent reasoning and confidence scores
  - Extended context window for complex meetings
  
## Running Classification Experiments

### Option 1: GitHub Copilot (Recommended for quick tests)
```python
# Just ask GitHub Copilot to classify meetings directly
# Example: "classify today's meetings using your LLM capabilities"
```

### Option 2: GPT-5 (Windows DevBox)
```bash
python classify_todays_meetings.py --classifier gpt5
```

### Option 3: Ollama (macOS)
```bash
python classify_todays_meetings.py --classifier ollama --model gpt-oss:20b
```

### Option 4: GPT-4o (Azure OpenAI)
```bash
python classify_todays_meetings.py --classifier gpt4o
```

## Comparing Experiments

To compare different classifier results:

```python
import json

# Load multiple experiment results
with open('experiments/2025-10-28/meeting_classification_github_copilot_gpt4.json') as f:
    copilot_results = json.load(f)

with open('experiments/2025-10-28/meeting_classification_gpt5.json') as f:
    gpt5_results = json.load(f)

# Compare classifications, confidence scores, reasoning quality
```

## Best Practices

1. **Date-based Organization**: Always save experiments in date-specific directories
2. **Model Documentation**: Include detailed model information in metadata
3. **Reproducibility**: Document platform, model version, and input source
4. **Comparison Testing**: Run same meetings through multiple classifiers
5. **Notes**: Add experiment_notes.md for observations and insights

## Taxonomy

All experiments use the **Enterprise Meeting Taxonomy v3.0**:

**Categories**:
- Strategic Planning & Decision (7 types)
- Team Coordination & Status (8 types)
- Performance & Review (6 types)
- Learning & Development (5 types)
- Administrative & HR (5+ types)

## Future Experiments

Potential areas for future experiments:
- Cross-platform comparison (Windows vs macOS)
- Model comparison (GPT-5 vs GPT-4 vs Ollama)
- Confidence calibration across models
- Multi-language meeting classification
- Real-time vs batch classification performance
