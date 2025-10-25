# SilverFlow Integration Guide for Scenara 2.0

**Last Updated:** October 26, 2025  
**Source:** Innovation Studio Hackathon 2025 Project #105957  
**Repository:** https://github.com/gim-home/SilverFlow

## Overview

SilverFlow provides production-ready, tested Microsoft 365 data extraction scripts using **MSAL + Windows Broker (WAM)** authentication. These scripts are battle-tested and should be used as the PRIMARY method for data collection in Scenara 2.0.

## Authentication Pattern

**All SilverFlow scripts use consistent authentication:**
- **Tenant ID:** `72f988bf-86f1-41af-91ab-2d7cd011db47` (Microsoft)
- **Client ID:** `9ce97a32-d9ab-4ab2-aadc-f49b39b94e11`
- **Method:** MSAL PublicClientApplication with `enable_broker_on_windows=True`
- **Scopes:** Varies by script (documented below)

**Key Features:**
- ✅ Silent token refresh when possible
- ✅ Automatic Windows Broker (WAM) integration
- ✅ Graceful fallback if broker unavailable
- ✅ Login hint using current Windows user

---

## 📅 Calendar & Meetings

### 1. `graph_get_meetings.py` ⭐ PRIMARY CALENDAR EXTRACTOR

**Purpose:** Fetch calendar events with auto-pagination  
**Scopes:** `Calendars.Read`, `offline_access`, `openid`, `profile`

**Usage:**
```powershell
# Get next 90 days of meetings
python SilverFlow/data/graph_get_meetings.py 90

# Get past 30 days + future 60 days
python SilverFlow/data/graph_get_meetings.py 2025-09-26T00:00:00 2025-11-25T23:59:59

# Customize filters and fields
python SilverFlow/data/graph_get_meetings.py 90 --top 100 --filter "(isCancelled eq false)"
```

**Output:**
- JSON: `SilverFlow/data/out/graph_meetings.json`
- Markdown: `SilverFlow/data/out/graph_meetings.md`

**Output Format:**
```json
{
  "generatedAt": "2025-10-26T...",
  "startUtc": "...",
  "endUtc": "...",
  "timeZone": "Asia/Shanghai",
  "totalEvents": 67,
  "events": [
    {
      "id": "...",
      "subject": "Meeting Title",
      "start": { "dateTime": "2025-10-27T13:00:00", "timeZone": "Asia/Shanghai" },
      "end": { ... },
      "organizer": { "emailAddress": { "name": "...", "address": "..." } },
      "bodyPreview": "...",
      "responseStatus": { "response": "accepted", "time": "..." },
      "showAs": "busy",
      "type": "singleInstance"
    }
  ]
}
```

**Integration with Scenara:**
```python
# Convert to Scenara format
import json
sf_data = json.load(open('SilverFlow/data/out/graph_meetings.json'))
scenara_data = {
    "scenarios": sf_data['events'],
    "metadata": {
        "generated_at": sf_data['generatedAt'],
        "total_events": sf_data['totalEvents'],
        "source": "SilverFlow"
    }
}
```

---

## 💬 Teams Chat

### 2. `graph_list_chats_last_preview.py` ⭐ PRIMARY CHAT EXTRACTOR

**Purpose:** List Teams chats with last message preview  
**Scopes:** `Chat.Read`, `User.Read`, `openid`, `profile`, `offline_access`

**Usage:**
```powershell
# Get top 100 chats
python SilverFlow/data/graph_list_chats_last_preview.py --top 50 --max 100

# With verbose logging
python SilverFlow/data/graph_list_chats_last_preview.py --top 50 --verbose
```

**Output:**
- JSON: `SilverFlow/data/out/graph_chats.json`
- Markdown: `SilverFlow/data/out/graph_chats.md`

**Output Format:**
```json
{
  "generatedAt": "...",
  "totalChats": 100,
  "chats": [
    {
      "id": "19:...",
      "topic": "Chat Title or null",
      "chatType": "oneOnOne|group|meeting",
      "createdDateTime": "...",
      "lastUpdatedDateTime": "...",
      "lastMessagePreview": {
        "id": "...",
        "createdDateTime": "...",
        "body": { "content": "..." },
        "from": {
          "user": { "displayName": "...", "id": "..." }
        }
      }
    }
  ]
}
```

**Already Integrated:** Used by `tools/teams_chat_api.py` (created based on this script)

### 3. `graph_list_my_sent_messages.py`

**Purpose:** Fetch recent chat messages SENT by current user  
**Scopes:** `Chat.Read`, `User.Read`, `openid`, `profile`, `offline_access`

**Usage:**
```powershell
# Get messages from top 50 chats, 3 messages per chat
python SilverFlow/data/graph_list_my_sent_messages.py --chat-top 50 --per-chat-top 3

# Limit total messages
python SilverFlow/data/graph_list_my_sent_messages.py --limit 100
```

**Output:** `SilverFlow/data/out/graph_my_sent_messages.json`

**Use Case:** Analyze communication patterns, identify active collaborators

### 4. `get_chat_messages.py`

**Purpose:** Fetch messages from a SPECIFIC chat ID  
**Scopes:** `Chat.Read`, `User.Read`

**Usage:**
```powershell
python SilverFlow/data/get_chat_messages.py <CHAT_ID> --top 50
```

---

## 📧 Email

### 5. `get_mail_content.py`

**Purpose:** Download first mail hit from BizChat search results  
**Scopes:** `Mail.Read`, `User.Read`

**Usage:**
```powershell
# Requires bizchat_search_mail.json as input
python SilverFlow/data/get_mail_content.py
```

**Output:** `SilverFlow/data/out/mail_content.json`

---

## 📄 Documents

### 6. `get_docx_content.py`

**Purpose:** Download DOCX content from search results  
**Scopes:** `Sites.Read.All`, `Files.Read.All`

**Usage:**
```powershell
# Requires bizchat_search_docx.json as input
python SilverFlow/data/get_docx_content.py
```

**Output:** `SilverFlow/data/out/docx_content.json`

---

## 🔍 Substrate/BizChat Search APIs

These scripts query Microsoft's internal Substrate search endpoints (used by M365 Copilot/BizChat).

### 7. `bizchat_search.py` 

**Purpose:** General purpose Substrate search  
**Scopes:** `https://substrate.office.com/search/SearchAnon.All`

**Usage:**
```powershell
python SilverFlow/data/bizchat_search.py "query text" --top 25
```

### 8. `bizchat_search_chats.py`

**Purpose:** Aggregate Teams chat search results by thread

### 9. `bizchat_search_meetings.py`

**Purpose:** Search for meetings via Substrate

### 10. `bizchat_search_mail.py`

**Purpose:** Search emails via Substrate

### 11. `bizchat_search_docx.py`

**Purpose:** Search Word documents

### 12. `bizchat_search_pptx.py`

**Purpose:** Search PowerPoint files

### 13. `bizchat_search_loop.py`

**Purpose:** Search Loop files

### 14. `bizchat_search_ado.py`

**Purpose:** Search Azure DevOps work items

### 15. `bizchat_all_chats.py`

**Purpose:** Fetch all chats without user-scoped query

### 16. `bizchat_context.py`

**Purpose:** Request BizChat context from Substrate context endpoint

### 17. `bizchat_meeting_chats.py`

**Purpose:** Query chats matching a specific meeting title

### 18. `bizchat_recommendations.py`

**Purpose:** Get meeting recommendations from search results

---

## 🧠 Substrate AI Features

### 19. `substrate_chat_insights.py`

**Purpose:** Generate AI insights for chat threads  
**Scopes:** Substrate AI endpoints

**Use Case:** Chat summaries, action items, key points

### 20. `substrate_chat_insights_e2e.py`

**Purpose:** End-to-end: fetch chats → generate insights

### 21. `substrate_meeting_prep.py` ⭐ MEETING PREP INSIGHTS

**Purpose:** Fetch AI-generated meeting preparation insights  
**Scopes:** Substrate meeting prep endpoints

**Use Case:** Meeting prep recommendations, context summaries

---

## 👤 Loki/Viva People APIs

These query Microsoft's internal people/org APIs (Loki = Live persona card system).

### 22. `loki_get_conversations.py`

**Purpose:** Query conversation history from persona APIs

### 23. `loki_get_graphql_org.py`

**Purpose:** Execute GraphQL queries against Org Explorer API

### 24. `loki_get_linkedin_profiles.py`

**Purpose:** Fetch LinkedIn profile data

### 25. `loki_get_manager.py`

**Purpose:** Get manager/org chart information

### 26. `loki_get_personacards.py`

**Purpose:** Fetch persona card metadata

### 27. `loki_get_vivaskills.py`

**Purpose:** Get Viva Skills data for people

---

## 🔧 Utility Scripts

### 28. `meeting_worthy_metadata.py`

**Purpose:** Combine Graph meetings with Substrate search metadata

**Use Case:** Enrich meeting data with AI-generated insights

### 29. `extract_projects.py`

**Purpose:** Extract project information from data

### 30. `expand_prompt.py`

**Purpose:** Expand/enhance prompts using AI

---

## 🎯 Recommended Integration Strategy for Scenara 2.0

### Priority 1: Core Data Collection ✅

**Calendar Data:**
```powershell
# Replace all calendar extraction with:
python SilverFlow/data/graph_get_meetings.py 90
# Output: SilverFlow/data/out/graph_meetings.json
```

**Teams Chat Data:** ✅ ALREADY INTEGRATED
```powershell
# Current implementation in tools/teams_chat_api.py
# Based on graph_list_chats_last_preview.py patterns
python tools/teams_chat_api.py --top 50 --max 100 --days 90
```

**Email Data:**
```powershell
# Use bizchat_search_mail.py for email search
python SilverFlow/data/bizchat_search_mail.py "keywords" --top 50
# Then get_mail_content.py to download content
```

### Priority 2: Enhanced Features

**People/Collaborator Data:**
```powershell
# Graph API People rankings - already integrated
# Add Loki APIs for richer profiles:
python SilverFlow/data/loki_get_personacards.py <user_id>
python SilverFlow/data/loki_get_linkedin_profiles.py <user_id>
```

**Meeting Prep Insights:**
```powershell
python SilverFlow/data/substrate_meeting_prep.py <meeting_id>
# Provides AI-generated prep recommendations
```

**Chat Insights:**
```powershell
python SilverFlow/data/substrate_chat_insights_e2e.py
# End-to-end chat → insights pipeline
```

### Priority 3: Search & Discovery

**Universal Search:**
```powershell
python SilverFlow/data/bizchat_search.py "project keywords"
# Returns meetings, chats, documents, emails
```

**Document Discovery:**
```powershell
python SilverFlow/data/bizchat_search_docx.py "topic"
python SilverFlow/data/get_docx_content.py  # Downloads content
```

---

## 📋 Standard Output Location

**All SilverFlow scripts output to:**
```
SilverFlow/data/out/
├── graph_meetings.json         # Calendar events
├── graph_meetings.md           # Human-readable calendar
├── graph_chats.json            # Teams chats
├── graph_chats.md              # Human-readable chats
├── graph_my_sent_messages.json # Sent messages
├── bizchat_*.json              # Search results
└── ...
```

---

## 🔄 Data Freshness Strategy

**For Real-Time Accuracy:**

```powershell
# 1. Collect fresh calendar (< 30 min old)
python SilverFlow/data/graph_get_meetings.py 90

# 2. Collect fresh Teams chat (< 30 min old)
python tools/teams_chat_api.py --top 50 --max 100 --days 90

# 3. Run collaborator discovery with fresh data
python tools/collaborator_discovery.py --calendar-data <converted_format>
```

**Conversion Required:** SilverFlow → Scenara format (see converter scripts)

---

## ⚠️ Important Notes

### Data Format Differences

**SilverFlow Format:**
```json
{
  "events": [ { "id": "...", "subject": "...", ... } ],
  "totalEvents": 67
}
```

**Scenara Format:**
```json
{
  "scenarios": [ { "id": "...", "context": { ... } } ]
}
```

**Solution:** Use `convert_silverflow_to_scenara.py` converter

### Authentication Caching

- MSAL automatically caches tokens
- Silent refresh attempted first
- Interactive login only when needed
- Windows Broker (WAM) provides SSO

### Error Handling

All scripts include:
- Graceful degradation
- UTF-8 encoding fixes for Windows
- Comprehensive error messages
- Retry logic for network issues

---

## 🚀 Quick Start Commands

```powershell
# Get everything you need in 3 commands:

# 1. Fresh calendar (90 days)
python SilverFlow/data/graph_get_meetings.py 90

# 2. Fresh Teams chat (90 days, 100 chats)
python tools/teams_chat_api.py --top 50 --max 100 --days 90

# 3. Convert and analyze
python convert_silverflow_to_scenara.py
python tools/collaborator_discovery.py --calendar-data meeting_prep_data/real_calendar_scenarios_fresh.json
```

---

## 📚 Reference Implementation

**teams_chat_api.py** (700+ lines) is the reference implementation showing how to:
1. Use MSAL + Windows Broker authentication
2. Handle pagination with @odata.nextLink
3. Implement proper error handling
4. Save results in structured JSON
5. Generate markdown summaries
6. Support CLI arguments

**Pattern to follow for all new integrations.**

---

## 🎓 Lessons Learned

### What Works ✅

1. **MSAL + Windows Broker** - Most reliable authentication
2. **graph_get_meetings.py** - Production-ready calendar extraction
3. **graph_list_chats_last_preview.py** - Comprehensive chat data
4. **Substrate APIs** - Rich AI-generated insights
5. **Auto-pagination** - Handles large datasets gracefully

### What to Avoid ❌

1. **Browser automation** - Fragile, unreliable
2. **Manual Graph Explorer** - Not programmatic
3. **Custom auth implementations** - Use SilverFlow patterns
4. **Hard-coded paths** - Use environment variables

### Best Practices 🌟

1. **Always use fresh data** (< 30 minutes for real-time accuracy)
2. **Convert formats** immediately after extraction
3. **Validate data** before analysis
4. **Cache tokens** but refresh data
5. **Handle UTF-8** explicitly on Windows
6. **Log verbosely** for debugging
7. **Fail gracefully** with helpful messages

---

## 🔗 Integration Checklist for New Features

When integrating a new SilverFlow script:

- [ ] Copy authentication pattern from existing script
- [ ] Use same tenant ID / client ID
- [ ] Add appropriate scopes
- [ ] Save to `SilverFlow/data/out/` directory
- [ ] Implement UTF-8 encoding for Windows
- [ ] Add CLI argument parsing
- [ ] Include verbose logging option
- [ ] Generate both JSON and Markdown output
- [ ] Create converter to Scenara format if needed
- [ ] Update this documentation
- [ ] Test with fresh data collection
- [ ] Validate output format
- [ ] Add error handling for edge cases

---

**End of Guide**

*For questions or issues, refer to SilverFlow repository or contact the Scenara 2.0 team.*
