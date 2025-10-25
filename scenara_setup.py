#!/usr/bin/env python3
"""
Scenara 2.0 Project Setup Script
Quickly creates a new Scenara project with optimized structure
"""

import os
import shutil
from pathlib import Path

def create_scenara_project(target_dir: str):
    """Create a new Scenara 2.0 project structure"""
    
    base_path = Path(target_dir)
    
    # Create directory structure
    directories = [
        "tools",
        "src/meeting_intelligence", 
        "src/gutt_framework",
        "src/data_architecture",
        "src/scenara_core",
        "data/real_meetings",
        "data/synthetic_scenarios", 
        "data/evaluation_results",
        "config",
        "tests/unit",
        "tests/integration", 
        "tests/evaluation",
        "docs",
        "scripts",
        ".github"
    ]
    
    print("🏗️  Creating Scenara 2.0 directory structure...")
    for directory in directories:
        (base_path / directory).mkdir(parents=True, exist_ok=True)
        print(f"   ✅ {directory}")
    
    # Create core files
    files_to_create = {
        "README.md": create_readme(),
        "requirements.txt": create_requirements(),
        "startup.py": create_startup_script(),
        ".cursorrules": create_cursorrules(),
        ".github/copilot-instructions.md": create_copilot_instructions(),
        "tools/__init__.py": "",
        "src/__init__.py": "",
        "config/scenara_config.yaml": create_config(),
        "docs/README.md": "# Scenara 2.0 Documentation\n\nComprehensive documentation for the enterprise meeting intelligence system.\n"
    }
    
    print("\n📄 Creating core project files...")
    for file_path, content in files_to_create.items():
        full_path = base_path / file_path
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ {file_path}")
    
    print(f"\n🎉 Scenara 2.0 project created successfully at: {base_path}")
    print("\n📋 Next steps:")
    print("   1. cd", str(base_path))
    print("   2. python -m venv venv")
    print("   3. source venv/bin/activate")
    print("   4. pip install -r requirements.txt")
    print("   5. python startup.py")

def create_readme():
    return """# Scenara 2.0: Enterprise Meeting Intelligence System

🎯 **Advanced meeting intelligence powered by AI, designed for enterprise environments**

## Overview

Scenara 2.0 is an enterprise-grade meeting intelligence system that leverages Chain-of-Thought reasoning and advanced LLM integration to provide comprehensive meeting preparation, analysis, and optimization capabilities.

### Key Features

- **🧠 Meeting Intelligence**: Advanced classification of 31+ meeting types
- **📊 GUTT v4.0 Framework**: Comprehensive evaluation and quality assessment
- **🔄 Real-time Data Integration**: Microsoft Graph API and multi-source data collection
- **🤖 AI Assistant Integration**: Cross-platform support (Cursor AI, GitHub Copilot)
- **🌐 Platform Detection**: Automatic environment optimization
- **🛡️ Enterprise Security**: Compliance-ready data handling and authentication

## Quick Start

```bash
# Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install -r requirements.txt

# Run platform detection
python startup.py

# Start meeting intelligence analysis
python -m src.scenara_core
```

## Architecture

- **Meeting Intelligence**: Core analysis and classification engine
- **Data Architecture**: Separated real/synthetic data handling  
- **GUTT Framework**: Quality evaluation and scoring
- **Tools Ecosystem**: Utilities for data collection, LLM integration, and automation

## Documentation

- [User Guide](docs/user_guide.md)
- [API Reference](docs/api_reference.md)
- [Deployment Guide](docs/deployment_guide.md)
- [System Architecture](docs/architecture.md)

## Requirements

- Python 3.8+
- Virtual environment recommended
- Microsoft Graph API access (for calendar integration)
- LLM provider access (Ollama, OpenAI, Anthropic, or Azure OpenAI)

## License

Enterprise Meeting Intelligence System - Scenara 2.0
"""

def create_requirements():
    return """# Scenara 2.0 Dependencies

# Core Python packages
python-dateutil>=2.8.2
pytz>=2023.3

# Data processing
pandas>=2.0.0
numpy>=1.24.0
json5>=0.9.14

# LLM and AI integration
openai>=1.3.0
anthropic>=0.8.0

# Microsoft Graph API
msal>=1.24.0
requests>=2.31.0

# Web scraping and automation
aiohttp>=3.8.0
beautifulsoup4>=4.12.0
selenium>=4.15.0

# Visualization and analysis
matplotlib>=3.7.0
seaborn>=0.12.0
plotly>=5.17.0

# Development and testing
pytest>=7.4.0
pytest-asyncio>=0.21.0

# Configuration and utilities
pyyaml>=6.0.1
python-dotenv>=1.0.0
click>=8.1.7

# Optional: Streamlit for UI (uncomment if needed)
# streamlit>=1.28.0

# Optional: Playwright for automation (uncomment if needed)
# playwright>=1.40.0

# Optional: Azure OpenAI (uncomment if needed)
# azure-openai>=1.0.0

# Optional: Ollama integration (uncomment if needed)
# ollama>=0.1.0
"""

def create_startup_script():
    return """#!/usr/bin/env python3
\"\"\"
Scenara 2.0 Startup Script
Automatically detects platform and provides appropriate tool recommendations
\"\"\"

import sys
import os
from pathlib import Path

def main():
    \"\"\"Scenara 2.0 startup and platform detection\"\"\"
    print("🚀 Starting Scenara 2.0: Enterprise Meeting Intelligence System")
    print("=" * 60)
    
    project_root = Path.cwd()
    
    # Check for platform detection tool
    platform_tool = project_root / "tools" / "platform_detection.py"
    
    if platform_tool.exists():
        print("🔍 Running platform detection...")
        # Import and run platform detection
        sys.path.insert(0, str(project_root / "tools"))
        try:
            from platform_detection import PlatformDetector
            detector = PlatformDetector(project_root)
            recommendations = detector.generate_startup_recommendations()
            print(recommendations)
        except ImportError as e:
            print(f"⚠️  Platform detection unavailable: {e}")
    else:
        print("📋 Basic Scenara 2.0 Setup")
        print("🎯 Enterprise Meeting Intelligence System")
        print("📁 Project root:", project_root)
    
    # Check environment setup
    venv_path = project_root / "venv"
    if not venv_path.exists():
        print("\\n⚠️  SETUP REQUIRED:")
        print("   Virtual environment not found.")
        print("   Run: python -m venv venv && source venv/bin/activate")
        print("   Then: pip install -r requirements.txt")
    
    # Check Python version for zoneinfo support
    import sys
    if sys.version_info >= (3, 9):
        print("✅ Python", sys.version.split()[0], "- zoneinfo support available")
    else:
        print("⚠️  Python", sys.version.split()[0], "- consider upgrading to 3.9+ for built-in timezone support")
    
    print("\\n✨ Ready to work on Scenara 2.0!")

if __name__ == "__main__":
    main()
"""

def create_cursorrules():
    return """# Scenara 2.0 Configuration & Task Management

## Instructions for AI Assistant

**IMPORTANT**: This file serves as the primary configuration for both Cursor AI and GitHub Copilot. GitHub Copilot is configured via `.github/copilot-instructions.md` to always read this file first before providing assistance.

**PLATFORM DETECTION**: Use `python startup.py` or `python tools/platform_detection.py` to automatically detect the current development platform and get appropriate tool recommendations.

During interactions, if you find anything reusable in this project (e.g. version of a library, model name), especially about a fix to a mistake you made or a correction you received, you should take note in the `Lessons` section so you will not make the same mistake again.

Use this .cursorrules file as a Scratchpad to organize your thoughts. When you receive a new task:
1. Review the content of the Scratchpad
2. Clear old different tasks if necessary  
3. First explain the task
4. Plan the steps you need to take to complete the task
5. Use todo markers to indicate progress: [X] Completed, [ ] Pending

Update the progress of the task in the Scratchpad when you finish a subtask. When you finish a milestone, reflect and plan using the Scratchpad. The goal is to maintain a big picture as well as task progress. Always refer to the Scratchpad when planning the next step.

## Project Overview
Scenara 2.0: Enterprise meeting intelligence system with GUTT v4.0 ACRUE evaluation framework, separated data architecture, and advanced LLM integration.

## Tools Available

All tools are in Python. For batch processing, consult the python files and write custom scripts.

### Platform Detection and Startup
Automatically detect development environment and get appropriate tool recommendations:
```bash
# Quick startup with platform detection
python startup.py

# Detailed platform detection
python tools/platform_detection.py --json
```

Platform detection identifies:
- Operating system and Python environment
- Active editor (Cursor, VS Code, PyCharm, Jupyter)
- AI assistant (Cursor AI, GitHub Copilot)
- Project configuration status (.cursorrules, copilot instructions)
- Recommended tools and workflows for current platform

## Current Task Progress

### Active: Scenara 2.0 Fresh Start Development

[ ] Project structure creation and setup
[ ] Core tools migration and adaptation
[ ] Meeting intelligence system implementation
[ ] GUTT v4.0 evaluation framework integration
[ ] Platform detection and AI assistant configuration
[ ] Documentation and deployment preparation

### Current Sprint Focus: Initial Project Setup
[ ] Create clean project structure
[ ] Port platform detection system
[ ] Set up meeting intelligence core
[ ] Implement LLM integration
[ ] Configure AI assistant synchronization
[ ] Test end-to-end functionality

## Lessons Learned

### Technical Lessons
- Use Python virtual environment (./venv) for all development
- Always use "Scenara 2.0" in user-facing output and documentation
- Platform detection provides optimal development environment setup
- Cross-platform AI integration ensures consistent development experience

### Environment Configuration
- Virtual Environment: `./venv`
- Requirements: `requirements.txt`
- Python Version: 3.8+
- Primary LLM: Ollama (with OpenAI/Anthropic fallbacks)

## Next Steps & Planning

### Immediate
- [ ] Complete project structure setup
- [ ] Port core tools from PromptCoT
- [ ] Implement meeting intelligence features
- [ ] Set up evaluation framework

### Medium Term
- [ ] Enterprise deployment preparation
- [ ] Advanced meeting analysis features
- [ ] Performance optimization
- [ ] Documentation completion

---

*Scenara 2.0: Clean start, enterprise focus, AI-powered meeting intelligence*
"""

def create_copilot_instructions():
    return """# GitHub Copilot Instructions for Scenara 2.0

## CRITICAL: Always Read .cursorrules First

**MANDATORY**: Before providing any code suggestions or assistance, ALWAYS read and follow the current `.cursorrules` file in the project root. This file contains:

1. **Active Task Context** - Current sprint focus and progress tracking
2. **Lessons Learned** - Project-specific insights and fixes to avoid repeating mistakes
3. **Environment Configuration** - Python setup, LLM models, and dependencies
4. **Implementation Notes** - Ongoing work status and priorities
5. **Platform Detection** - Use `python startup.py` for environment-specific recommendations

The `.cursorrules` file is the **primary source of truth** for project state and should guide all interactions.

## Project Context
Scenara 2.0 is an enterprise meeting intelligence system focusing on AI-powered meeting analysis, preparation, and optimization. The system features advanced LLM integration, real-time data processing, and enterprise-grade security and compliance.

## Code Style and Standards

### Python Environment
- **Virtual Environment**: Use `./venv` for all Python development
- **Requirements**: Install from `requirements.txt`
- **Python Version**: 3.8+ required
- **Project Structure**: Clean separation of concerns with src/, tools/, config/ directories

### Coding Conventions
- Follow PEP 8 style guidelines
- Include comprehensive docstrings for functions and classes
- Use type hints for better code clarity
- Implement proper error handling and logging
- Include debugging information in program output

## Meeting Intelligence Features

### Core Capabilities
- **Meeting Classification**: 31+ meeting types with high accuracy
- **Real-time Analysis**: Live meeting data processing and insights
- **Enterprise Integration**: Microsoft Graph API, calendar systems
- **Multi-provider LLM**: Ollama, OpenAI, Anthropic, Azure OpenAI support
- **Quality Assessment**: GUTT v4.0 evaluation framework

### Data Architecture
- **Separated Data Design**: Real and synthetic data handling
- **Privacy Compliance**: Enterprise-grade data protection
- **Quality Metrics**: Comprehensive evaluation and scoring
- **Scalable Processing**: Efficient batch and real-time processing

## AI Integration Guidelines

### Cross-Platform Support
- **Cursor AI**: Task management, real-time learning, scratchpad functionality
- **GitHub Copilot**: Code suggestions, pattern recognition, workflow guidance
- **Synchronized Context**: Both assistants share project state via .cursorrules

### LLM Integration Patterns
```python
from tools.llm_api import LLMAPIClient
client = LLMAPIClient()
response = client.query_llm(prompt, provider="ollama", model="gpt-oss:20b")
```

## Development Workflow

### Before Any Code Suggestion
1. **READ** `.cursorrules` for current context and priorities
2. **DETECT** platform using `python startup.py` if needed
3. **FOLLOW** established patterns and lessons learned
4. **MAINTAIN** consistency with project architecture

### Code Generation Guidelines
- Always check current sprint focus before suggesting features
- Follow established patterns for LLM integration and meeting analysis
- Include appropriate error handling and logging
- Respect enterprise security and privacy requirements
- Use platform-appropriate tools and recommendations

## Integration with .cursorrules

### Synchronization Protocol
- **ALWAYS** read `.cursorrules` before any coding assistance
- **FOLLOW** the active sprint focus and task priorities  
- **RESPECT** completed tasks and avoid re-implementing
- **CONTRIBUTE** to pending tasks based on current needs
- **LEARN** from the lessons section to avoid repeating mistakes
- **UPDATE** `.cursorrules` with new insights and task progress

**Remember**: `.cursorrules` is the dynamic, living document that reflects current project state, while this file provides static guidance. Always prioritize `.cursorrules` for up-to-date context.

---

*These instructions help GitHub Copilot understand Scenara 2.0 and provide relevant code suggestions aligned with current project state defined in `.cursorrules`.*
"""

def create_config():
    return """# Scenara 2.0 Configuration

project:
  name: "Scenara 2.0"
  description: "Enterprise Meeting Intelligence System"
  version: "2.0.0"

# LLM Configuration
llm:
  primary:
    provider: "ollama"
    model: "gpt-oss:20b"
    temperature: 0.3
  
  fallbacks:
    - provider: "openai"
      model: "gpt-4o"
      temperature: 0.3
    - provider: "anthropic" 
      model: "claude-3-sonnet-20240229"
      temperature: 0.3

# Meeting Intelligence
meeting_intelligence:
  classification_types: 31
  accuracy_target: 0.97
  
  data_architecture:
    real_data_ratio: 0.2
    synthetic_data_ratio: 0.8
    quality_threshold: 8.0

# GUTT Framework
gutt:
  version: "4.0"
  scoring_method: "multiplicative"
  target_score: 3.0
  
# Platform Detection
platform:
  auto_detect: true
  supported_editors: ["cursor", "vscode", "pycharm", "jupyter"]
  supported_os: ["darwin", "windows", "linux"]
"""

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python scenara_setup.py <target_directory>")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    create_scenara_project(target_dir)