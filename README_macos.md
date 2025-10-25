# PromptCoT 2.0 Meeting Prep Pipeline - macOS Version

This directory contains a macOS-optimized version of the PromptCoT 2.0 meeting preparation pipeline.

## Quick Start

### 1. Test Your Environment
First, run the environment test to ensure all dependencies are available:

```bash
./test_macos_environment.sh
```

This will check for:
- Python 3.8+ 
- Required Python packages (torch, transformers, etc.)
- File permissions
- GPU acceleration (NVIDIA CUDA or Apple MPS)

### 2. Run the Pipeline

Run the full pipeline with default settings:

```bash
./run_meeting_prep_pipeline_macos.sh
```

Or customize with environment variables:

```bash
export MODEL_PATH="Qwen/Qwen2.5-7B-Instruct"
export N_GPUS=1
export OUTPUT_DIR="my_meeting_data"
./run_meeting_prep_pipeline_macos.sh
```

## macOS-Specific Optimizations

The macOS version includes several improvements over the original Linux script:

### ✅ **Enhanced Error Handling**
- Pre-flight dependency checks
- Graceful handling of missing optional components
- Clear error messages with installation suggestions

### ✅ **macOS Compatibility**
- Uses `#!/usr/bin/env bash` for better portability
- Compatible with macOS command line tools
- Handles Apple Silicon MPS acceleration
- Works with both Intel and Apple Silicon Macs

### ✅ **Better User Experience**
- Colored output for better readability
- Progress indicators and status messages
- Disk space checking
- Comprehensive summary statistics

### ✅ **Robust File Handling**
- Proper error checking for file operations
- Safe directory creation with permissions
- Graceful handling of missing files

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_PATH` | `Qwen/Qwen3-32B-Instruct` | Hugging Face model path |
| `N_GPUS` | `1` | Number of GPUs to use |
| `SEED` | `42` | Random seed for reproducibility |
| `TEMPERATURE` | `0.8` | Generation temperature |
| `OUTPUT_DIR` | `meeting_prep_data` | Output directory |

### Example Configurations

**For local testing (small model):**
```bash
export MODEL_PATH="microsoft/DialoGPT-small"
export N_GPUS=1
export OUTPUT_DIR="test_output"
```

**For production (large model):**
```bash
export MODEL_PATH="Qwen/Qwen3-32B-Instruct"
export N_GPUS=4  # If you have multiple GPUs
export OUTPUT_DIR="production_meeting_data"
```

## Output Files

The pipeline generates several datasets:

- `meeting_prep_sft_training.jsonl` - For supervised fine-tuning
- `meeting_prep_training_pairs.jsonl` - For self-play/DPO training  
- `golden_prompts_evaluation.json` - Quality assessment results
- `meeting_scenarios.jsonl` - Generated meeting scenarios
- Various intermediate files for debugging

## Troubleshooting

### Common Issues

**vllm not available on macOS:**
```bash
# Try alternative installation
pip install vllm --no-deps
# Or use transformers backend by modifying the Python scripts
```

**Out of memory errors:**
```bash
# Reduce batch size or use smaller model
export MODEL_PATH="Qwen/Qwen2.5-7B-Instruct"
```

**Permission denied:**
```bash
# Ensure scripts are executable
chmod +x *.sh
```

**Python module not found:**
```bash
# Install missing modules
pip install torch transformers vllm
```

### Apple Silicon Specific

For Apple Silicon Macs, ensure you have:
- Python 3.8+ compiled for arm64
- PyTorch with MPS support: `pip install torch --index-url https://download.pytorch.org/whl/cpu`

### Performance Tips

1. **Use Apple MPS** (Apple Silicon): Automatically detected and used
2. **Adjust batch sizes**: Start small and increase based on available memory
3. **Use local models**: Download models locally for faster access
4. **Monitor resources**: Use Activity Monitor to track CPU/GPU usage

## Dependencies

### Required
- Python 3.8+
- torch
- transformers 
- vllm (optional, fallback available)
- json (built-in)
- argparse (built-in)

### Optional
- CUDA toolkit (for NVIDIA GPUs)
- Apple Developer Tools (for MPS)

## Support

For issues specific to the macOS version:
1. Run `./test_macos_environment.sh` to diagnose problems
2. Check the colored output for specific error messages
3. Ensure all file permissions are correct
4. Verify Python environment compatibility

For general PromptCoT issues, refer to the main README.md.