# Quick Start: Meeting Classification Experiments

## Overview
This guide shows you how to run meeting classification experiments using different LLM models and save results for comparison.

## Experiment Directory Structure

```
experiments/
├── README.md                           # Experiment documentation
├── 2025-10-28/                        # Daily experiment directory
│   ├── meeting_classification_github_copilot_gpt4.json
│   ├── meeting_classification_gpt5.json (future)
│   └── meeting_classification_ollama_gptoss20b.json (future)
└── 2025-10-29/                        # Next day's experiments
    └── ...
```

## Quick Start Options

### Option 1: GitHub Copilot (Fastest - No Setup)

**Best for**: Quick tests, Windows/macOS, no authentication needed

Just ask GitHub Copilot in the chat:
```
"Classify today's meetings using your LLM capabilities"
```

**Advantages**:
- ✅ No API setup required
- ✅ No authentication complexity
- ✅ Direct access to meeting context
- ✅ High quality reasoning (93% avg confidence)
- ✅ Works on any platform

**Model Used**: GPT-4 Turbo (gpt-4-1106-preview)

---

### Option 2: GPT-5 (Windows DevBox Only)

**Best for**: Enterprise-grade classification, Windows DevBox environment

```bash
python classify_todays_meetings.py --classifier gpt5
```

**Requirements**:
- Windows DevBox with MSAL + Windows Broker (WAM)
- Access to Microsoft internal LLMAPI
- Scopes: `https://substrate.office.com/llmapi/LLMAPI.dev`

**Model Used**: dev-gpt-5-chat-jj
**Endpoint**: `https://fe-26.qas.bing.net/chat/completions`

---

### Option 3: Ollama (macOS)

**Best for**: Local processing, macOS development, offline work

```bash
python classify_todays_meetings.py --classifier ollama --model gpt-oss:20b
```

**Requirements**:
- Ollama installed (`brew install ollama`)
- Model downloaded (`ollama pull gpt-oss:20b`)
- Local API server running (`ollama serve`)

**Model Used**: gpt-oss:20b (local open-source model)

---

### Option 4: GPT-4o (Azure OpenAI)

**Best for**: Azure-integrated environments, fallback option

```bash
python classify_todays_meetings.py --classifier gpt4o
```

**Requirements**:
- Azure OpenAI subscription
- API key configured
- GPT-4o model deployment

**Model Used**: gpt-4o

---

## Running Your First Experiment

### Step 1: Extract Today's Meetings

```bash
# Windows DevBox
python get_todays_meetings.py

# macOS (alternative)
python3 get_todays_meetings.py
```

**Output**: `data/meetings/meetings_YYYY-MM-DD.json`

### Step 2: Run Classification

**Option A - GitHub Copilot (Recommended)**:
1. Open GitHub Copilot Chat
2. Say: "Classify today's meetings using your LLM capabilities"
3. Copilot will analyze and create experiment JSON automatically

**Option B - Command Line**:
```bash
python classify_todays_meetings.py --classifier [gpt5|ollama|gpt4o]
```

### Step 3: Review Results

Results are saved to:
```
experiments/YYYY-MM-DD/meeting_classification_[model].json
```

Each result includes:
- **Experiment metadata**: ID, date, platform, description
- **Classifier details**: Name, model, version, capabilities
- **Meeting classifications**: Type, category, confidence, reasoning
- **Summary statistics**: Averages, distributions, insights

### Step 4: Compare Results (Optional)

Run multiple classifiers on the same day:

```bash
# GitHub Copilot (in chat)
"Classify today's meetings"

# Then run GPT-5 (Windows DevBox)
python classify_todays_meetings.py --classifier gpt5

# Then run Ollama (macOS)
python classify_todays_meetings.py --classifier ollama
```

All results saved in `experiments/YYYY-MM-DD/` for comparison!

---

## Understanding Results

### Experiment Metadata
```json
{
  "experiment": {
    "experiment_id": "meeting_classification_20251028_001",
    "experiment_type": "meeting_classification",
    "run_date": "2025-10-28T14:00:00",
    "platform": "Windows DevBox"
  }
}
```

### Classifier Information
```json
{
  "classifier": {
    "name": "GitHub Copilot",
    "model": "GPT-4 Turbo",
    "model_version": "gpt-4-1106-preview",
    "provider": "Microsoft Azure OpenAI"
  }
}
```

### Classification Details
Each meeting gets:
- **Primary category**: Administrative & HR, Team Coordination, Strategic Planning, Learning & Development, Performance & Review
- **Specific type**: Interview, Status Update, Office Hours, etc.
- **Confidence score**: 0.0 to 1.0 (higher is better)
- **Reasoning**: Why this classification was chosen
- **Key indicators**: Evidence supporting the classification
- **Alternate classification**: Second-best option (if applicable)

### Summary Statistics
- Total meetings classified
- Distribution by category/type
- Average confidence score
- Total meeting time
- Key projects identified
- Collaboration insights

---

## Best Practices

### 1. Daily Organization
Create new directory for each day's experiments:
```
experiments/2025-10-28/
experiments/2025-10-29/
experiments/2025-10-30/
```

### 2. Descriptive Filenames
Include model name in filename:
```
meeting_classification_github_copilot_gpt4.json
meeting_classification_gpt5.json
meeting_classification_ollama_gptoss20b.json
```

### 3. Complete Metadata
Always include:
- Experiment ID
- Run date and time
- Platform (Windows DevBox, macOS, etc.)
- Full classifier details (model, version, provider)

### 4. Document Findings
Add notes about:
- Classification quality differences
- Model-specific strengths/weaknesses
- Performance observations
- Confidence score patterns

### 5. Cross-Platform Testing
Test same meetings on different platforms:
- Windows DevBox → GPT-5 or GitHub Copilot
- macOS → Ollama or GitHub Copilot

---

## Troubleshooting

### "No meetings found"
Run extraction first:
```bash
python get_todays_meetings.py
```

### Authentication errors (GPT-5)
Ensure Windows Broker is configured:
```python
# Check SilverFlow/model/llmapi-dev-gpt-5-chat-jj.py
# Verify MSAL authentication setup
```

### Ollama connection failed
Start Ollama server:
```bash
ollama serve
```

### GitHub Copilot not responding
Try being more specific:
```
"Classify the 8 meetings in data/meetings/meetings_2025-10-28.json 
using your LLM capabilities and save to experiments/2025-10-28/"
```

---

## Example Results

**Experiment 001 - October 28, 2025**:
- **Model**: GitHub Copilot GPT-4 Turbo
- **Meetings**: 8 total
- **Confidence**: 93% average
- **Distribution**: 
  - Administrative & HR: 2 meetings
  - Team Coordination: 2 meetings
  - Strategic Planning: 1 meeting
  - Learning & Development: 2 meetings
  - Performance & Review: 1 meeting
- **Total Time**: 7.6 hours
- **Key Finding**: 50% of meetings focused on Meeting Prep product

---

## Next Steps

1. **Run your first experiment** using GitHub Copilot
2. **Review the results** in `experiments/YYYY-MM-DD/`
3. **Try different models** for comparison
4. **Document insights** in experiment notes
5. **Compare accuracy** across models

For detailed documentation, see `experiments/README.md`
