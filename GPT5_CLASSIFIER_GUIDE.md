# GPT-5 Meeting Classifier Integration

## Overview

New enterprise meeting classifier using Microsoft's **GPT-5 (dev-gpt-5-chat-jj)** model via SilverFlow LLM API. This provides an alternative to the Ollama-based classifier with potentially higher accuracy and enterprise-grade infrastructure.

## Files Created

### 1. `tools/meeting_classifier_gpt5.py` (770 lines)
**GPT5MeetingClassifier** - Main classifier implementation

**Key Features**:
- ✅ Uses Microsoft's dev-gpt-5-chat-jj model
- ✅ MSAL authentication with Azure AD
- ✅ Same Enterprise Meeting Taxonomy (31+ types, 5 categories)
- ✅ Fallback to keyword-based classification
- ✅ Low temperature (0.1) for consistent classification
- ✅ Token caching for performance
- ✅ Comprehensive error handling

**Architecture**:
```
GPT5MeetingClassifier
├── __init__(model, endpoint, app_id, scopes, access_token)
├── test_model_availability() → bool
├── classify_meeting_with_llm() → Dict[str, Any]
├── classify_meeting() → Dict[str, Any]
├── _acquire_token() → Optional[str]
├── _call_gpt5_api() → ClassificationResult
├── _prepare_meeting_context() → str
├── _create_classification_prompt() → str
├── _parse_llm_response() → Dict[str, Any]
└── _fallback_classification() → Dict[str, Any]
```

### 2. `compare_classifiers.py` (450 lines)
**ClassifierComparison** - Side-by-side comparison tool

**Features**:
- ✅ Tests both Ollama and GPT-5 classifiers
- ✅ 10 comprehensive test cases covering all categories
- ✅ Performance metrics (latency, confidence, accuracy)
- ✅ Agreement rate analysis
- ✅ Detailed JSON report generation
- ✅ Visual comparison output

## Usage Examples

### Quick Start - GPT-5 Classifier

```python
from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier

# Initialize classifier
classifier = GPT5MeetingClassifier()

# Test availability
if classifier.test_model_availability():
    print("✅ GPT-5 ready")

# Classify a meeting
result = classifier.classify_meeting(
    subject="Weekly Team Standup",
    description="Quick sync on sprint progress",
    attendees=["Alice", "Bob", "Charlie"],
    duration_minutes=15
)

print(f"Type: {result['specific_type']}")
print(f"Category: {result['primary_category']}")
print(f"Confidence: {result['confidence']:.1%}")
print(f"Reasoning: {result['reasoning']}")
```

### Run Demo

```bash
# Demo GPT-5 classifier with 4 test meetings
python tools/meeting_classifier_gpt5.py
```

### Compare Both Classifiers

```bash
# Run comprehensive comparison (10 test cases)
python compare_classifiers.py
```

**Output**:
- Console: Real-time comparison results
- File: `data/evaluation_results/classifier_comparison_YYYYMMDD_HHMMSS.json`

## Authentication

### MSAL Interactive Login

GPT-5 classifier uses **Microsoft Authentication Library (MSAL)** with:
- **Tenant ID**: 72f988bf-86f1-41af-91ab-2d7cd011db47
- **App ID**: 942b706f-826e-426b-98f7-59e1e376b37c
- **Scopes**: https://substrate.office.com/llmapi/LLMAPI.dev
- **Broker**: Windows integrated authentication (WAM)

**First Run**:
1. Script will open browser for Microsoft login
2. Authenticate with your Microsoft account
3. Token is cached for subsequent requests
4. Silent token refresh when expired

**Provide Token Manually**:
```python
classifier = GPT5MeetingClassifier(
    access_token="your_bearer_token_here"
)
```

## API Configuration

### SilverFlow LLM API

**Default Endpoint**: `https://fe-26.qas.bing.net/chat/completions`

**Model**: `dev-gpt-5-chat-jj`

**Request Parameters**:
```json
{
  "messages": [
    {"role": "system", "content": "..."},
    {"role": "user", "content": "..."}
  ],
  "temperature": 0.1,
  "top_p": 0.95,
  "max_completion_tokens": 2048,
  "presence_penalty": 0,
  "frequency_penalty": 0
}
```

**Headers**:
```http
Authorization: Bearer <token>
X-ModelType: dev-gpt-5-chat-jj
X-ScenarioGUID: <uuid>
Content-Type: application/json
```

### Timeouts
- **Connect**: 10 seconds
- **Read**: 60 seconds (configurable)

## Classification Response Format

### Success Response

```json
{
  "specific_type": "One-on-One Meeting",
  "primary_category": "Internal Recurring (Cadence)",
  "confidence": 0.95,
  "reasoning": "Subject and 2-person attendee count clearly indicate 1:1 meeting"
}
```

### Fallback Response

```json
{
  "specific_type": "Team Status Update/Standup",
  "primary_category": "Internal Recurring (Cadence)",
  "confidence": 0.6,
  "reasoning": "Keyword-based classification (fallback mode)"
}
```

## Comparison Results Structure

```json
{
  "timestamp": "2025-10-26 12:00:00",
  "summary": {
    "total_tests": 10,
    "ollama": {
      "success_rate": 1.0,
      "accuracy": 0.9,
      "avg_confidence": 0.87,
      "avg_latency": 2.3
    },
    "gpt5": {
      "success_rate": 1.0,
      "accuracy": 0.95,
      "avg_confidence": 0.92,
      "avg_latency": 1.8
    },
    "agreement_rate": 0.85
  },
  "detailed_results": [...]
}
```

## Enterprise Meeting Taxonomy

Both classifiers use the same taxonomy:

### 1. Strategic Planning & Decision (8 types)
- Strategic Planning Session
- Decision-Making Meeting
- Problem-Solving Meeting
- Brainstorming Session
- Workshop/Design Session
- Budget Planning Meeting
- Project Planning Meeting
- Risk Assessment Meeting

### 2. Internal Recurring (Cadence) (7 types)
- Team Status Update/Standup
- Progress Review Meeting
- One-on-One Meeting
- Team Retrospective
- Governance/Leadership Meeting
- Performance Review
- Weekly/Monthly Check-in

### 3. External & Client-Facing (7 types)
- Sales & Client Meeting
- Vendor/Supplier Meeting
- Partnership Meeting
- Interview Meeting
- Client Training/Onboarding
- Customer Discovery Call
- Contract Negotiation

### 4. Informational & Broadcast (7 types)
- All-Hands/Town Hall
- Informational Briefing
- Training Session
- Webinar/Presentation
- Knowledge Sharing Session
- Product Demo
- Announcement Meeting

### 5. Team-Building & Culture (6 types)
- Team-Building Activity
- Recognition/Celebration Event
- Social/Networking Event
- Community Meeting
- Offsite/Retreat
- Welcome/Farewell Event

## Performance Expectations

### GPT-5 Advantages
- ✅ **Claimed 97-99% accuracy** (from taxonomy documentation)
- ✅ **Enterprise infrastructure** (Microsoft-hosted)
- ✅ **Lower latency** (~1-2s vs 2-3s for Ollama)
- ✅ **Better context understanding** (GPT-5 vs GPT-OSS 20B)
- ✅ **Production-ready** SilverFlow API

### Ollama Advantages
- ✅ **Local deployment** (no external API dependency)
- ✅ **No authentication** required
- ✅ **Privacy** (data stays local)
- ✅ **Free** (no API costs)
- ✅ **Offline support**

## Integration into Collaborator Discovery

### Current State
`tools/collaborator_discovery.py` uses **keyword-based** classification:

```python
def classify_meeting_type(self, subject: str, attendee_count: int, 
                         organizer: str, has_email_list: bool):
    # Simple keyword matching
    if attendee_count == 2:
        return 'one_on_one', 'Internal Recurring - One-on-One Meetings'
    # ... more keyword rules
```

### Recommended Enhancement

```python
from tools.meeting_classifier_gpt5 import GPT5MeetingClassifier

class CollaboratorDiscovery:
    def __init__(self):
        # Initialize GPT-5 classifier
        self.meeting_classifier = GPT5MeetingClassifier()
        self.use_llm_classifier = self.meeting_classifier.test_model_availability()
        
        if self.use_llm_classifier:
            print("✅ Using GPT-5 for meeting classification")
        else:
            print("⚠️  Using keyword-based classification (fallback)")
    
    def classify_meeting_type(self, subject: str, description: str = "", 
                             attendees: List[str] = None, duration: int = 60):
        if self.use_llm_classifier:
            result = self.meeting_classifier.classify_meeting(
                subject, description, attendees, duration
            )
            return result['specific_type'], result['primary_category']
        else:
            # Fallback to existing keyword logic
            return self._keyword_classification(subject, len(attendees or []))
```

## Troubleshooting

### Issue: "msal is not installed"
```bash
pip install msal
```

### Issue: "requests is not installed"
```bash
pip install requests
```

### Issue: Authentication fails
1. Check internet connection
2. Verify Microsoft account has SilverFlow API access
3. Try clearing MSAL cache: Delete `~/.msal_token_cache.bin`

### Issue: "HTTP 401 Unauthorized"
- Token expired - will auto-refresh on next request
- Insufficient permissions - verify account access to LLMAPI.dev scope

### Issue: "HTTP 429 Rate Limit"
- Add delays between requests
- Reduce concurrent API calls
- Check quota limits in SilverFlow portal

### Issue: Ollama classifier unavailable
```bash
# Start Ollama service
ollama serve

# Pull model
ollama pull gpt-oss:20b
```

## Dependencies

```txt
# Required for GPT-5 classifier
msal>=1.20.0
requests>=2.28.0

# Required for Ollama classifier (existing)
ollama>=0.1.0
```

## Next Steps

### 1. Validation Testing
- [ ] Run `compare_classifiers.py` to generate accuracy report
- [ ] Compare against ground truth dataset
- [ ] Measure production performance

### 2. Integration
- [ ] Update `collaborator_discovery.py` to use GPT-5 classifier
- [ ] Add meeting type weights to importance scoring
- [ ] Integrate with Priority Calendar rankings

### 3. Documentation
- [ ] Update `.cursorrules` with GPT-5 integration lessons
- [ ] Create daily log entry for this work
- [ ] Document classification accuracy results

### 4. Monitoring
- [ ] Track classification latency
- [ ] Monitor API errors and rate limits
- [ ] Collect user feedback on accuracy

## References

**Source Code**:
- SilverFlow LLM API: `SilverFlow/model/llmapi-dev-gpt-5-chat-jj.py`
- SilverFlow eval framework: `SilverFlow/evals/eval.py`
- Original Ollama classifier: `tools/meeting_classifier.py`
- Enterprise taxonomy: `docs/Enterprise_Meeting_Taxonomy.md`

**Documentation**:
- MSAL Python: https://msal-python.readthedocs.io/
- SilverFlow LLM API: Internal Microsoft documentation
- Meeting Taxonomy: `docs/Enterprise_Meeting_Taxonomy.md`

---

**Created**: October 26, 2025  
**Version**: 1.0  
**Status**: Ready for testing
