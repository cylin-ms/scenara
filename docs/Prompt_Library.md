
# Prompt Library

## Issues
<table>
<tr>
<td></td><th>Pri</th><th>Meeting Surface</th><th>User Job</th><th>Mobile text (\<20 characters)</th><th>Prompt</th><th>Revised prompt</th><th>Expectations</th><th>Notes</th><th>Quality</th><th>Issue Type</th><th>How Found</th><th>Model</th><th>Input</th><th>Metadata</th><th>Response</th><th>Cohort</th><th>User</th></tr>
<tr>
<td></td><td>1</td><td>Form</td><td>Organizer Meeting Prep</td><td>Create an agenda</td><td>Go through my emails, chats and documents on /Meeting and create an agenda by asking me what goals I want to accomplish in the meeting</td><td></td><td>Includes the meeting’s themes from emails, chats and documents, a summary of the suggested agenda/topics.
- Well-organized (e.g., separated by sections or bullet points for each aspect).
- aks the user for the goals and provide suggestions based on the themes, Clearly states the meeting’s objective or outcome when the goal is provided (e.g., “to decide on X”, “to brainstorm Y”). References citations and links are provided inline. Include timeline for each agenda item and can be edited. Generates 3-4 agenda items for most meetings.</td><td>If there is a document (word doc, ppt or loop) that contains agenda then it should take that agenda into account and should not ask the user for the objectives or goals.</td><td>High </td><td>Relevent Content</td><td>Copilot Hub</td><td>GPT5</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr>
<td></td><td>1</td><td>Form</td><td>Organizer Meeting Prep</td><td>Create an agenda</td><td>Go through my emails, chats and documents on /Meeting and create an agenda by asking me what goals I want to accomplish in the meeting</td><td></td><td></td><td>Agenda risks being too generic (when no explicit reference to meeting) to first response being too detailed (because the project context is not clearly understood, but the model does ask for clarification and can be refined).</td><td>High </td><td>Generic content</td><td>Copilot Hub</td><td>GPT5</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr>
<td></td><td>1</td><td>Form</td><td>Organizer Meeting Prep</td><td>Create an agenda</td><td>Go through my emails, chats and documents on /Meeting and create an agenda by asking me what goals I want to accomplish in the meeting</td><td></td><td></td><td>Reduce the verbosity to fit a mobile experience (define redability metric). </td><td>High </td><td>Not mobile friendly</td><td>Outlook Mobile</td><td>GPT5</td><td></td><td></td><td></td><td></td><td></td></tr>
<tr>
<td></td><td>1</td><td>Form</td><td>Organizer Meeting Prep</td><td>Create an agenda</td><td>Go through my emails, chats and documents on /Meeting and create an agenda by asking me what goals I want to accomplish in the meeting</td><td></td><td></td><td> If meeting is not explicitly specified, in-correctly identifies which meeting (e.g., the next one on the calendar) and focuses on that. It should prompt the user instead to confirm the right meeting. </td><td>High </td><td>System Prompting </td><td>Copilot Hub</td><td>GPT5</td><td>Meeting Context</td><td></td><td>Proposed Agenda (50 min)
0:00–0:05 — Kickoff & Goal Setting
Confirm top three outcomes for today (see options below).
Quick review of last meeting’s action items (PM Team Meeting 2025-09-25, Meeting Notes 2025-10-02). [PM Team Meeting \ Meeting]
0:05–0:15 — Customer Engagement & Product Prioritization
Status on lighthouse customers (Goldman Sachs, Kaiser, Walmart, Stryker) and integration feedback.
Review customer calls cadence and next steps for McKinsey and PwC threads. [PM Team Meeting \ Meeting], [PM Team Meeting \ Meeting]
0:15–0:25 — Technical Rollouts & Operational Scale
Customer Zero rollout progress and blockers (desk booking, device auto check-in).
Streamlining device-to-desk mapping and GUI proposals.
Updates on Bizchat DSATs analysis and FHL event prep. [PM Team Meeting \ Meeting], [PM Team Meeting \ Meeting]
0:25–0:35 — AI Features & Copilot Strategy
Golden prompts and prompt-driven development priorities.
Immersive Search, meeting prep, and evaluation practices.
Sticky Peak integration and preconditions for Copilot replies. [PM Team Meeting \ Meeting], [PM Team Meeting \ Meeting]
0:35–0:45 — Metrics, OKRs & Communication
Define 1–3 key metrics for the next year (weekly active users, adoption goals).
Newsletter cadence and scorecard updates for leadership visibility.
Alignment with organizational strategy and escalation of unclear priorities. [PM Team Meeting \ Meeting], [PM Team Meeting \ Meeting]
0:45–0:50 — Wrap-Up & Action Items
Confirm owners for tasks like:
Copilot query tool training and insight engine usage.
Customer engagement documentation for RTO initiatives.
Engineering weekly updates and meeting documentation. [PM Team Meeting \ Meeting]
Pre-Reads & References
Meeting Notes 2025-10-02 — latest notes and tasks.
PM Team Meeting 2025-09-25 — prior meeting summary and backlog items. [PM Team Meeting \ Meeting]
Quick Question to Finalize
Which three outcomes do you want to drive in this meeting? Here are some options based on recent priorities:
Lock Customer Zero rollout blockers and next steps.
Define golden prompts and Copilot preconditions for Q4.
Confirm metrics and newsletter strategy for leadership alignment.
Decide on Bizchat DSATs fixes and FHL event deliverables.
Align on EU settlement compliance and feature exposure timelines. [PM Team Meeting \ Meeting]
Reply with your top three (or alternatives). I’ll refine the agenda flow and can also post the final version into the meeting Loop and invite if you’d like.</td><td>Organizer</td><td></td></tr>

