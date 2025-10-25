# Graph Explorer Automation Solutions

Based on analysis of the saved Graph Explorer HTML and .cursorrules documented success patterns, here are the comprehensive solutions for Microsoft Graph collaboration data extraction.

## UI Analysis Results

### Key Graph Explorer Components Identified

**Response Preview Tab Structure:**
```html
<button role="tab" value="Response preview" aria-selected="true" class="fui-Tab">
  <span class="fui-Tab__content">Response preview</span>
</button>
```

**Monaco Editor Structure:**
```html
<div class="monaco-editor">
  <div class="view-lines">
    <div class="view-line">
      <span class="mtk9 bracket-highlighting-0">{</span>
    </div>
    <div class="view-line">
      <span class="mtk4">"@odata.context"</span>
      <span class="mtk5">"https://graph.microsoft.com/v1.0/$metadata#users..."</span>
    </div>
  </div>
</div>
```

**Sample Query Categories:**
- People (2 API samples)
- Outlook Calendar (7 API samples) 
- Users (19 API samples)
- Outlook Mail (10 API samples)
- Personal Contacts (2 API samples)

## Available Solutions

### 1. Manual Authentication Extractor (Recommended)
**File:** `tools/manual_auth_graph_extractor.py`

**Features:**
- ✅ User controls authentication manually
- ✅ Waits for user confirmation before proceeding
- ✅ Targets Response Preview tab specifically
- ✅ 5 extraction strategies based on UI analysis
- ✅ Collaboration-focused queries for Haidong Zhang analysis

**Usage:**
```bash
python tools/manual_auth_graph_extractor.py
```

**Process:**
1. Browser opens with Graph Explorer
2. User signs in manually
3. User confirms readiness in terminal
4. Automated query execution begins
5. Results extracted and analyzed

### 2. Auto-Trigger Authentication Extractor
**File:** `tools/auto_trigger_graph_extractor.py`

**Features:**
- ✅ Automatic OAuth authentication triggering
- ✅ Protected resource navigation
- ✅ Authentication flow detection
- ⚠️ Response extraction needs refinement

### 3. Hybrid Auto-Trigger Extractor  
**File:** `tools/hybrid_auto_trigger_extractor.py`

**Features:**
- ✅ Combines auto-auth with proven extraction methods
- ✅ Uses .cursorrules documented 5-strategy approach
- ✅ Enhanced collaboration analysis framework
- ⚠️ Response content timing optimization needed

### 4. Robust Collaboration Extractor
**File:** `tools/robust_graph_collaboration_extractor.py`

**Features:**
- ✅ 8 JSON extraction strategies
- ✅ Comprehensive collaboration queries
- ✅ Enhanced error handling and fallbacks
- ⚠️ Authentication integration needed

## Collaboration Analysis Framework

### Primary Queries for Haidong Zhang Ranking

**1. People API - Microsoft ML Rankings:**
```
GET /me/people
```
- Uses Microsoft's ML algorithms to rank collaboration
- Returns relevance scores for true collaboration signals
- Primary method to find genuine Haidong Zhang vs false positives

**2. Calendar Meeting Analysis:**
```
GET /me/calendar/events?$select=subject,organizer,attendees,start,end&$filter=start/dateTime ge '2024-01-01T00:00:00.000Z'
```
- Analyzes meeting attendance patterns
- Identifies frequent collaborators
- Cross-references with People API rankings

**3. Email Communication Patterns:**
```
GET /me/messages?$select=from,toRecipients,subject,receivedDateTime&$top=100
```
- Email frequency analysis
- Communication pattern detection
- Validates collaboration signals

**4. Teams Chat Collaboration:**
```
GET /me/chats?$expand=members&$top=50
```
- Teams chat frequency analysis
- Group collaboration identification
- Real-time communication patterns

**5. Shared Content Analysis:**
```
GET /me/insights/shared?$top=50
```
- Document collaboration tracking
- Shared item analysis
- Content-based collaboration evidence

## Extraction Strategies

### Monaco Editor Content Extraction (Primary)

**Strategy 1: View Lines Extraction**
```python
monaco_container = driver.find_element(By.CLASS_NAME, "monaco-editor")
view_lines = monaco_container.find_elements(By.CLASS_NAME, "view-line")
content = '\n'.join([line.get_attribute('textContent') for line in view_lines])
```

**Strategy 2: Response Preview Tab Targeting**
```python
response_tab = driver.find_element(By.XPATH, "//button[@value='Response preview' and @aria-selected='true']")
```

**Strategy 3: JSON Container Detection**
```python
selectors = [
    "[data-testid*='response']",
    "[class*='response']", 
    "[class*='json']",
    ".monaco-editor .view-lines"
]
```

### Validation Methods

**JSON Structure Validation:**
```python
def _is_valid_json_response(self, content):
    # Check for Graph API indicators
    graph_indicators = [
        '@odata.context',
        'value',
        'displayName', 
        'userPrincipalName',
        'microsoft.com'
    ]
    return any(indicator in content for indicator in graph_indicators)
```

## Success Patterns from .cursorrules

### Documented Working Approach:
- **Success Rate:** "5/8 perfect extractions, 2/8 partial, 1/8 needs improvement"
- **Timing Patterns:** Short waits (0.5s, 1s), quick response detection
- **Extraction Methods:** 5-strategy approach with Monaco editor focus
- **Authentication:** MSAL acquire_token_interactive() proven working

### Lessons Learned:
- Response preview tab is key target (lower right panel)
- Monaco editor uses .view-line classes for content
- Quick response detection works better than long waits
- Multiple extraction fallbacks essential for reliability

## Recommendations

### For Production Use:
1. **Use Manual Authentication Extractor** for reliability
2. **Implement People API first** for core collaboration ranking
3. **Cross-validate with calendar/email data** for comprehensive analysis
4. **Focus on Response Preview tab** for consistent extraction

### For Development:
1. **Test auto-trigger approaches** for full automation potential
2. **Refine timing patterns** based on .cursorrules success
3. **Enhance response detection** for Monaco editor content
4. **Optimize extraction strategies** for different response types

## Technical Implementation Notes

### Browser Requirements:
- Chrome or Edge WebDriver
- Window size: 1920x1080 for optimal layout
- Non-headless mode for manual authentication

### Authentication Flow:
- Protected resource triggers: `/me/people`, `/me/calendar`
- OAuth consent handling automatic
- Manual sign-in provides highest reliability

### Response Processing:
- Monaco editor syntax highlighting preserved
- JSON structure validation essential
- Multiple extraction fallbacks required
- Graph API response patterns recognized

### Error Handling:
- TimeoutException for slow loads
- NoSuchElementException for missing elements
- JSON parsing errors with fallback strategies
- Authentication state detection and retry logic

This comprehensive framework provides reliable Microsoft Graph collaboration data extraction with focus on distinguishing genuine collaboration signals from false positives in the Haidong Zhang ranking analysis.