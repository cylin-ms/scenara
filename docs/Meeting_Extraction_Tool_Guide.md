# Scenara Meeting Extraction Tool Documentation

## Overview

The Scenara Meeting Extraction Tool (`tools/meeting_extractor.py`) is a comprehensive utility for retrieving and processing meeting data from multiple sources for meeting intelligence analysis. It provides unified access to Microsoft Graph Calendar API, MEvals meeting evaluation system, local calendar exports, and existing meeting preparation scenarios.

## Features

### 🔍 **Multi-Source Meeting Extraction**
- **Microsoft Graph API**: Direct calendar access with authentication
- **MEvals Integration**: Leverages existing MEvals fetch_meetings.py infrastructure  
- **Local JSON Files**: Process Graph Explorer calendar exports
- **Meeting Prep Scenarios**: Extract from existing scenario databases

### 📊 **Data Processing & Analysis**
- Standardized meeting object format across all sources
- Automatic meeting type classification (1:1, project, review, training, etc.)
- Attendee analysis and contact extraction
- Duration and scheduling pattern analysis
- Duplicate detection and deduplication

### 💾 **Output Formats**
- JSON export with metadata and statistics
- Summary analytics and insights
- Timestamped extraction logs
- Source attribution and traceability

## Installation & Dependencies

### Required Dependencies
```bash
# Core dependencies (already in requirements_tools.txt)
pip install msal requests

# Optional for enhanced functionality
pip install python-dateutil tzlocal
```

### Authentication Setup
The tool uses the same Microsoft Graph authentication as MEvals:
- **Tenant ID**: `72f988bf-86f1-41af-91ab-2d7cd011db47` (Microsoft)
- **Client ID**: `9ce97a32-d9ab-4ab2-aadc-f49b39b94e11` (MEvals app)
- **Scopes**: `Calendars.Read`

## Usage Guide

### 📋 **Command Line Interface**

#### List Available Data Sources
```bash
python tools/meeting_extractor.py --list-sources
```

#### Extract from All Sources
```bash
python tools/meeting_extractor.py --source all
```

#### Extract from Specific Source
```bash
# Local JSON files (Graph Explorer exports)
python tools/meeting_extractor.py --source local

# MEvals system
python tools/meeting_extractor.py --source mevals

# Microsoft Graph API (requires authentication)
python tools/meeting_extractor.py --source graph

# Meeting preparation scenarios
python tools/meeting_extractor.py --source scenarios
```

#### Custom Time Range (Graph API)
```bash
# Last 60 days, next 30 days
python tools/meeting_extractor.py --source graph --days-back 60 --days-forward 30
```

#### Specific Local File
```bash
python tools/meeting_extractor.py --source local --file-path my_calendar_events.json
```

#### Summary Only (No File Output)
```bash
python tools/meeting_extractor.py --summary-only
```

#### Custom Output File
```bash
python tools/meeting_extractor.py --output my_meetings_analysis.json
```

### 🐍 **Python API Usage**

#### Basic Extraction
```python
from tools.meeting_extractor import ScenearaMeetingExtractor

# Initialize extractor
extractor = ScenearaMeetingExtractor()

# Extract from local JSON files
meetings = extractor.extract_from_local_json()

# Extract from Graph API
meetings = extractor.extract_from_graph_api(days_back=30, days_forward=14)

# Generate summary
summary = extractor.generate_meeting_summary(meetings)
print(f"Found {summary['total_meetings']} meetings")
```

#### Advanced Processing
```python
# Check available sources
sources = extractor.get_available_sources()
for source_name, info in sources.items():
    if info['available']:
        print(f"✅ {source_name}: {info['description']}")

# Extract from multiple sources
all_meetings = []

# Local files
try:
    local_meetings = extractor.extract_from_local_json()
    all_meetings.extend(local_meetings)
except Exception as e:
    print(f"Local extraction failed: {e}")

# Graph API
try:
    graph_meetings = extractor.extract_from_graph_api()
    all_meetings.extend(graph_meetings)
except Exception as e:
    print(f"Graph extraction failed: {e}")

# Save results
output_path = extractor.save_extracted_meetings(all_meetings)
print(f"Saved to: {output_path}")
```

#### Integration with Scenara LLM
```python
from tools.meeting_extractor import ScenearaMeetingExtractor
from tools.llm_api import LLMAPIClient

# Extract meetings
extractor = ScenearaMeetingExtractor()
meetings = extractor.extract_from_local_json()

# Analyze with LLM
llm_client = LLMAPIClient()

for meeting in meetings[:5]:  # Analyze first 5 meetings
    prompt = f"""
    Analyze this meeting for preparation insights:
    
    Subject: {meeting['subject']}
    Type: {meeting['meeting_type']}
    Duration: {meeting['duration_minutes']} minutes
    Attendees: {meeting['attendee_count']} people
    
    Provide preparation recommendations.
    """
    
    analysis = llm_client.query_llm(prompt, provider="ollama")
    print(f"Meeting: {meeting['subject']}")
    print(f"Analysis: {analysis[:200]}...")
    print("-" * 50)
```

## Data Structure

### Standardized Meeting Object
```json
{
  "id": "unique_meeting_identifier",
  "subject": "Meeting Title",
  "start_time": "2025-10-21T15:00:00Z",
  "end_time": "2025-10-21T16:00:00Z",
  "duration_minutes": 60,
  "attendees": [
    {
      "name": "John Doe",
      "email": "john@company.com",
      "response": "accepted"
    }
  ],
  "attendee_count": 3,
  "body_preview": "Meeting description or agenda",
  "is_online_meeting": true,
  "meeting_type": "project_management",
  "is_organizer": false,
  "location": "Conference Room A",
  "importance": "normal",
  "source": "microsoft_graph",
  "extracted_at": "2025-10-21T14:30:00Z"
}
```

### Output File Format
```json
{
  "metadata": {
    "extraction_timestamp": "2025-10-21T14:30:00Z",
    "total_meetings": 45,
    "meeting_types": {
      "one_on_one": 12,
      "project_management": 8,
      "team_meeting": 10,
      "client_meeting": 5,
      "training": 3,
      "review": 4,
      "general": 3
    },
    "sources": ["microsoft_graph", "local_json"]
  },
  "meetings": [
    // Array of meeting objects
  ]
}
```

## Meeting Type Classification

The tool automatically classifies meetings into types based on subject, description, and attendee patterns:

| Type | Triggers | Description |
|------|----------|-------------|
| `one_on_one` | ≤2 attendees + "1-1", "one-on-one", "1:1" | Personal meetings |
| `project_management` | "project", "sprint", "scrum", "standup", "planning" | Project coordination |
| `review` | "review", "feedback", "retrospective" | Evaluation meetings |
| `training` | "training", "workshop", "demo", "presentation" | Learning sessions |
| `team_meeting` | "team", "all hands", "sync" | Team coordination |
| `client_meeting` | "client", "customer", "external" | External stakeholder meetings |
| `general` | Default for unclassified meetings | Standard meetings |

## Integration Scenarios

### 🔧 **Scenara Workflow Integration**

#### 1. Real-time Meeting Preparation
```python
# Daily meeting extraction and preparation
extractor = ScenearaMeetingExtractor()
today_meetings = extractor.extract_from_graph_api(days_back=0, days_forward=1)

for meeting in today_meetings:
    if meeting['start_time'].startswith('2025-10-21'):  # Today's meetings
        # Generate preparation materials
        prep_prompt = f"Create agenda for {meeting['subject']} with {meeting['attendee_count']} attendees"
        # ... LLM processing
```

#### 2. Historical Meeting Analysis
```python
# Analyze meeting patterns
extractor = ScenearaMeetingExtractor()
historical_meetings = extractor.extract_from_local_json()

summary = extractor.generate_meeting_summary(historical_meetings)
print(f"Most common meeting type: {max(summary['meeting_types'], key=summary['meeting_types'].get)}")
```

#### 3. Meeting Intelligence Pipeline
```python
# Full pipeline integration
from tools.promptcot_rules_integration import ScenaraRulesIntegration

extractor = ScenearaMeetingExtractor()
rules = ScenaraRulesIntegration()

# Extract meetings
meetings = extractor.extract_from_graph_api()

# Add task to track meeting preparation
rules.add_new_task(
    f"Prepare for {len(meetings)} upcoming meetings",
    "Generate preparation materials and agenda items"
)

# Process each meeting
for meeting in meetings:
    # ... preparation logic
    pass

# Mark task complete
rules.update_task_progress("Prepare for upcoming meetings", completed=True)
```

## Advanced Features

### 🔍 **Source Detection**
The tool automatically detects available meeting sources:
- Scans for `my_calendar_events*.json` files
- Checks MEvals directory structure
- Validates Graph API connectivity
- Inventories meeting preparation scenario files

### 📊 **Analytics & Reporting**
- Meeting frequency patterns
- Attendee network analysis  
- Duration distribution statistics
- Meeting type trend analysis
- Source reliability metrics

### ⚡ **Performance Optimization**
- Lazy loading of large datasets
- Efficient duplicate detection
- Streaming JSON processing for large files
- Configurable pagination for Graph API

## Error Handling & Troubleshooting

### Common Issues

#### Authentication Errors
```bash
# Error: "Authentication failed"
# Solution: Clear cached credentials
rm -rf ~/.cache/msal_token_cache/
python tools/meeting_extractor.py --source graph
```

#### Missing Dependencies
```bash
# Error: "No module named 'msal'"
# Solution: Install requirements
pip install -r requirements_tools.txt
```

#### Graph API Rate Limits
```bash
# Error: "Too Many Requests"
# Solution: Reduce time range
python tools/meeting_extractor.py --source graph --days-back 7 --days-forward 7
```

#### MEvals Integration Issues
```bash
# Error: "MEvals directory not found"
# Solution: Ensure MEvals is properly set up
ls -la MEvals/fetch_meetings.py
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

extractor = ScenearaMeetingExtractor()
# Detailed logging will show API calls and processing steps
```

## Best Practices

### 🔒 **Security**
- Never commit authentication tokens
- Use environment variables for sensitive configuration
- Regularly rotate API credentials
- Audit access logs periodically

### 📈 **Performance**
- Use specific time ranges for large calendars
- Cache results for repeated analysis
- Implement incremental updates for regular extractions
- Monitor API quota usage

### 🔄 **Data Management**
- Regular backups of extracted meeting data
- Version control for meeting preparation templates
- Automated cleanup of old extraction files
- Data retention policy compliance

## Example Workflows

### Daily Meeting Intelligence
```bash
#!/bin/bash
# Daily meeting preparation script

# Extract today's meetings
python tools/meeting_extractor.py --source graph --days-back 0 --days-forward 1 --output today_meetings.json

# Generate preparation materials (integrate with LLM)
python tools/llm_api.py --prompt "Analyze today's meetings from today_meetings.json" --provider ollama

# Update Scenara task tracker
python tools/promptcot_rules_integration.py --add-lesson user "Daily meeting extraction automated"
```

### Weekly Analytics
```bash
#!/bin/bash
# Weekly meeting pattern analysis

# Extract last week's meetings
python tools/meeting_extractor.py --source all --days-back 7 --days-forward 0 --output weekly_analysis.json

# Generate summary report
python tools/meeting_extractor.py --source local --file-path weekly_analysis.json --summary-only
```

### Meeting Preparation Automation
```python
#!/usr/bin/env python3
# Automated meeting preparation pipeline

from tools.meeting_extractor import ScenearaMeetingExtractor
from tools.llm_api import LLMAPIClient

def prepare_meetings():
    extractor = ScenearaMeetingExtractor()
    llm_client = LLMAPIClient()
    
    # Get upcoming meetings
    upcoming = extractor.extract_from_graph_api(days_back=0, days_forward=3)
    
    for meeting in upcoming:
        if meeting['attendee_count'] > 2:  # Focus on team meetings
            prep_prompt = f"""
            Prepare agenda for meeting: {meeting['subject']}
            Duration: {meeting['duration_minutes']} minutes
            Attendees: {meeting['attendee_count']} people
            Type: {meeting['meeting_type']}
            
            Provide:
            1. Suggested agenda items
            2. Time allocation
            3. Preparation materials needed
            4. Key discussion points
            """
            
            agenda = llm_client.query_llm(prep_prompt, provider="ollama")
            print(f"=== {meeting['subject']} ===")
            print(agenda)
            print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    prepare_meetings()
```

## Integration with Other Scenara Tools

The Meeting Extractor integrates seamlessly with other Scenara tools:

- **LLM API** (`tools/llm_api.py`): Meeting content analysis and preparation
- **Rules Integration** (`tools/promptcot_rules_integration.py`): Task tracking and lessons learned
- **Web Scraper** (`tools/web_scraper.py`): Research meeting topics and attendees
- **Search Engine** (`tools/search_engine.py`): Find relevant meeting preparation resources
- **Screenshot Utils** (`tools/screenshot_utils.py`): Document meeting interfaces and tools

This comprehensive meeting extraction capability transforms Scenara from a meeting preparation tool into a complete meeting intelligence platform! 🚀