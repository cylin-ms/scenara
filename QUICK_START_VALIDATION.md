# 🎯 Quick Start - Meeting Validation App

## One-Command Start

```powershell
.\START_VALIDATION.ps1
```

That's it! The app will:
1. ✅ Check/install Flask if needed
2. 🚀 Start the web server
3. 🌐 Open your browser automatically

## What You'll See

A beautiful web interface showing:
- All 8 meetings from today (October 28, 2025)
- GPT-5 and GitHub Copilot classifications side-by-side
- Interactive buttons to rate each classification
- Dropdown menus to select correct type if AI was wrong
- Real-time accuracy statistics
- Progress tracking

## How to Validate (Super Easy!)

For each meeting:

1. **Read the meeting details** (subject, time, description)
2. **Review AI classifications** (left = GPT-5, right = Copilot)
3. **Click ✓ Correct or ✗ Incorrect** for each model
4. **If incorrect**: Select the correct type from dropdown
5. **Add notes** (optional) - your reasoning
6. **Rate difficulty**: Easy 😊 / Medium 🤔 / Hard 😰
7. **Click "💾 Save Validation"**
8. **Auto-scroll to next meeting** ✨

## Time Required

⏱ **5-10 minutes total** (~1 minute per meeting)

## Live Statistics

Watch accuracy update in real-time:
- **Total Meetings**: 8
- **Validated**: Updates as you go
- **GPT-5 Accuracy**: % correct
- **Copilot Accuracy**: % correct

## Export Results

Click **"📊 Export Results"** button (bottom-right corner) to download:
- `human_validation_results.json`
- All your ratings and corrections
- Ready for analysis

## Meeting Types Available

When selecting correct type, choose from 31+ options across 5 categories:

**1. Internal Recurring Meetings**
- Team Status Update, Progress Review, 1:1, Action Review, Governance

**2. Strategic Planning & Decision**
- Planning, Decision-Making, Problem-Solving, Brainstorming, Workshops

**3. External & Client-Facing**
- Sales & Client, Vendor, Partnership, Interviews, Training

**4. Informational & Broadcast**
- All-Hands, Briefings, Training, Webinars

**5. Team-Building & Culture**
- Team-Building, Recognition, Communities of Practice

## Tips

💡 **High Confidence Cases** (99%)
- Usually correct - quick validation!
- Example: Meeting 2 "Virtual Interview"

💡 **Disagreement Cases** (models differ)
- Most interesting for learning
- Example: Meeting 1 "[Async Task]"
- Your expert judgment breaks the tie!

💡 **Keywords to Watch**
- "Meeting Prep" → Usually Planning
- "Sync" → Could be Status OR Planning (context matters)
- "Weekly Review" → Progress Review
- "Office Hours" → Informational

## Stopping the App

Press **Ctrl+C** in the terminal window

Results are saved automatically after each validation!

## Where Are Results Saved?

📁 `experiments/2025-10-28/human_validation_results.json`

Contains:
- Your correct/incorrect ratings for each model
- Correct classifications (when you provided them)
- Your notes and reasoning
- Difficulty ratings
- Timestamps

## Troubleshooting

**Port 5000 already in use?**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process
```

**Flask not installing?**
```powershell
pip install flask
```

**Browser didn't open?**
Manually navigate to: **http://localhost:5000**

## What's Next?

After validating all 8 meetings:

1. ✅ **Review your accuracy scores**
   - How did GPT-5 perform?
   - How did GitHub Copilot perform?
   - Which model is better?

2. 📊 **Export and analyze results**
   - Compare to 87.5% cross-model agreement
   - Identify error patterns
   - Suggest prompt improvements

3. 🔄 **Iterate if needed**
   - Refine prompt based on errors
   - Re-run experiments
   - Validate improvements

## Questions?

Check **VALIDATION_APP_README.md** for detailed documentation.

---

**Ready? Let's validate!** 🚀

```powershell
.\START_VALIDATION.ps1
```
