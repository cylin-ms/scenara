#!/bin/bash
# setup_mevals_macos.sh - macOS Setup for MEvals Integration
# Adapted from MEvals Windows setup.ps1 for Meeting PromptCoT

set -euo pipefail

echo "🍎 Setting up MEvals for macOS Integration with Meeting PromptCoT"
echo "================================================================"

# Configuration
CONDA_ENV="mevals"
DOWNLOADS_DIR="$PWD/Downloads"
MEVALS_DIR="$PWD/MEvals"

# 1. Ensure Downloads folder exists
echo "📁 Creating Downloads directory..."
mkdir -p "$DOWNLOADS_DIR"

# 2. Detect macOS architecture and set appropriate Miniconda URL
echo "🔍 Detecting macOS architecture..."
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]]; then
    echo "   Apple Silicon (M1/M2) detected"
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh"
    INSTALLER="Miniconda3-latest-MacOSX-arm64.sh"
else
    echo "   Intel x86_64 detected"
    MINICONDA_URL="https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh"
    INSTALLER="Miniconda3-latest-MacOSX-x86_64.sh"
fi

DEST="$DOWNLOADS_DIR/$INSTALLER"

# 3. Download Miniconda if not exists
if [ ! -f "$DEST" ]; then
    echo "⬇️ Downloading Miniconda for macOS..."
    curl -L "$MINICONDA_URL" -o "$DEST"
else
    echo "✅ Miniconda installer already exists"
fi

# 4. Verify download
echo "📊 Verifying download..."
ls -la "$DEST"

# 5. Check if conda is already installed
if command -v conda &> /dev/null; then
    echo "✅ Conda already installed"
    eval "$(conda shell.bash hook)"
else
    echo "📦 Installing Miniconda..."
    bash "$DEST" -b -p "$HOME/miniconda3"
    
    # Initialize conda for current session
    eval "$($HOME/miniconda3/bin/conda shell.bash hook)"
    
    # Add conda to PATH for future sessions
    echo 'eval "$($HOME/miniconda3/bin/conda shell.bash hook)"' >> ~/.bashrc
    echo 'eval "$($HOME/miniconda3/bin/conda shell.bash hook)"' >> ~/.zshrc
fi

# 6. Verify conda installation
echo "🔧 Verifying conda installation..."
conda --version

# 7. Create MEvals conda environment
echo "🐍 Creating MEvals conda environment..."
if conda env list | grep -q "^$CONDA_ENV "; then
    echo "   Environment '$CONDA_ENV' already exists"
else
    conda create -n "$CONDA_ENV" python=3.11 -y
fi

# 8. Activate environment and install dependencies
echo "📚 Installing Python dependencies..."
conda activate "$CONDA_ENV"

# Core dependencies for MEvals
pip install --upgrade pip
pip install "msal>=1.20,<2" requests pathlib argparse

# Additional dependencies for Meeting PromptCoT integration
pip install pandas numpy python-dateutil tzlocal

# 9. Create MEvals macOS directory structure
echo "📂 Setting up MEvals macOS structure..."
mkdir -p "$MEVALS_DIR/macos"
mkdir -p "$MEVALS_DIR/macos/out"
mkdir -p "$MEVALS_DIR/macos/logs"
mkdir -p "$MEVALS_DIR/macos/data"

# 10. Display setup summary
echo ""
echo "✅ MEvals macOS Setup Complete!"
echo "================================"
echo "📁 Installation Directory: $HOME/miniconda3"
echo "🐍 Conda Environment: $CONDA_ENV"
echo "📂 MEvals Directory: $MEVALS_DIR"
echo ""
echo "🚀 Next Steps:"
echo "1. Activate environment: conda activate $CONDA_ENV"
echo "2. Run authentication test: python test_mevals_auth.py"
echo "3. Start data collection: ./run_mevals_macos.sh"
echo ""
echo "🔗 Integration with Meeting PromptCoT:"
echo "   The setup includes bridge modules to convert MEvals data"
echo "   to Meeting PromptCoT training format automatically."