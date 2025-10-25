# PromptCoT 2.0 Meeting Prep Pipeline - Ollama Version

This is a locally-runnable version of the PromptCoT 2.0 meeting preparation pipeline that uses **Ollama** for model inference. This eliminates the need for cloud APIs, GPU clusters, or complex model hosting setups.

## 🚀 Quick Start

### 1. Prerequisites

**Install Ollama:**
```bash
# macOS
brew install ollama
# Or download from https://ollama.ai

# Start Ollama service
ollama serve
```

**Pull a recommended model:**
```bash
# Fast, good quality (5.2GB)
ollama pull qwen3:8b

# Better quality, larger (13GB) 
ollama pull gpt-oss:20b

# High quality reasoning (9GB)
ollama pull deepseek-r1:14b
```

**Install Python dependencies:**
```bash
pip install requests
```

### 2. Test Your Setup

```bash
./test_ollama_environment.sh
```

This will verify:
- ✅ Ollama is installed and running
- ✅ Models are available
- ✅ Python dependencies are ready
- ✅ Model can respond to prompts

### 3. Run the Pipeline

**Quick demo (5 scenarios):**
```bash
export NUM_SCENARIOS=5
export OUTPUT_DIR="demo_ollama"
./run_meeting_prep_pipeline_ollama.sh
```

**Full pipeline (100 scenarios):**
```bash
./run_meeting_prep_pipeline_ollama.sh
```

**Custom configuration:**
```bash
export OLLAMA_MODEL="gpt-oss:20b"
export NUM_SCENARIOS=200
export MAX_EXAMPLES=10000
export OUTPUT_DIR="my_meeting_data"
./run_meeting_prep_pipeline_ollama.sh
```

## 🔧 Configuration Options

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_MODEL` | `qwen3:8b` | Model to use for generation |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama API endpoint |
| `NUM_SCENARIOS` | `100` | Number of meeting scenarios to generate |
| `MAX_EXAMPLES` | `5000` | Maximum training examples to create |
| `OUTPUT_DIR` | `meeting_prep_data_ollama` | Output directory |
| `SEED` | `42` | Random seed for reproducibility |
| `TEMPERATURE` | `0.8` | Generation temperature |

## 📊 Model Recommendations

### **For Development/Testing:**
- **`qwen3:8b`** (5.2GB) - Fast, good quality, efficient on most hardware
- **`deepseek-r1:1.5b`** (1.1GB) - Very fast, decent quality for prototyping

### **For Production:**
- **`gpt-oss:20b`** (13GB) - High quality, good reasoning
- **`deepseek-r1:14b`** (9GB) - Excellent reasoning, good for complex scenarios  
- **`gemma3:12b`** (8.1GB) - Balanced quality and performance

### **For Maximum Quality:**
- **`gpt-oss:120b`** (65GB) - Highest quality (requires significant RAM)
- **`mistral-small:24b`** (15-48GB) - Very high quality, multiple quantizations

## 🏗️ Pipeline Architecture

The Ollama pipeline consists of **4 main steps**:

### **Step 1: Scenario Generation**
- Generates realistic enterprise meeting scenarios
- Uses taxonomy of meeting types (QBR, Strategic Planning, etc.)
- Creates detailed contexts with participants, stakes, and challenges
- Output: `meeting_scenarios.jsonl`

### **Step 2: Response Generation** 
- Generates comprehensive meeting preparation responses
- Multiple responses per scenario for diversity
- Structured format covering 7 key areas (objectives, agenda, etc.)
- Output: `meeting_scenarios_with_responses.jsonl`

### **Step 3: Evaluation & Filtering**
- Quality assessment based on content structure and completeness
- Creates chosen vs. rejected pairs for preference learning
- Filters high-quality responses for training
- Output: `meeting_scenarios_evaluated.jsonl`, `meeting_prep_training_pairs.jsonl`

### **Step 4: Dataset Preparation**
- Formats data for supervised fine-tuning
- Chat format with user prompts and assistant responses  
- Quality scoring and ranking
- Output: `meeting_prep_sft_training.jsonl`

## 📈 Performance Expectations

**System Requirements:**
- **RAM:** 8GB+ (for 8B models), 16GB+ (for 20B models), 64GB+ (for 120B models)
- **Storage:** 10-100GB depending on model size
- **CPU:** Modern multi-core processor (Apple Silicon recommended for macOS)

**Generation Speed:**
- **qwen3:8b:** ~1-2 minutes per 10 scenarios
- **gpt-oss:20b:** ~3-5 minutes per 10 scenarios  
- **Total pipeline time:** 15-60 minutes for 100 scenarios

## 📂 Output Files

The pipeline generates several useful datasets:

### **Training Data:**
- **`meeting_prep_sft_training.jsonl`** - For supervised fine-tuning (chat format)
- **`meeting_prep_training_pairs.jsonl`** - For preference learning (DPO/RLHF)

### **Scenarios & Responses:**
- **`meeting_scenarios.jsonl`** - Generated meeting scenarios
- **`meeting_scenarios_with_responses.jsonl`** - Scenarios with generated responses
- **`meeting_scenarios_evaluated.jsonl`** - Quality-evaluated responses

### **Example Usage:**
```python
import json

# Load SFT training data
with open('meeting_prep_data_ollama/meeting_prep_sft_training.jsonl') as f:
    training_data = [json.loads(line) for line in f]

# Each example has this structure:
example = training_data[0]
print("User prompt:", example['messages'][0]['content'])
print("Assistant response:", example['messages'][1]['content'])
print("Quality score:", example['quality_score'])
```

## 🔍 Quality Assessment

The pipeline includes automated quality evaluation based on:

- **Content Structure:** Presence of all 7 required sections
- **Completeness:** Response length and detail level
- **Coherence:** Logical flow and enterprise relevance

**Quality Scores:**
- **0.8-1.0:** Excellent - comprehensive, well-structured responses
- **0.6-0.8:** Good - solid responses with minor gaps
- **0.4-0.6:** Fair - adequate but incomplete responses  
- **<0.4:** Poor - filtered out from training data

## 🛠️ Troubleshooting

### **Common Issues:**

**"Ollama not running"**
```bash
# Start Ollama service
ollama serve
```

**"Model not found"**
```bash
# Check available models
ollama list

# Pull missing model
ollama pull qwen3:8b
```

**"JSON parsing errors"**
- Normal for some responses; pipeline handles gracefully
- Consider using a larger/better model for fewer errors
- Check model temperature (lower = more structured)

**"Out of memory"**
```bash
# Use smaller model
export OLLAMA_MODEL="qwen3:8b"  # instead of gpt-oss:20b

# Or reduce batch size
export NUM_SCENARIOS=50  # instead of 100
```

**"Slow generation"**
- Use smaller models for development
- Ensure Ollama has sufficient RAM allocated
- Consider CPU vs GPU optimization

### **Model Selection Guide:**

**If you have:**
- **8GB RAM:** Use `qwen3:8b` or `deepseek-r1:1.5b`
- **16GB RAM:** Use `gpt-oss:20b` or `deepseek-r1:14b`  
- **32GB+ RAM:** Use `mistral-small:24b` or `gpt-oss:120b`

## 🎯 Use Cases

### **Research & Development:**
- Generate synthetic training data for meeting assistant models
- Study enterprise communication patterns
- Benchmark model performance on business scenarios

### **Model Training:**
- Supervised fine-tuning on meeting preparation tasks
- Preference learning with chosen/rejected pairs
- Domain adaptation for business AI assistants

### **Data Augmentation:**
- Expand existing meeting preparation datasets
- Create diverse scenarios for robust training
- Generate evaluation benchmarks

## 🚀 Advanced Usage

### **Custom Model Integration:**
```bash
# Use your own fine-tuned model
ollama create my-meeting-model -f ./Modelfile
export OLLAMA_MODEL="my-meeting-model"
./run_meeting_prep_pipeline_ollama.sh
```

### **Batch Processing:**
```bash
# Generate multiple datasets with different models
for model in qwen3:8b gpt-oss:20b deepseek-r1:14b; do
    export OLLAMA_MODEL="$model"
    export OUTPUT_DIR="data_${model//[^a-zA-Z0-9]/_}"
    ./run_meeting_prep_pipeline_ollama.sh
done
```

### **Quality Filtering:**
```bash
# Generate large dataset and filter by quality
export NUM_SCENARIOS=1000
export MAX_EXAMPLES=50000
./run_meeting_prep_pipeline_ollama.sh

# Post-process to keep only high-quality examples
python -c "
import json
with open('meeting_prep_data_ollama/meeting_prep_sft_training.jsonl') as f:
    data = [json.loads(line) for line in f if json.loads(line)['quality_score'] > 0.8]
with open('high_quality_training.jsonl', 'w') as f:
    for item in data:
        f.write(json.dumps(item) + '\n')
print(f'Filtered to {len(data)} high-quality examples')
"
```

## 🔄 Integration with Other Tools

### **Hugging Face Integration:**
```python
from datasets import Dataset
import json

# Load generated data
with open('meeting_prep_sft_training.jsonl') as f:
    data = [json.loads(line) for line in f]

# Create Hugging Face dataset
dataset = Dataset.from_list(data)
dataset.push_to_hub("your-org/meeting-prep-synthetic")
```

### **OpenAI Fine-tuning Format:**
```python
import json

# Convert to OpenAI JSONL format
with open('meeting_prep_sft_training.jsonl') as f:
    data = [json.loads(line) for line in f]

with open('openai_format.jsonl', 'w') as f:
    for item in data:
        openai_format = {
            "messages": item["messages"]
        }
        f.write(json.dumps(openai_format) + '\n')
```

## 📝 License & Attribution

This Ollama version maintains compatibility with the original PromptCoT 2.0 framework while providing local execution capabilities. Please cite the original PromptCoT papers when using this pipeline for research.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Better JSON parsing and error handling
- Additional evaluation metrics
- Support for more model backends
- Integration with other local LLM frameworks

---

**Ready to generate your meeting preparation training data locally? Start with:**

```bash
./test_ollama_environment.sh && ./run_meeting_prep_pipeline_ollama.sh
```