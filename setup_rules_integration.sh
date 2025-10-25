#!/bin/bash
# Setup script for integrating XiadongLiu rules into PromptCoT project

set -e

echo "🚀 Setting up Scenara with Scenara Rules Integration"
echo "======================================================="

# Check if we're in the right directory
if [ ! -f "requirements_meeting_prep.txt" ]; then
    echo "Error: Please run this script from the Scenara project root directory"
    exit 1
fi

# Activate virtual environment
echo "📦 Activating Python virtual environment..."
if [ -d ".venv" ]; then
    source .venv/bin/activate
    echo "✅ Virtual environment activated"
else
    echo "❌ Virtual environment not found. Please run:"
    echo "   python -m venv .venv"
    echo "   source .venv/bin/activate"
    exit 1
fi

# Install additional tool requirements
echo "📦 Installing tool dependencies..."
if [ -f "requirements_tools.txt" ]; then
    pip install -r requirements_tools.txt
    echo "✅ Tool dependencies installed"
else
    echo "⚠️  requirements_tools.txt not found, skipping additional dependencies"
fi

# Install Playwright browsers (for screenshots)
echo "🌐 Installing Playwright browsers..."
if command -v playwright &> /dev/null; then
    playwright install chromium
    echo "✅ Playwright browsers installed"
else
    echo "⚠️  Playwright not available, skipping browser installation"
fi

# Make tools executable
echo "🔧 Making tools executable..."
chmod +x tools/*.py
echo "✅ Tools are now executable"

# Verify .cursorrules file
if [ -f ".cursorrules" ]; then
    echo "✅ .cursorrules file found"
else
    echo "⚠️  .cursorrules file not found - it should have been created during integration"
fi

# Test basic tool functionality
echo "🧪 Testing tool functionality..."

# Test LLM API tool
echo "Testing LLM API tool..."
python tools/llm_api.py --prompt "Hello, this is a test" --provider "ollama" || echo "⚠️  LLM API test failed (this is expected if Ollama is not running)"

# Test search engine tool
echo "Testing search engine tool..."
python tools/search_engine.py "meeting best practices" --max-results 3 || echo "⚠️  Search engine test failed"

# Test integration utility
echo "Testing integration utility..."
python tools/promptcot_rules_integration.py --list-tasks || echo "⚠️  Integration utility test failed"

# Test complete workflow
echo "Testing complete Scenara Rules workflow integration..."
python demo_scenara_rules_integration.py || echo "⚠️  Complete workflow test failed"

echo ""
echo "🎉 Scenara Rules Integration Setup Complete!"
echo "========================================================"
echo ""
echo "Available tools:"
echo "  • tools/llm_api.py          - Multi-provider LLM queries"
echo "  • tools/web_scraper.py      - Web content scraping"
echo "  • tools/search_engine.py    - Web search functionality"
echo "  • tools/screenshot_utils.py - Screenshot capture"
echo "  • tools/promptcot_rules_integration.py - Task and lesson management"
echo ""
echo "Usage examples:"
echo "  # Query LLM"
echo "  python tools/llm_api.py --prompt 'Analyze this meeting type' --provider ollama"
echo ""
echo "  # Search for information"
echo "  python tools/search_engine.py 'strategic planning meeting best practices'"
echo ""
echo "  # Add a lesson learned"
echo "  python tools/promptcot_rules_integration.py --add-lesson technical 'Always validate Ollama model availability'"
echo ""
echo "  # Update task progress"
echo "  python tools/promptcot_rules_integration.py --update-task 'Microsoft Graph API Integration' completed"
echo ""
echo "  # Run complete workflow demo"
echo "  python demo_scenara_rules_integration.py"
echo ""
echo "  # Generate status report"
echo "  python tools/promptcot_rules_integration.py --status-report"
echo ""
echo "Configuration file: .cursorrules"
echo "Task management and lessons are tracked in this file."
echo "Integration guide: docs/Scenara_Rules_Integration_Guide.md"