#!/usr/bin/env bash

# Test script for Ollama meeting prep pipeline
# This checks if Ollama and required models are available

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_info() {
    echo -e "${PURPLE}ℹ $1${NC}"
}

print_step "Testing Ollama Meeting Prep Pipeline Environment"

# Test Ollama installation
echo "Testing Ollama installation..."
if command -v ollama &> /dev/null; then
    ollama_version=$(ollama --version 2>&1 | head -1 || echo "Unknown")
    print_success "Ollama installed: $ollama_version"
else
    print_error "Ollama not found"
    echo "   Install from: https://ollama.ai"
    exit 1
fi

# Test Ollama service
echo ""
echo "Testing Ollama service..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    print_success "Ollama service is running"
else
    print_error "Ollama service not running"
    echo "   Start with: ollama serve"
    exit 1
fi

# List available models
echo ""
echo "Available Ollama models:"
ollama list

# Test recommended models
echo ""
echo "Checking recommended models..."
recommended_models=("qwen3:8b" "gpt-oss:20b" "deepseek-r1:14b" "gemma3:12b")

available_models=()
for model in "${recommended_models[@]}"; do
    if ollama list | grep -q "^$model"; then
        print_success "$model is available"
        available_models+=("$model")
    else
        print_warning "$model not found"
        echo "   Pull with: ollama pull $model"
    fi
done

if [[ ${#available_models[@]} -eq 0 ]]; then
    print_error "No recommended models found"
    echo "   Please pull at least one model:"
    echo "   ollama pull qwen3:8b  # Fast, good quality"
    echo "   ollama pull gpt-oss:20b  # Larger, better quality"
    exit 1
fi

# Test Python dependencies
echo ""
echo "Testing Python dependencies..."
required_modules=("requests" "json")

for module in "${required_modules[@]}"; do
    if python -c "import $module" &> /dev/null; then
        print_success "$module module available"
    else
        if [[ "$module" == "requests" ]]; then
            print_error "$module module not found"
            echo "   Install with: pip install requests"
            exit 1
        else
            print_success "$module module available (built-in)"
        fi
    fi
done

# Test model with simple prompt
echo ""
echo "Testing model response..."
test_model="${available_models[0]}"
print_info "Testing $test_model with simple prompt..."

test_response=$(timeout 30 ollama generate "$test_model" "Please respond with exactly: 'Test successful'" 2>/dev/null || echo "")

if [[ "$test_response" == *"Test successful"* ]]; then
    print_success "Model $test_model responding correctly"
elif [[ -n "$test_response" ]]; then
    print_warning "Model $test_model responding (output: ${test_response:0:50}...)"
else
    print_error "Model $test_model not responding"
    echo "   Check if model is working: ollama run $test_model"
fi

# System resources
echo ""
echo "System resources:"
echo "  OS: $(uname -s) $(uname -r)"
echo "  Architecture: $(uname -m)"
echo "  Available RAM: $(sysctl -n hw.memsize | awk '{print $1/1024/1024/1024 " GB"}')"
echo "  Available disk: $(df -h . | tail -1 | awk '{print $4}')"

# Estimate performance
echo ""
echo "Performance estimates:"
if [[ ${#available_models[@]} -gt 0 ]]; then
    for model in "${available_models[@]}"; do
        model_size=$(ollama list | grep "^$model" | awk '{print $3}')
        echo "  $model ($model_size): Good for meeting prep tasks"
    done
fi

echo ""
print_step "Ollama Environment Test Complete"
echo ""
if [[ ${#available_models[@]} -gt 0 ]]; then
    print_success "Ready to run Ollama pipeline!"
    echo ""
    echo "🚀 To run with default model (${available_models[0]}):"
    echo "   ./run_meeting_prep_pipeline_ollama.sh"
    echo ""
    echo "🔧 To use a specific model:"
    for model in "${available_models[@]}"; do
        echo "   export OLLAMA_MODEL='$model'"
    done
    echo "   ./run_meeting_prep_pipeline_ollama.sh"
    echo ""
    echo "⚙️ To customize pipeline:"
    echo "   export NUM_SCENARIOS=200      # Generate more scenarios"
    echo "   export MAX_EXAMPLES=10000     # Create larger dataset"
    echo "   export OUTPUT_DIR='my_data'   # Custom output directory"
    echo ""
    echo "📊 Expected performance:"
    echo "   • Scenario generation: ~1-2 minutes per 10 scenarios"
    echo "   • Response generation: ~2-3 minutes per 10 responses"
    echo "   • Total time for 100 scenarios: ~15-30 minutes"
else
    print_error "Please install at least one recommended model first"
fi