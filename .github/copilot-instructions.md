# GitHub Copilot Instructions for Scenara 2.0

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
