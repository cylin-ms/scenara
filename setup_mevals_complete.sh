#!/bin/bash
# MEvals macOS Integration Setup Script
# Configures MEvals Windows codebase for macOS compatibility

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project configuration
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MEVALS_REPO_URL="https://github.com/microsoft/MEvals"  # Placeholder - update with actual URL
CONDA_ENV_NAME="mevals-macos"
PYTHON_VERSION="3.11"

echo -e "${BLUE}🍎 MEvals macOS Integration Setup${NC}"
echo "================================="
echo "Setting up MEvals Windows codebase for macOS compatibility"
echo "Project root: $PROJECT_ROOT"
echo

# Function to print status
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Check if running on macOS
check_macos() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This script is designed for macOS only"
        echo "Detected OS: $OSTYPE"
        exit 1
    fi
    print_status "macOS detected"
}

# Detect architecture
detect_architecture() {
    ARCH=$(uname -m)
    if [[ "$ARCH" == "arm64" ]]; then
        print_status "Apple Silicon (M1/M2/M3) detected"
        CONDA_INSTALLER="Miniconda3-latest-MacOSX-arm64.sh"
    elif [[ "$ARCH" == "x86_64" ]]; then
        print_status "Intel Mac detected"
        CONDA_INSTALLER="Miniconda3-latest-MacOSX-x86_64.sh"
    else
        print_error "Unsupported architecture: $ARCH"
        exit 1
    fi
}

# Install Homebrew if needed
install_homebrew() {
    if command -v brew &> /dev/null; then
        print_status "Homebrew already installed"
    else
        print_info "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add to PATH for Apple Silicon
        if [[ "$ARCH" == "arm64" ]]; then
            echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
            export PATH="/opt/homebrew/bin:$PATH"
        fi
        
        print_status "Homebrew installed"
    fi
}

# Install system dependencies
install_system_deps() {
    print_info "Installing system dependencies..."
    
    # Essential tools
    brew_packages=(
        "git"
        "wget"
        "curl"
        "jq"
        "python@3.11"
    )
    
    for package in "${brew_packages[@]}"; do
        if brew list "$package" &> /dev/null; then
            print_status "$package already installed"
        else
            print_info "Installing $package..."
            brew install "$package"
        fi
    done
}

# Setup conda environment
setup_conda_environment() {
    # Check if conda is installed
    if command -v conda &> /dev/null; then
        print_status "Conda already installed"
    else
        print_info "Installing Miniconda..."
        cd /tmp
        wget "https://repo.anaconda.com/miniconda/$CONDA_INSTALLER" -O miniconda.sh
        bash miniconda.sh -b -p "$HOME/miniconda3"
        rm miniconda.sh
        
        # Initialize conda
        "$HOME/miniconda3/bin/conda" init zsh
        source ~/.zshrc
        
        print_status "Miniconda installed"
    fi
    
    # Create MEvals environment
    print_info "Creating conda environment: $CONDA_ENV_NAME"
    
    if conda env list | grep -q "$CONDA_ENV_NAME"; then
        print_warning "Environment $CONDA_ENV_NAME already exists, updating..."
        conda env update -n "$CONDA_ENV_NAME" -f environment.yml
    else
        conda create -n "$CONDA_ENV_NAME" python="$PYTHON_VERSION" -y
        print_status "Environment $CONDA_ENV_NAME created"
    fi
}

# Create conda environment file
create_environment_file() {
    print_info "Creating environment.yml..."
    
    cat > "$PROJECT_ROOT/environment.yml" << EOF
name: $CONDA_ENV_NAME
channels:
  - conda-forge
  - defaults
dependencies:
  - python=$PYTHON_VERSION
  - pip
  - jupyter
  - notebook
  - pip:
    - msal>=1.24.0
    - requests>=2.28.0
    - python-dotenv>=1.0.0
    - pandas>=2.0.0
    - numpy>=1.24.0
    - matplotlib>=3.7.0
    - seaborn>=0.12.0
    - plotly>=5.15.0
    - openai>=1.0.0
    - anthropic>=0.7.0
    - transformers>=4.30.0
    - torch>=2.0.0
    - scikit-learn>=1.3.0
    - nltk>=3.8.0
    - spacy>=3.6.0
    - beautifulsoup4>=4.12.0
    - lxml>=4.9.0
    - openpyxl>=3.1.0
    - xlsxwriter>=3.1.0
    - python-dateutil>=2.8.0
    - pytz>=2023.3
    - tqdm>=4.65.0
    - rich>=13.4.0
    - click>=8.1.0
    - pyyaml>=6.0
    - jsonlines>=3.1.0
    - pathlib2>=2.3.7
    - psutil>=5.9.0
EOF

    print_status "Environment file created"
}

# Install Python dependencies
install_python_deps() {
    print_info "Activating conda environment and installing dependencies..."
    
    # Activate environment
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "$CONDA_ENV_NAME"
    
    # Install dependencies
    conda env update -f "$PROJECT_ROOT/environment.yml"
    
    # Install additional packages that might not be in conda
    pip install --upgrade pip
    pip install msal-extensions  # For token caching
    
    print_status "Python dependencies installed"
}

# Clone MEvals repository
clone_mevals() {
    if [[ -d "$PROJECT_ROOT/MEvals" ]]; then
        print_warning "MEvals directory already exists"
        read -p "Do you want to update it? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            cd "$PROJECT_ROOT/MEvals"
            git pull
            print_status "MEvals repository updated"
        fi
    else
        print_info "Cloning MEvals repository..."
        print_warning "Note: You may need to update the repository URL with the actual MEvals repo"
        
        # For now, create a placeholder structure
        mkdir -p "$PROJECT_ROOT/MEvals/data/meeting_prep.prompt.samples"
        mkdir -p "$PROJECT_ROOT/MEvals/scripts"
        
        # Create sample structure
        cat > "$PROJECT_ROOT/MEvals/README.md" << EOF
# MEvals - Meeting Evaluation Dataset

This is a placeholder structure for the MEvals repository.

## Directory Structure
- \`data/\` - Meeting evaluation data
- \`scripts/\` - Processing scripts
- \`meeting_prep.prompt.samples/\` - Sample meeting data

## Setup
1. Replace this placeholder with the actual MEvals repository
2. Ensure proper authentication is configured
3. Run the macOS adaptation scripts

## Notes
- Original codebase is Windows-focused
- This adaptation provides cross-platform compatibility
- Authentication uses device flow instead of Windows Broker
EOF

        print_status "MEvals placeholder structure created"
        print_warning "Please replace with actual MEvals repository when available"
    fi
}

# Set up authentication configuration
setup_authentication() {
    print_info "Setting up authentication configuration..."
    
    # Create .env template
    cat > "$PROJECT_ROOT/.env.template" << EOF
# Microsoft Graph API Configuration
# Copy this file to .env and fill in your actual values

AZURE_CLIENT_ID=your_client_id_here
AZURE_CLIENT_SECRET=your_client_secret_here
AZURE_TENANT_ID=your_tenant_id_here

# Optional: Redirect URI for web authentication
AZURE_REDIRECT_URI=http://localhost:8000/callback

# Graph API Configuration
GRAPH_API_BASE_URL=https://graph.microsoft.com/v1.0
GRAPH_API_SCOPES=https://graph.microsoft.com/.default

# Cache configuration
TOKEN_CACHE_FILE=.token_cache.json

# Logging
LOG_LEVEL=INFO
EOF

    if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
        cp "$PROJECT_ROOT/.env.template" "$PROJECT_ROOT/.env"
        print_status "Environment configuration template created"
        print_warning "Please edit .env file with your Microsoft Graph API credentials"
    else
        print_status "Environment configuration already exists"
    fi
}

# Convert PowerShell scripts to Bash
convert_powershell_scripts() {
    print_info "Converting PowerShell scripts to Bash..."
    
    # Create converted scripts directory
    mkdir -p "$PROJECT_ROOT/scripts_macos"
    
    # Convert common PowerShell patterns
    cat > "$PROJECT_ROOT/scripts_macos/run_meeting_prep_macos.sh" << 'EOF'
#!/bin/bash
# Converted from PowerShell MEvals script for macOS

set -e

# Configuration
CONDA_ENV_NAME="mevals-macos"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}🍎 MEvals Meeting Prep Pipeline (macOS)${NC}"
echo "======================================="

# Activate conda environment
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate "$CONDA_ENV_NAME"

# Run authentication test
echo -e "${YELLOW}Testing authentication...${NC}"
python "$PROJECT_ROOT/mevals_auth_manager.py"

# Run data bridge
echo -e "${YELLOW}Running data bridge...${NC}"
python "$PROJECT_ROOT/mevals_promptcot_bridge.py" \
    --mevals-data "$PROJECT_ROOT/MEvals/data/meeting_prep.prompt.samples" \
    --output "$PROJECT_ROOT/meeting_prep_data_real"

# Run Meeting PromptCoT pipeline
echo -e "${YELLOW}Running Meeting PromptCoT pipeline...${NC}"
if [[ -f "$PROJECT_ROOT/run_meeting_prep_pipeline.sh" ]]; then
    bash "$PROJECT_ROOT/run_meeting_prep_pipeline.sh" \
        --data-dir "$PROJECT_ROOT/meeting_prep_data_real" \
        --real-data
else
    echo "Meeting PromptCoT pipeline not found, skipping..."
fi

echo -e "${GREEN}✅ Pipeline complete!${NC}"
EOF

    chmod +x "$PROJECT_ROOT/scripts_macos/run_meeting_prep_macos.sh"
    print_status "PowerShell scripts converted to Bash"
}

# Make scripts executable
make_scripts_executable() {
    print_info "Making scripts executable..."
    
    # Make all .sh files executable
    find "$PROJECT_ROOT" -name "*.sh" -exec chmod +x {} \;
    
    # Make Python scripts executable
    find "$PROJECT_ROOT" -name "*.py" -exec chmod +x {} \;
    
    print_status "Scripts made executable"
}

# Run integration tests
run_integration_tests() {
    print_info "Running integration tests..."
    
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate "$CONDA_ENV_NAME"
    
    python "$PROJECT_ROOT/test_mevals_integration.py"
    
    print_status "Integration tests completed"
}

# Create documentation
create_documentation() {
    print_info "Creating documentation..."
    
    cat > "$PROJECT_ROOT/MEvals_macOS_Setup.md" << EOF
# MEvals macOS Setup Guide

This guide explains how to set up and use the MEvals Windows codebase on macOS.

## Quick Start

1. Run the setup script:
   \`\`\`bash
   ./setup_mevals_complete.sh
   \`\`\`

2. Activate the conda environment:
   \`\`\`bash
   conda activate mevals-macos
   \`\`\`

3. Configure authentication:
   \`\`\`bash
   cp .env.template .env
   # Edit .env with your Microsoft Graph API credentials
   \`\`\`

4. Test the integration:
   \`\`\`bash
   python test_mevals_integration.py
   \`\`\`

5. Run the Meeting PromptCoT pipeline:
   \`\`\`bash
   ./scripts_macos/run_meeting_prep_macos.sh
   \`\`\`

## Components

### Authentication Manager (\`mevals_auth_manager.py\`)
- Cross-platform Microsoft Graph authentication
- Handles device flow for macOS (no Windows Broker dependency)
- Token caching and refresh

### Data Bridge (\`mevals_promptcot_bridge.py\`)
- Converts MEvals real meeting data to Meeting PromptCoT format
- Extracts business context from professional meeting samples
- Quality filtering and enhancement

### Integration Tests (\`test_mevals_integration.py\`)
- Validates entire setup
- Tests authentication, data processing, and pipeline integration
- Provides troubleshooting guidance

## Architecture

The macOS adaptation addresses:
- **Authentication**: Device flow instead of Windows Broker
- **Scripts**: Bash conversion of PowerShell automation
- **Dependencies**: Cross-platform package management
- **Environment**: Conda-based setup for consistency

## Troubleshooting

### Authentication Issues
- Ensure Azure app registration allows device flow
- Check network connectivity to Microsoft Graph
- Verify client ID, secret, and tenant ID

### Data Processing Issues
- Confirm MEvals repository structure
- Check sample data availability
- Validate file permissions

### Pipeline Issues
- Ensure conda environment is activated
- Check Meeting PromptCoT dependencies
- Verify script permissions

## Next Steps

1. Replace placeholder MEvals repo with actual repository
2. Configure production authentication credentials
3. Test with real meeting data
4. Integrate with Meeting PromptCoT training pipeline

For detailed technical information, see \`MEvals_macOS_Adaptation_Analysis.md\`.
EOF

    print_status "Documentation created"
}

# Main setup function
main() {
    echo "Starting MEvals macOS integration setup..."
    echo
    
    check_macos
    detect_architecture
    install_homebrew
    install_system_deps
    create_environment_file
    setup_conda_environment
    install_python_deps
    clone_mevals
    setup_authentication
    convert_powershell_scripts
    make_scripts_executable
    create_documentation
    
    echo
    print_status "Setup completed successfully!"
    echo
    print_info "Next steps:"
    echo "1. Edit .env file with your Microsoft Graph API credentials"
    echo "2. Activate environment: conda activate $CONDA_ENV_NAME"
    echo "3. Run integration tests: python test_mevals_integration.py"
    echo "4. Start the pipeline: ./scripts_macos/run_meeting_prep_macos.sh"
    echo
    print_warning "Note: Replace MEvals placeholder with actual repository when available"
    
    # Optional: Run tests immediately
    read -p "Do you want to run integration tests now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        run_integration_tests
    fi
}

# Run main function
main "$@"