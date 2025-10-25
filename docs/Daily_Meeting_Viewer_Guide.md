# Scenara Daily Meeting Viewer Documentation

## Overview

The Scenara Daily Meeting Viewer is a powerful tool that retrieves and displays meetings for a specific date in beautiful, easy-to-read formats. It supports both real-time Microsoft Graph API integration and demo mode with sample data.

## Features

### 🎯 **Date-Specific Meeting Retrieval**
- Fetch meetings for any specific date using YYYYMMDD format (e.g., 20251020)
- Real-time Microsoft Graph API integration for live calendar data
- Demo mode using local calendar data for testing and demonstrations

### 🎨 **Multiple Output Formats**
- **Markdown (.md)**: Perfect for documentation and sharing
- **HTML (.html)**: Beautiful web page with modern styling
- **JSON (.json)**: Structured data for programmatic use
- **Console**: Rich terminal display with emojis and formatting

### 📊 **Comprehensive Meeting Information**
- Meeting times, duration, and scheduling details
- Attendee lists with response status (✅ Accepted, ❌ Declined, ❓ Tentative)
- Online meeting detection with join links
- Location information for in-person meetings
- Meeting importance levels and priorities
- Body preview and description text
- Direct links to Outlook for meeting management

### 📈 **Daily Summary Analytics**
- Total meeting count and duration
- Online vs. in-person meeting breakdown
- Meetings you're organizing vs. attending
- Time distribution and scheduling patterns

## Installation & Setup

### Dependencies
```bash
# Required for Graph API integration
pip install msal requests

# All dependencies are included in requirements_tools.txt
pip install -r requirements_tools.txt
```

### Authentication
Uses the same Microsoft Graph authentication as other Scenara tools:
- **Tenant ID**: `72f988bf-86f1-41af-91ab-2d7cd011db47`
- **Client ID**: `9ce97a32-d9ab-4ab2-aadc-f49b39b94e11`
- **Scopes**: `Calendars.Read`

## Usage Guide

### 📋 **Command Line Interface**

#### Basic Usage
```bash
# Get today's meetings (October 21, 2025)
python daily_meeting_viewer.py 20251021

# Specific date with custom format
python daily_meeting_viewer.py 20251020 --format html

# Console display only (no file output)
python daily_meeting_viewer.py 20251022 --console-only

# Save to custom filename
python daily_meeting_viewer.py 20251020 --output my_meetings.md

# Generate and auto-open in browser
python daily_meeting_viewer.py 20251020 --format html --open
```

#### Demo Mode (No Authentication Required)
```bash
# Demo version using local sample data
python demo_daily_meeting_viewer.py 20251020

# Demo with different output formats
python demo_daily_meeting_viewer.py 20251020 --format html
python demo_daily_meeting_viewer.py 20251020 --format json
python demo_daily_meeting_viewer.py 20251020 --console-only
```

### 🎨 **Output Format Examples**

#### Console Output
```
📅 Daily Meeting Schedule - October 21, 2025
============================================================
📊 Total meetings: 3

1. Scenara Project Review
   ⏰ 09:00 - 10:00 (1h 0m)
   🌐 Online Meeting
   👥 2 attendees
      (Alice Johnson, Bob Smith)
   🔴 High priority

2. Client Demo Preparation
   ⏰ 14:00 - 15:30 (1h 30m)
   📍 Conference Room A
   👥 3 attendees

📈 Summary:
   Total meeting time: 2h 30m
   Online meetings: 1
   You're organizing: 1
```

#### Markdown Output
```markdown
# 📅 Daily Meeting Schedule - October 21, 2025

## 1. Scenara Project Review

**⏰ Time:** 09:00 - 10:00 (1h 0m)  
**📍 Location:** 🌐 Online Meeting  
**🔗 Join Link:** [Join Meeting](https://teams.microsoft.com/meet/...)  
**👥 Attendees:** 2 people  
  - ✅ Alice Johnson, ❓ Bob Smith  
**Priority:** 🔴 High  

**📝 Description:**
> Weekly review of Scenara meeting intelligence platform progress...
```

#### HTML Output
Beautiful styled web page with:
- Modern responsive design
- Color-coded meeting types and priorities
- Interactive elements and hover effects
- Professional typography and spacing
- Meeting summaries and analytics

## Advanced Features

### 🔄 **Integration with Scenara Ecosystem**

#### With LLM Analysis
```python
from daily_meeting_viewer import ScenaraDailyMeetingViewer
from tools.llm_api import LLMAPIClient

viewer = ScenaraDailyMeetingViewer()
llm_client = LLMAPIClient()

# Get meetings for today
meetings = viewer.fetch_meetings_for_date(datetime.now())

# Analyze with AI
for meeting in meetings:
    analysis_prompt = f"Suggest preparation items for: {meeting['subject']}"
    suggestions = llm_client.query_llm(analysis_prompt, provider="ollama")
    print(f"Meeting: {meeting['subject']}")
    print(f"AI Suggestions: {suggestions}")
```

#### With Task Management
```python
from tools.promptcot_rules_integration import ScenaraRulesIntegration

rules = ScenaraRulesIntegration()

# Add preparation tasks for upcoming meetings
for meeting in today_meetings:
    if meeting['attendee_count'] > 3:  # Focus on team meetings
        task_name = f"Prepare for {meeting['subject']}"
        task_desc = f"Meeting at {meeting['start_time']} with {meeting['attendee_count']} attendees"
        rules.add_new_task(task_name, task_desc)
```

### 📊 **Date Range Analysis**
```bash
# Analyze multiple days
for date in 20251020 20251021 20251022; do
    python daily_meeting_viewer.py $date --console-only
done
```

### 🔄 **Automated Daily Reports**
```bash
#!/bin/bash
# Daily meeting report automation

DATE=$(date +%Y%m%d)
python daily_meeting_viewer.py $DATE --format html --output "daily_meetings_$(date +%Y%m%d).html"
python daily_meeting_viewer.py $DATE --format md --output "daily_meetings_$(date +%Y%m%d).md"

echo "Daily meeting reports generated for $DATE"
```

## API Reference

### Date Format
- **Input**: `YYYYMMDD` (8 digits)
- **Examples**: 
  - `20251020` → October 20, 2025
  - `20251231` → December 31, 2025

### Output Formats
- **`md`**: Markdown format, perfect for documentation
- **`html`**: Styled web page with modern design
- **`json`**: Structured data for programmatic processing
- **Console**: Rich terminal display (always shown)

### Command Line Options
```
positional arguments:
  date                  Date in format YYYYMMDD

optional arguments:
  --format {md,html,json}    Output format (default: md)
  --output OUTPUT           Custom output filename
  --console-only            Only display in console, don't save file
  --open                    Open generated file after creation
```

## Use Cases

### 📋 **Daily Planning**
```bash
# Morning routine: Check today's meetings
python daily_meeting_viewer.py $(date +%Y%m%d) --console-only
```

### 📄 **Meeting Documentation**
```bash
# Generate shareable meeting schedule
python daily_meeting_viewer.py 20251020 --format html --open
```

### 📊 **Weekly Review**
```bash
# Generate weekly meeting summary
for i in {0..6}; do
    date=$(date -d "+$i day" +%Y%m%d)
    python daily_meeting_viewer.py $date --format md --output "week_${date}.md"
done
```

### 🔄 **Integration Workflows**
```bash
# Automated meeting preparation pipeline
python daily_meeting_viewer.py $(date +%Y%m%d) --format json > today_meetings.json
python tools/llm_api.py --prompt "Analyze meetings from today_meetings.json" --provider ollama
```

## Comparison: Live vs Demo Versions

| Feature | `daily_meeting_viewer.py` | `demo_daily_meeting_viewer.py` |
|---------|---------------------------|--------------------------------|
| **Data Source** | Microsoft Graph API (live) | Local sample data |
| **Authentication** | Required (interactive) | None required |
| **Meeting Data** | Real calendar events | Simulated/sample meetings |
| **Use Case** | Production daily use | Testing and demonstrations |
| **Output Quality** | Complete real data | Representative examples |

## Troubleshooting

### Authentication Issues
```bash
# Clear cached credentials
rm -rf ~/.cache/msal_token_cache/
python daily_meeting_viewer.py 20251021
```

### No Meetings Found
- Check date format (must be YYYYMMDD)
- Verify you have calendar events for the specified date
- Ensure correct Microsoft Graph permissions

### File Output Issues
```bash
# Check output directory permissions
ls -la meeting_outputs/
mkdir -p meeting_outputs
```

## Best Practices

### 🕐 **Daily Workflow**
1. **Morning Check**: Run with `--console-only` for quick overview
2. **Detailed Planning**: Generate HTML for thorough review
3. **Sharing**: Use Markdown for team communication
4. **Data Analysis**: Export JSON for programmatic processing

### 📱 **Mobile-Friendly HTML**
The generated HTML is responsive and works well on:
- Desktop browsers
- Mobile devices
- Tablet screens
- Print layouts

### 🔄 **Automation Integration**
- Add to crontab for daily reports
- Integrate with CI/CD pipelines
- Use in meeting preparation workflows
- Combine with other Scenara tools

This tool transforms the way you view and manage daily meetings, providing beautiful, actionable insights for better meeting preparation and time management! 🚀