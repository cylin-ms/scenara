# Scenara Rules Integration Guide

**Complete Workflow System for Enhanced Project Management and Learning**

## Overview

This guide documents the complete integration of Scenara's rules system into Scenara 2.0, providing a comprehensive framework for task management, lessons learned tracking, and enhanced development workflows.

## Integration Components

### 1. Configuration System (.cursorrules)

The `.cursorrules` file serves as the central hub for:
- **Task Management**: Track project progress with markdown checkboxes
- **Lessons Learned**: Categorized knowledge retention (User, Project, Technical)
- **Environment Configuration**: LLM, data, and deployment settings
- **Planning & Reflection**: Scratchpad for strategic thinking

### 2. Tools Directory

Complete Python-based toolchain:

#### **LLM Integration (`tools/llm_api.py`)**
- Multi-provider support: Ollama, OpenAI, Anthropic, Azure, DeepSeek, Gemini
- Vision capabilities for screenshot analysis
- Fallback provider handling
- Scenara-optimized for meeting intelligence

#### **Web Research (`tools/web_scraper.py` & `tools/search_engine.py`)**
- Async web scraping with meeting context extraction
- Search engine integration with business intelligence
- Content analysis for meeting preparation insights
- Rate limiting and error handling

#### **Screenshot Verification (`tools/screenshot_utils.py`)**
- Playwright-based screenshot capture
- LLM-powered visual verification
- Interface documentation automation
- Multi-resolution support

#### **Rules Management (`tools/promptcot_rules_integration.py`)**
- Task progress tracking
- Lesson categorization and storage
- Status report generation
- Workflow automation utilities

### 3. Workflow Integration

#### **Task Management Workflow**
```bash
# Add new task
python tools/promptcot_rules_integration.py --add-task "API Integration" "Complete Microsoft Graph integration"

# Update progress
python tools/promptcot_rules_integration.py --update-task "API Integration" completed

# List all tasks
python tools/promptcot_rules_integration.py --list-tasks
```

#### **Lessons Learned Workflow**
```bash
# Add technical lesson
python tools/promptcot_rules_integration.py --add-lesson technical "Ollama requires model verification before use"

# Add project lesson
python tools/promptcot_rules_integration.py --add-lesson project "Real data provides superior quality benchmarks"

# Add user lesson
python tools/promptcot_rules_integration.py --add-lesson user "Always test integration end-to-end"
```

#### **LLM Analysis Workflow**
```bash
# Analyze meeting scenario
python tools/llm_api.py --prompt "Analyze this strategic planning meeting for preparation requirements" --provider ollama

# Multi-provider fallback
python tools/llm_api.py --prompt "Meeting analysis request" --provider openai

# Vision analysis
python tools/llm_api.py --prompt "Describe this Scenara interface" --provider ollama --image screenshot.png
```

#### **Web Research Workflow**
```bash
# Search for best practices
python tools/search_engine.py "strategic planning meeting best practices" --max-results 5

# Scrape relevant content
python tools/web_scraper.py https://example.com/meeting-guide --extract-insights

# Industry-specific research
python tools/search_engine.py --industry "technology" --topic "digital transformation" --max-results 8
```

#### **Screenshot Verification Workflow**
```bash
# Capture Scenara interface
python tools/screenshot_utils.py http://localhost:8503 --output scenara_ui.png

# Capture with specific viewport
python tools/screenshot_utils.py http://localhost:8503 --width 1920 --height 1080 --wait 5

# Capture all interfaces
python tools/screenshot_utils.py http://localhost:8503 --meeting-interfaces --output-dir screenshots/
```

## Usage Examples

### Complete Analysis Workflow

```python
#!/usr/bin/env python3
"""Example: Complete meeting analysis workflow"""

import asyncio
from tools.llm_api import LLMAPIClient
from tools.search_engine import SearchEngine
from tools.promptcot_rules_integration import ScenaraRulesIntegration

async def analyze_meeting_scenario():
    # Initialize components
    llm_client = LLMAPIClient()
    rules = ScenaraRulesIntegration()
    
    # 1. Define meeting scenario
    scenario = """
    Executive Strategy Session - Q1 2026 Planning
    Attendees: C-suite executives, VPs
    Duration: 3 hours
    Goals: Strategic direction, budget allocation, market positioning
    """
    
    # 2. Research best practices
    async with SearchEngine() as search:
        research = await search.search_meeting_best_practices("executive strategy")
        print(f"Found {len(research)} relevant resources")
    
    # 3. LLM analysis
    analysis = llm_client.query_llm(
        f"Provide comprehensive preparation guide for:\n{scenario}",
        provider="ollama"
    )
    
    # 4. Update task progress
    rules.update_task_progress("Meeting Analysis Workflow", completed=True)
    
    # 5. Record lessons
    rules.update_lesson_learned(
        "project", 
        "Combined research and LLM analysis provides superior meeting preparation"
    )
    
    return analysis

# Run the workflow
if __name__ == "__main__":
    result = asyncio.run(analyze_meeting_scenario())
    print(result)
```

### Daily Development Workflow

```bash
#!/bin/bash
# Daily Scenara development workflow with XiadongLiu rules

# 1. Check current task status
echo "📋 Current Tasks:"
python tools/promptcot_rules_integration.py --list-tasks

# 2. Update environment
source .venv/bin/activate

# 3. Run any web research needed
python tools/search_engine.py "latest meeting intelligence trends" --max-results 3

# 4. Test LLM integration
python tools/llm_api.py --prompt "Test Scenara LLM integration" --provider ollama

# 5. Update progress and lessons
python tools/promptcot_rules_integration.py --update-task "Daily Development" completed
python tools/promptcot_rules_integration.py --add-lesson technical "Daily workflow automation improves consistency"

# 6. Generate status report
python tools/promptcot_rules_integration.py --status-report
```

## Best Practices

### 1. Task Management
- **Granular Tasks**: Break large features into specific, actionable items
- **Regular Updates**: Update progress after each major milestone
- **Clear Descriptions**: Include context and acceptance criteria
- **Priority Tracking**: Use task order to indicate priority

### 2. Lessons Learned
- **Immediate Capture**: Record lessons as soon as insights emerge
- **Categorization**: Use appropriate categories (technical, project, user)
- **Specific Details**: Include enough detail for future reference
- **Regular Review**: Periodically review lessons during planning

### 3. Tool Integration
- **Fallback Providers**: Always configure multiple LLM providers
- **Error Handling**: Implement robust error handling and logging
- **Rate Limiting**: Respect API limits and implement delays
- **Testing**: Test tools integration regularly

### 4. Workflow Automation
- **Script Common Patterns**: Automate frequently used tool combinations
- **Documentation**: Document complex workflows for team use
- **Version Control**: Track workflow changes and improvements
- **Monitoring**: Set up alerts for critical workflow failures

## Integration Benefits

### Enhanced Productivity
- **Systematic Task Tracking**: Never lose sight of project progress
- **Knowledge Retention**: Prevent repeating solved problems
- **Research Automation**: Quickly gather relevant context and insights
- **Quality Assurance**: Screenshot verification catches UI issues

### Improved Quality
- **Lesson Application**: Apply learned optimizations systematically
- **Multi-source Analysis**: Combine LLM, research, and screenshots
- **Fallback Reliability**: Multiple providers ensure system resilience
- **Documentation**: Automatic workflow documentation and reporting

### Team Collaboration
- **Shared Knowledge Base**: Centralized lessons and insights
- **Consistent Workflows**: Standardized development processes
- **Visual Verification**: Screenshots for design and feature validation
- **Progress Visibility**: Clear task and milestone tracking

## Troubleshooting

### Common Issues

#### Tool Import Errors
```bash
# Solution: Install requirements
pip install -r requirements_tools.txt
```

#### Ollama Connection Issues
```bash
# Solution: Verify Ollama is running and model available
ollama list
ollama pull gpt-oss:20b
```

#### Screenshot Capture Failures
```bash
# Solution: Install Playwright browsers
pip install playwright
playwright install chromium
```

#### Web Research Timeouts
```bash
# Solution: Reduce concurrent requests
python tools/web_scraper.py --max-concurrent 1 URL1 URL2
```

### Debugging Tips
- Check `.cursorrules` file for lesson updates
- Use `--json` flag for structured tool output
- Monitor stderr for debug information
- Test tools individually before workflow integration

## Future Enhancements

### Planned Improvements
- **AI-Powered Task Suggestions**: LLM-generated task breakdowns
- **Automated Research Summaries**: Context-aware research compilation
- **Visual Workflow Builder**: GUI for complex workflow creation
- **Integration Analytics**: Metrics on tool usage and effectiveness

### Extension Points
- **Custom Tool Integration**: Framework for adding new tools
- **Workflow Templates**: Pre-built workflows for common scenarios
- **Team Collaboration Features**: Multi-user task and lesson sharing
- **Performance Monitoring**: Tool usage analytics and optimization

---

**The Scenara rules integration transforms Scenara from a meeting intelligence platform into a comprehensive, self-improving development ecosystem that learns, adapts, and optimizes continuously.**