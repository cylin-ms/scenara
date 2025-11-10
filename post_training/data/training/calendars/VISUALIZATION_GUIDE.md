# Calendar Visualization Tool

**Purpose**: Visualize generated 4-week calendars in multiple formats for easy inspection and validation.

---

## Features

✅ **Weekly Grid View** - See all meetings organized by week and day (like Outlook/Google Calendar)  
✅ **Daily Timeline View** - Detailed view of a specific day with full meeting details  
✅ **Statistics Dashboard** - Importance distribution, prep time analysis, meeting types  
✅ **HTML Export** - Beautiful shareable calendar views  
✅ **Cross-Tier Comparison** - Compare multiple personas side-by-side

---

## Usage

### View Statistics
```bash
python post_training/tools/visualize_calendar.py \
  --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
  --view stats
```

Output:
```
Total Meetings: 97
Avg Meetings/Week: 24.2
Importance: 81% critical, 10% high, 8% medium
Prep Needed: 65 (67.0%)
Total Prep Time: 32.5 hours/month
```

### View Weekly Grid
```bash
python post_training/tools/visualize_calendar.py \
  --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
  --view week
```

Shows meetings organized by week and day with color-coded importance.

### View Daily Timeline
```bash
python post_training/tools/visualize_calendar.py \
  --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
  --view day \
  --date 2025-11-17
```

Shows detailed timeline for specific day including:
- Meeting subject, time, duration
- Importance level with reasoning
- Prep requirements
- Attendee counts
- Full descriptions

### Export to HTML
```bash
python post_training/tools/visualize_calendar.py \
  --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
  --output tier1_calendar.html
```

Creates beautiful HTML calendar with:
- Color-coded importance badges
- Prep time indicators
- Week-by-week organization
- Responsive design

### Compare Multiple Calendars
```bash
python post_training/tools/visualize_calendar.py \
  --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
  --calendar post_training/data/training/calendars/tier2_senior_ic_architect_calendar_4weeks.jsonl \
  --calendar post_training/data/training/calendars/tier3_specialist_legal_calendar_4weeks.jsonl \
  --compare \
  --view stats
```

Shows side-by-side comparison of:
- Total meetings
- Importance distribution
- Prep time requirements

---

## View Modes

| Mode | Description | Best For |
|------|-------------|----------|
| `week` | Weekly grid view | Seeing calendar patterns, recurring meetings |
| `day` | Daily timeline with details | Inspecting specific meeting details |
| `stats` | Statistics dashboard | Quick validation, distribution checks |
| `all` | All views combined | Complete overview (default) |

---

## HTML Calendars Generated

**Tier 1: Sales Manager - Pipeline Juggler**  
File: `tier1_calendar_view.html`  
- 97 meetings across 4 weeks
- 81% critical importance (high-stakes)
- 67% prep needed (~8 hours/week)
- Peak week: 30 meetings

**Tier 2: Senior IC - Technical Architect**  
File: `tier2_calendar_view.html`  
- 58 meetings across 4 weeks
- 29% critical, **50% medium** (balanced)
- 22% prep needed (~1.6 hours/week)
- Consistent: 14-16 meetings/week

**Tier 3: Legal Specialist - Contracts**  
File: `tier3_calendar_view.html`  
- 33 meetings across 4 weeks
- 64% critical (contract-focused)
- 21% prep needed (~0.9 hours/week)
- Steady: 8-9 meetings/week

---

## Color Coding

| Importance | Terminal Color | HTML Badge | Usage |
|------------|----------------|------------|-------|
| **Critical** 🔴 | Red | Red badge | Must attend, high stakes |
| **High** 🟡 | Yellow | Yellow badge | Important but not critical |
| **Medium** 🟢 | Green | Green badge | Standard priority |
| **Low** 🔵 | Blue | Blue badge | Optional, low priority |
| **Prep** 📝 | Magenta | Purple badge | Requires preparation |

---

## Key Insights from Visualization

### Tier 1 (Sales Manager)
- **Calendar Pressure**: 24 meetings/week = 6 hours/day in meetings
- **Recurring Pattern**: Weekly 1:1 (Monday 10am), Forecast Call (Tuesday 9am), Team Sync (Wednesday 2pm)
- **Peak Days**: Mondays and Tuesdays (5-6 meetings/day)
- **Customer Focus**: 40%+ meetings have external attendees
- **Prep Heavy**: 65 meetings need prep (8 hours/week)

### Tier 2 (Senior IC)
- **Balanced Load**: 14.5 meetings/week = 3.5 hours/day
- **Design Heavy**: Architecture reviews, design sessions, cross-team syncs
- **Learning Time**: Weekly learning sessions (Advanced Kubernetes, Observability)
- **Best Distribution**: 50% medium importance (team syncs, planning)
- **Technical Focus**: Most meetings internal (engineering team)

### Tier 3 (Legal Specialist)
- **Light Load**: 8.2 meetings/week = 2 hours/day
- **Contract Focus**: 60%+ meetings are contract reviews/negotiations
- **Recurring Pattern**: Weekly 1:1 (Monday 10am), Team Sync (Wednesday 2pm), Compliance Check-in (Thursday 11am)
- **External Vendors**: ~30% meetings with vendors/partners
- **Deadline Driven**: Most meetings critical (contract deadlines)

---

## Validation Checks

Use visualization to verify:

✅ **Recurring Meetings**: Same day/time each week?  
✅ **Work Hours**: All meetings 8am-6pm?  
✅ **Importance Distribution**: Matches persona tier expectations?  
✅ **Prep Time**: Reasonable for persona role?  
✅ **Meeting Subjects**: Authentic for function?  
✅ **Attendee Counts**: 2-15 attendees (realistic)?

---

## Example: Inspecting a Specific Day

```bash
python post_training/tools/visualize_calendar.py \
  --calendar post_training/data/training/calendars/tier1_sales_manager_pipeline_calendar_4weeks.jsonl \
  --view day \
  --date 2025-11-17
```

Output shows:
```
Monday, November 17, 2025

Meeting 1/4
🔴 Weekly 1:1 with Regional Director
⏰ 10:00 AM - 10:45 AM (45 minutes)
▸ Importance: CRITICAL
📝 Prep Required: 30 minutes
👥 Attendees: 1 required
Description: Discuss team performance, forecast accuracy, and strategic priorities.
Reasoning: Always important: forecast; Matches priority: Team performance (hit 120% quota)

Meeting 2/4
🔴 Regional Pipeline Review
⏰ 2:00 PM - 3:30 PM (90 minutes)
...
```

Perfect for:
- Quality checking generated meetings
- Validating importance labels
- Verifying prep time logic
- Inspecting reasoning explanations

---

## Tips

**Performance**:
- Weekly view can be long for 97-meeting calendars (use `| Select-Object -First 100` on Windows PowerShell)
- Daily view is fastest for spot checks
- Stats view is instant

**HTML Export**:
- Open HTML files in any browser
- Responsive design works on mobile
- Can share with stakeholders for review
- No dependencies (pure HTML/CSS)

**Comparison**:
- Use `--compare` flag to see trends across tiers
- Useful for validating relative importance distributions
- Helps identify outliers (e.g., Tier 3 should have lower critical %)

---

## Files

**Tool**: `visualize_calendar.py`  
**HTML Exports**:
- `tier1_calendar_view.html` (97 meetings)
- `tier2_calendar_view.html` (58 meetings)
- `tier3_calendar_view.html` (33 meetings)

**Source Data**:
- `tier1_sales_manager_pipeline_calendar_4weeks.jsonl`
- `tier2_senior_ic_architect_calendar_4weeks.jsonl`
- `tier3_specialist_legal_calendar_4weeks.jsonl`

---

## Next Steps

1. **Open HTML files** in browser to see visual calendars
2. **Spot check quality** - Review 5-10 meetings per tier
3. **Validate patterns** - Confirm recurring meetings repeat correctly
4. **Check edge cases** - Look for unusual meeting times or durations
5. **Share with team** - HTML files easy to share for feedback

**Status**: ✅ Visualization tool ready for all calendar data!
