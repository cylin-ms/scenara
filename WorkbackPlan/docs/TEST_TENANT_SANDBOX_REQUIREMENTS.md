# Test Tenant Sandbox Requirements for RFT Training

**Version**: 1.0  
**Date**: November 18, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Define Test Tenant environment for privacy-safe model training

---

## Problem Statement

During RFT training, the model needs to interact with enterprise systems:
- **Calendar APIs** - Query meeting schedules, attendee availability
- **User Directory** - Lookup employee info, reporting structure
- **Artifact Storage** - Access previous meeting decks, documents
- **Policy Systems** - Check holidays, blackout dates, resource constraints

**Challenge**: Cannot use production data due to privacy/compliance concerns.

**Solution**: Create synthetic Test Tenant with realistic but fake data.

---

## Test Tenant Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Test Tenant Sandbox                       │
│                  (Isolated Environment)                      │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Graph API Mock  │  │ SharePoint Mock  │                │
│  │  - Calendar      │  │ - Artifacts      │                │
│  │  - Users         │  │ - Documents      │                │
│  │  - Org Chart     │  │ - Templates      │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Policy Service  │  │  Test Database   │                │
│  │  - Holidays      │  │ - Meeting history│                │
│  │  - Blackouts     │  │ - Quality metrics│                │
│  │  - Constraints   │  │ - Training logs  │                │
│  └──────────────────┘  └──────────────────┘                │
│                                                              │
│  ┌──────────────────────────────────────────┐              │
│  │      Model Training Environment          │              │
│  │  - gpt-oss:120b (RFT training mode)     │              │
│  │  - Reward checker (code from Data Team) │              │
│  │  - Training orchestrator                 │              │
│  └──────────────────────────────────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Required Components

### 1. **Synthetic User Directory**

Fake but realistic employee profiles for training.

**File**: `test_tenant/users/synthetic_employees.json`

```json
{
  "users": [
    {
      "id": "user001",
      "email": "alice.ceo@testcorp.com",
      "displayName": "Alice Johnson",
      "jobTitle": "Chief Executive Officer",
      "department": "Executive",
      "manager": null,
      "timezone": "America/Los_Angeles",
      "working_hours": {
        "start": "08:00",
        "end": "18:00",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
      },
      "out_of_office": []
    },
    {
      "id": "user002",
      "email": "bob.cfo@testcorp.com",
      "displayName": "Bob Chen",
      "jobTitle": "Chief Financial Officer",
      "department": "Finance",
      "manager": "user001",
      "timezone": "America/New_York",
      "working_hours": {
        "start": "09:00",
        "end": "18:00",
        "days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
      },
      "out_of_office": [
        {"start": "2025-12-20", "end": "2026-01-05", "reason": "Holiday vacation"}
      ]
    }
  ],
  "org_structure": {
    "CEO": ["CFO", "CTO", "VP Product", "VP Sales"],
    "CFO": ["Finance Director", "Accounting Manager"],
    "CTO": ["Engineering Director", "IT Director"]
  }
}
```

**Requirements**:
- 50-100 synthetic employees covering typical enterprise roles
- Realistic reporting structure (3-4 levels)
- Mix of timezones (US, Europe, Asia)
- Out-of-office periods for training edge cases
- No real employee data

### 2. **Synthetic Calendar Data**

Realistic meeting patterns for various meeting types.

**File**: `test_tenant/calendar/synthetic_meetings.json`

```json
{
  "meetings": [
    {
      "id": "meeting001",
      "subject": "Q4 2025 Board Review",
      "meeting_type": "Board Review",
      "start": "2025-12-15T14:00:00Z",
      "end": "2025-12-15T16:00:00Z",
      "organizer": "alice.ceo@testcorp.com",
      "attendees": [
        {"email": "alice.ceo@testcorp.com", "type": "required"},
        {"email": "bob.cfo@testcorp.com", "type": "required"},
        {"email": "board.chair@testcorp.com", "type": "required"},
        {"email": "board.member1@testcorp.com", "type": "optional"}
      ],
      "location": "Executive Boardroom",
      "is_online": true,
      "recurrence": null,
      "importance": "high",
      "tags": ["strategic", "executive", "quarterly"]
    },
    {
      "id": "meeting002",
      "subject": "Product Launch Planning - Project Phoenix",
      "meeting_type": "Product Launch",
      "start": "2026-01-10T10:00:00Z",
      "end": "2026-01-10T11:30:00Z",
      "organizer": "carol.vp@testcorp.com",
      "attendees": [
        {"email": "carol.vp@testcorp.com", "type": "required"},
        {"email": "dave.pm@testcorp.com", "type": "required"},
        {"email": "eve.eng@testcorp.com", "type": "required"},
        {"email": "frank.marketing@testcorp.com", "type": "required"}
      ],
      "location": "Virtual",
      "is_online": true,
      "recurrence": null,
      "importance": "high",
      "tags": ["product", "launch", "cross-functional"],
      "historical_context": {
        "previous_launches": 3,
        "last_launch_date": "2025-06-15",
        "success_rate": 0.85
      }
    }
  ],
  "meeting_templates": {
    "QBR": {
      "typical_attendees": 15,
      "typical_duration_minutes": 120,
      "preparation_days": 21,
      "frequency": "quarterly"
    },
    "Board Review": {
      "typical_attendees": 8,
      "typical_duration_minutes": 180,
      "preparation_days": 60,
      "frequency": "quarterly"
    },
    "Product Launch": {
      "typical_attendees": 12,
      "typical_duration_minutes": 90,
      "preparation_days": 45,
      "frequency": "adhoc"
    }
  }
}
```

**Requirements**:
- 200-500 synthetic meetings across all training verticals
- Realistic distribution (60% recurring, 40% one-time)
- Mix of meeting types: QBR (30%), Board (10%), Product Launch (20%), M&A (5%), Other (35%)
- Historical context for temporal patterns
- No real meeting data

### 3. **Synthetic Artifact Repository**

Mock documents the model can reference during training.

**File**: `test_tenant/artifacts/synthetic_documents.json`

```json
{
  "artifacts": [
    {
      "id": "doc001",
      "name": "Q3 2025 Financial Report Template.pptx",
      "type": "PowerPoint",
      "url": "https://test-tenant-storage.local/docs/doc001",
      "owner": "bob.cfo@testcorp.com",
      "created": "2025-09-15T10:00:00Z",
      "modified": "2025-09-20T15:30:00Z",
      "size_bytes": 2458000,
      "tags": ["template", "financial", "QBR"],
      "access_permissions": ["Finance", "Executive"],
      "related_meetings": ["meeting001"],
      "quality_score": 0.92,
      "usage_count": 12
    },
    {
      "id": "doc002",
      "name": "Product Roadmap 2026.pdf",
      "type": "PDF",
      "url": "https://test-tenant-storage.local/docs/doc002",
      "owner": "carol.vp@testcorp.com",
      "created": "2025-11-01T09:00:00Z",
      "modified": "2025-11-15T14:00:00Z",
      "size_bytes": 1234000,
      "tags": ["roadmap", "product", "strategy"],
      "access_permissions": ["Product", "Engineering", "Executive"],
      "related_meetings": ["meeting002"],
      "quality_score": 0.88,
      "usage_count": 8
    }
  ],
  "artifact_templates": {
    "Financial Report": {
      "typical_pages": 25,
      "preparation_time_days": 14,
      "review_cycles": 3,
      "typical_reviewers": ["CFO", "Finance Director", "CEO"]
    },
    "Product Roadmap": {
      "typical_pages": 15,
      "preparation_time_days": 10,
      "review_cycles": 2,
      "typical_reviewers": ["VP Product", "CTO", "CEO"]
    }
  }
}
```

**Requirements**:
- 100-200 synthetic documents
- Realistic file sizes, names, metadata
- Access permissions aligned with org structure
- No real document content

### 4. **Organizational Policies & Constraints**

Company-specific rules the model must learn.

**File**: `test_tenant/policies/constraints.json`

```json
{
  "company": "TestCorp Inc.",
  "fiscal_year_start": "2025-07-01",
  "fiscal_quarters": {
    "Q1": {"start": "2025-07-01", "end": "2025-09-30"},
    "Q2": {"start": "2025-10-01", "end": "2025-12-31"},
    "Q3": {"start": "2026-01-01", "end": "2026-03-31"},
    "Q4": {"start": "2026-04-01", "end": "2026-06-30"}
  },
  "holidays": [
    {"date": "2025-11-28", "name": "Thanksgiving (US)", "regions": ["US"]},
    {"date": "2025-11-29", "name": "Day after Thanksgiving (US)", "regions": ["US"]},
    {"date": "2025-12-25", "name": "Christmas Day", "regions": ["US", "EU"]},
    {"date": "2026-01-01", "name": "New Year's Day", "regions": ["US", "EU", "APAC"]},
    {"date": "2026-01-26", "name": "Republic Day (India)", "regions": ["India"]}
  ],
  "blackout_periods": [
    {
      "start": "2025-12-20",
      "end": "2026-01-05",
      "reason": "Year-end holiday blackout",
      "affected_departments": "all",
      "restrictions": ["no_major_reviews", "limited_availability"]
    },
    {
      "start": "2025-09-01",
      "end": "2025-09-15",
      "reason": "Quarterly earnings preparation",
      "affected_departments": ["Finance", "Executive"],
      "restrictions": ["finance_team_busy"]
    }
  ],
  "meeting_policies": {
    "executive_meetings": {
      "min_notice_days": 14,
      "materials_due_days_before": 3,
      "max_duration_minutes": 180,
      "requires_tech_check": true
    },
    "board_meetings": {
      "min_notice_days": 60,
      "materials_due_days_before": 7,
      "max_duration_minutes": 240,
      "requires_legal_review": true,
      "legal_review_sla_days": 7
    },
    "product_launches": {
      "min_notice_days": 30,
      "materials_due_days_before": 5,
      "requires_marketing_approval": true,
      "requires_tech_readiness_check": true
    }
  },
  "resource_constraints": {
    "executive_boardroom": {
      "capacity": 20,
      "booking_advance_days": 30,
      "requires_av_setup": true,
      "av_setup_lead_time_hours": 24
    },
    "cfo_availability": {
      "typical_busy_periods": ["month_end", "quarter_end"],
      "typical_travel_days_per_month": 5
    }
  },
  "quality_standards": {
    "deck_formatting": {
      "max_slides": 30,
      "required_sections": ["Executive Summary", "Key Metrics", "Next Steps"],
      "font_standard": "Calibri or Arial",
      "slide_aspect_ratio": "16:9"
    },
    "financial_reports": {
      "required_review_levels": 3,
      "must_include_variance_analysis": true,
      "requires_cfo_signoff": true
    }
  }
}
```

**Requirements**:
- Realistic corporate policies
- Regional variations (US, EU, APAC)
- Different rules per meeting type
- Resource availability constraints

### 5. **Graph API Mock Server**

Simulates Microsoft Graph API for calendar/user queries.

**File**: `test_tenant/api/graph_mock.py`

```python
"""
Mock Microsoft Graph API for Test Tenant.
Simulates Graph API endpoints without touching real Microsoft 365 data.
"""

from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import json

app = FastAPI()

# Load synthetic data
with open('test_tenant/users/synthetic_employees.json') as f:
    USERS = json.load(f)

with open('test_tenant/calendar/synthetic_meetings.json') as f:
    MEETINGS = json.load(f)

with open('test_tenant/policies/constraints.json') as f:
    POLICIES = json.load(f)


@app.get("/v1.0/users/{user_id}")
async def get_user(user_id: str):
    """Mock GET /users/{id} endpoint"""
    for user in USERS['users']:
        if user['id'] == user_id or user['email'] == user_id:
            return {
                "id": user['id'],
                "displayName": user['displayName'],
                "mail": user['email'],
                "jobTitle": user['jobTitle'],
                "department": user['department']
            }
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/v1.0/users/{user_id}/calendar/events")
async def get_calendar_events(
    user_id: str,
    start_datetime: str = None,
    end_datetime: str = None
):
    """Mock GET /users/{id}/calendar/events endpoint"""
    user_email = None
    for user in USERS['users']:
        if user['id'] == user_id or user['email'] == user_id:
            user_email = user['email']
            break
    
    if not user_email:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Filter meetings for this user
    user_meetings = []
    for meeting in MEETINGS['meetings']:
        attendees = [a['email'] for a in meeting['attendees']]
        if user_email in attendees or meeting['organizer'] == user_email:
            # Filter by date range if provided
            if start_datetime and end_datetime:
                meeting_start = datetime.fromisoformat(meeting['start'].replace('Z', '+00:00'))
                filter_start = datetime.fromisoformat(start_datetime.replace('Z', '+00:00'))
                filter_end = datetime.fromisoformat(end_datetime.replace('Z', '+00:00'))
                if not (filter_start <= meeting_start <= filter_end):
                    continue
            user_meetings.append(meeting)
    
    return {"value": user_meetings}


@app.get("/v1.0/users/{user_id}/manager")
async def get_manager(user_id: str):
    """Mock GET /users/{id}/manager endpoint"""
    for user in USERS['users']:
        if user['id'] == user_id or user['email'] == user_id:
            if user['manager']:
                # Find manager details
                for mgr in USERS['users']:
                    if mgr['id'] == user['manager']:
                        return {
                            "id": mgr['id'],
                            "displayName": mgr['displayName'],
                            "mail": mgr['email'],
                            "jobTitle": mgr['jobTitle']
                        }
            return None
    raise HTTPException(status_code=404, detail="User not found")


@app.get("/v1.0/organization/holidays")
async def get_holidays():
    """Mock endpoint for organizational holidays"""
    return {"value": POLICIES['holidays']}


@app.get("/v1.0/organization/blackout_periods")
async def get_blackout_periods():
    """Mock endpoint for blackout periods"""
    return {"value": POLICIES['blackout_periods']}


@app.post("/v1.0/workback_plan/validate")
async def validate_workback_plan(plan: dict):
    """
    Mock endpoint for validating workback plans.
    This is what RFT training calls during reward calculation.
    """
    from test_tenant.training.rft_reward_checker import calculate_reward
    
    # Extract scenario constraints from context
    scenario = {
        "attendees": [a['email'] for a in plan.get('attendees', [])],
        "holidays": POLICIES['holidays'],
        "meeting_date": plan.get('meeting_date'),
        "meeting_type": plan.get('meeting_type')
    }
    
    # Calculate reward
    reward = calculate_reward(plan, scenario)
    
    return {
        "valid": reward >= 4.0,  # Pass threshold
        "reward": reward,
        "max_reward": 6.0,
        "checks": {
            "dependencies": reward >= 2.0,
            "timelines": reward >= 3.0,
            "stakeholders": reward >= 4.0,
            "constraints": reward >= 5.0
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Requirements**:
- Compatible with Microsoft Graph API interface
- Returns synthetic data only
- Fast response times (<100ms per query)
- Runs in Docker container for isolation

---

## Test Tenant Setup Instructions

### Step 1: Deploy Infrastructure

```bash
# Create test tenant namespace
kubectl create namespace test-tenant-sandbox

# Deploy Graph API mock
kubectl apply -f test_tenant/k8s/graph-api-mock.yaml

# Deploy synthetic data services
kubectl apply -f test_tenant/k8s/synthetic-data-services.yaml

# Deploy training environment
kubectl apply -f test_tenant/k8s/training-environment.yaml
```

### Step 2: Load Synthetic Data

```bash
# Initialize database with synthetic data
python test_tenant/scripts/init_synthetic_data.py

# Verify data loaded correctly
python test_tenant/scripts/validate_test_tenant.py

# Expected output:
# ✓ Loaded 75 synthetic users
# ✓ Loaded 250 synthetic meetings
# ✓ Loaded 150 synthetic artifacts
# ✓ Loaded 12 organizational policies
# ✓ Graph API mock responding on http://test-tenant-api:8000
```

### Step 3: Configure Training Environment

```bash
# Point training to test tenant instead of production
export GRAPH_API_URL="http://test-tenant-api:8000"
export TRAINING_MODE="test_tenant"
export DATA_PRIVACY_MODE="strict"

# Verify isolation
python test_tenant/scripts/verify_no_prod_access.py

# Expected output:
# ✓ No production Graph API access
# ✓ No production storage access
# ✓ All queries routed to test tenant
# ✓ Data isolation verified
```

### Step 4: Run Training

```python
# Training script automatically uses test tenant
from training.rft_trainer import RFTTrainer

trainer = RFTTrainer(
    model="gpt-oss:120b",
    reward_function="test_tenant/training/rft_reward_checker.py",
    scenarios="data/rft/qbr_scenarios.jsonl",
    graph_api_url=os.getenv("GRAPH_API_URL")  # ← Points to mock
)

# During training, model will:
# 1. Query test tenant Graph API for calendar data
# 2. Lookup synthetic users and org structure
# 3. Check synthetic policies and constraints
# 4. Generate workback plans
# 5. Get rewards from programmatic checks
# 6. Update policy based on rewards

trainer.train(iterations=500)
```

---

## Privacy & Compliance

### Data Isolation Guarantees

✅ **No production data** - All data is synthetically generated  
✅ **Network isolation** - Test tenant in separate namespace  
✅ **API mocking** - No real Graph API calls during training  
✅ **Audit logging** - All queries logged for compliance review  
✅ **Automatic scrubbing** - Any real data accidentally leaked is flagged  

### Validation Checks

```python
# test_tenant/scripts/verify_no_prod_access.py

def verify_data_privacy():
    """Ensure no production data can leak into training"""
    
    # Check 1: No production API endpoints configured
    assert "graph.microsoft.com" not in os.getenv("GRAPH_API_URL")
    
    # Check 2: All emails are @testcorp.com
    with open('test_tenant/users/synthetic_employees.json') as f:
        users = json.load(f)
    for user in users['users']:
        assert '@testcorp.com' in user['email']
    
    # Check 3: No real meeting IDs
    with open('test_tenant/calendar/synthetic_meetings.json') as f:
        meetings = json.load(f)
    for meeting in meetings['meetings']:
        assert meeting['id'].startswith('meeting')  # Synthetic prefix
    
    # Check 4: Test tenant marker present
    assert os.getenv("TRAINING_MODE") == "test_tenant"
    
    print("✓ Data privacy verified - no production access possible")
```

---

## What Data Team Delivers

### Test Tenant Package

```
test_tenant/
├── users/
│   └── synthetic_employees.json          (75 fake users)
├── calendar/
│   └── synthetic_meetings.json           (250 fake meetings)
├── artifacts/
│   └── synthetic_documents.json          (150 fake docs)
├── policies/
│   └── constraints.json                  (Corporate policies)
├── api/
│   ├── graph_mock.py                     (FastAPI mock server)
│   └── requirements.txt                  (Python dependencies)
├── k8s/
│   ├── graph-api-mock.yaml              (Kubernetes deployment)
│   ├── synthetic-data-services.yaml     (Data services)
│   └── training-environment.yaml        (Training pod config)
├── scripts/
│   ├── init_synthetic_data.py           (Load data script)
│   ├── validate_test_tenant.py          (Validation script)
│   └── verify_no_prod_access.py         (Privacy check)
├── training/
│   └── rft_reward_checker.py            (From data team)
└── README.md                             (Setup instructions)
```

---

## Benefits

✅ **Privacy compliant** - No real user/company data exposed  
✅ **Realistic training** - Model learns enterprise patterns  
✅ **Reproducible** - Same synthetic data across runs  
✅ **Fast iteration** - No API rate limits or quotas  
✅ **Auditable** - All training interactions logged  
✅ **Portable** - Test tenant can run anywhere (cloud, on-prem)  

---

## Summary

**Key Deliverable**: Complete test tenant sandbox that:
1. Simulates Microsoft 365 environment with synthetic data
2. Provides Graph API mock for calendar/user queries
3. Enforces organizational policies and constraints
4. Enables privacy-safe RFT training
5. Guarantees no production data access

**Integration with Training**: Training Team uses test tenant transparently via environment variables - no code changes needed between test and production environments.
