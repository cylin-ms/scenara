# Outlook-Style Calendar Interface Guide

## Overview

The interactive Outlook-style calendar provides a realistic, Microsoft Outlook-inspired interface for viewing and analyzing generated training data calendars.

**File**: `outlook_calendar_interactive.html`

## Features

### 🎨 **Authentic Outlook Design**
- **Blue ribbon header** matching Outlook's design language
- **Week view layout** with time slots (8 AM - 6 PM)
- **Color-coded meetings** by importance level
- **Hover tooltips** with full meeting details
- **Statistics panel** showing weekly metrics

### 📅 **Calendar Views**

#### Week View
- **7-day layout** (Monday - Sunday)
- **Time slots** displayed on left (8 AM - 6 PM)
- **Meeting blocks** positioned by actual time
- **Visual duration** - block height = meeting length

#### Meeting Display
- **Time label** (e.g., "9:00 AM")
- **Subject line** with overflow truncation
- **Prep indicator** (📝 badge) for meetings requiring prep
- **Color-coded border** showing importance level

### 🎯 **Color Coding**

| Importance | Color | Border | Usage |
|-----------|-------|---------|-------|
| **🔴 Critical** | Light red gradient | Red | High-stakes customer meetings, escalations |
| **🟡 High** | Light yellow gradient | Orange | Important reviews, decision meetings |
| **🟢 Medium** | Light green gradient | Green | Team syncs, regular 1:1s |
| **🔵 Low** | Light blue gradient | Blue | Optional trainings, social events |

### 💡 **Interactive Features**

#### 1. Persona Switcher
- **Dropdown menu** in header (top-right)
- Switch between:
  - Tier1 Sales Manager Pipeline
  - Tier2 Senior Ic Architect
  - Tier3 Specialist Legal

#### 2. Week Navigation
- **◀ Previous** button - Navigate to earlier weeks
- **Week label** - Shows current week range (e.g., "Nov 17 - Nov 23")
- **Next ▶** button - Navigate to later weeks

#### 3. Meeting Tooltips
**Hover over any meeting** to see:
- Full subject line
- Start/end time with duration
- Importance badge
- Prep time needed (if applicable)
- Attendee count
- Meeting type (recurring/ad-hoc)
- Description preview
- AI reasoning for importance label

#### 4. Statistics Panel (Right Side)

**Week Overview**:
- Total meetings in current week
- Average meeting duration
- Total prep time needed

**Importance Distribution**:
- Visual bar chart showing proportions
- Count by importance level
- Validates tier differentiation

**Meeting Types**:
- Recurring vs. ad-hoc count
- Shows meeting pattern balance

## How to Use

### Opening the Calendar

1. Navigate to: `post_training/data/training/calendars/`
2. Double-click: `outlook_calendar_interactive.html`
3. Opens in your default web browser

### Inspecting Different Personas

```
1. Open calendar in browser
2. Click persona dropdown (top-right)
3. Select different tier:
   - Tier 1: High-stakes sales (81% critical)
   - Tier 2: Balanced IC workload (50% medium)
   - Tier 3: Contract-focused legal (64% critical)
4. Observe differences in:
   - Meeting density
   - Color distribution
   - Prep indicators
```

### Navigating Weeks

```
1. Start at Week 1 (Nov 17-23 for Tier 1)
2. Click "Next ▶" to see Week 2, 3, 4
3. Click "◀ Previous" to go back
4. Notice patterns:
   - Recurring meetings same day/time
   - Ad-hoc meetings scattered
   - Calendar pressure varies by week
```

### Analyzing Meeting Quality

**Hover over meetings** to verify:
- ✅ Subject matches persona role
- ✅ Importance reasoning makes sense
- ✅ Prep time appropriate (30-60 min for critical)
- ✅ Attendee count realistic (2-15)
- ✅ Recurring meetings show pattern
- ✅ Description provides context

## Visual Examples

### Tier 1 Sales Manager - Typical Monday

```
8:00 AM  ────────────────────────────────
         
9:00 AM  ┌──────────────────────────────┐
         │ 🔴 Weekly Forecast Call      │
         │ 9:00 AM - 10:00 AM (60 min) │
         │ 📝 Prep: 30 min              │
         └──────────────────────────────┘
         
10:00 AM ┌──────────────────────────────┐
         │ 🔴 Weekly 1:1: Regional Dir  │
         │ 10:00 AM - 10:30 AM (30 min)│
         └──────────────────────────────┘
         
11:00 AM ┌──────────────────────────────┐
         │ 🔴 Customer Escalation       │
         │ 11:00 AM - 12:00 PM (60 min)│
         │ 📝 Prep: 45 min              │
         └──────────────────────────────┘
         
2:00 PM  ┌──────────────────────────────┐
         │ 🟡 Deal Review: APAC Q4      │
         │ 2:00 PM - 3:30 PM (90 min)  │
         │ 📝 Prep: 30 min              │
         └──────────────────────────────┘
```

**Observations**:
- ✅ Back-to-back meetings in morning
- ✅ High density (4 meetings before lunch)
- ✅ All critical/high importance
- ✅ 105 minutes prep time needed
- ✅ ~4.5 hours in meetings

### Tier 2 Senior IC - Typical Wednesday

```
10:00 AM ┌──────────────────────────────┐
         │ 🟢 Learning Session          │
         │ 10:00 AM - 11:00 AM (60 min)│
         └──────────────────────────────┘
         
11:00 AM ────────────────────────────────

2:00 PM  ┌──────────────────────────────┐
         │ 🟢 Weekly Team Sync          │
         │ 2:00 PM - 3:00 PM (60 min)  │
         └──────────────────────────────┘
         
3:30 PM  ┌──────────────────────────────┐
         │ 🔴 Architecture Review       │
         │ 3:30 PM - 5:00 PM (90 min)  │
         │ 📝 Prep: 45 min              │
         └──────────────────────────────┘
```

**Observations**:
- ✅ Balanced importance (2 medium, 1 critical)
- ✅ Gaps for focused work time
- ✅ 3 meetings total (~3.5 hours)
- ✅ Learning session (medium priority)
- ✅ Only 1 meeting needs prep

## Quality Validation Checklist

### ✅ Visual Inspection

- [ ] **Time slots accurate** - Meetings positioned at correct times
- [ ] **Duration realistic** - No 5-minute or 4-hour meetings
- [ ] **Work hours respected** - All meetings between 8 AM - 6 PM
- [ ] **Color distribution varies** - Tier 1 mostly red, Tier 2 balanced
- [ ] **Prep indicators present** - Customer meetings, escalations show 📝

### ✅ Temporal Patterns

- [ ] **Recurring meetings consistent**
  - Weekly 1:1 → Every Monday 10:00 AM
  - Team Sync → Every Wednesday 2:00 PM
  - Same day/time across weeks
  
- [ ] **Ad-hoc meetings scattered**
  - Different times each week
  - Various durations
  - Mix of importance levels

### ✅ Persona Differentiation

| Metric | Tier 1 | Tier 2 | Tier 3 |
|--------|---------|---------|---------|
| **Meetings/Week** | 24-30 | 10-16 | 8-9 |
| **Critical %** | 80%+ | 20-30% | 60-65% |
| **Prep Indicators** | 65-70% | 20-25% | 20-25% |
| **Meeting Focus** | Customer/Sales | Design/Tech | Contracts/Legal |
| **Color Dominance** | 🔴 Red | 🟢 Green | 🔴 Red + 🟡 Yellow |

### ✅ Meeting Content Quality

**Hover 10 random meetings per tier**, verify:
- [ ] Subject line matches persona role
- [ ] Importance reasoning makes logical sense
- [ ] Prep time appropriate for importance level
- [ ] Attendee count realistic (2-15)
- [ ] Description provides relevant context
- [ ] Type (recurring/ad-hoc) matches pattern

## Statistics Panel Validation

### Week Overview Metrics

**Tier 1 Sales Manager** (Target):
```
Total Meetings: 24-30
Avg Duration: 55-65 minutes
Prep Time Needed: 6-10 hours/week
```

**Tier 2 Senior IC** (Target):
```
Total Meetings: 10-16
Avg Duration: 60-70 minutes
Prep Time Needed: 1-3 hours/week
```

**Tier 3 Legal Specialist** (Target):
```
Total Meetings: 8-9
Avg Duration: 45-60 minutes
Prep Time Needed: 0.5-1.5 hours/week
```

### Importance Bar Chart

Should show:
- **Tier 1**: Dominated by red (critical) segment
- **Tier 2**: Balanced mix, green (medium) largest
- **Tier 3**: Red (critical) + yellow (high) predominant

## Key Insights from Visualization

### 1. Calendar Pressure Simulation

**Tier 1 (Sales Manager)**:
- Visual: Back-to-back red/yellow blocks
- Pattern: Little white space during work hours
- Insight: Simulates high-stakes, overbooked calendar
- Validation: ✅ Realistic for manager-level sales

**Tier 2 (Senior IC)**:
- Visual: Scattered green/yellow blocks with gaps
- Pattern: Balanced meeting distribution
- Insight: Time for focused work between meetings
- Validation: ✅ Realistic for senior individual contributor

**Tier 3 (Legal Specialist)**:
- Visual: Fewer blocks, critical concentration
- Pattern: Light meeting load, deadline-driven
- Insight: Focused on contract reviews/negotiations
- Validation: ✅ Realistic for legal specialist role

### 2. Recurring Meeting Patterns

**Visual Validation**:
```
Week 1: Monday 10:00 AM - Weekly 1:1
Week 2: Monday 10:00 AM - Weekly 1:1
Week 3: Monday 10:00 AM - Weekly 1:1
Week 4: Monday 10:00 AM - Weekly 1:1
```

**What to Look For**:
- Same meeting subject across weeks
- Same day of week
- Same time slot
- Same duration
- Consistent importance label

### 3. Meeting Subject Authenticity

**Tier 1 Examples** (should see):
- "Customer Escalation: [Company Name]"
- "Q4 Forecast Deep Dive"
- "Weekly Pipeline Review"
- "Client Demo: [Product Feature]"
- "Deal Review: [Region]"

**Tier 2 Examples** (should see):
- "Architecture Review: [System Component]"
- "Design Review: [API/Feature]"
- "Learning Session: [Technology]"
- "Cross-Team Sync: [Integration]"
- "Code Review: [Module]"

**Tier 3 Examples** (should see):
- "Contract Review: [Agreement Type]"
- "Vendor Negotiation: [Service]"
- "Legal Consultation: [Topic]"
- "Compliance Review: [Area]"
- "Risk Assessment: [Contract]"

## Comparison with Static HTML

| Feature | Static HTML | Outlook Interface |
|---------|-------------|-------------------|
| **Layout** | List view by day | Week grid with time slots |
| **Visual** | Badges and text | Positioned blocks like Outlook |
| **Navigation** | Scroll through all weeks | Week-by-week navigation |
| **Interactivity** | Static display | Hover tooltips, persona switching |
| **Statistics** | End summary | Live panel on right |
| **Time Slots** | Implicit (timestamps) | Explicit (8 AM - 6 PM grid) |
| **Meeting Duration** | Text (e.g., 60 min) | Visual (block height) |
| **Calendar Pressure** | Hard to visualize | Immediately visible |
| **Best For** | Documentation | Analysis and validation |

## Browser Compatibility

✅ **Works in**:
- Chrome/Edge (recommended)
- Firefox
- Safari
- Any modern browser with JavaScript

❌ **Limitations**:
- No drag-and-drop editing (view-only)
- No calendar export
- Local HTML file only (no backend)

## Tips for Quality Review

### 1. Quick Spot Check (5 minutes)

```
1. Open calendar → Select Tier 1
2. Look at Week 1 Monday
3. Verify: 3-5 meetings, mostly red
4. Hover one meeting → Check tooltip details
5. Click "Next" → See Week 2 Monday
6. Verify: Recurring meetings same time
7. Switch to Tier 2 → Compare color distribution
8. Check statistics panel → Validate percentages
```

### 2. Deep Dive (30 minutes)

```
For each tier:
1. Navigate all 4 weeks
2. Verify recurring pattern consistency
3. Hover 10 random meetings
4. Check subject/importance reasoning
5. Validate prep indicators
6. Confirm work hours (8 AM - 6 PM)
7. Review statistics match expectations
8. Compare with persona definition
```

### 3. Cross-Tier Comparison

```
1. Load Tier 1 → Navigate Week 2
2. Screenshot or note patterns
3. Switch to Tier 2 → Same week
4. Compare:
   - Meeting density (Tier 1 >> Tier 2)
   - Color distribution (Tier 1 red, Tier 2 green)
   - Prep indicators (Tier 1 ~70%, Tier 2 ~20%)
5. Repeat for Tier 3
6. Validate tier differentiation working
```

## Troubleshooting

### Issue: Calendar not loading
**Solution**: Check browser JavaScript is enabled

### Issue: No meetings visible
**Solution**: Verify JSONL files in correct location, check file paths in HTML

### Issue: Tooltip cut off on right edge
**Solution**: Tooltip auto-repositions to left side if near screen edge

### Issue: Persona dropdown empty
**Solution**: Ensure calendar data embedded in HTML correctly

## Next Steps

1. **Open Calendar**: Double-click `outlook_calendar_interactive.html`
2. **Review All Personas**: Use dropdown to switch between tiers
3. **Validate Patterns**: Navigate weeks, hover meetings, check statistics
4. **Compare to Persona Definitions**: Verify meeting subjects/importance match rules
5. **Share with Team**: Send HTML file for stakeholder review
6. **Document Findings**: Note any quality issues or improvements needed

---

**Generated**: November 2025  
**Format**: Interactive HTML (self-contained, no dependencies)  
**Data Source**: GPT-5 generated calendars (4 weeks each)  
**Purpose**: Validate training data quality before full-scale generation
