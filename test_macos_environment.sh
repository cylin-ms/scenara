#!/usr/bin/env bash

# Test script for macOS meeting prep pipeline
# This checks if all dependencies are available before running the full pipeline

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

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

print_step "Testing macOS Meeting Prep Pipeline Environment"

# Test basic commands
echo "Testing basic commands..."
for cmd in python pip; do
    if command -v "$cmd" &> /dev/null; then
        version=$($cmd --version 2>&1 | head -1)
        print_success "$cmd: $version"
    else
        print_error "$cmd not found"
        exit 1
    fi
done

# Test Python version
python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
python_major=$(python -c "import sys; print(sys.version_info.major)")
python_minor=$(python -c "import sys; print(sys.version_info.minor)")

if [[ $python_major -gt 3 ]] || [[ $python_major -eq 3 && $python_minor -ge 8 ]]; then
    print_success "Python version: $python_version"
else
    print_error "Python version $python_version is too old (need >= 3.8)"
    exit 1
fi

# Test Python modules
echo ""
echo "Testing Python dependencies..."
modules=("torch" "transformers" "json" "argparse" "os" "multiprocessing")

for module in "${modules[@]}"; do
    if python -c "import $module" &> /dev/null; then
        print_success "$module module available"
    else
        print_error "$module module not found"
        if [[ "$module" == "torch" ]]; then
            echo "   Install with: pip install torch"
        elif [[ "$module" == "transformers" ]]; then
            echo "   Install with: pip install transformers"
        fi
    fi
done

# Test vllm specifically (often problematic on macOS)
echo ""
echo "Testing vllm (may take a moment)..."
if python -c "import vllm" &> /dev/null; then
    print_success "vllm module available"
else
    print_warning "vllm module not found"
    echo "   Note: vllm may not be available on macOS. Consider alternatives:"
    echo "   - Use transformers backend instead"
    echo "   - Install with: pip install vllm (may require specific versions)"
fi

# Test file access
echo ""
echo "Testing file system..."
if [[ -w . ]]; then
    print_success "Current directory is writable"
else
    print_error "Current directory is not writable"
fi

# Test required Python files
echo ""
echo "Testing required Python files..."
required_files=(
    "meeting_scenario_generation.py"
    "meeting_prep_inference.py" 
    "meeting_prep_self_play_eval.py"
    "meeting_prep_self_play.py"
    "meeting_prep_evaluation.py"
    "prepare_meeting_prep_sft_data.py"
)

for file in "${required_files[@]}"; do
    if [[ -f "$file" ]]; then
        print_success "$file exists"
    else
        print_error "$file not found"
    fi
done

# Test optional files
echo ""
echo "Testing optional files..."
if [[ -f "meeting_prep_golden_prompts.py" ]]; then
    print_success "meeting_prep_golden_prompts.py exists"
else
    print_warning "meeting_prep_golden_prompts.py not found (golden prompt evaluation will be skipped)"
fi

# System info
echo ""
echo "System information:"
echo "  OS: $(uname -s) $(uname -r)"
echo "  Architecture: $(uname -m)"
echo "  Available RAM: $(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')"

# GPU info (if available)
if command -v nvidia-smi &> /dev/null; then
    echo "  NVIDIA GPU: Available"
    nvidia-smi --query-gpu=name --format=csv,noheader,nounits | head -1
else
    print_warning "NVIDIA GPU tools not available (using CPU or MPS)"
fi

# Check if MPS is available (Apple Silicon)
if python -c "import torch; print('MPS available:', torch.backends.mps.is_available())" 2>/dev/null | grep -q "True"; then
    print_success "Apple MPS acceleration available"
else
    print_warning "Apple MPS acceleration not available"
fi

echo ""
print_step "Environment Test Complete"
echo ""
echo "🚀 To run the pipeline:"
echo "   ./run_meeting_prep_pipeline_macos.sh"
echo ""
echo "📝 To customize settings:"
echo "   export MODEL_PATH='your/model/path'"
echo "   export N_GPUS=1"
echo "   export OUTPUT_DIR='custom/output'"
echo ""