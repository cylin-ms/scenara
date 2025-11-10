# Organizational Context Enhancement - Implementation Plan

## Problem Statement

**Current Issue**: Generated calendars have unrealistic attendee counts (1-2 people per meeting)

**Root Cause**: No organizational context or social network for personas

**Required**: Realistic organizational structures with:
- Teams and reporting hierarchies
- Multiple companies (internal + customers + vendors)
- Persona-specific attendee networks
- Meeting type → attendee pattern mappings

## Solution Architecture

### 1. Organizational Context Structure

```
organizational_context/
├── companies/                          # Company definitions
│   ├── contoso_corp.json              # ✅ Our company (2,500 employees)
│   ├── fabrikam_inc.json              # ✅ Customer ($2.5M deal)
│   ├── adventure_works.json           # ✅ Customer ($1.2M deal)
│   └── litware_inc.json               # ✅ Vendor (cloud services)
│
├── teams/                             # Internal team org charts
│   ├── sales_team.json                # ✅ Sales hierarchy (VP → Directors → Managers)
│   ├── engineering_team.json          # ✅ Engineering hierarchy (Director → Managers → ICs)
│   └── legal_team.json                # ✅ Legal hierarchy (GC → Senior Counsel → Specialists)
│
└── attendee_networks/                 # Persona-specific contact networks
    ├── tier1_sales_network.json       # ✅ Who Sales Manager meets with
    ├── tier2_architect_network.json   # ✅ Who Senior IC meets with
    └── tier3_legal_network.json       # ✅ Who Legal Specialist meets with
```

### 2. Attendee Pattern Design

Each persona has **meeting type → attendee pattern** mappings:

#### Example: Tier 1 Sales Manager (Alex Chen)

```json
{
  "weekly_1on1_manager": {
    "meeting_types": ["Weekly 1:1 with Regional Director"],
    "attendees": ["emily.tan@contoso.com"],
    "count": 2  // Always 2 people
  },
  
  "customer_calls": {
    "meeting_types": ["Customer Call", "Client Demo", "Discovery Call"],
    "internal_team": [
      "jessica.wu@contoso.com",  // Account Executive
      "steven.zhao@contoso.com"   // Sales Engineer
    ],
    "external_companies": ["fabrikam_inc", "adventure_works"],
    "count_range": [5, 10]  // 5-10 total attendees
  },
  
  "team_meetings": {
    "meeting_types": ["Sales Team Weekly Sync"],
    "attendees": [
      "jessica.wu@contoso.com",
      "kevin.lin@contoso.com",
      "lisa.zhang@contoso.com",
      "tom.wang@contoso.com"
    ],
    "count_range": [5, 7]
  }
}
```

**How it works**:
1. Calendar generator sees meeting subject: "Customer Call: Fabrikam Deal Review"
2. Matches meeting type: "Customer Call" → `customer_calls` pattern
3. Selects 2-3 from `internal_team`
4. Adds 2-3 from `fabrikam_inc.contacts`
5. Total: 5-7 realistic attendees

### 3. Realistic Attendee Counts by Meeting Type

| Meeting Type | Attendee Count | Composition |
|--------------|----------------|-------------|
| **1:1 with Manager** | 2 | Persona + Manager |
| **Team Sync** | 5-8 | Team members + manager |
| **Customer Call** | 5-10 | 2-4 internal + 2-5 customer |
| **Architecture Review** | 6-10 | Architects + engineers + PM |
| **Contract Review** | 3-6 | Legal team + business stakeholders |
| **Forecast Review** | 3-5 | Manager + directors + VPs |
| **Learning Session** | 4-8 | Team members + interested peers |
| **Cross-Team Sync** | 4-8 | Representatives from 2-3 teams |

## Implementation Steps

### Phase 1: Core Infrastructure (COMPLETED ✅)

- [x] Create organizational context directory structure
- [x] Define Contoso Corp (internal company) with 5 divisions
- [x] Create 3 internal teams (Sales, Engineering, Legal)
- [x] Define 3 external companies (2 customers, 1 vendor)
- [x] Build attendee networks for all 3 personas
- [x] Map meeting types to attendee patterns

### Phase 2: Calendar Generator Integration (NEXT)

**Update**: `generate_calendar_training_data.py`

**New Features**:
1. Load organizational context files
2. Parse attendee networks for persona
3. Match meeting subjects to patterns
4. Generate realistic attendee lists
5. Mix internal + external contacts appropriately

**Key Changes**:

```python
class CalendarTrainingDataGenerator:
    def __init__(self, persona_path, org_context_path):
        self.persona = self._load_persona(persona_path)
        self.org_context = self._load_org_context(org_context_path)
        self.attendee_network = self._load_attendee_network()
        
    def _generate_realistic_attendees(self, meeting):
        """
        Generate realistic attendee list based on meeting type.
        
        Returns:
            List of attendees with proper structure:
            [
                {
                    "emailAddress": {"name": "...", "address": "..."},
                    "type": "required" | "optional",
                    "status": {"response": "accepted" | "tentative" | "none"}
                }
            ]
        """
        # 1. Match meeting subject to pattern
        pattern = self._match_meeting_pattern(meeting['subject'])
        
        # 2. Select attendees from network
        if pattern['external_companies']:
            # Customer/vendor meeting
            internal = self._select_internal_attendees(pattern, 2, 4)
            external = self._select_external_attendees(pattern, 2, 5)
            attendees = internal + external
        else:
            # Internal meeting
            attendees = self._select_internal_attendees(pattern, 3, 10)
        
        # 3. Format as Microsoft Graph API structure
        return self._format_attendees(attendees)
```

**Pattern Matching Logic**:

```python
def _match_meeting_pattern(self, subject):
    """
    Match meeting subject to attendee pattern.
    
    Examples:
        "Customer Call: Fabrikam" → customer_calls pattern
        "Weekly Team Sync" → team_meetings pattern
        "Architecture Review" → architecture_reviews pattern
    """
    subject_lower = subject.lower()
    
    for pattern_name, pattern in self.attendee_network['attendee_patterns'].items():
        for meeting_type in pattern['meeting_types']:
            if meeting_type.lower() in subject_lower:
                return pattern
    
    # Default: generic team meeting
    return self.attendee_network['attendee_patterns']['team_meetings']
```

### Phase 3: Validation & Quality Checks

**Validate Generated Calendars**:

```bash
# Check attendee counts
python post_training/tools/validate_attendee_counts.py \
  --calendar tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
  --min-attendees 2 \
  --expected-avg 5-7

# Expected output:
# ✅ Total meetings: 97
# ✅ Avg attendees: 6.2 (target: 5-7)
# ✅ 1:1 meetings: 4 (2 attendees each)
# ✅ Team meetings: 12 (6-8 attendees)
# ✅ Customer calls: 18 (7-10 attendees)
# ⚠️ 3 meetings with only 2 attendees (should be 3+)
```

**Quality Metrics**:
- ✅ No meetings with 1 attendee (invalid)
- ✅ 1:1 meetings have exactly 2 attendees
- ✅ Team meetings have 5-12 attendees
- ✅ Customer meetings have internal + external mix
- ✅ Average attendees per meeting: 5-7 (realistic)

### Phase 4: Visualization Updates

**Update Outlook Calendar Interface**:

Show attendee details in tooltips:
```
Attendees (7):
  Internal:
    • Alex Chen (Organizer)
    • Jessica Wu (Required)
    • Steven Zhao (Required)
  
  External (Fabrikam Inc.):
    • Susan Li (Required)
    • Jason Wu (Required)
    • Tony Wang (Optional)
```

## Organizational Context Details

### Contoso Corporation (Internal Company)

**Structure**:
- **2,500 employees** across 5 divisions
- **Headquarters**: Shanghai, China
- **Industry**: Enterprise Software

**Divisions**:
1. **Sales & Customer Success** (120 employees)
   - VP: David Zhang
   - Regional Directors → Sales Managers → Account Executives
   
2. **Engineering** (450 employees)
   - VP: Sarah Chen
   - Directors → Engineering Managers → ICs (L59-L67)
   
3. **Product Management** (80 employees)
   - CPO: Michael Liu
   
4. **Legal & Compliance** (35 employees)
   - General Counsel: Jennifer Wang
   - Senior Counsel → Legal Specialists
   
5. **Finance & Operations** (65 employees)
   - CFO: Robert Huang

### External Companies

#### 1. Fabrikam Inc. (Customer)
- **Industry**: Manufacturing
- **Headquarters**: Beijing
- **Employees**: 15,000
- **Deal Size**: $2.5M ARR
- **Key Contacts**: 5 people (CIO, VP IT, Director, Managers)

#### 2. Adventure Works (Customer)
- **Industry**: Retail & E-commerce
- **Headquarters**: Shenzhen
- **Employees**: 8,000
- **Deal Size**: $1.2M ARR
- **Key Contacts**: 4 people (VP Tech, Director, PM, Engineer)

#### 3. Litware Inc. (Vendor)
- **Industry**: Cloud Services Provider
- **Headquarters**: Singapore
- **Employees**: 3,500
- **Relationship**: Hosting vendor
- **Key Contacts**: 3 people (Account Manager, Solutions Architect, CSM)

## Persona Attendee Networks

### Tier 1: Sales Manager (Alex Chen)

**Team**:
- Reports to: Emily Tan (Regional Director)
- Direct reports: 4 Account Executives
- Works with: Sales Engineer, Customer Success Manager

**Frequent Contacts** (9 internal + 6 external):
- **Internal**: Regional Director, 4 AEs, Sales Engineer, CSM, Legal, Product
- **External**: 3 from Fabrikam, 3 from Adventure Works

**Meeting Patterns**:
- 1:1 with manager: 2 people
- Team syncs: 6-7 people
- Customer calls: 7-10 people (mixed)
- Forecast reviews: 3-5 people (leadership)
- Deal reviews: 4-6 people (cross-functional)

### Tier 2: Senior IC Architect (Daniel Kim)

**Team**:
- Reports to: James Park (Engineering Manager)
- Peers: 3 engineers on team
- Collaborates with: Staff/Principal engineers, Product, DevOps

**Frequent Contacts** (9 internal + 4 external):
- **Internal**: Manager, 3 team peers, 2 staff engineers, PM, DevOps, QA
- **External**: 2 from Fabrikam, 2 from Adventure Works

**Meeting Patterns**:
- 1:1 with manager: 2 people
- Team syncs: 5-6 people
- Architecture reviews: 6-9 people
- Cross-team syncs: 5-8 people
- Learning sessions: 4-7 people

### Tier 3: Legal Specialist (Michelle Zhang)

**Team**:
- Reports to: Richard Tan (Senior Legal Counsel)
- Peers: 1 other specialist
- Works with: Compliance Manager, Procurement

**Frequent Contacts** (8 internal + 3 external):
- **Internal**: Manager, peer, GC, compliance, procurement, sales leadership
- **External**: 2 from Litware, 1 from Fabrikam

**Meeting Patterns**:
- 1:1 with manager: 2 people
- Team syncs: 4-5 people
- Contract reviews: 3-6 people
- Vendor negotiations: 4-7 people (mixed)
- Compliance meetings: 3-5 people

## Expected Impact

### Before (Current State)
```
Meeting: "Customer Call: Fabrikam Deal Review"
Attendees: 2 people
  • alex.chen@contoso.com (organizer)
  • Attendee 1

Problem: Unrealistic for customer call
```

### After (With Org Context)
```
Meeting: "Customer Call: Fabrikam Deal Review"
Attendees: 7 people
  Internal (4):
    • alex.chen@contoso.com (organizer, required)
    • jessica.wu@contoso.com (required) - Account Executive
    • steven.zhao@contoso.com (required) - Sales Engineer
    • emily.tan@contoso.com (optional) - Regional Director
  
  External - Fabrikam Inc. (3):
    • susan.li@fabrikam.com (required) - VP of IT
    • jason.wu@fabrikam.com (required) - Director
    • tony.wang@fabrikam.com (optional) - Senior Architect

Result: ✅ Realistic customer call
```

## Implementation Timeline

| Phase | Tasks | Status | Time Estimate |
|-------|-------|--------|---------------|
| **Phase 1** | Create org context structures | ✅ DONE | 1 hour |
| **Phase 2** | Update calendar generator | 🔄 NEXT | 2-3 hours |
| **Phase 3** | Regenerate all 3 calendars | ⏳ PENDING | 30 minutes |
| **Phase 4** | Validate attendee counts | ⏳ PENDING | 30 minutes |
| **Phase 5** | Update visualization | ⏳ PENDING | 1 hour |
| **Total** | | | ~5-6 hours |

## Next Action

**Ready to implement Phase 2**:

```bash
# Update calendar generator to use organizational context
# This will add realistic attendee lists to all meetings
python post_training/tools/update_calendar_generator_with_attendees.py

# Then regenerate calendars with new attendee logic
python post_training/tools/generate_calendar_training_data.py \
  --persona post_training/data/personas/tier1_sales_manager_pipeline.json \
  --org-context post_training/data/organizational_context/ \
  --weeks 4 \
  --output tier1_sales_manager_pipeline_calendar_4weeks_v2.jsonl
```

**Validation**:
- Open Outlook calendar interface
- Hover over meetings
- Verify attendee counts realistic (3-10 people)
- Check internal/external mix for customer meetings
- Confirm 1:1 meetings have exactly 2 attendees

---

**Status**: Phase 1 Complete ✅ | Ready for Phase 2 Implementation 🚀
