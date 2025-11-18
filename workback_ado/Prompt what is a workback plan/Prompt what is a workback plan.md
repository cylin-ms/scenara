# Prompt: what is a workback plan  
**Building an “Automatic Work‑Back Plan Generator” Agent**  
Below is a complete play‑book you can follow to design, develop, test, and ship an autonomous agent that takes a single end‑goal description (e.g., “Launch the new e‑commerce site on 30 Oct 2025”) and spits out a ready‑to‑use workbook(Excel, Google‑Sheets, CSV, etc.) containing:  
* Milestones, tasks, sub‑tasks  
* Estimated durations & buffers  
* Dependencies & critical‑path identification  
* Owner assignments (optional)  
* A Gantt‑style timeline (optional)  
  
**1️⃣ Clarify the Product Vision & Success Criteria**  

| Question | Answer (example) |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| What is the primary output? | A downloadable .xlsx (or a live Google Sheet) with a fully‑filled work‑back schedule. |
| Who are the users? | Project managers, product owners, marketers, small‑business founders. |
| What level of detail is expected? | 1‑2 day tasks, optional “owner” field, automatic critical‑path highlight. |
| What are the KPIs? | • % of generated schedules that pass a manual QA check (≥ 90 %) 
• Average generation latency < 5 seconds 
• User‑satisfaction NPS ≥ 8/10. |
| Constraints? | • No proprietary data collection (privacy‑by‑design). 
• Must work on both Excel & Google‑Sheets. 
• Free tier should stay under $0.01 per request. |
  
**2️⃣ High‑Level Architecture**  
  
```
┌─────────────────────┐
│  User Interface (UI)│  ← Web app / Slack bot / Teams add‑in
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   API Gateway /     │  (REST/GraphQL, auth, rate‑limit)
│   Request Router    │
└───────┬─────────────┘
          │
          ▼
┌─────────────────────┐
│   Orchestrator      │  (LangChain / CrewAI / custom)
│   - Prompt Builder │
│   - Tool Dispatcher│
│   - State Store    │
└───────┬─────────────┘
          │
   ┌──────┴───────┐
   │              │
   ▼              ▼
┌─────────┐   ┌─────────────┐
│  LLM    │   │  Domain    │
│  (GPT‑4│   │  Services  ││
│  /Claude│   │  (estimation││
│  /Gemini)│ │   library,  ││
└─────┬───┘   │   graph    ││
      │       │   analyzer)││
      │       └─────┬──────┘│
      │             │      │
      ▼             ▼      ▼
┌─────────────┐ ┌───────────────┐
│  Prompt     │ │  Planner      │
│  Templates  │ │  (critical‑   │
│  (system)   │ │   path,       │
└─────┬───────┘ │   timeline)   │
      │       └───────┬───────┘
      │               │
      ▼               ▼
┌─────────────────────────────┐
│  Workbook Generator Service  │
│  – Excel SDK (openpyxl)      │
│  – Google‑Sheets API         │
│  – CSV fallback              │
└───────┬─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Storage / Cache    │  (Redis, S3, DB for logs, user‑history)
└─────────────────────┘
┌─────────────────────┐
│  User Interface (UI)│  ← Web app / Slack bot / Teams add‑in
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│   API Gateway /     │  (REST/GraphQL, auth, rate‑limit)
│   Request Router    │
└───────┬─────────────┘
          │
          ▼
┌─────────────────────┐
│   Orchestrator      │  (LangChain / CrewAI / custom)
│   - Prompt Builder │
│   - Tool Dispatcher│
│   - State Store    │
└───────┬─────────────┘
          │
   ┌──────┴───────┐
   │              │
   ▼              ▼
┌─────────┐   ┌─────────────┐
│  LLM    │   │  Domain    │
│  (GPT‑4│   │  Services  ││
│  /Claude│   │  (estimation││
│  /Gemini)│ │   library,  ││
└─────┬───┘   │   graph    ││
      │       │   analyzer)││
      │       └─────┬──────┘│
      │             │      │
      ▼             ▼      ▼
┌─────────────┐ ┌───────────────┐
│  Prompt     │ │  Planner      │
│  Templates  │ │  (critical‑   │
│  (system)   │ │   path,       │
└─────┬───────┘ │   timeline)   │
      │       └───────┬───────┘
      │               │
      ▼               ▼
┌─────────────────────────────┐
│  Workbook Generator Service  │
│  – Excel SDK (openpyxl)      │
│  – Google‑Sheets API         │
│  – CSV fallback              │
└───────┬─────────────────────┘
        │
        ▼
┌─────────────────────┐
│  Storage / Cache    │  (Redis, S3, DB for logs, user‑history)
└─────────────────────┘

```
Key components  

| Component | Role | Recommended Tech |
| ------------------ | ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| UI | Collect end‑goal, optional parameters (team size, working days, holidays). | React/Next.js, Slack Block Kit, Teams Adaptive Card, or a simple Flask HTML form. |
| Orchestrator | Glue everything together, maintain conversational state, decide which tool to call next. | LangChain AgentExecutor, CrewAI Crew, or a custom FastAPI orchestrator. |
| LLM | Generate textual breakdowns (milestones, tasks) and understand user intent. | GPT‑4o (OpenAI), Claude‑3.5, Gemini‑1.5‑Flash – choose based on cost/latency. |
| Domain Services | Estimate durations, identify dependencies, run critical‑path analysis. | pydantic models + numpy/networkx for graph algorithms. |
| Workbook Generator | Translate the structured plan into a spreadsheet. | openpyxl/xlsxwriter for Excel, Google Sheets API (google-api-python-client) for live sheets, pandas for CSV. |
| Storage/Cache | Persist user requests, generated files, telemetry. | Redis (short‑term), AWS S3 (files), PostgreSQL (metadata). |
  
**3️⃣ Data & Knowledge Requirements**  

| Knowledge Area | How to Acquire / Encode |
| ------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------ |
| Task taxonomy (common project phases: “Requirement gathering”, “Design”, “Development”, “Testing”, “Launch”) | Build a static knowledge base (JSON/YAML) or fine‑tune a small LLM on a curated set of project plans. |
| Typical durations for each task type (e.g., UI design ≈ 5 days, code review ≈ 1 day) | Three‑point estimates from historical data or industry benchmarks; store as a lookup table. |
| Resource capacity model (e.g., 1 person = 8 h/day, 5 day work week) | Simple rule‑engine; optionally allow user override. |
| Holiday calendars (US, EU, custom) | Pull from public iCal feeds or let user upload .ics. |
| Dependency patterns (Design → Development → QA) | Encode as a directed acyclic graph (DAG) template that can be expanded per project. |
| Critical‑path calculation | Use networkx to compute longest path on weighted DAG (weights = duration+buffer). |
| Prompt templates | System prompt that instructs the LLM to output JSON with a fixed schema (milestones → tasks). Example below. |
  
**4️⃣ Prompt Engineering – “LLM‑to‑JSON” Contract**  
System Prompt (high‑level)  
  
```
You are an expert project planner. Given a concise end‑goal description, produce a complete work‑back schedule in JSON that follows this schema:

{
  "goal": "<string>",
  "deadline": "<YYYY‑MM‑DD>",
  "milestones": [
    {
      "name": "<milestone title>",
      "due": "<YYYY‑MM‑DD>",
      "tasks": [
        {
          "id": "<unique‑id>",
          "name": "<task title>",
          "duration_days": <float>,
          "buffer_days": <float>,
          "owner": "<optional>",
          "depends_on": ["<task‑id>", ...]   // may be empty
        },
        ...
      ]
    },
    ...
  ]
}
You are an expert project planner. Given a concise end‑goal description, produce a complete work‑back schedule in JSON that follows this schema:

{
  "goal": "<string>",
  "deadline": "<YYYY‑MM‑DD>",
  "milestones": [
    {
      "name": "<milestone title>",
      "due": "<YYYY‑MM‑DD>",
      "tasks": [
        {
          "id": "<unique‑id>",
          "name": "<task title>",
          "duration_days": <float>,
          "buffer_days": <float>,
          "owner": "<optional>",
          "depends_on": ["<task‑id>", ...]   // may be empty
        },
        ...
      ]
    },
    ...
  ]
}

```
User Prompt (example)  
  
```
Goal: Launch the new e‑commerce website on 2025‑10‑30.
Team: 2 developers, 1 designer, 1 QA, 1 marketing lead.
Working days: Mon‑Fri, 8 h per day.
Holidays: US Federal holidays 2025.
Goal: Launch the new e‑commerce website on 2025‑10‑30.
Team: 2 developers, 1 designer, 1 QA, 1 marketing lead.
Working days: Mon‑Fri, 8 h per day.
Holidays: US Federal holidays 2025.

```
Few‑shot examples (embed 2–3 sample inputs/outputs in the system prompt) to teach the model the exact JSON format and to surface realistic durations & buffers.  
Post‑processing validation  
* Parse JSON with pydantic models.  
* Verify: all depends_on IDs exist, no cycles (use networkx.is_directed_acyclic_graph).  
* Compute earliest start / latest finish dates based on deadline and dependencies.  
  
**5️⃣ Core Algorithms**  
**5.1 Duration Estimation**  
python  
```
def estimate_duration(task_name: str, team_profile: dict) -> float:
    # lookup base duration from taxonomy
    base = DURATION_TABLE.get(task_name.lower(), 3.0)   # default 3 days
    # apply scaling factor for team size / skill
    factor = team_profile.get('efficiency_factor', 1.0)
    return round(base / factor, 2)
def estimate_duration(task_name: str, team_profile: dict) -> float:
    # lookup base duration from taxonomy
    base = DURATION_TABLE.get(task_name.lower(), 3.0)   # default 3 days
    # apply scaling factor for team size / skill
    factor = team_profile.get('efficiency_factor', 1.0)
    return round(base / factor, 2)

```
**5.2 Buffer Allocation**  
* Simple rule: 10 % of task duration + 0.5 day for high‑risk tasks (detected by keyword: “integration”, “migration”).  
**5.3 Critical‑Path (Longest Path)**  
python  
```
import networkx as nx

def critical_path(plan):
    G = nx.DiGraph()
    for m in plan.milestones:
        for t in m.tasks:
            G.add_node(t.id, weight=t.duration_days + t.buffer_days)
            for dep in t.depends_on:
                G.add_edge(dep, t.id)
    # longest path in weighted DAG
    length, path = nx.algorithms.dag.dag_longest_path_length(G, weight='weight'), \
                   nx.algorithms.dag.dag_longest_path(G, weight='weight')
    return length, path
import networkx as nx

def critical_path(plan):
    G = nx.DiGraph()
    for m in plan.milestones:
        for t in m.tasks:
            G.add_node(t.id, weight=t.duration_days + t.buffer_days)
            for dep in t.depends_on:
                G.add_edge(dep, t.id)
    # longest path in weighted DAG
    length, path = nx.algorithms.dag.dag_longest_path_length(G, weight='weight'), \
                   nx.algorithms.dag.dag_longest_path(G, weight='weight')
    return length, path

```
**5.4 Date Assignment (Backward Scheduling)**  
1. Start from deadline.  
2. For each milestone (reverse order) assign due = current_deadline.  
3. For each task (reverse topological order) compute finish = min(child.start_dates) - buffer.  
4. start = finish - duration.  
5. Propagate up the chain, skipping weekends & holidays (use pandas.tseries.offsets.CustomBusinessDay).  
  
**6️⃣ Workbook Generation**  
**6.1 Excel (OpenPyXL)**  

| Sheet | Columns |
| ---------------- | ---------------------------------------------------------------------------- |
| Summary | Goal, Deadline, Critical‑Path Length |
| Milestones | Milestone, Due Date |
| Tasks | ID, Name, Owner, Duration, Buffer, Start, Finish, Depends‑On, Critical (Y/N) |
| Gantt (optional) | Use conditional formatting to color cells between Start‑Finish dates. |
  
python  
```
from openpyxl import Workbook
from openpyxl.styles import PatternFill
import pandas as pd

def to_excel(plan, filename):
    wb = Workbook()
    # create sheets & fill data...
    # add Gantt using fill on date columns
    wb.save(filename)
from openpyxl import Workbook
from openpyxl.styles import PatternFill
import pandas as pd

def to_excel(plan, filename):
    wb = Workbook()
    # create sheets & fill data...
    # add Gantt using fill on date columns
    wb.save(filename)

```
**6.2 Google‑Sheets (API)**  
* Create a new spreadsheet via drive.files.create.  
* Populate tabs using sheets.spreadsheets.values.update.  
* Use Data Validation for owners, Conditional Formatting for critical tasks.  
python  
```
service = build('sheets', 'v4', credentials=creds)
spreadsheet = service.spreadsheets().create(body={
    "properties": {"title": f"Work‑back – {plan['goal']}"}
}).execute()
# batchUpdate with values & formatting
service = build('sheets', 'v4', credentials=creds)
spreadsheet = service.spreadsheets().create(body={
    "properties": {"title": f"Work‑back – {plan['goal']}"}
}).execute()
# batchUpdate with values & formatting

```
**6.3 CSV Fallback**  
* Export the Tasks table as CSV for downstream import.  
  
**7️⃣ Development Roadmap (MVP → Production)**  

| Phase | Goal | Deliverables | Time |
| ----------------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------- | ------- |
| 0 – Discovery | Finalize scope, data sources, compliance. | Requirements doc, data schema, cost model. | 1 wk |
| 1 – Prototype | Build a minimal “LLM‑to‑JSON → Excel” pipeline. | Notebook demo, sample prompts, static task taxonomy. | 2 wks |
| 2 – Orchestration | Wrap prototype in a FastAPI/LangChain agent, add validation. | API endpoint /generate, error handling, unit tests. | 2 wks |
| 3 – Google‑Sheets Integration | Add optional live‑sheet output. | OAuth flow, sheet creation, formatting. | 1 wk |
| 4 – UI & Auth | Simple React front‑end + API key auth. | Deploy on Vercel/Netlify, CI/CD pipeline. | 2 wks |
| 5 – Scaling & Monitoring | Rate limiting, Redis cache, logging, health checks. | Dockerfile, Kubernetes manifest (optional). | 1 wk |
| 6 – Beta Testing | Invite 5‑10 power‑users, collect feedback. | Bug‑fixes, UX tweaks, documentation. | 2 wks |
| 7 – Production Launch | Go‑live with monitoring & support. | SLA docs, pricing plan (if SaaS). | 1 wk |
| 8 – Continuous Improvement | Add “resource‑allocation optimizer”, “risk‑heat map”, “export to MS Project”. | Roadmap items, iterative releases. | Ongoing |
  
Total MVP timeline: ~10 weeks.  
  
**8️⃣ Testing & Quality Assurance**  

| Test Type | What to Verify | Tools |
| ----------------- | --------------------------------------------------------------------- | ----------------------------------------- |
| Unit | Duration estimator, buffer logic, DAG creation. | pytest, hypothesis |
| Integration | End‑to‑end: prompt → JSON → workbook (Excel & Sheets). | Postman, FastAPI test client |
| Schema Validation | Output conforms to pydantic model. | pydantic’s .parse_obj |
| Performance | Latency < 5 s for typical request. | Locust, k6 |
| Security | No credential leakage, proper OAuth scopes. | OWASP ZAP, Snyk |
| Usability | Users can edit generated sheet without breaking dates. | Manual exploratory testing + user surveys |
| Regression | After any code change, critical‑path length unchanged for same input. | Snapshot testing (store JSON hash). |
  
**9️⃣ Operational Concerns**  

| Area | Considerations |
| ----------------- | ------------------------------------------------------------------------------------------------ |
| Cost control | Use gpt‑4o-mini for cheap parsing, switch to gpt‑4o only for complex prompts. |
| Rate limiting | 30 req/min per API key; implement token bucket in Redis. |
| Data privacy | No user‑provided data stored beyond request‑ID; delete sheets after 30 days unless user opts‑in. |
| Observability | Structured logs (JSON) → ELK; metrics: request_latency, error_rate, generated_files. |
| Disaster recovery | Store generated files in S3 with versioning; backup Redis snapshots. |
| Compliance | If serving EU customers, host in EU region, GDPR‑compliant consent flow. |
| Scalability | Stateless FastAPI workers behind an ALB; horizontal scaling via Kubernetes HPA. |
  
**10️⃣ Sample End‑to‑End Flow (Pseudo‑code)**  
python  
```
# 1️⃣ API entry point
@app.post("/workback")
async def create_plan(request: PlanRequest):
    # a) Store request meta, generate request_id
    request_id = uuid4()
    
    # b) Build LLM prompt
    prompt = build_prompt(request.goal, request.deadline,
                          request.team, request.holidays)
    
    # c) Call LLM (async)
    raw_json = await llm_chat(prompt)
    
    # d) Validate & parse
    plan = PlanModel.parse_raw(raw_json)   # pydantic
    
    # e) Compute schedule (critical path, dates)
    schedule = compute_schedule(plan, request.holidays)
    
    # f) Generate workbook (choose format)
    if request.format == "excel":
        file_path = generate_excel(schedule, request_id)
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif request.format == "gsheets":
        sheet_url = generate_google_sheet(schedule, request.user_token)
        return {"sheet_url": sheet_url}
    else:
        csv_bytes = generate_csv(schedule)
        mime = "text/csv"
    
    # g) Return signed URL (S3 presigned) or file stream
    return FileResponse(file_path, media_type=mime,
                        filename=f"{plan.goal}_plan.xlsx")
# 1️⃣ API entry point
@app.post("/workback")
async def create_plan(request: PlanRequest):
    # a) Store request meta, generate request_id
    request_id = uuid4()
    
    # b) Build LLM prompt
    prompt = build_prompt(request.goal, request.deadline,
                          request.team, request.holidays)
    
    # c) Call LLM (async)
    raw_json = await llm_chat(prompt)
    
    # d) Validate & parse
    plan = PlanModel.parse_raw(raw_json)   # pydantic
    
    # e) Compute schedule (critical path, dates)
    schedule = compute_schedule(plan, request.holidays)
    
    # f) Generate workbook (choose format)
    if request.format == "excel":
        file_path = generate_excel(schedule, request_id)
        mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    elif request.format == "gsheets":
        sheet_url = generate_google_sheet(schedule, request.user_token)
        return {"sheet_url": sheet_url}
    else:
        csv_bytes = generate_csv(schedule)
        mime = "text/csv"
    
    # g) Return signed URL (S3 presigned) or file stream
    return FileResponse(file_path, media_type=mime,
                        filename=f"{plan.goal}_plan.xlsx")

```
  
**11️⃣ “Cheat‑Sheet” for the Engineer**  

| Task | Command / Code Snippet |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Create LLM client (OpenAI) | client = openai.AsyncClient(api_key=…) |
| Prompt with function calling | Use functions=[{"name":"schedule","parameters":{…}}] to force JSON output. |
| Validate DAG | assert nx.is_directed_acyclic_graph(G) |
| Business‑day offset | bday = pd.tseries.offsets.CustomBusinessDay(weekmask='Mon Tue Wed Thu Fri', holidays=holidays_list) |
| OpenPyXL conditional formatting | ws.conditional_formatting.add(f"E{row}:Z{row}", CellIsRule(operator='between', formula=[start, end], fill=fill)) |
| Google Sheets batch update | batch_update = {"requests": [...], "valueInputOption": "RAW"} |
| Dockerfile | FROM python:3.12-slim\\nRUN pip install fastapi[all] openai langchain google-auth\\nCOPY . /app\\nWORKDIR /app\\nCMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] |
| Kubernetes HPA | apiVersion: autoscaling/v2\\nkind: HorizontalPodAutoscaler\\nspec:\\n maxReplicas: 5\\n minReplicas: 2\\n metrics:\\n - type: Resource\\n resource:\\n name: cpu\\n target:\\n type: Utilization\\n averageUtilization: 70 |
  
**12️⃣ Future‑Proof Extensions**  

| Idea | Value |
| ------------------------------------------------------------------------------------------------- | ----- |
| Resource‑leveling optimizer – automatically reshuffle tasks to respect individual capacity. |  |
| Risk heat‑map – LLM tags high‑risk tasks; UI shows colored risk bars. |  |
| Multi‑project portfolio view – combine several generated sheets into a master dashboard. |  |
| Natural‑language updates – “Move the QA phase two weeks later” → re‑run only the affected branch. |  |
| Template marketplace – industry‑specific work‑back templates (construction, SaaS, event). |  |
| Export to MS Project / Primavera – generate .mpp or .xer files via third‑party libraries. |  |
| Chat‑bot UI – embed in Slack/Teams where users type “Launch X by Y” and receive a live sheet. |  |
  
**🎉 TL;DR – One‑Page Action List**  
1. Define schema for the JSON plan (goal, deadline, milestones, tasks).  
2. Write system & few‑shot prompts that force the LLM to output that schema.  
3. Build a validator (pydantic + networkx) to catch malformed output.  
4. Implement core algorithms – duration estimate, buffer, critical‑path, backward date calculation (skip weekends/holidays).  
5. Create workbook exporters – openpyxl for Excel, Google Sheets API for live sheets, CSV fallback.  
6. Wrap everything in an orchestrator (LangChain/crewAI/FastAPI) that:  
    * receives the user request,  
    * calls the LLM,  
    * validates & enriches the plan,  
    * generates the file,  
    * returns a download link or sheet URL.  
7. Add auth, rate‑limit, caching, logging for production readiness.  
8. Build a minimal UI (web form or Slack command) to collect the end‑goal and options.  
9. Test end‑to‑end, monitor latency, and iterate on prompt quality.  
10. Launch MVP, collect feedback, then add advanced features (resource leveling, risk analysis, multi‑project view).  
Follow the roadmap above and you’ll have a fully autonomous work‑back planner that turns a single sentence of intent into a polished, actionable project schedule—ready for download or direct collaboration in Google Sheets. Good luck, and feel free to ask for deeper dives on any of the modules!  
