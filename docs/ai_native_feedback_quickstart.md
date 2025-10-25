# AI-Native Feedback Learning System - Quick Start Guide

## What Makes This AI-Native?

Traditional systems: User overrides → System accepts blindly → No learning

**Our AI-Native approach:**
1. System explains WHY it made decisions
2. User provides feedback about actual reality
3. System ANALYZES discrepancy to find root cause
4. System identifies WHAT data is missing
5. System suggests HOW to fix the problem
6. System LEARNS patterns for future improvement

**Result**: Self-correcting, continuously improving system that builds knowledge

## Quick Start

### 1. Discover Your Collaborators

```bash
python tools/collaborator_discovery.py
```

Output: Ranked list of collaborators with importance scores

### 2. Understand a Ranking

```bash
python tools/collaborator_discovery.py --explain "Haidong Zhang"
```

Output:
```
📊 RANKING EXPLANATION: Haidong Zhang
Rank: #1
Importance Score: 111.67
Confidence: 100.0%

🔍 COLLABORATION EVIDENCE:
  • Total meetings: 18
  • Genuine collaboration meetings: 12 (66.7%)
  • 1:1 meetings: 0
  • Meetings you organized: 0
  • Working sessions attended: 7
  • Microsoft Graph API rank: #2 (ML-verified collaboration)
  • Shared documents: 2

💡 SCORING BREAKDOWN:
  • Collaboration activities (30%): 35.5 points
  • Interaction quality (25%): 16.7 points
  • Confidence level (20%): 20.0 points
  • Graph API ranking (15%): 40.0 points (top 3 boost!)
  • Time consistency (10%): 9.5 points
  • Document sharing (5%): 10.0 points
```

**Translation**: "Haidong ranks #1 because Microsoft's ML verified high collaboration (#2), you attended 7 working sessions together, shared 2 documents, and 66.7% of meetings were genuine collaboration (not broadcasts)"

### 3. Provide Feedback When System Is Wrong

```bash
python tools/collaborator_discovery.py \
  --feedback "Xiaodong Liu" \
  --feedback-comment "We co-organized a workshop on Agentic Memory and have regular 1:1s" \
  --expected-rank 5
```

**AI-Native Response**:

```
🧠 AI-NATIVE FEEDBACK ANALYSIS
==============================================================

Collaborator: Xiaodong Liu
System Rank: NOT FOUND
Expected Rank: #5

💬 USER FEEDBACK:
  We co-organized a workshop on Agentic Memory and have regular 1:1s

🔍 SYSTEM ANALYSIS:
  Discrepancy Type: not_found
  Severity: critical
  
  System Perspective: No collaboration evidence found for Xiaodong Liu
  
  Likely Causes:
    • User mentions 1:1s but none found in calendar data
    • Co-organization mentioned but not reflected in meeting data
    • Recent collaboration mentioned - calendar data may be outdated

🔴 DATA GAPS IDENTIFIED:
  • Calendar data incomplete - missing recent meetings
  • Meeting co-organization not fully captured in calendar data

✅ ACTION ITEMS:
  ✓ Re-run Graph API extractor to get fresh calendar events
  ✓ Verify Meeting.Read.All permission includes organizer data
  ✓ Check calendar event organizer field parsing
  ✓ Log this feedback for algorithm training and improvement

📚 LEARNING POINTS:
  • COVERAGE GAP: User collaborates via workshop co-organization, 
    ad hoc meetings which are not fully captured in current data sources.
  • TEMPORAL: Recent collaboration is important to users. 
    Ensure data sources are refreshed regularly.
  • DATA PRIORITY: Missing 2 data sources. 
    Multi-source fusion is critical for accuracy.
```

**What Just Happened**:
- ❌ System didn't just accept "make him #5"
- ✅ System analyzed WHY there's a discrepancy
- ✅ System identified MISSING calendar data and co-organization tracking
- ✅ System suggested CONCRETE actions to fix
- ✅ System learned PATTERNS about workshop collaboration and recency

### 4. View All Learned Patterns

```bash
python tools/collaborator_discovery.py --feedback-summary
```

Output:
```
📊 DATA GAP SUMMARY
Total gaps identified: 4
Unique gap types: 4

Top Data Gaps:
  1x: Calendar data incomplete - missing recent meetings
      Affects: Xiaodong Liu
  
  1x: Teams chat data not captured - need Chat.Read permission
      Affects: Vani Soff
  
  1x: Meeting co-organization not fully captured
      Affects: Xiaodong Liu
  
  1x: Document sharing incomplete - may need additional scopes
      Affects: Vani Soff

🎯 SYSTEM IMPROVEMENT SUGGESTIONS:
  Priority 1: Request Chat.Read permission (affects Vani Soff)
  Priority 1: Refresh calendar data (affects Xiaodong Liu)

📈 ALGORITHM LEARNING PATTERNS:
  • COVERAGE GAP: 2 occurrences
  • TEMPORAL: 2 occurrences  
  • DATA PRIORITY: 2 occurrences
```

**What This Reveals**:
- System identified 4 systematic data gaps
- Multiple users affected by same root causes
- Clear priorities for system improvements
- Patterns emerging across feedback

## Real Example: Vani Soff Case Study

### The Problem

User: "Vani Soff should be in my top 10, we chat in Teams daily and share documents"

System: Ranked Vani at #12

### Traditional Approach (Bad)

```
User override: Move Vani to #8
System: OK, Vani is now #8
[No learning, will make same mistake for other Teams-active collaborators]
```

### AI-Native Approach (Good)

```bash
python tools/collaborator_discovery.py \
  --feedback "Vani Soff" \
  --feedback-comment "We chat in Teams most recently and share documents" \
  --expected-rank 8
```

**System Response**:

```
🔍 SYSTEM ANALYSIS:
  Discrepancy Type: ranked_too_low
  Severity: medium (ranked #12 vs expected #8)
  
  System Perspective: Ranked at #12 based on available data
  
  Likely Causes:
    • Teams chat collaboration mentioned but not captured (need Chat.Read)
    • Document sharing mentioned but not detected
    • Recent collaboration mentioned - calendar data may be outdated

🔴 DATA GAPS IDENTIFIED:
  • Teams chat data not captured - need Chat.Read permission
  • Document sharing incomplete - may need additional Graph API scopes

✅ ACTION ITEMS:
  ✓ Request Chat.Read permission in Graph Explorer
  ✓ Add Teams chat analysis to extraction pipeline
  ✓ Verify Files.Read.All scope in Graph API permissions
  ✓ Check shared documents query is working correctly

📚 LEARNING POINTS:
  • COVERAGE GAP: User collaborates via Teams chat which are not 
    fully captured in current data sources.
  • TEMPORAL: Recent collaboration is important to users.
```

**What the System Learned**:

1. **Data Gap**: Teams chat is a critical collaboration channel we're not capturing
2. **Action Required**: Need to request Chat.Read permission
3. **Pattern**: "Most recently" and "chat" indicates temporal collaboration we're missing
4. **Fix**: Document created at `docs/graph_api_chat_permission_request.md`

### After Fix Applied

1. User follows `docs/graph_api_chat_permission_request.md`
2. Adds Chat.Read permission in Graph Explorer
3. Re-runs `python tools/manual_auth_graph_extractor.py`
4. Teams chat data now captured
5. Vani automatically ranks higher (algorithm unchanged!)
6. ALL users with Teams chat collaboration benefit

**This is AI-native**: Fix the data gap once, benefit everyone forever

## Why This Matters

### For Users
- **Transparency**: Understand why each decision was made
- **Trust**: AI explains its reasoning, not a black box
- **Empowerment**: Feedback improves the system for everyone

### For Developers
- **Gap Discovery**: User feedback reveals missing data sources
- **Root Cause Analysis**: Distinguish algorithm bugs from data issues
- **Priority Guidance**: Know what to fix first based on user impact

### For the System
- **Self-Correction**: Identifies and documents how to fix problems
- **Knowledge Building**: Accumulates patterns and solutions over time
- **Continuous Improvement**: Gets better with every feedback

## Advanced Features

### Feedback Log Persistence

All feedback is saved to: `data/evaluation_results/collaborator_feedback_log.json`

This builds a knowledge base of:
- What users expect vs what system produces
- What data sources are missing
- What patterns emerge across users
- What fixes have been applied

### Pattern Recognition

System learns patterns like:
- **COVERAGE GAP**: New collaboration types not in data model
- **TEMPORAL**: Recent collaboration valued more than old data
- **DATA PRIORITY**: Multi-source fusion requires all sources
- **PATTERN**: Broadcast-only may indicate missing 1:1s

### Proactive Suggestions

After accumulating feedback, system can suggest:
- Which permissions to request
- When to refresh data
- Which data sources are most critical
- What algorithm improvements would help most

## Command Reference

```bash
# Basic discovery
python tools/collaborator_discovery.py

# Limit results
python tools/collaborator_discovery.py --limit 10

# Explain a ranking
python tools/collaborator_discovery.py --explain "Name"

# Submit feedback
python tools/collaborator_discovery.py \
  --feedback "Name" \
  --feedback-comment "Description of actual collaboration" \
  --expected-rank 5

# View feedback summary
python tools/collaborator_discovery.py --feedback-summary

# Quiet mode (no summary)
python tools/collaborator_discovery.py --quiet
```

## Philosophy

**Traditional AI**: Make decision → User accepts or overrides → No learning

**AI-Native**: Make decision → Explain why → User provides reality → Analyze gap → Fix root cause → Learn pattern → Improve system → Benefit everyone

**Result**: A system that continuously learns, explains itself, and gets better over time while building trust with users.

---

**Remember**: This is not about manual overrides. This is about the AI understanding what it got wrong, why it got it wrong, and how to not make the same mistake again.
