# Scenara 2.0 Tools Inventory

**Last Updated**: October 25, 2025  
**Version**: 2.0  
**Location**: `/Users/cyl/projects/Scenara/tools/`

## Overview

This directory contains specialized tools for the Scenara 2.0 meeting intelligence system. Each tool is designed to accomplish specific tasks related to meeting analysis, collaboration discovery, and AI-powered insights.

---

## 🤝 **Collaboration & Meeting Analysis Tools**

### 1. **Collaborator Discovery Tool** 
**File**: `collaborator_discovery.py`  
**Purpose**: Discover and rank professional collaborators from most important to least important using Enterprise Meeting Taxonomy.

**Key Features**:
- Enterprise Meeting Taxonomy integration
- Genuine collaboration vs information consumption distinction
- Email list pattern detection (filters bulk invitations)
- Multi-factor importance scoring
- Confidence assessment for each collaborator

**Usage**:
```bash
# Basic usage
python tools/collaborator_discovery.py

# With custom data and user
python tools/collaborator_discovery.py --calendar-data "path/to/calendar.json" --user-name "Your Name"

# Limit results and specify output
python tools/collaborator_discovery.py --limit 10 --output "my_collaborators.json"

# Quiet mode (no summary)
python tools/collaborator_discovery.py --quiet
```

**Input**: Calendar data JSON file with meeting events  
**Output**: Ranked list of collaborators with importance scores, evidence, and analysis

**Algorithm**: Enhanced Collaboration Algorithm v4.2 with Enterprise Taxonomy integration

**Use Cases**:
- Identify key professional relationships
- Prioritize collaboration efforts
- Prepare for meetings with important collaborators
- Generate Me Notes about professional network
- Validate collaboration assumptions (e.g., filter false positives like Jason Virtue)

**⚠️ Critical Limitation**: Calendar-only analysis misses Teams chat collaborations. For comprehensive analysis including daily chat patterns, use `enhanced_collaborator_discovery_v5.py`.

**Example**: Xiaodong Liu may not appear in calendar-based results despite frequent Teams chat collaboration. Chat integration reveals true collaboration intensity.

---

### 2b. **Enhanced Collaborator Discovery v5.0 (Chat Integration)**
**File**: `enhanced_collaborator_discovery_v5.py`  
**Purpose**: Complete collaborator discovery combining calendar meetings + Microsoft Teams chat activity.

**Key Innovation**: Addresses the major blind spot of calendar-only analysis by incorporating Teams chat data.

**Features**:
- **Hybrid Data Sources**: Calendar meetings + Teams chat frequency
- **Manual Chat Input**: When API access unavailable (Chat.Read permissions)
- **Data Source Transparency**: Shows calendar-only vs chat-enhanced vs chat-only collaborators  
- **False Negative Prevention**: Identifies chat-heavy collaborators missed by calendar analysis
- **Weighted Scoring**: Daily chats weighted heavily as indicator of active collaboration

**Critical Use Cases**:
- Collaborators who primarily use Teams chat (e.g., Xiaodong Liu with 5 daily messages)
- Cross-timezone colleagues who rely on async chat
- Daily operational partners who don't schedule formal meetings
- Informal mentoring relationships conducted via chat

**Manual Chat Data Setup**:
```python
discovery.add_manual_chat_collaborator(
    name="Xiaodong Liu",
    daily_chats=5,          # Average daily messages  
    weekly_group_chats=3,   # Group chat participation
    relationship_strength=1  # 1=Essential, 2=Regular, 3=Occasional
)
```

**Impact Example**: Xiaodong Liu ranks #1 collaborator (611.5 score) with chat data vs not appearing at all in calendar-only analysis.

---

### 2. **Meeting Classifier Tool**
**File**: `meeting_classifier.py`  
**Purpose**: Classify meetings using LLM-based analysis with Ollama gpt-oss:20b model.

**Key Features**:
- Uses local Ollama LLM (gpt-oss:20b) for classification
- Enterprise Meeting Taxonomy support
- Context-aware analysis (attendees, duration, description)
- Fallback to keyword-based classification
- High accuracy through AI reasoning

**Usage**:
```python
from tools.meeting_classifier import OllamaLLMMeetingClassifier

classifier = OllamaLLMMeetingClassifier(model_name="gpt-oss:20b")

result = classifier.classify_meeting_with_llm(
    subject="Q3 Sprint Planning",
    description="Planning for the next quarter development sprint",
    attendees=["john@company.com", "sarah@company.com"],
    duration_minutes=120
)

print(f"Category: {result['primary_category']}")
print(f"Type: {result['specific_type']}")
print(f"Confidence: {result['confidence']}")
```

**Input**: Meeting subject, description, attendees, duration  
**Output**: Meeting classification with category, type, confidence, and reasoning

**Meeting Categories**:
- Strategic Planning & Decision
- Internal Recurring (Cadence)
- External & Client-Facing
- Informational & Broadcast
- Team-Building & Culture

**Use Cases**:
- Automatically categorize calendar events
- Improve meeting preparation with context-aware suggestions
- Analyze meeting patterns and effectiveness
- Generate meeting-type specific insights
- Support collaboration analysis with accurate meeting classification

---

## 🧠 **AI & LLM Integration Tools**

### 3. **LLM API Client**
**File**: `llm_api.py`  
**Purpose**: Unified interface for multiple LLM providers (Ollama, OpenAI, Anthropic, Azure).

**Features**:
- Multi-provider support
- Consistent API interface
- Error handling and fallbacks
- Model selection and configuration

**Usage**:
```python
from tools.llm_api import LLMAPIClient

client = LLMAPIClient()
response = client.query_llm(
    prompt="Analyze this meeting pattern...",
    provider="ollama",
    model="gpt-oss:20b"
)
```

---

## 📅 **Meeting & Calendar Tools**

### 4. **Meeting Extractor**
**File**: `meeting_extractor.py`  
**Purpose**: Extract and process meeting data from various sources.

**Features**:
- Calendar event parsing
- Meeting context extraction
- Data normalization
- Format conversion

---

### 5. **Daily Interaction Logger**
**File**: `daily_interaction_logger.py`  
**Purpose**: Log and track daily meeting interactions for analysis.

**Features**:
- Interaction tracking
- Pattern recognition
- Behavioral analysis
- Data persistence

---

## 🔧 **Utility Tools**

### 6. **Platform Detection**
**File**: `platform_detection.py`  
**Purpose**: Detect operating system and platform-specific configurations.

**Features**:
- OS detection
- Environment configuration
- Platform-specific recommendations
- Cross-platform compatibility

---

### 7. **Screenshot Utils**
**File**: `screenshot_utils.py`  
**Purpose**: Capture and process screenshots for meeting analysis.

**Features**:
- Screen capture
- Image processing
- OCR capabilities
- Meeting context extraction

---

### 8. **Search Engine**
**File**: `search_engine.py`  
**Purpose**: Search and retrieve information from various sources.

**Features**:
- Multi-source search
- Content indexing
- Relevance ranking
- Query processing

---

### 9. **Web Scraper**
**File**: `web_scraper.py`  
**Purpose**: Extract information from web sources for meeting intelligence.

**Features**:
- Web content extraction
- Data cleaning
- Format standardization
- Rate limiting

---

### 10. **PromptCoT Rules Integration**
**File**: `promptcot_rules_integration.py`  
**Purpose**: Integration with PromptCoT reasoning framework.

**Features**:
- Chain-of-thought processing
- Rule-based reasoning
- Context management
- Decision support

---

## 🚀 **Quick Start Guide**

### Prerequisites
1. **Python Environment**: Ensure Python 3.8+ with required dependencies
2. **Ollama Setup**: Install Ollama and pull gpt-oss:20b model for LLM tools
3. **Calendar Data**: Have meeting/calendar data in JSON format

### Installation
```bash
# Navigate to Scenara project directory
cd /Users/cyl/projects/Scenara

# Install dependencies
pip install -r requirements.txt

# Verify Ollama model (for LLM tools)
ollama pull gpt-oss:20b
```

### Basic Workflow

1. **Discover Collaborators**:
```bash
python tools/collaborator_discovery.py --limit 5
```

2. **Classify Meetings**:
```python
from tools.meeting_classifier import OllamaLLMMeetingClassifier
classifier = OllamaLLMMeetingClassifier()
result = classifier.classify_meeting_with_llm("Team Planning Session", "...")
```

3. **Integrate with Me Notes**:
The tools are designed to integrate with the main Me Notes generation system in `generate_real_me_notes.py`.

---

## 📊 **Tool Integration Matrix**

| Tool | Input | Output | Dependencies | Use Case |
|------|-------|--------|--------------|----------|
| `collaborator_discovery.py` | Calendar JSON | Ranked collaborators | None | Relationship analysis |
| `meeting_classifier.py` | Meeting details | Classification | Ollama | Meeting categorization |
| `llm_api.py` | Text prompts | LLM responses | Multiple LLM providers | AI integration |
| `meeting_extractor.py` | Raw meeting data | Structured data | None | Data processing |
| `platform_detection.py` | System info | Platform config | None | Environment setup |

---

## 🎯 **Best Practices**

### For Collaboration Discovery
1. **Use Recent Data**: Calendar data should be recent for accurate collaboration patterns
2. **Validate Results**: Always review high-confidence collaborators for accuracy
3. **Filter System Accounts**: The tool automatically filters system accounts, but verify edge cases
4. **Consider Context**: Use collaboration evidence to understand relationship nature

### For Meeting Classification
1. **Provide Context**: Include meeting description and attendee information for better accuracy
2. **Verify LLM Results**: Check classification results, especially for edge cases
3. **Use Fallback**: Keyword-based fallback ensures classification even if LLM fails
4. **Model Consistency**: Use consistent LLM model (gpt-oss:20b) for comparable results

### General Guidelines
1. **Data Quality**: Ensure input data is clean and well-formatted
2. **Error Handling**: Tools include error handling, but monitor for edge cases
3. **Performance**: LLM tools may take time; use appropriately sized datasets
4. **Privacy**: Be mindful of sensitive meeting data when using external LLM providers

---

## 🔮 **Future Enhancements**

### Planned Features
- **Real-time Integration**: Live calendar integration for continuous analysis
- **Advanced Analytics**: Deeper meeting pattern analysis and insights
- **Multi-user Support**: Analysis across multiple users and teams
- **Custom Taxonomies**: Support for organization-specific meeting classifications
- **API Endpoints**: REST API for tool integration with other systems

### Enhancement Requests
- **Sentiment Analysis**: Meeting tone and collaboration quality assessment
- **Predictive Analytics**: Forecast collaboration patterns and meeting effectiveness
- **Integration APIs**: Direct integration with Microsoft Graph, Google Calendar
- **Dashboard UI**: Web interface for tool management and visualization
- **Batch Processing**: Support for large-scale meeting data analysis

---

## 📚 **References**

- **Enterprise Meeting Taxonomy**: `/Users/cyl/projects/Scenara/docs/Enterprise_Meeting_Taxonomy.md`
- **Algorithm Documentation**: Enhanced Collaboration Algorithm v4.2 with Enterprise Taxonomy
- **Ollama Documentation**: https://ollama.ai/
- **Meeting Intelligence Framework**: Scenara 2.0 Architecture

---

## 🤝 **Contributing**

When adding new tools to this directory:

1. **Follow Naming Convention**: Use descriptive names with underscores
2. **Include Documentation**: Add comprehensive docstrings and comments
3. **Update Inventory**: Update this README with tool description and usage
4. **Test Integration**: Ensure tools work with existing Scenara components
5. **Error Handling**: Include proper error handling and fallback mechanisms

---

## 📞 **Support**

For questions about these tools:
- **Documentation**: Check individual tool docstrings and comments
- **Examples**: Review usage examples in each tool's main() function
- **Integration**: See `generate_real_me_notes.py` for integration patterns
- **Issues**: Test with sample data and check error messages

---

*This inventory serves as the definitive guide for Scenara 2.0 tools. Keep it updated as new tools are added or existing tools are modified.*