# Workback Plan Strategy: Real-World Implementation

**Created**: November 12, 2025  
**Author**: Chin-Yew Lin  
**Purpose**: Strategy for creating workback plans for real executive reviews using historical data + synthesis

---

## Executive Summary

**Your Vision**: Create workback plans for upcoming executive reviews (e.g., Rajesh review in 1 month) by learning from historical preparation patterns (e.g., past Gaurav reviews).

**3 Critical Tasks Identified**:
1. **Event Targeting**: Which meetings need workback plans? (Executive reviews, milestone meetings)
2. **Training Data Creation**: Extract historical plans + synthesize variations
3. **Evaluation Framework**: How to measure workback plan quality?

---

## Task 1: Event Targeting - Which Meetings Need Workback Plans?

### 1.1 Target Event Categories

#### High-Priority Events (Always need workback plans)

**Executive Reviews** 🎯 PRIMARY TARGET
- **Examples**: Rajesh review, Gaurav review, CVP reviews, VP business reviews
- **Characteristics**:
  - Fixed recurring schedule (monthly, quarterly)
  - High-stakes visibility
  - Require extensive preparation
  - Multiple work streams must converge
- **Workback Horizon**: 2-4 weeks before review
- **Complexity**: High (Q1)

**Sales & Marketing Events** 🎯 HIGH PRIORITY
- **Examples**: 
  - Sales kickoffs (SKO), regional sales meetings
  - Product launch events, GTM (Go-To-Market) launches
  - Marketing campaigns, analyst briefings (Gartner, Forrester)
  - Customer advisory board (CAB) meetings
  - Trade shows, industry conferences
- **Characteristics**:
  - High external visibility (customers, press, analysts)
  - Revenue impact (sales deals, market positioning)
  - Cross-functional coordination (marketing, sales, product, engineering)
  - Material-intensive (pitch decks, demo scripts, competitive analysis, ROI calculators)
  - Time-sensitive deadlines (event dates, launch windows)
- **Workback Horizon**: 4-12 weeks before event (depending on scale)
- **Complexity**: High (Q1) for major launches, Medium (Q3) for regional events

**Milestone Presentations**
- **Examples**: Product launch reviews, quarterly business reviews (QBRs), roadmap reviews
- **Characteristics**:
  - Fixed deadline (end of quarter, fiscal year)
  - Cross-functional coordination
  - Deliverable-heavy (decks, demos, data)
- **Workback Horizon**: 4-8 weeks before presentation
- **Complexity**: High (Q1)

**Customer/Partner Meetings**
- **Examples**: 
  - Major customer visits, executive briefing center (EBC) visits
  - Partner technical reviews, co-sell meetings
  - Proof-of-concept (POC) presentations
  - Contract renewal discussions
- **Characteristics**:
  - External stakeholders (revenue implications)
  - Represents team/product/company
  - Requires demo/material preparation
  - May require custom solutions or analysis
- **Workback Horizon**: 1-3 weeks before meeting
- **Complexity**: Medium-High (Q3-Q1) depending on customer size

**Team Planning Sessions**
- **Examples**: Sprint planning, roadmap reviews, design reviews, retrospectives
- **Characteristics**:
  - Recurring cadence
  - Requires data gathering/analysis
  - Coordination across team members
- **Workback Horizon**: 3-5 days before meeting
- **Complexity**: Low-Medium (Q2-Q3)

### 1.2 Calendar Pattern Detection

**Strategy**: Automatically identify target events from your calendar

```python
def identify_workback_targets(calendar_events, lookahead_days=60):
    """
    Scan calendar for events that need workback plans
    
    Detection Signals:
    1. Event title contains: "review", "exec", "CVP", "presentation", "milestone", "launch", "SKO", "GTM"
    2. Attendees include: Executives, sales leaders, marketing leaders, external customers
    3. Recurring pattern: monthly/quarterly cadence
    4. Duration: 60+ minutes (substantial meetings)
    5. Your role: organizer or key participant
    6. External domain: Customer/partner email domains (not @microsoft.com)
    """
    targets = []
    
    # Executive and leadership patterns (customize to your org)
    exec_names = ['Rajesh', 'Gaurav', 'CVP', 'VP', 'GM']
    sales_marketing_titles = ['CMO', 'CRO', 'Sales VP', 'Marketing VP', 'Field', 'GTM']
    
    # High-value keywords for different event types
    exec_keywords = ['review', 'exec', 'qbr', 'business review']
    sales_marketing_keywords = [
        'launch', 'sko', 'sales kickoff', 'gtm', 'go-to-market', 
        'campaign', 'analyst', 'gartner', 'forrester',
        'customer advisory', 'cab', 'trade show', 'conference',
        'roadshow', 'webinar', 'event'
    ]
    milestone_keywords = ['milestone', 'presentation', 'demo', 'showcase']
    customer_keywords = ['customer', 'client', 'partner', 'ebc', 'briefing', 'poc', 'proof of concept']
    
    for event in calendar_events:
        score = 0
        event_type = []
        
        subject_lower = event.subject.lower()
        
        # Executive review detection
        if any(keyword in subject_lower for keyword in exec_keywords):
            score += 4
            event_type.append('Executive Review')
        
        # Sales & Marketing event detection
        if any(keyword in subject_lower for keyword in sales_marketing_keywords):
            score += 4
            event_type.append('Sales/Marketing Event')
        
        # Milestone detection
        if any(keyword in subject_lower for keyword in milestone_keywords):
            score += 3
            event_type.append('Milestone')
        
        # Customer/Partner meeting detection
        if any(keyword in subject_lower for keyword in customer_keywords):
            score += 3
            event_type.append('Customer/Partner Meeting')
            
            # Extra score for external attendees
            external_attendees = [a for a in event.attendees 
                                if not a.endswith('@microsoft.com') and '@' in a]
            if external_attendees:
                score += 2
        
        # Attendee analysis - Executives
        if any(exec in ' '.join(event.attendees) for exec in exec_names):
            score += 3
        
        # Attendee analysis - Sales/Marketing leadership
        if any(title in ' '.join(event.attendees) for title in sales_marketing_titles):
            score += 2
        
        # Duration analysis (longer meetings = more prep needed)
        if event.duration_minutes >= 120:  # 2+ hours
            score += 3
        elif event.duration_minutes >= 60:  # 1+ hours
            score += 2
        
        # Your role (organizer = higher responsibility)
        if event.organizer == 'you@microsoft.com':
            score += 2
        elif 'you@microsoft.com' in event.required_attendees:
            score += 1
        
        # Recurring pattern (regular reviews need plans)
        if event.is_recurring and event.recurrence in ['monthly', 'quarterly', 'annual']:
            score += 2
        
        # Location analysis (off-site events need more prep)
        if event.location and event.location not in ['Teams', 'Skype', 'Online', '']:
            score += 1  # Physical location
        
        if score >= 6:  # Threshold for workback plan
            # Determine workback horizon based on event type
            if 'Sales/Marketing Event' in event_type:
                workback_weeks = 8 if score >= 10 else 4  # Major launch vs regional event
            elif 'Executive Review' in event_type:
                workback_weeks = 4
            elif 'Customer/Partner Meeting' in event_type:
                workback_weeks = 2
            else:
                workback_weeks = 2
            
            targets.append({
                'event': event,
                'score': score,
                'event_types': event_type,
                'workback_start_date': event.start_date - timedelta(weeks=workback_weeks),
                'workback_weeks': workback_weeks,
                'urgency': 'critical' if score >= 12 else 'high' if score >= 9 else 'medium',
                'prep_complexity': 'Q1' if score >= 10 else 'Q3' if score >= 8 else 'Q2'
            })
    
    return sorted(targets, key=lambda x: (x['urgency'], x['score']), reverse=True)
```

### 1.3 Example: Your Rajesh Review

**Scenario**: Rajesh review in 1 month (Dec 12, 2025)

**Workback Plan Requirements**:
```
Event: Rajesh Monthly Review
Date: December 12, 2025, 2:00 PM
Attendees: Rajesh (CVP), You, Team Leads
Duration: 60 minutes
Format: Presentation + Discussion

Workback Start: November 14, 2025 (4 weeks before)

Key Deliverables:
1. Executive summary deck (15 slides max)
2. Metrics dashboard (updated data)
3. Key accomplishments summary
4. Issues/blockers list
5. Q&A preparation

Work Streams:
- Data collection (Engineering metrics, user adoption, bug counts)
- Deck creation (Storyline, slide design, content writing)
- Demo preparation (If showing new features)
- Stakeholder alignment (Pre-brief with Gaurav, team leads)
- Review cycles (Draft → Review → Final)
```

### 1.4 Example: Product Launch / GTM Event

**Scenario**: New AI Feature Launch at Microsoft Ignite (March 15, 2026)

**Workback Plan Requirements**:
```
Event: AI Copilot Feature Launch at Ignite
Date: March 15, 2026, 10:00 AM (Keynote slot)
Attendees: Press, Analysts, Customers (1000+), Internal executives
Duration: 45-minute keynote + booth demos
Format: Keynote presentation + Product demos + Press briefings + Social media campaign

Workback Start: December 15, 2025 (12 weeks before)

Key Deliverables:
1. Keynote deck and script (30 slides, rehearsed)
2. Product demo (polished, foolproof, backup plans)
3. Press kit (fact sheet, images, videos, blog posts)
4. Analyst briefings (Gartner, Forrester - scheduled 2 weeks before)
5. Sales enablement materials (pitch deck, demo script, FAQ, competitive analysis)
6. Marketing assets (website updates, social posts, email campaign, ads)
7. Customer testimonials (3-5 reference customers lined up)
8. Booth materials (signage, handouts, swag)

Work Streams:
- Product readiness (Feature completion, bug fixes, performance tuning)
- Demo creation (Script, test data, backup environment)
- Keynote development (Storyline, slides, speaker notes, rehearsals)
- Press/Analyst relations (Pre-briefings, embargo agreements, press releases)
- Marketing campaign (Web, social, email, ads - coordinated launch)
- Sales enablement (Training sessions, materials, competitive positioning)
- Customer recruitment (Testimonials, case studies, beta participants)
- Event logistics (Booth design, travel, equipment shipping)
- Risk mitigation (Demo backups, contingency plans, crisis communication plan)

Timeline Example:
- Week 1-4 (Dec 15 - Jan 12): Product finalization, demo script
- Week 5-6 (Jan 13 - Jan 26): Press/analyst briefings, testimonial collection
- Week 7-8 (Jan 27 - Feb 9): Keynote creation, marketing asset development
- Week 9-10 (Feb 10 - Feb 23): Sales enablement, rehearsals
- Week 11 (Feb 24 - Mar 2): Final polishing, booth setup planning
- Week 12 (Mar 3 - Mar 14): Dry runs, press preview, final checks
- Launch Day (Mar 15): Execution!
```

**Complexity Factors**:
- External visibility: HIGH (press, analysts, customers)
- Coordination: VERY HIGH (product, marketing, sales, PR, field, events)
- Risk: HIGH (live demo, keynote timing, competitive response)
- Material volume: VERY HIGH (8+ major deliverable categories)
- Lead time: 12 weeks (major launch) vs 4-6 weeks (regional GTM)

---

## Task 2: Training Data Creation - Historical + Synthetic

### 2.1 Historical Data Extraction (Your Past Preparations)

**Strategy A: Discover Past Workback Plans from Your Actions**

#### 2.1.1 Data Sources for Historical Plans

**Source 1: Email Analysis**
```python
def extract_preparation_activities_from_email(email_history, target_event):
    """
    Analyze emails sent in 2-4 weeks before past executive reviews
    
    Signals:
    - Emails with subject: "Prep for Gaurav review", "Rajesh review deck"
    - Emails requesting data: "Can you send me the metrics for..."
    - Review requests: "Please review this deck by..."
    - Meeting invites: "Prep session for exec review"
    """
    
    # Example pattern from your past Gaurav review
    past_event = "Gaurav Review - Oct 15, 2025"
    
    # Scan emails from Sep 17 - Oct 14 (4 weeks before)
    prep_emails = [
        {
            'date': '2025-09-18',
            'subject': 'Metrics needed for Gaurav review',
            'action': 'Data request to engineering team',
            'task_inferred': 'Collect engineering metrics (velocity, bug counts)'
        },
        {
            'date': '2025-09-25',
            'subject': 'Draft deck for Gaurav review - please review',
            'action': 'Sent draft deck to team leads',
            'task_inferred': 'Create first draft of executive deck'
        },
        {
            'date': '2025-10-02',
            'subject': 'Prep session for Gaurav review',
            'action': 'Meeting invite to practice presentation',
            'task_inferred': 'Conduct dry run with team'
        }
    ]
    
    return prep_emails
```

**Source 2: Calendar History**
```python
def extract_preparation_meetings(calendar_history, target_event_date):
    """
    Find meetings in 2-4 weeks before exec review that were prep-related
    
    Patterns:
    - "Prep for X review"
    - "Data review for X"
    - "Dry run for X presentation"
    - Meetings with same attendees as main review (pre-alignment)
    """
    
    # Example from past Gaurav review
    prep_meetings = [
        {
            'date': '2025-09-20',
            'subject': 'Metrics alignment for Gaurav review',
            'attendees': ['Engineering Lead', 'PM Lead'],
            'duration': 30,
            'task_inferred': 'Align on which metrics to present'
        },
        {
            'date': '2025-10-10',
            'subject': 'Final review - Gaurav deck',
            'attendees': ['Your Manager', 'Team Leads'],
            'duration': 60,
            'task_inferred': 'Final review before exec presentation'
        }
    ]
    
    return prep_meetings
```

**Source 3: File/Document History**
```python
def extract_preparation_artifacts(file_system, sharepoint, target_event):
    """
    Find documents created in 2-4 weeks before exec review
    
    Look for:
    - PowerPoint decks with "Gaurav", "Rajesh", "Review" in filename
    - Excel files with metrics/data
    - OneNote pages with talking points
    - Word docs with Q&A prep
    """
    
    # Example artifacts from past Gaurav review
    artifacts = [
        {
            'filename': 'Gaurav_Review_Oct2025_v1.pptx',
            'created': '2025-09-22',
            'modified_until': '2025-10-14',
            'versions': 12,
            'task_inferred': 'Deck creation and iteration (3 weeks)'
        },
        {
            'filename': 'Engineering_Metrics_Q3.xlsx',
            'created': '2025-09-18',
            'task_inferred': 'Metrics data collection'
        },
        {
            'filename': 'QA_Prep_Gaurav.docx',
            'created': '2025-10-08',
            'task_inferred': 'Anticipate questions and prepare answers'
        }
    ]
    
    return artifacts
```

**Source 4: ADO Work Items** (Already have this!)
```python
def extract_ado_prep_work_items(ado_client, target_event_date):
    """
    Find ADO work items created for exec review prep
    
    WIQL Query:
    - Created 2-4 weeks before exec review
    - Title/Description contains: "Gaurav review", "exec prep", etc.
    - Area: Your team's area path
    """
    
    query = f"""
    SELECT [System.Id], [System.Title], [System.Description]
    FROM WorkItems
    WHERE [System.TeamProject] = 'Outlook'
      AND [System.CreatedDate] >= '2025-09-15'
      AND [System.CreatedDate] <= '2025-10-15'
      AND ([System.Title] CONTAINS 'Gaurav review' 
           OR [System.Title] CONTAINS 'exec prep'
           OR [System.Description] CONTAINS 'prepare for review')
    """
    
    # Example work items
    work_items = [
        {
            'id': 45678,
            'title': 'Prepare metrics for Gaurav review',
            'description': 'Collect velocity, bug trends, user adoption for Oct review',
            'created': '2025-09-18',
            'closed': '2025-09-22',
            'duration': 4,
            'task_inferred': 'Metrics collection (4 days)'
        }
    ]
    
    return work_items
```

#### 2.1.2 Reconstruction Algorithm

**Convert Historical Actions → Workback Plan**

```python
def reconstruct_historical_workback_plan(
    emails, meetings, artifacts, ado_items, target_event
):
    """
    Reconstruct the implicit workback plan from your past actions
    
    Algorithm:
    1. Collect all preparation activities (emails, meetings, files, ADO)
    2. Sort by date (earliest to latest)
    3. Cluster into logical work streams
    4. Infer dependencies from sequencing
    5. Calculate actual durations
    6. Extract lessons learned (what worked, what didn't)
    """
    
    # Step 1: Combine all sources
    all_activities = []
    all_activities.extend(parse_emails(emails))
    all_activities.extend(parse_meetings(meetings))
    all_activities.extend(parse_artifacts(artifacts))
    all_activities.extend(parse_ado_items(ado_items))
    
    # Step 2: Sort by date
    all_activities.sort(key=lambda x: x['date'])
    
    # Step 3: Cluster into work streams
    work_streams = {
        'data_collection': [],
        'deck_creation': [],
        'stakeholder_alignment': [],
        'review_cycles': [],
        'demo_prep': [],
        'qa_prep': []
    }
    
    for activity in all_activities:
        stream = classify_activity_to_stream(activity)
        work_streams[stream].append(activity)
    
    # Step 4: Build WorkbackPlan
    workback_plan = {
        'event': target_event,
        'summary': f'Preparation plan for {target_event.subject}',
        'total_prep_time': (target_event.date - min(a['date'] for a in all_activities)).days,
        'work_streams': work_streams,
        'deliverables': extract_deliverables(artifacts),
        'tasks': convert_activities_to_tasks(all_activities),
        'lessons_learned': [
            'Started deck creation 3 weeks before - good timing',
            'Should have collected metrics earlier (data requests took 4 days)',
            'Dry run 5 days before was helpful for Q&A prep'
        ]
    }
    
    return workback_plan
```

#### 2.1.3 Example: Reconstructed Gaurav Review Plan

```json
{
  "event": {
    "subject": "Gaurav Monthly Review",
    "date": "2025-10-15T14:00:00",
    "attendees": ["Gaurav", "You", "Team Leads"]
  },
  "summary": "4-week preparation plan for Gaurav executive review",
  "prep_start_date": "2025-09-17",
  "prep_duration_days": 28,
  
  "deliverables": [
    {
      "name": "Executive Summary Deck",
      "description": "15-slide deck covering Q3 accomplishments, Q4 plan, issues",
      "due_date": "2025-10-14",
      "actual_completion": "2025-10-14",
      "versions": 12,
      "total_hours": 24
    },
    {
      "name": "Metrics Dashboard",
      "description": "Engineering velocity, bug trends, user adoption stats",
      "due_date": "2025-10-01",
      "actual_completion": "2025-09-22",
      "total_hours": 8
    }
  ],
  
  "tasks": [
    {
      "id": "T1",
      "name": "Request metrics from engineering team",
      "description": "Email engineering lead for velocity, bug counts, deployment frequency",
      "start_date": "2025-09-17",
      "due_date": "2025-09-18",
      "actual_completion": "2025-09-18",
      "dependencies": [],
      "participants": [{"name": "You", "role": "Requestor"}],
      "evidence": "Email: 'Metrics needed for Gaurav review'"
    },
    {
      "id": "T2",
      "name": "Collect and analyze metrics data",
      "description": "Compile metrics into dashboard format",
      "start_date": "2025-09-19",
      "due_date": "2025-09-22",
      "actual_completion": "2025-09-22",
      "dependencies": ["T1"],
      "participants": [{"name": "Engineering Lead", "role": "Data Provider"}],
      "evidence": "File: Engineering_Metrics_Q3.xlsx"
    },
    {
      "id": "T3",
      "name": "Create deck outline and storyline",
      "description": "Define structure: accomplishments, challenges, plan, Q&A",
      "start_date": "2025-09-22",
      "due_date": "2025-09-24",
      "actual_completion": "2025-09-25",
      "dependencies": ["T2"],
      "participants": [{"name": "You", "role": "Deck Author"}],
      "evidence": "File: Gaurav_Review_Oct2025_v1.pptx (created)"
    },
    {
      "id": "T4",
      "name": "Draft slide content (first 10 slides)",
      "description": "Write content for key slides with data and visuals",
      "start_date": "2025-09-25",
      "due_date": "2025-10-01",
      "actual_completion": "2025-10-02",
      "dependencies": ["T3"],
      "participants": [{"name": "You", "role": "Content Creator"}],
      "evidence": "File: Gaurav_Review_Oct2025_v5.pptx (5 versions)"
    },
    {
      "id": "T5",
      "name": "First review cycle with team leads",
      "description": "Share draft deck, collect feedback on content and messaging",
      "start_date": "2025-10-02",
      "due_date": "2025-10-03",
      "actual_completion": "2025-10-03",
      "dependencies": ["T4"],
      "participants": [
        {"name": "You", "role": "Presenter"},
        {"name": "PM Lead", "role": "Reviewer"},
        {"name": "Eng Lead", "role": "Reviewer"}
      ],
      "evidence": "Email: 'Draft deck for Gaurav review - please review'"
    },
    {
      "id": "T6",
      "name": "Incorporate feedback and refine deck",
      "description": "Address comments, improve visuals, polish messaging",
      "start_date": "2025-10-03",
      "due_date": "2025-10-08",
      "actual_completion": "2025-10-09",
      "dependencies": ["T5"],
      "participants": [{"name": "You", "role": "Deck Author"}],
      "evidence": "File: Gaurav_Review_Oct2025_v11.pptx (v5→v11)"
    },
    {
      "id": "T7",
      "name": "Prepare Q&A talking points",
      "description": "Anticipate Gaurav's questions and prepare answers",
      "start_date": "2025-10-08",
      "due_date": "2025-10-10",
      "actual_completion": "2025-10-10",
      "dependencies": ["T6"],
      "participants": [{"name": "You", "role": "Presenter"}],
      "evidence": "File: QA_Prep_Gaurav.docx"
    },
    {
      "id": "T8",
      "name": "Final review and dry run",
      "description": "Practice presentation with manager, final polish",
      "start_date": "2025-10-10",
      "due_date": "2025-10-12",
      "actual_completion": "2025-10-11",
      "dependencies": ["T7"],
      "participants": [
        {"name": "You", "role": "Presenter"},
        {"name": "Your Manager", "role": "Reviewer"}
      ],
      "evidence": "Meeting: 'Final review - Gaurav deck'"
    },
    {
      "id": "T9",
      "name": "Finalize deck and distribute",
      "description": "Make final edits, send to Gaurav 24h before meeting",
      "start_date": "2025-10-13",
      "due_date": "2025-10-14",
      "actual_completion": "2025-10-14",
      "dependencies": ["T8"],
      "participants": [{"name": "You", "role": "Organizer"}],
      "evidence": "Email: Deck sent to Gaurav on Oct 14"
    }
  ],
  
  "lessons_learned": [
    "✅ Started 4 weeks before - appropriate for executive review",
    "✅ Dry run 5 days before helped identify gaps in Q&A prep",
    "⚠️ Metrics request should have been 1-2 days earlier (engineering team needed 4 days)",
    "⚠️ First review cycle happened late (week 3) - should be week 2 for more iteration time",
    "💡 Having Q&A prep document was very helpful - do this every time",
    "💡 Version control on deck was messy (v12!) - use better naming convention"
  ],
  
  "outcome_metrics": {
    "delivered_on_time": true,
    "total_prep_hours": 40,
    "number_of_review_cycles": 2,
    "deck_version_count": 12,
    "meeting_outcome": "Success - Gaurav approved Q4 plan",
    "stress_level": "Medium - manageable with 4-week prep"
  }
}
```

### 2.2 Synthetic Data Generation

**Strategy B: Create Variations for Different Scenarios**

#### 2.2.1 Template-Based Generation

```python
def generate_synthetic_workback_plan(base_template, parameters):
    """
    Generate variations of executive review preparation plans
    
    Parameters to vary:
    - Executive level: CVP, VP, GM, Director
    - Prep duration: 2 weeks, 4 weeks, 8 weeks
    - Team size: 1-3 people, 4-10 people, 10+ people
    - Complexity: Simple update, Major milestone, Crisis response
    - Format: Deck only, Deck + demo, Deck + data review
    """
    
    # Example: Rajesh review (1 month from now)
    rajesh_plan = adapt_template(
        base_template=gaurav_historical_plan,
        changes={
            'executive': 'Rajesh (CVP)',
            'event_date': '2025-12-12',
            'prep_weeks': 4,
            'format': 'Deck + demo',
            'new_tasks': [
                'Demo preparation (2 weeks)',
                'Demo dry run (3 days before)'
            ],
            'additional_complexity': 'Need to show new AI features'
        }
    )
    
    return rajesh_plan
```

#### 2.2.2 LLM-Enhanced Synthesis

```python
def enhance_synthetic_plan_with_llm(base_plan, context):
    """
    Use LLM to add realistic details to synthetic plans
    """
    
    prompt = f"""
    Given this base workback plan for an executive review:
    {json.dumps(base_plan, indent=2)}
    
    Context:
    - Executive: {context['executive_name']} ({context['title']})
    - Review type: {context['review_type']}
    - Your role: {context['your_role']}
    - Team size: {context['team_size']}
    
    Enhance this plan with:
    1. Realistic task descriptions (what actually happens in prep)
    2. Common dependencies (what blocks what)
    3. Typical challenges (data delays, reviewer availability, scope creep)
    4. Best practices (when to do dry runs, how many review cycles)
    5. Time estimates (based on executive level and complexity)
    
    Output a detailed WorkbackPlan with all tasks, dependencies, and realistic timelines.
    """
    
    enhanced = llm_client.query(prompt, temperature=0.3)
    return WorkbackPlan.model_validate(enhanced)
```

### 2.3 Training Data Pipeline

**Combined Approach: Historical (60%) + Synthetic (40%)**

```python
def create_training_dataset_for_workback_plans():
    """
    Build training dataset from both historical and synthetic sources
    """
    
    # Step 1: Extract historical plans (past Gaurav reviews, other exec reviews)
    historical_plans = []
    
    # Your past Gaurav reviews (last 6 months)
    for month in ['Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct']:
        plan = extract_historical_plan(
            event_name=f'Gaurav Review - {month} 2025',
            data_sources=['email', 'calendar', 'files', 'ado']
        )
        if plan:
            historical_plans.append(plan)
    
    # Other executive reviews (Rajesh, CVP, etc.)
    for exec_review in find_exec_reviews(calendar_history):
        plan = extract_historical_plan(exec_review)
        if plan:
            historical_plans.append(plan)
    
    print(f"Extracted {len(historical_plans)} historical plans")
    
    # Step 2: Generate synthetic variations
    synthetic_plans = []
    
    for base_plan in historical_plans:
        # Generate 2-3 variations per historical plan
        variations = [
            # Variation 1: Different executive level
            adapt_plan(base_plan, executive='VP', prep_weeks=3),
            
            # Variation 2: Different format
            adapt_plan(base_plan, format='Deck + demo', add_tasks=['demo_prep']),
            
            # Variation 3: Crisis/urgent scenario
            adapt_plan(base_plan, urgency='high', prep_weeks=2, remove_buffer=True)
        ]
        synthetic_plans.extend(variations)
    
    print(f"Generated {len(synthetic_plans)} synthetic variations")
    
    # Step 3: Combine and format
    training_data = {
        'historical': historical_plans,  # 60% - real data
        'synthetic': synthetic_plans,     # 40% - variations
        'total': len(historical_plans) + len(synthetic_plans)
    }
    
    return training_data
```

---

## Task 3: Evaluation Framework - Measuring Workback Plan Quality

### 3.1 Evaluation Dimensions

**Quality Rubric: 5 Dimensions, 1-5 Scale Each**

#### Dimension 1: Completeness (1-5)

**Question**: Does the plan cover all necessary preparation activities?

**Scoring**:
- **5 - Comprehensive**: All major work streams identified (data, deck, review cycles, Q&A, alignment)
- **4 - Complete**: Most work streams covered, minor gaps
- **3 - Adequate**: Core tasks present, but missing some important activities
- **2 - Incomplete**: Missing major work streams (e.g., no review cycles, no Q&A prep)
- **1 - Minimal**: Only basic tasks, many critical activities missing

**Checklist**:
- [ ] Data collection/metrics gathering
- [ ] Deck/document creation
- [ ] Stakeholder alignment (pre-briefs)
- [ ] Review cycles (draft → feedback → revision)
- [ ] Q&A preparation
- [ ] Demo preparation (if applicable)
- [ ] Final review/dry run
- [ ] Distribution to attendees

**Example Evaluation**:
```json
{
  "dimension": "completeness",
  "score": 4,
  "reasoning": "Plan includes data collection, deck creation, 2 review cycles, Q&A prep, and dry run. Missing: explicit stakeholder pre-alignment task.",
  "missing_activities": ["Pre-brief with executive's staff"],
  "improvement": "Add task for pre-briefing executive's admin/chief of staff"
}
```

#### Dimension 2: Timeline Realism (1-5)

**Question**: Are task durations and sequencing realistic and achievable?

**Scoring**:
- **5 - Highly Realistic**: Durations match typical patterns, appropriate buffers, dependencies correct
- **4 - Mostly Realistic**: Minor timing issues, but generally achievable
- **3 - Somewhat Realistic**: Some tasks under/over-estimated, may cause stress
- **2 - Unrealistic**: Several timing problems, likely to miss deadline
- **1 - Infeasible**: Timeline impossible to execute

**Key Checks**:
- [ ] Deck creation: 1-2 weeks (for executive review)
- [ ] Data collection: 3-5 days (depends on data availability)
- [ ] Review cycles: 2-3 days per cycle
- [ ] Q&A prep: 2-3 days
- [ ] Buffer time: 10-20% of total duration
- [ ] Dependencies: Correct sequencing (data before deck, draft before review)

**Example Evaluation**:
```json
{
  "dimension": "timeline_realism",
  "score": 3,
  "reasoning": "Deck creation allocated 1 week is reasonable. However, data collection (1 day) is too optimistic - typically takes 4-5 days due to engineering team availability.",
  "unrealistic_tasks": [
    {"task": "Collect metrics", "allocated": "1 day", "typical": "4-5 days"}
  ],
  "improvement": "Increase data collection to 4 days, start earlier"
}
```

#### Dimension 3: Dependency Accuracy (1-5)

**Question**: Are task dependencies correctly identified and sequenced?

**Scoring**:
- **5 - Perfect**: All dependencies correct, no circular deps, logical flow
- **4 - Mostly Correct**: Minor dependency issues, overall flow is sound
- **3 - Some Issues**: Several dependency problems, but plan still executable
- **2 - Significant Issues**: Many dependency errors, will cause execution problems
- **1 - Broken**: Circular dependencies, impossible sequencing

**Dependency Types**:
- **Sequential**: Task B starts after Task A completes
- **Parallel**: Tasks can run simultaneously
- **Blocking**: Task B cannot start until Task A is 100% done
- **Soft Dependency**: Task B benefits from Task A but can start without it

**Example Evaluation**:
```json
{
  "dimension": "dependency_accuracy",
  "score": 4,
  "reasoning": "Most dependencies correct: data → deck → review → finalize. One issue: Q&A prep should depend on first review cycle (to know what questions to expect), not just deck completion.",
  "dependency_errors": [
    {
      "task": "Q&A preparation",
      "current_dependencies": ["Deck creation"],
      "should_be": ["First review cycle"],
      "reason": "Q&A questions emerge during review, not just from deck"
    }
  ],
  "improvement": "Add dependency: Q&A prep → First review cycle"
}
```

#### Dimension 4: Actionability (1-5)

**Question**: Is the plan detailed enough to execute without ambiguity?

**Scoring**:
- **5 - Highly Actionable**: Clear owners, specific deliverables, concrete steps
- **4 - Mostly Actionable**: Minor ambiguities, but generally clear
- **3 - Somewhat Actionable**: Vague in places, requires interpretation
- **2 - Limited Actionability**: Many tasks too vague to execute
- **1 - Not Actionable**: Plan is abstract, cannot be executed

**Actionability Checklist**:
- [ ] Each task has clear owner (who)
- [ ] Each task has specific deliverable (what)
- [ ] Each task has concrete steps (how)
- [ ] Task descriptions are specific, not generic
- [ ] Success criteria defined (done when...)

**Example Evaluation**:
```json
{
  "dimension": "actionability",
  "score": 4,
  "reasoning": "Most tasks have clear owners and deliverables. Task 'Create deck' is too vague - should specify: outline structure, slide count, key messages, visual style.",
  "vague_tasks": [
    {
      "task": "Create executive deck",
      "issue": "Too generic, no guidance on structure/content",
      "improvement": "Break into subtasks: 1) Define storyline, 2) Create outline (15 slides), 3) Draft content, 4) Add visuals/data"
    }
  ],
  "improvement": "Decompose 'Create deck' into 4 concrete subtasks"
}
```

#### Dimension 5: Risk Awareness (1-5)

**Question**: Does the plan account for common risks and include mitigation strategies?

**Scoring**:
- **5 - Highly Risk-Aware**: All major risks identified, mitigation plans included
- **4 - Risk-Aware**: Most risks covered, reasonable mitigation
- **3 - Some Risk Awareness**: Basic risks mentioned, limited mitigation
- **2 - Limited Risk Awareness**: Few risks identified, no mitigation
- **1 - Risk-Blind**: No risk consideration

**Common Risks**:
- [ ] Data delays (engineering team busy, data quality issues)
- [ ] Reviewer availability (stakeholders traveling, schedule conflicts)
- [ ] Scope creep (executive requests additional analysis)
- [ ] Technical issues (demo breaks, file corruption)
- [ ] Last-minute changes (priorities shift, new directives)

**Example Evaluation**:
```json
{
  "dimension": "risk_awareness",
  "score": 3,
  "reasoning": "Plan includes buffer time (good) but doesn't explicitly identify risks or mitigation strategies. No contingency for common issues like data delays or reviewer unavailability.",
  "missing_risks": [
    "Data collection delays (engineering team bandwidth)",
    "Reviewer availability conflicts",
    "Demo technical issues"
  ],
  "suggested_mitigations": [
    "Request data 5 days early instead of 3",
    "Schedule backup review slots with alternate reviewers",
    "Test demo in production-like environment 2 days before"
  ],
  "improvement": "Add 'Notes' section with risk mitigation strategies"
}
```

### 3.2 Composite Quality Score

**Overall Score Formula**:

```python
def compute_workback_plan_quality_score(evaluations):
    """
    Compute composite quality score from 5 dimensions
    
    Weighted average:
    - Completeness: 25% (most important - must have all activities)
    - Timeline Realism: 25% (critical for execution)
    - Dependency Accuracy: 20% (affects coordination)
    - Actionability: 20% (determines execution ease)
    - Risk Awareness: 10% (nice to have, but less critical)
    """
    
    weights = {
        'completeness': 0.25,
        'timeline_realism': 0.25,
        'dependency_accuracy': 0.20,
        'actionability': 0.20,
        'risk_awareness': 0.10
    }
    
    weighted_score = sum(
        evaluations[dim]['score'] * weights[dim]
        for dim in weights.keys()
    )
    
    return {
        'overall_score': round(weighted_score, 2),
        'grade': get_grade(weighted_score),
        'dimension_scores': {dim: evaluations[dim]['score'] for dim in weights.keys()},
        'weighted_contribution': {dim: evaluations[dim]['score'] * weights[dim] for dim in weights.keys()}
    }

def get_grade(score):
    if score >= 4.5: return 'A (Excellent)'
    elif score >= 4.0: return 'B (Good)'
    elif score >= 3.5: return 'C (Acceptable)'
    elif score >= 3.0: return 'D (Needs Improvement)'
    else: return 'F (Poor)'
```

**Example Evaluation Report**:

```json
{
  "workback_plan_id": "Rajesh_Review_Dec2025",
  "evaluated_date": "2025-11-12",
  "evaluator": "Expert PM",
  
  "dimension_scores": {
    "completeness": {
      "score": 4,
      "reasoning": "Missing stakeholder pre-alignment",
      "weight": 0.25,
      "weighted_score": 1.0
    },
    "timeline_realism": {
      "score": 3,
      "reasoning": "Data collection too optimistic (1 day vs 4-5 typical)",
      "weight": 0.25,
      "weighted_score": 0.75
    },
    "dependency_accuracy": {
      "score": 4,
      "reasoning": "Q&A prep should depend on first review cycle",
      "weight": 0.20,
      "weighted_score": 0.8
    },
    "actionability": {
      "score": 4,
      "reasoning": "'Create deck' task too vague",
      "weight": 0.20,
      "weighted_score": 0.8
    },
    "risk_awareness": {
      "score": 3,
      "reasoning": "Has buffer but no explicit risk mitigation",
      "weight": 0.10,
      "weighted_score": 0.3
    }
  },
  
  "overall_score": 3.65,
  "grade": "C (Acceptable)",
  "percentile": "60th",
  
  "strengths": [
    "Good task coverage (completeness: 4/5)",
    "Dependencies mostly correct (4/5)",
    "Clear owners and deliverables (actionability: 4/5)"
  ],
  
  "weaknesses": [
    "Timeline for data collection unrealistic (3/5)",
    "Missing risk mitigation strategies (3/5)"
  ],
  
  "recommendations": [
    "1. Increase data collection timeline to 4-5 days",
    "2. Add stakeholder pre-alignment task (brief exec's chief of staff)",
    "3. Add risk mitigation section with contingency plans",
    "4. Make Q&A prep dependent on first review cycle, not just deck completion",
    "5. Break 'Create deck' into concrete subtasks"
  ],
  
  "pass_threshold": 3.5,
  "status": "PASS (3.65 >= 3.5)"
}
```

### 3.3 Automated Evaluation Pipeline

```python
class WorkbackPlanEvaluator:
    """
    Automated evaluation of workback plans using rubric
    """
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.rubric = load_evaluation_rubric()
    
    def evaluate_plan(self, workback_plan, context=None):
        """
        Evaluate a workback plan across all 5 dimensions
        """
        evaluations = {}
        
        # Dimension 1: Completeness
        evaluations['completeness'] = self.evaluate_completeness(workback_plan)
        
        # Dimension 2: Timeline Realism
        evaluations['timeline_realism'] = self.evaluate_timeline(workback_plan, context)
        
        # Dimension 3: Dependency Accuracy
        evaluations['dependency_accuracy'] = self.evaluate_dependencies(workback_plan)
        
        # Dimension 4: Actionability
        evaluations['actionability'] = self.evaluate_actionability(workback_plan)
        
        # Dimension 5: Risk Awareness
        evaluations['risk_awareness'] = self.evaluate_risk_awareness(workback_plan)
        
        # Compute composite score
        overall = compute_workback_plan_quality_score(evaluations)
        
        return {
            'dimension_evaluations': evaluations,
            'overall': overall,
            'recommendations': self.generate_recommendations(evaluations)
        }
    
    def evaluate_completeness(self, plan):
        """Check if all necessary work streams are present"""
        required_work_streams = [
            'data_collection',
            'content_creation',
            'review_cycles',
            'qa_preparation',
            'final_review'
        ]
        
        present = []
        missing = []
        
        for stream in required_work_streams:
            if self.has_work_stream(plan.tasks, stream):
                present.append(stream)
            else:
                missing.append(stream)
        
        score = (len(present) / len(required_work_streams)) * 5
        
        return {
            'score': round(score),
            'present': present,
            'missing': missing,
            'reasoning': f"Found {len(present)}/{len(required_work_streams)} required work streams"
        }
    
    def evaluate_timeline(self, plan, context):
        """Check if task durations are realistic"""
        # Use LLM to assess realism
        prompt = f"""
        Evaluate the timeline realism of this workback plan:
        
        {json.dumps(plan.model_dump(), indent=2)}
        
        Context: {context}
        
        For each task, assess if the duration is:
        - Too short (underestimated)
        - Appropriate (realistic)
        - Too long (overestimated)
        
        Score on 1-5 scale:
        5 = All durations realistic
        4 = Most realistic, minor issues
        3 = Some unrealistic durations
        2 = Many unrealistic durations
        1 = Timeline infeasible
        
        Return JSON:
        {{
          "score": <1-5>,
          "reasoning": "<explanation>",
          "unrealistic_tasks": [<list of tasks with timing issues>]
        }}
        """
        
        result = self.llm_client.query(prompt, temperature=0.1)
        return json.loads(result)
    
    def evaluate_dependencies(self, plan):
        """Check for dependency errors"""
        errors = []
        
        # Check for circular dependencies
        if has_circular_dependencies(plan.tasks):
            errors.append("Circular dependencies detected")
        
        # Check for missing dependencies
        for task in plan.tasks:
            if self.should_have_dependencies(task) and not task.dependencies:
                errors.append(f"Task '{task.name}' likely needs dependencies")
        
        # Check for incorrect sequencing
        for task in plan.tasks:
            for dep_id in task.dependencies:
                dep_task = find_task_by_id(plan.tasks, dep_id)
                if dep_task.due_date >= task.start_date:
                    errors.append(f"Dependency timing issue: {task.name} starts before {dep_task.name} completes")
        
        score = max(1, 5 - len(errors))
        
        return {
            'score': score,
            'errors': errors,
            'reasoning': f"Found {len(errors)} dependency issues"
        }
    
    def evaluate_actionability(self, plan):
        """Check if tasks are specific and executable"""
        vague_tasks = []
        
        for task in plan.tasks:
            # Check for vague descriptions
            if len(task.description) < 50:
                vague_tasks.append(f"{task.name}: Description too short")
            
            # Check for missing participants
            if not task.participants:
                vague_tasks.append(f"{task.name}: No participants assigned")
            
            # Check for generic names
            if any(generic in task.name.lower() for generic in ['create', 'prepare', 'work on']):
                if len(task.description) < 100:
                    vague_tasks.append(f"{task.name}: Generic name with short description")
        
        score = max(1, 5 - len(vague_tasks))
        
        return {
            'score': score,
            'vague_tasks': vague_tasks,
            'reasoning': f"Found {len(vague_tasks)} actionability issues"
        }
    
    def evaluate_risk_awareness(self, plan):
        """Check if common risks are addressed"""
        # Check for buffer time
        has_buffer = any('buffer' in task.name.lower() or task.description.lower() 
                        for task in plan.tasks)
        
        # Check for risk mitigation in notes
        has_risk_notes = any('risk' in note.lower() or 'contingency' in note.lower() 
                            for note in plan.notes)
        
        # Check for backup plans
        has_backup = any('backup' in task.name.lower() or 'alternative' in task.description.lower()
                        for task in plan.tasks)
        
        risk_score = sum([has_buffer, has_risk_notes, has_backup])
        score = 1 + (risk_score * 1.33)  # Scale 0-3 to 1-5
        
        return {
            'score': round(score),
            'has_buffer': has_buffer,
            'has_risk_notes': has_risk_notes,
            'has_backup_plans': has_backup,
            'reasoning': f"Risk awareness indicators: {risk_score}/3"
        }
```

---

## Implementation Roadmap

### Phase 1: Historical Data Extraction (Weeks 1-2)

**Goal**: Extract 5-10 historical workback plans from your past exec reviews

**Steps**:
1. **Identify target events**: Past Gaurav reviews (last 6 months)
2. **Collect data sources**: 
   - Email export (search: "Gaurav review", "exec prep")
   - Calendar export (meetings 2-4 weeks before reviews)
   - File history (OneDrive/SharePoint: presentation decks, data files)
   - ADO work items (WIQL query for prep tasks)
3. **Reconstruct plans**: Use reconstruction algorithm
4. **Validate**: Compare reconstructed plan to what actually happened

**Deliverable**: `historical_workback_plans_10.json`

### Phase 2: Synthetic Data Generation (Weeks 3-4)

**Goal**: Generate 20-30 synthetic variations

**Steps**:
1. **Create base templates**: One per event type (CVP review, VP review, milestone)
2. **Parameterize**: Define variation parameters (duration, format, complexity)
3. **Generate variations**: 2-3 per base template
4. **LLM enhancement**: Add realistic details

**Deliverable**: `synthetic_workback_plans_30.json`

### Phase 3: Evaluation Framework (Week 5)

**Goal**: Implement rubric and evaluation pipeline

**Steps**:
1. **Implement evaluator class**: `WorkbackPlanEvaluator`
2. **Test on historical plans**: Validate rubric makes sense
3. **Create evaluation UI**: HTML interface for human evaluation

**Deliverable**: `workback_plan_evaluator.py` + `evaluation_results.json`

### Phase 4: Training Dataset Creation (Week 6)

**Goal**: Format 40-50 examples for model training

**Steps**:
1. **Combine historical + synthetic**: 60/40 split
2. **Quality filter**: Only plans scoring 3.5+
3. **Format for SFT**: Create input/output pairs
4. **Add evaluation scores**: Include scores as quality signal

**Deliverable**: `workback_plan_training_data_50.jsonl`

---

## Next Steps (This Week)

### Immediate Action Items

**Day 1-2: Calendar Analysis**
```bash
# Extract your calendar to find past executive reviews
python extract_exec_reviews_from_calendar.py \
  --start-date 2025-04-01 \
  --end-date 2025-11-12 \
  --exec-names "Gaurav,Rajesh,CVP" \
  --output past_exec_reviews.json
```

**Day 3-4: Historical Data Collection**
```bash
# For each past exec review, collect preparation data
python extract_historical_workback_plan.py \
  --event "Gaurav Review - Oct 2025" \
  --event-date 2025-10-15 \
  --prep-window-weeks 4 \
  --data-sources email,calendar,files,ado \
  --output historical_gaurav_oct2025.json
```

**Day 5: Create Evaluation Framework**
```bash
# Implement the rubric evaluator
touch workback_ado/workback_plan_evaluator.py

# Test on first historical plan
python workback_ado/workback_plan_evaluator.py \
  --input historical_gaurav_oct2025.json \
  --output evaluation_gaurav_oct2025.json
```

---

## Summary: Your 3-Task Strategy

| Task | Approach | Deliverable | Timeline |
|------|----------|-------------|----------|
| **1. Event Targeting** | Calendar pattern detection → Identify Rajesh review (Dec 12) + other exec reviews | List of target events needing workback plans | Week 1 |
| **2. Training Data** | Extract historical plans (past Gaurav reviews) + Generate synthetic variations | 40-50 training examples | Weeks 1-4 |
| **3. Evaluation** | 5-dimension rubric (completeness, timeline, dependencies, actionability, risk) | Evaluation framework + scores for all plans | Week 5 |

**First Concrete Use Case**: Create workback plan for Rajesh review (Dec 12, 2025) by learning from your past Gaurav review preparations.

**Key Insight**: Your historical preparation patterns are **gold-standard training data** because they represent what actually worked in your real work environment.
