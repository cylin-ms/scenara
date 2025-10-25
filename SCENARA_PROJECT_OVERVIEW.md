# 🎯 Scenara 2.0: Enterprise Meeting Intelligence System

## Project Status: ACTIVE DEVELOPMENT

**Created**: October 22, 2025  
**Migration Status**: ✅ COMPLETE FROM PROMPTCOT  
**Current Location**: `/Users/cyl/projects/Scenara`  
**Original Location**: `/Users/cyl/projects/PromptCoT`

---

## 🏢 About Scenara 2.0

Scenara 2.0 is an enterprise meeting intelligence system that evolved from the PromptCoT research project. It combines advanced Chain-of-Thought reasoning with practical meeting intelligence capabilities for enterprise environments.

### 🎯 Core Features

- **Enterprise Meeting Classification**: 31+ meeting types with 97-99% accuracy
- **GUTT v4.0 ACRUE Framework**: Advanced evaluation with multiplicative scoring
- **Separated Data Architecture**: Real (20%) + Synthetic (80%) data approach
- **Advanced LLM Integration**: Multi-provider support (Ollama, OpenAI, Anthropic)
- **Microsoft Graph API Integration**: Real calendar data with compliance
- **Platform Detection**: Automatic environment optimization
- **Comprehensive Tool Ecosystem**: 8+ specialized utilities

---

## 📁 Project Structure

### Core Components

```
/Scenara/
├── tools/                    # Core utility tools
│   ├── meeting_extractor.py  # Multi-source meeting data
│   ├── platform_detection.py # Environment detection
│   ├── llm_api.py            # Multi-provider LLM
│   ├── web_scraper.py        # Research capabilities
│   └── screenshot_utils.py   # UI verification
├── src/                      # Source code modules
├── data/                     # Core datasets
├── meeting_prep_data/        # Meeting preparation data
├── ContextFlow/              # Context flow integration
├── MEvals/                   # Meeting evaluation system
├── Priority_Calendar/        # Calendar prioritization
└── daily_intelligence/      # Daily intelligence reports
```

### Enterprise Features

- **Real Meeting Integration**: Microsoft Graph API calendar access
- **Me Notes System**: Personal meeting preparation enhancement
- **Daily Meeting Viewer**: Beautiful formatted meeting schedules
- **Demo Systems**: Testing and validation frameworks
- **Analytics**: Meeting ranking and intelligence tools

---

## 🔄 Migration From PromptCoT

### ✅ What Was Migrated

This Scenara directory contains **everything** from the original PromptCoT project plus enterprise enhancements:

- **Complete PromptCoT codebase**: All 122+ Python files
- **Research algorithms**: PromptCoT_1.0, PromptCoT_Mamba implementations
- **Complete Git history**: Full version control preserved
- **All data and assets**: Complete research datasets
- **Configuration files**: All requirements, configs, documentation

### 🚀 Enterprise Enhancements Added

- **Meeting Intelligence Framework**: Enterprise-grade meeting processing
- **Tool Ecosystem**: Comprehensive utility collection
- **Platform Detection**: Automatic environment optimization
- **AI Assistant Integration**: Cursor AI + GitHub Copilot synchronization
- **Real Data Integration**: Microsoft 365 calendar connectivity
- **Security Framework**: Enterprise compliance and audit capabilities

---

## 🛠️ Getting Started

### Quick Start

```bash
# Navigate to project
cd /Users/cyl/projects/Scenara

# Activate environment
source venv/bin/activate

# Run platform detection
python startup.py

# Test meeting extraction
python tools/meeting_extractor.py --list-sources

# View today's meetings
python demo_daily_meeting_viewer.py 20251022 --console-only
```

### Development Environment

- **Python**: 3.12.4 with virtual environment
- **Platform**: macOS (Darwin) with zsh shell
- **Editor**: VS Code with GitHub Copilot
- **Dependencies**: All installed and verified working

---

## 📋 Current Status

### ✅ Completed Tasks

- [x] Complete project migration from PromptCoT
- [x] Tool ecosystem integration and testing
- [x] Platform detection system implementation
- [x] Microsoft Graph API integration framework
- [x] Cross-platform AI assistant synchronization
- [x] Git repository integrity verification

### 🚧 Active Development

- [ ] Automated testing suite for tool integration
- [ ] Performance optimization for enterprise scale
- [ ] GUTT v4.0 template materialization completion
- [ ] Production deployment guide creation
- [ ] Enterprise security audit and compliance

---

## 🔧 Tool Ecosystem

### Available Tools

1. **meeting_extractor.py**: Multi-source meeting data aggregation
2. **platform_detection.py**: Environment detection and optimization
3. **llm_api.py**: Multi-provider LLM integration
4. **web_scraper.py**: Research and content gathering
5. **screenshot_utils.py**: UI verification and testing
6. **search_engine.py**: Intelligent search capabilities
7. **daily_interaction_logger.py**: Session and activity logging
8. **promptcot_rules_integration.py**: Task and lesson management

### Key Applications

- **daily_meeting_viewer.py**: Real-time calendar integration
- **demo_daily_meeting_viewer.py**: Testing with sample data
- **me_notes_viewer.py**: Personal meeting preparation
- **meeting_intelligence_suite_demo.py**: Complete system demonstration

---

## 📖 Documentation

### Primary Configuration

- **.cursorrules**: Main configuration and task management
- **.github/copilot-instructions.md**: GitHub Copilot integration
- **README.md**: Project overview and setup instructions

### Specialized Guides

- **README_meeting_prep.md**: Meeting preparation system
- **Platform Detection Summary**: Environment optimization
- **Microsoft Graph Integration**: Calendar API setup

---

## 🔗 Relationship to PromptCoT

### Original Repository

- **Location**: `/Users/cyl/projects/PromptCoT`
- **Status**: Archive/Reference (no active development)
- **Purpose**: Historical research and algorithm reference
- **Content**: Original PromptCoT research implementations

### This Repository (Scenara)

- **Location**: `/Users/cyl/projects/Scenara`
- **Status**: Active development (primary working directory)
- **Purpose**: Enterprise meeting intelligence system
- **Content**: Complete PromptCoT + Scenara 2.0 enterprise features

---

## 📞 Support and Next Steps

### For Development

1. **Platform Detection**: Run `python startup.py` for environment-specific recommendations
2. **Tool Testing**: Use `python tools/meeting_extractor.py --list-sources` to verify integration
3. **Meeting Intelligence**: Test with `python demo_daily_meeting_viewer.py YYYYMMDD`

### For Questions

- **Configuration**: Check `.cursorrules` for current task status and lessons learned
- **Platform Issues**: Run platform detection for environment-specific guidance
- **Integration**: All tools designed for enterprise meeting intelligence use cases

---

*Scenara 2.0 - Enterprise Meeting Intelligence System*  
*Built on PromptCoT research foundation*  
*October 2025*