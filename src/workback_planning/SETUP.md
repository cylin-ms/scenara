# Workback Planning Setup Guide

## Prerequisites

The workback planning module uses LLMs via Scenara's `LLMAPIClient`. You need at least one of the following:

### Option 1: Ollama (Local, Free)

**Install Ollama:**
```bash
# macOS
brew install ollama

# Start Ollama service
ollama serve
```

**Pull a model:**
```bash
ollama pull gpt-oss:20b
# or
ollama pull llama3
```

**Note**: Ollama models can be used for the structuring stage, but O1-level reasoning is only available via OpenAI.

### Option 2: OpenAI (Cloud, Paid)

**Set API key:**
```bash
export OPENAI_API_KEY="sk-..."
```

**Add to ~/.zshrc for persistence:**
```bash
echo 'export OPENAI_API_KEY="sk-..."' >> ~/.zshrc
source ~/.zshrc
```

**Recommended models:**
- Analysis stage: `o1-preview` or `o1` (when available)
- Structuring stage: `gpt-4o` or `gpt-4-turbo`

### Option 3: Anthropic (Cloud, Paid)

**Set API key:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

**Add to ~/.zshrc for persistence:**
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-..."' >> ~/.zshrc
source ~/.zshrc
```

**Recommended models:**
- Analysis stage: `claude-3-opus-20240229`
- Structuring stage: `claude-3-sonnet-20240229`

## Running Tests

### Test with OpenAI (Recommended)

```bash
# Set API key
export OPENAI_API_KEY="sk-..."

# Run test
python src/workback_planning/test_generator.py
```

### Test with Ollama (Local)

```bash
# Ensure Ollama is running
ollama serve &

# Run test with Ollama override
python src/workback_planning/test_generator_ollama.py
```

### Test Analysis Only (Faster)

```bash
# Skip structured generation to save time/cost
python src/workback_planning/test_generator.py --analysis-only
```

## Configuration

### Model Configuration

Edit model configs in `generator/plan_generator.py`:

```python
# Analysis stage (O1 reasoning)
_analysis_model = {
    "provider": "openai",
    "model": "o1-preview",
    "temperature": 1.0
}

# Structuring stage (JSON conversion)
_structure_model = {
    "provider": "openai",
    "model": "gpt-4o",
    "temperature": 0.1
}
```

### Using Ollama

```python
# For structuring stage (O1 not available locally)
_structure_model = {
    "provider": "ollama",
    "model": "gpt-oss:20b",
    "temperature": 0.1
}
```

### Using Anthropic

```python
_analysis_model = {
    "provider": "anthropic",
    "model": "claude-3-opus-20240229",
    "temperature": 1.0
}

_structure_model = {
    "provider": "anthropic",
    "model": "claude-3-sonnet-20240229",
    "temperature": 0.1
}
```

## Troubleshooting

### "OPENAI_API_KEY is not set"

**Solution**: Export the API key in your terminal
```bash
export OPENAI_API_KEY="sk-..."
```

### "Ollama connection refused"

**Solution**: Start the Ollama service
```bash
ollama serve
```

### "Model not found"

**Solution**: Pull the model first
```bash
ollama pull gpt-oss:20b
```

### "Rate limit exceeded"

**Solution**: 
- Wait a few minutes and retry
- Use a different model
- Switch to Ollama for testing

### JSON parsing errors

**Symptom**: "Failed to parse structured response"

**Causes**:
- Model generated invalid JSON
- Model added markdown formatting (```json)
- Temperature too high (set to 0.1 for structuring)

**Solutions**:
- Lower temperature for structuring stage
- Use a more capable model (gpt-4o, claude-3-sonnet)
- Add JSON validation retry logic

## Performance

### Expected Execution Times

**With OpenAI:**
- Analysis stage (O1): 30-60 seconds
- Structuring stage (GPT-4): 5-10 seconds
- Total: ~45-70 seconds

**With Ollama (local):**
- Analysis stage: 60-120 seconds (depends on hardware)
- Structuring stage: 10-20 seconds
- Total: ~70-140 seconds

### Cost Estimates (OpenAI)

**Per workback plan generation:**
- Analysis stage (O1-preview): ~$0.50-$2.00
- Structuring stage (GPT-4o): ~$0.10-$0.30
- Total: ~$0.60-$2.30

**Note**: Costs vary based on context length and complexity.

## Next Steps

1. **Run test**: `python src/workback_planning/test_generator.py`
2. **Review output**: Check analysis and structured JSON
3. **Integrate with Scenara**: Add to meeting intelligence pipeline
4. **Customize prompts**: Edit files in `prompts/` directory
5. **Add evaluation**: Implement Phase 4 quality assessment
