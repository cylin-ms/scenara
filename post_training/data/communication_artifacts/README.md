# Communication Artifacts Framework

## Overview

To create realistic meeting intelligence training data, we need **multi-modal communication artifacts** that reflect how people actually work:

1. **Teams/Slack Chat Threads** - Pre-meeting coordination, quick questions
2. **Email Chains** - Meeting invites, follow-ups, decisions
3. **Meeting Transcripts** - What was actually said during meetings
4. **Meeting Recordings Metadata** - Duration, speakers, engagement
5. **Meeting Recaps/Notes** - Post-meeting summaries, action items
6. **Document Attachments** - Slides, contracts, proposals referenced

## Why This Matters

### Current State (Calendar Only)
```
Meeting: "Customer Call: Fabrikam Deal Review"
- Subject: "Customer Call: Fabrikam Deal Review"
- Time: Nov 18, 2:00 PM - 3:00 PM
- Attendees: 7 people
- Importance: Critical

❌ Problem: No context on WHAT happened or WHY it matters
```

### Realistic State (Multi-Modal)
```
Meeting: "Customer Call: Fabrikam Deal Review"

📅 Calendar Event
- Time: Nov 18, 2:00 PM - 3:00 PM
- Attendees: 7 people
- Importance: Critical

💬 Pre-Meeting Chat (Teams)
[Nov 18, 1:45 PM] Alex Chen: @Jessica quick sync before Fabrikam call?
[Nov 18, 1:47 PM] Jessica Wu: Yes! They're asking about Q1 timeline
[Nov 18, 1:50 PM] Alex Chen: Let's commit to March 1st delivery

📧 Email Thread
From: susan.li@fabrikam.com
Subject: Re: Q4 Contract Terms - Concerns
"We need to discuss the SLA guarantees before signing..."

📝 Meeting Transcript
[00:02:15] Alex Chen: "Thanks for joining. Let's address the SLA concerns..."
[00:05:30] Susan Li: "Our procurement team needs 99.9% uptime guarantee..."
[00:12:45] Steven Zhao: "We can commit to that with our premium tier..."

📋 Meeting Recap
Action Items:
1. Legal to draft SLA amendment - @Michelle Zhang - Due: Nov 20
2. Send premium tier pricing - @Alex Chen - Due: Nov 19
3. Schedule contract signing call - @Jessica Wu - Due: Nov 22

✅ Result: AI can understand context, relationships, decisions made
```

## Artifact Structure

```
communication_artifacts/
├── README.md                          # This file
├── templates/                         # Generation templates
│   ├── chat_templates.json           # Teams/Slack message patterns
│   ├── email_templates.json          # Email structure patterns
│   ├── transcript_templates.json     # Meeting dialogue patterns
│   └── recap_templates.json          # Summary/action item patterns
│
├── generated/                         # Generated artifacts per meeting
│   ├── tier1_sales_manager/
│   │   ├── 2025-11-18_1400_fabrikam_deal/
│   │   │   ├── meeting.json          # Calendar event
│   │   │   ├── pre_meeting_chat.json # Teams chat (day before + morning of)
│   │   │   ├── email_thread.json     # Related email chain
│   │   │   ├── transcript.json       # Full meeting transcript
│   │   │   ├── recording_metadata.json # Recording details
│   │   │   └── recap.json            # Post-meeting summary
│   │   └── 2025-11-18_1000_weekly_1on1/
│   │       └── ...
│   ├── tier2_senior_ic_architect/
│   └── tier3_specialist_legal/
│
└── schemas/                           # JSON schemas for validation
    ├── chat_schema.json
    ├── email_schema.json
    ├── transcript_schema.json
    └── recap_schema.json
```

## Artifact Types

### 1. Teams/Slack Chat Threads

**Use Case**: Quick coordination, questions, context sharing

**Example Structure**:
```json
{
  "chat_id": "fabrikam_deal_prep_20251118",
  "channel_type": "direct_message",
  "participants": [
    {"name": "Alex Chen", "email": "alex.chen@contoso.com"},
    {"name": "Jessica Wu", "email": "jessica.wu@contoso.com"}
  ],
  "messages": [
    {
      "timestamp": "2025-11-18T13:45:00Z",
      "sender": "alex.chen@contoso.com",
      "message": "@Jessica quick sync before Fabrikam call?",
      "reactions": [{"emoji": "👍", "user": "jessica.wu@contoso.com"}]
    },
    {
      "timestamp": "2025-11-18T13:47:00Z",
      "sender": "jessica.wu@contoso.com",
      "message": "Yes! They're asking about Q1 timeline. I think we should commit to March 1st.",
      "mentions": []
    }
  ],
  "related_meeting": "2025-11-18_1400_fabrikam_deal"
}
```

**Generation Patterns**:
- **Pre-meeting** (1 hour before): Coordination, last-minute prep
- **During meeting** (async): Quick lookups, "can someone find the doc?"
- **Post-meeting** (within 1 hour): Quick decisions, action confirmations

### 2. Email Threads

**Use Case**: Formal communication, meeting invites, follow-ups

**Example Structure**:
```json
{
  "email_thread_id": "fabrikam_contract_terms_thread",
  "subject": "Re: Q4 Contract Terms - Concerns",
  "messages": [
    {
      "message_id": "msg_001",
      "timestamp": "2025-11-15T09:30:00Z",
      "from": {"name": "Susan Li", "email": "susan.li@fabrikam.com"},
      "to": [{"name": "Alex Chen", "email": "alex.chen@contoso.com"}],
      "cc": [{"name": "Jason Wu", "email": "jason.wu@fabrikam.com"}],
      "subject": "Q4 Contract Terms - Concerns",
      "body": "Hi Alex,\n\nOur procurement team has raised concerns about the SLA guarantees in Section 5.2. We need 99.9% uptime commitment...",
      "attachments": []
    },
    {
      "message_id": "msg_002",
      "timestamp": "2025-11-15T14:20:00Z",
      "from": {"name": "Alex Chen", "email": "alex.chen@contoso.com"},
      "to": [{"name": "Susan Li", "email": "susan.li@fabrikam.com"}],
      "subject": "Re: Q4 Contract Terms - Concerns",
      "body": "Hi Susan,\n\nLet's schedule a call to discuss this in detail. Can you do Tuesday 2 PM?...",
      "related_meeting": "2025-11-18_1400_fabrikam_deal"
    }
  ]
}
```

### 3. Meeting Transcripts

**Use Case**: What was actually discussed, key quotes, decisions

**Example Structure**:
```json
{
  "transcript_id": "transcript_2025-11-18_1400_fabrikam_deal",
  "meeting_id": "2025-11-18_1400_fabrikam_deal",
  "duration_minutes": 60,
  "speakers": [
    {"name": "Alex Chen", "role": "organizer", "company": "Contoso"},
    {"name": "Susan Li", "role": "attendee", "company": "Fabrikam"},
    {"name": "Steven Zhao", "role": "attendee", "company": "Contoso"}
  ],
  "segments": [
    {
      "timestamp": "00:00:00",
      "duration": 135,
      "speaker": "Alex Chen",
      "text": "Thanks everyone for joining. Susan, I know your team had concerns about the SLA guarantees. Let's walk through those today.",
      "sentiment": "neutral",
      "topics": ["meeting_opening", "agenda_setting"]
    },
    {
      "timestamp": "00:02:15",
      "duration": 187,
      "speaker": "Susan Li",
      "text": "Yes, thanks Alex. Our procurement team needs a 99.9% uptime guarantee. The current contract says 'best effort' which won't work for our operations.",
      "sentiment": "concerned",
      "topics": ["sla_requirements", "concerns"],
      "keywords": ["99.9% uptime", "guarantee", "procurement"]
    },
    {
      "timestamp": "00:05:22",
      "duration": 156,
      "speaker": "Steven Zhao",
      "text": "We can absolutely commit to 99.9% uptime with our premium tier. That includes 24/7 support and guaranteed response times.",
      "sentiment": "positive",
      "topics": ["solution_proposal", "technical_details"],
      "action_implied": true
    }
  ],
  "key_moments": [
    {
      "timestamp": "00:05:22",
      "description": "Steven commits to 99.9% SLA with premium tier",
      "importance": "high"
    }
  ]
}
```

### 4. Meeting Recording Metadata

**Use Case**: Engagement metrics, speaker distribution, recording quality

```json
{
  "recording_id": "rec_2025-11-18_1400_fabrikam_deal",
  "meeting_id": "2025-11-18_1400_fabrikam_deal",
  "duration_seconds": 3600,
  "file_size_mb": 245.3,
  "recording_quality": "HD",
  "speaker_analytics": [
    {
      "speaker": "Alex Chen",
      "talk_time_seconds": 1200,
      "talk_time_percentage": 33.3,
      "turns": 24,
      "avg_turn_length": 50
    },
    {
      "speaker": "Susan Li",
      "talk_time_seconds": 1440,
      "talk_time_percentage": 40.0,
      "turns": 28,
      "avg_turn_length": 51
    }
  ],
  "engagement_metrics": {
    "questions_asked": 12,
    "decisions_made": 3,
    "action_items_identified": 5,
    "sentiment_overall": "positive"
  }
}
```

### 5. Meeting Recaps/Notes

**Use Case**: Post-meeting summaries, action items, decisions

```json
{
  "recap_id": "recap_2025-11-18_1400_fabrikam_deal",
  "meeting_id": "2025-11-18_1400_fabrikam_deal",
  "generated_at": "2025-11-18T15:05:00Z",
  "generated_by": "AI Meeting Assistant",
  
  "executive_summary": "Productive discussion addressing Fabrikam's SLA concerns. Agreed to upgrade to premium tier with 99.9% uptime guarantee. Legal to draft amendment by Nov 20.",
  
  "key_decisions": [
    {
      "decision": "Upgrade Fabrikam to premium tier with 99.9% SLA",
      "rationale": "Required by customer procurement team",
      "impact": "Increases contract value by $300K annually"
    }
  ],
  
  "action_items": [
    {
      "action": "Draft SLA amendment for 99.9% uptime guarantee",
      "owner": "Michelle Zhang",
      "due_date": "2025-11-20",
      "priority": "high",
      "status": "pending"
    },
    {
      "action": "Send updated premium tier pricing to Susan",
      "owner": "Alex Chen",
      "due_date": "2025-11-19",
      "priority": "high",
      "status": "pending"
    }
  ],
  
  "topics_discussed": [
    "SLA requirements and guarantees",
    "Premium tier features and pricing",
    "Contract amendment process",
    "Timeline for Q1 delivery"
  ],
  
  "next_steps": [
    "Schedule contract signing call for Nov 22",
    "Legal review of amendment (Nov 20)",
    "Final pricing approval from finance"
  ]
}
```

### 6. Document Attachments

**Referenced in Meetings**:
```json
{
  "document_id": "doc_fabrikam_proposal_v3",
  "document_name": "Fabrikam Enterprise Proposal v3.pdf",
  "document_type": "proposal",
  "shared_in_meeting": "2025-11-18_1400_fabrikam_deal",
  "shared_by": "Alex Chen",
  "timestamp": "00:15:30",
  "page_references": [
    {"page": 12, "topic": "SLA guarantees"},
    {"page": 23, "topic": "Premium tier pricing"}
  ]
}
```

## Generation Strategy

### Per Meeting Artifact Generation

For each meeting in calendar:

1. **Meeting Context Analysis**
   - Subject → Meeting type (customer call, 1:1, team sync)
   - Attendees → Internal vs. external
   - Importance → Determines artifact depth

2. **Artifact Generation Decision Tree**

```
IF meeting_type == "customer_call" AND importance == "critical":
  ✅ Generate: Pre-meeting chat
  ✅ Generate: Email thread (lead-up)
  ✅ Generate: Full transcript (15-20 speaker turns)
  ✅ Generate: Recording metadata
  ✅ Generate: Detailed recap with action items
  
ELIF meeting_type == "weekly_1on1":
  ✅ Generate: Brief transcript (8-10 turns)
  ✅ Generate: Simple recap (2-3 action items)
  ❌ Skip: Email thread (informal)
  ❌ Skip: Pre-meeting chat (routine)
  
ELIF meeting_type == "team_sync":
  ✅ Generate: Transcript (10-15 turns)
  ✅ Generate: Recap (team updates)
  ⚠️ Optional: Chat (if decisions needed)
```

3. **GPT-5 Prompting Strategy**

```python
# Generate transcript
prompt = f"""
Generate a realistic meeting transcript for:
Meeting: {meeting['subject']}
Type: {meeting_type}
Duration: {meeting['duration']} minutes
Attendees: {attendees_list}

Context:
- This is a {importance} priority {meeting_type}
- Key topics: {topics_from_subject}
- Company: {persona_company}
- Customer: {external_company if applicable}

Generate a natural conversation with:
- Opening/agenda setting (2 minutes)
- Main discussion ({duration - 5} minutes)
- Action items/next steps (3 minutes)

Include:
- Realistic speaking patterns
- Domain-appropriate terminology
- Clear decision moments
- Action item callouts
"""
```

## Implementation Plan

### Phase 1: Templates & Schemas (2-3 hours)
- [ ] Create chat message templates
- [ ] Create email templates
- [ ] Create transcript segment templates
- [ ] Create recap templates
- [ ] Define JSON schemas for validation

### Phase 2: Generator Tool (3-4 hours)
- [ ] Create `generate_communication_artifacts.py`
- [ ] Implement meeting → artifact type mapping
- [ ] Add GPT-5 integration for each artifact type
- [ ] Add realistic timing (chat 1hr before, email 2 days before)
- [ ] Add cross-artifact references (email mentions meeting)

### Phase 3: Batch Generation (1-2 hours)
- [ ] Generate artifacts for all Tier 1 meetings (97 meetings)
- [ ] Generate artifacts for all Tier 2 meetings (58 meetings)
- [ ] Generate artifacts for all Tier 3 meetings (33 meetings)
- [ ] Total: ~188 meetings × 3-5 artifacts each = 500-900 artifacts

### Phase 4: Visualization & Validation (2 hours)
- [ ] Update Outlook calendar to show artifact indicators
- [ ] Create artifact viewer interface
- [ ] Add transcript playback visualization
- [ ] Validate artifact quality

## Expected Output Structure

```
tier1_sales_manager/
├── 2025-11-18_1400_fabrikam_deal/
│   ├── meeting.json                    # Calendar event
│   ├── pre_meeting_chat.json          # Teams chat (5 messages)
│   ├── email_thread.json              # Email chain (3 messages)
│   ├── transcript.json                # Full transcript (18 speaker turns)
│   ├── recording_metadata.json        # Engagement metrics
│   └── recap.json                     # Summary + 5 action items
│
├── 2025-11-18_1000_weekly_1on1/
│   ├── meeting.json
│   ├── transcript.json                # Brief (8 turns)
│   └── recap.json                     # Simple notes
│
└── 2025-11-19_0900_pipeline_review/
    ├── meeting.json
    ├── transcript.json
    ├── recap.json
    └── shared_documents.json          # Forecast spreadsheet reference
```

## Training Data Value

### Before (Calendar Only)
```json
{
  "subject": "Customer Call: Fabrikam Deal Review",
  "start": "2025-11-18T14:00:00",
  "importance": "critical",
  "prep_needed": true
}
```

### After (Multi-Modal)
```json
{
  "meeting": {...},
  "pre_context": {
    "chat_messages": 5,
    "email_chain": 3,
    "sentiment": "concerned"
  },
  "transcript": {
    "duration": 60,
    "speakers": 7,
    "key_topics": ["SLA", "pricing", "timeline"],
    "decisions": 3,
    "action_items": 5
  },
  "post_context": {
    "recap_summary": "...",
    "action_items_assigned": 5,
    "follow_up_meetings": 2
  }
}
```

**AI can now learn**:
- Meeting context from chats/emails
- Actual discussion flow from transcripts
- Outcomes from recaps/action items
- Cross-artifact relationships

## Next Steps

1. **Create templates** for each artifact type
2. **Build generator tool** with GPT-5 integration
3. **Generate artifacts** for existing 188 meetings
4. **Validate quality** across artifact types
5. **Update visualization** to show artifacts

---

**Status**: Planning Complete | Ready for Implementation 🚀  
**Estimated Time**: 8-10 hours total  
**Output**: 500-900 communication artifacts across 188 meetings
