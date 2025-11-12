**TimeBerry: Calendar Agent and Post-training Plan**  
** **  
1. Executive Summary  
TimeBerry aims to transform the Calendar Copilot into a proactive, reasoning-grounded agent that can plan, prioritize, and coordinate real-world schedules with minimal manual intervention. Current frontier models like GPT-5 can reason conceptually about time but cannot yet manage live calendar scenarios consistently, as they lack structured grounding and domain-specific training. Our benchmarking across nine hero prompts shows strong precision (87%) and consistency (95%) but moderate recall (75%) and high variance, highlighting the need for targeted post-training. Preliminary post-training experiments on meeting-type and meeting-priority classification demonstrate that lightweight, domain-grounded fine-tuning can raise accuracy from 69% to 95%, improved recall by 20 points, and reduced token usage by 87%, validating both feasibility and ROI. Over a 12-month roadmap, TimeBerry will scale these methods across reasoning-heavy capabilities, such as meeting classification, constraint satisfaction, and scheduling optimization, culminating in an integrated, production-ready Calendar Copilot model with two- to threefold gains in reasoning robustness and efficiency.  
2. Frontier Model Multi-Step Reasoning Performance  
*2.1 Evaluation Summary*  
Frontier models can reason about time conceptually, including drafting schedules, explaining prioritization strategies, or describing how to plan a meeting. However, they cannot reliably manage or coordinate real calendars without external grounding or fine-tuning, because they were not trained on structured calendar or scheduling data, and most frontier AI labs do not operate calendar systems that provide real scheduling behavior.  
Accordingly, our objective is to build and evaluate an agentic calendar model capable of reasoning, planning, and coordinating time-sensitive actions by grounding LLM reasoning in real calendar context and user intent. The model aims to prioritize what matters, simplify scheduling, and ensure every meeting achieves its purpose.  
To evaluate this, we selected 9 hero prompts that represent these user promises. These prompts span the core pillars of Organize**, **Schedule, and** **Collaborate, capturing the full spectrum of reasoning, constraint satisfaction, and contextual understanding required for an autonomous Calendar agent.  
We first constructed gold-standard multi-step reasoning traces for the 9 prompts using the GUTT (Generative Unit Task Taxonomy) framework, referring to ++Appendix – Gold-Standard Multi-step Reasoning Plan for Hero Prompts++. These traces were derived from the voting consensus between frontier models (Claude Sonnet 4.5 and GPT-5) and subsequently validated through domain expert reviews inside the T+P team.   
We then evaluated GPT-5’s performance after targeted prompt tuning to quantify capability gaps relative to this gold standard. We conducted 3-Trial Stability Test for GPT-5 on the 9 hero prompts with extensive prompt tunings. Comparing to the gold standard, we observed the below performance statistics:  

| Average Performance (F1 Score) | 91.98% ± 16.38% (High average, high variance)[JZ1] |
| ------------------------------ | -------------------------------------------------- |
| Precision | 90.86% ± 19.27% (High precision, high variance) |
| Recall | 95.83% ± 17.02% (Excellent recall, high variance) |
| Consistency | 95.33% (High task agreement) |
  
These results show that GPT-5 demonstrates strong reasoning capability on calendar-related tasks when guided by optimized prompts. Its average F1 score 91.98%, precision 90.86%, recall 95.83%, and consistency 95.33% indicate strong step-level performance. The relatively high variance likely reflects the small sample of nine hero prompts rather than inherent instability. However, these metrics are computed at the reasoning step level. In the end-to-end workflow a single incorrect step renders the overall output incorrect. From this perspective we observed errors in the reasoning paths of two prompts, yielding an end-to-end **prompt-level accuracy of 77.8%**. This highlights the need for post-training to internalize structured, multi-step reasoning patterns and improve full-workflow reliability.  
*2.2 Error Analysis*  
While GPT-5 demonstrates strong reasoning performance at the step level, a closer inspection of the two prompts with reasoning path errors reveals important capability gaps that impact end-to-end reliability.  
For the Collaborate-1 Prompt *“Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks,” *GPT-5 failed to perform “Attendee/Contact Resolution”, leaving “product team” and “marketing team” unresolved as specific individuals. Without identifying actual participants, the generated agenda lacks awareness of who will attend, undermining the meeting’s contextual grounding. Additionally, GPT-5 incorrectly inserted a reasoning step for “Risk Anticipation,” interpreting the instruction as a request to analyze risks rather than to structure the agenda to include a section for risk discussion. This reflects a misunderstanding of task intent and role boundaries in multi-step reasoning.  
For the Schedule-2 Prompt* “Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status},”* GPT-5 omitted the critical step of “Availability Checking,” which involves identifying alternative time slots before rescheduling meetings. This omission breaks the logical chain of actions needed to execute the user’s request correctly.  
It is important to note that GPT-5 was provided with the complete list of reasoning capabilities as part of the prompt context, yet it still failed to apply certain key steps. These two cases highlight a consistent pattern: GPT-5 can follow structured reasoning but does not yet fully internalize the complete reasoning graph needed for complex, real-world scheduling workflows. This analysis underscores the necessity of targeted post-training to help GPT-5 better recognize, select, and sequence reasoning capabilities reliably, enabling robust and autonomous behavior for the Calendar Agent.  
3. Agent Capabilities We Need to Build  
*3.1 Capability Importance Across Hero Prompts*  
The gold-standard multi-step reasoning plan outlines 25++[CL2]++  canonical agent capabilities required for the Calendar Agent to operate as a proactive, context-aware assistant. The table below summarizes the relative importance of these capabilities across the 9 hero prompts, grouped into tiers based on the percentage of prompts that depend on them.** **  

| Tier | Agent Capabilities |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tier 1: Universal Capabilities (Used in >50% of prompts) | ·      Calendar Events Retrieval (100%)
·      Natural Language Understanding (100%)
·      Meeting Metadata Extraction (78%)
·      Meeting Importance Assessment (67%)
·      Attendee/Contact Resolution (67%)
·      Meeting Type Classification (56%)
·      Document Generation/Formatting (56%)
·      Priority/Preference Matching (56%) |
| Tier 2: Common Capabilities (Used in 25–50% of prompts) | ·      Availability Checking (44%)
·      Document/Content Retrieval (44%)
·      Constraint Satisfaction (44%)
·      RSVP Status Update (33%)
·      Recommendation Engine (33%) |
| Tier 3: Specialized Capabilities (Used in <25% of prompts) | ·      Time Aggregation/Statistical Analysis (22%)
·      Recurrence Rule Generation (22%)
·      Event Monitoring/Change Detection (22%)
·      Automatic Rescheduling (11%)
·      Objection/Risk Anticipation (11%)
·      Resource Booking (Rooms/Equipment) (11%)
·      Data Visualization/Reporting (11%)
·      Focus Time/Preparation Time Analysis (11%)
·      Research/Intelligence Gathering (11%)
·      Agenda Generation/Structuring (11%)
·      Multi-party Coordination/Negotiation (11%)
·      Event Annotation/Flagging (11%) |
  
* *  
*3.2 Build Strategy Categories*  
These 25 canonical agent capabilities require different build strategies, which fall into three categories:  
1.     Missing tools: capabilities that depend on APIs or actions not yet implemented.  
2.     Missing grounding data: capabilities limited by lack of access to structured calendar, organizational, or user context.  
3.     Reasoning-dependent capabilities: capabilities that require advanced reasoning and well-defined evaluation rubrics.  
Among these, we identified the following capabilities that specifically require the reasoning enhancement:  
·      Natural Language Understanding  
·      Meeting Type Classification  
·      Meeting Importance Assessment  
·      Document Generation/Formatting  
·      Priority/Preference Matching  
·      Recommendation Engine  
·      Recurrence Rule Generation  
·      Automatic Rescheduling  
·      Objection/Risk Anticipation  
·      Focus Time/Preparation Time Analysis   
·      Research/Intelligence Gathering  
·      Agenda Generation/Structuring  
·      Multi-party Coordination/Negotiation  
*3.3 Preliminary Experiments*  
Our analysis shows that multi-step planning and several agent capabilities depend heavily on structured reasoning. As an initial exploration, we selected “Meeting Classification” as an example to conduct or plan preliminary post-training experiments.  
The experiments aim to estimate:  
·      Required resources, capacities and time investment  
·      Volume and structure of training data  
·      Evaluation framework design  
·      Expected performance improvements after post-training  
These preliminary results or plans will help estimate the overall investment, complexity, and return expected from scaling post-training to other reasoning-heavy agent capabilities.  

| Task | GPU | Resource | Data | Base Model | Performance |
| ------------------------------------------------ | -------------------------------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------ | ------------------------------------------------------------------ |
| Meeting Type Classification (done) | 538000 training tokens and 3 epochs in AI Foundry (cost < $10) | 1.5 dev for 7d | 1000 synthetic calendar events (seeded from real events) are labeled automatically using implicit rules and heuristics derived from the Time Insights categorization framework; 552 real calendar events for evaluation | GPT-4.1-Mini | Accuracy 95.1% (vs. 69.6% prompt baseline)
87% reduction in tokens |
| Meeting Priority Classification (under planning) | 40 A100 | 2 dev planned for 14w | We plan to collect 10K training labels derived from direct user feedback, RSVP status, and Teams attendance data; 1K test labels | GPT-4o-Mini | Baseline: Precision 97% and Recall 78% |
  
These preliminary experiments and plans validate the feasibility and strong ROI of post-training for calendar reasoning tasks. The completed Meeting Type Classification experiment showed that even with minimal data and compute, targeted fine-tuning raised accuracy from 69.6% to 95.1% and reduced token usage by 87%, demonstrating significant efficiency and performance gains over prompt-only approaches. In parallel, a Meeting Priority Classification post-training effort is being planned, with a goal of leveraging 10K labeled examples derived from user feedback, RSVP status, and Teams attendance data to improve baseline performance (currently Precision 97%, Recall 78%). Together, these findings and plans illustrate that structured, domain-grounded post-training can meaningfully enhance GPT-based calendar reasoning and provide a scalable pathway for extending these gains to other reasoning-heavy capabilities—such as scheduling optimization and conflict resolution—advancing the agent’s autonomy and overall product value.  
4. Execution Roadmap  
The execution plan for **TimeBerry** follows a phased approach designed to build capability depth systematically while maintaining rapid iteration and clear evaluation checkpoints. Each phase expands the model’s reasoning competence, data grounding, and integration maturity toward a fully autonomous Calendar Agent.  
**Phase 1: Foundation Setup (Month 0–1)**  
The initial phase focuses on building the foundational infrastructure required for reasoning-based post-training. The team will finalize the structured capability taxonomy (based on the GUTT framework), define the unified data schema for synthetic and real calendar data, and implement automated labeling heuristics derived from the calendar domain knowledge. During this phase, we will also stand up an evaluation pipeline to measure precision, recall, and consistency against the 9 hero prompts. This establishes the baseline for tracking progress through subsequent phases.  
**Phase 2: Pilot Post-Training (Month 2–3)**  
With the foundation in place, the second phase scales the preliminary “Meeting Classification” and “Meeting Priority” experiments into full post-training pilots. The goal is to validate model gains, optimize token consumption, and quantify cost versus accuracy improvements compared to base model performance. The deliverables include fine-tuned checkpoints exceeding 90% task accuracy, a post-training cost analysis, and a refined evaluation rubric that supports reproducible comparisons across future capabilities.  
**Phase 3: Multi-Capability Expansion (Month 4–6)**  
The third phase extends post-training to additional reasoning-heavy capabilities, including Availability Checking, Constraint Satisfaction, Recurrence Rule Generation, and the Recommendation Engine. Synthetic datasets will be generated using GUTT templates to ensure diversity and coverage of multi-step reasoning chains. This phase also introduces partial grounding through limited API actions, such as calendar retrieval and RSVP updates. The outcome will be a suite of post-trained models covering multiple reasoning skills, evaluated through an expanded capability-level benchmark suite.  
**Phase 4: Agent Integration and Closed-Loop Evaluation (Month 7–9)**  
In the fourth phase, the individually fine-tuned reasoning modules will be integrated into a single TimeBerry agent capable of multi-capability reasoning and context persistence. The integration will enable cross-task coordination and grounding in real user calendars through controlled internal testing. Closed-loop evaluations will be conducted with opt-in participants to assess real-world behavior, such as scheduling accuracy, prioritization quality, and user satisfaction. The result will be a functional **TimeBerry Alpha** agent demonstrating coherent reasoning across Organize, Schedule, and Collaborate tasks.  
**Phase 5: Optimization and Deployment Preparation (Month 10–12)**  
The final phase focuses on production readiness. Key priorities include optimizing inference efficiency, reducing latency, implementing safety and alignment checks for autonomous scheduling, and preparing integration with the Copilot platform. A comprehensive post-training dataset report and Responsible AI review will be completed prior to launch. The end state is a production-quality TimeBerry model ready for Calendar Copilot deployment, capable of reasoning natively about time, place, åprioritization, and coordination without extensive prompt scaffolding.  
**Milestone Summary**  
By Month 3, the team will have validated the first post-trained models with ≥90% accuracy on classification tasks. By Month 6, reasoning coverage will extend to at least four additional capabilities. By Month 9, the integrated TimeBerry Alpha agent will achieve an average F1 score of at least 85% against the gold-standard reasoning benchmark. By Month 12, a fully optimized, deployment-ready model will be available for integration into Calendar Copilot.  
**Resourcing and Expected Outcomes**  
The full roadmap requires approximately 10-20 dedicated FTEs and 300–500 H100-equivalent GPUs. The expected outcome is a two- to threefold improvement in reasoning robustness and a 70% reduction in token usage relative to the prompt-only baseline. Together, these improvements will enable TimeBerry to deliver grounded, reliable, and efficient calendar reasoning, transforming the Calendar Copilot from a reactive assistant into a proactive, goal-oriented agent.  
Appendix – Gold-Standard Multi-step Reasoning Plan for Hero Prompts  
**1) Organizer-1: "Keep my Calendar up to date by committing to only meetings that are part of my priorities."**++[CL3]++ ++[CL4]++   

| Steps | Atomic Agent Capabilities |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | • Natural Language Understanding: Extract user priorities and time constraints from the prompt |
| 2. Retrieve Pending Invitations | • Calendar Events Retrieval: Retrieve all pending calendar invitations for the current week |
| 3. Extract Meeting Metadata | • Meeting Metadata Extraction: Extract detailed metadata from pending invitations (attendees, agenda, organizer) |
| 4. Classify & Analyze Meetings | • Meeting Type Classification: Classify each pending invitation by meeting type• Meeting Importance Assessment: Assess strategic importance of each meeting relative to user priorities |
| 5. Match Against Priorities | • Priority/Preference Matching: Compare meetings against user's stated priorities and calculate alignment scores |
| 6. Execute RSVP Actions | • RSVP Status Update: Update RSVP status based on prioritization decisions (accept/decline/tentative) |
  
**2) Organizer-2: "Track all my important meetings and flag any that require focus time to prepare for them."**  

| Steps | Atomic Agent Capabilities |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | • Natural Language Understanding: Extract user intent to identify "important meetings" and "prep time" requirements |
| 2. Retrieve Calendar | • Calendar Events Retrieval: Retrieve all upcoming meetings within planning horizon |
| 3. Identify Important Meetings | • Meeting Type Classification: Classify meetings by type to identify high-stakes formats• Meeting Importance Assessment: Identify which meetings qualify as "important" based on criteria• Meeting Metadata Extraction: Extract meeting details to assess prep requirements |
| 4. Assess Preparation Needs | • Document/Content Retrieval: Retrieve related documents, agendas, previous meeting notes• Focus Time/Preparation Time Analysis: Estimate how much prep time is needed for each important meeting |
| 5. Filter Important Meetings | • Priority/Preference Matching: Filter to "important meetings" based on user criteria |
| 6. Setup Meeting Tracking | • Event Monitoring/Change Detection: Setup tracking/monitoring for important meetings |
| 7. Flag Prep-Required Meetings | • Event Annotation/Flagging: Flag meetings that require focus time with visual indicators |
  
**3) Organizre-3: "Help me understand where I am spending my time and identify ways I can reclaim time to focus more on my top priorities."**  

| Steps | Atomic Agent Capabilities |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | • Natural Language Understanding: Extract user intent for time analysis and reclamation focus |
| 2. Retrieve Historical Data | • Calendar Events Retrieval: Load historical calendar events for time analysis period |
| 3. Classify & Enrich Historical Meetings | • Meeting Type Classification: Classify past meetings by type for categorization• Meeting Importance Assessment: Assess which past meetings aligned with top priorities• Meeting Metadata Extraction: Extract meeting details for analysis |
| 4. Aggregate & Analyze | • Time Aggregation/Statistical Analysis: Aggregate time spent per category, participant, project |
| 5. Match Against Priorities | • Priority/Preference Matching: Analyze alignment with user's top priorities and identify gaps |
| 6. Generate Reclamation Recommendations | • Recommendation Engine: Identify low-value meetings and reclamation opportunities |
| 7. Visualize Patterns | • Data Visualization/Reporting: Create visual representations of time distribution |
  
**4) Schedule-1: "Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts."**  

| Steps | Atomic Agent Capabilities |
| -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| 1. Parse Scheduling Requirements | • Natural Language Understanding: Extract scheduling requirements (recurring, participants, durations, timeframe, preferences) |
| 2. Resolve Participant Identity | • Attendee/Contact Resolution: Resolve {name} to full contact profile with calendar access |
| 3. Check Availability | • Availability Checking: Check user's and {name}'s availability for afternoons, excluding Fridays |
| 4. Analyze Constraints | • Constraint Satisfaction: Find time slots that satisfy all constraints (30 min, weekly, afternoon, not Friday) |
| 5. Generate Recurrence Pattern | • Recurrence Rule Generation: Create iCalendar RRULE for weekly recurrence pattern |
| 6. Create Recurring Meeting | • Calendar Event Creation: Create recurring calendar event with all specified details |
| 7. Setup Change Monitoring | • Event Monitoring/Change Detection: Setup monitoring for declines and conflicts |
| 8. Configure Auto-Reschedule | • Automatic Rescheduling: Configure orchestrated workflow to automatically reschedule on declines/conflicts |
  
**5) Schedule-2: "Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}."**  

| Steps | Atomic Agent Capabilities |
| --------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| 1. Understand Rescheduling Requirements | • Natural Language Understanding: Extract multi-action request (clear time block, update RSVPs, reschedule, set status) |
| 2. Retrieve Thursday Meetings | • Calendar Events Retrieval: Retrieve all meetings in Thursday afternoon time block |
| 3. Extract Meeting Metadata | • Meeting Metadata Extraction: Extract meeting details (attendees, organizer, duration, RSVP status) |
| 4. Resolve All Attendees | • Attendee/Contact Resolution: Resolve attendees for coordination and availability checking |
| 5. Update RSVPs | • RSVP Status Update: Update RSVP status to decline or tentative for Thursday meetings |
| 6. Find Alternative Time Slots | • Availability Checking: Check availability across all attendees to find alternative meeting times |
| 7. Select Optimal Alternatives | • Constraint Satisfaction: Apply preferences to select best alternative time slots |
| 8. Generate Rescheduling Plan | • Agenda Generation/Structuring: Create rescheduling proposal showing old time → new time |
| 9. Update Calendar | • Calendar Event Update: Execute rescheduling and set calendar status to {status} for Thursday afternoon |
  
**6) Schedule-3: "Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat's schedule. Make the meeting in person and add a room."**  

| Steps | Atomic Agent Capabilities |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Parse Complex Requirements | • Natural Language Understanding: Extract multi-constraint scheduling request (participants, duration, timeframe, conflict resolution, location, resources) |
| 2. Resolve Participant Identities | • Attendee/Contact Resolution: Resolve all participant names to full contact profiles with calendar access |
| 3. Check Multi-Party Availability | • Availability Checking: Check availability for all 4 participants within next 2 weeks |
| 4. Identify Conflict Types | • Meeting Type Classification: Classify existing meetings to identify reschedulable types (1:1s, lunches) |
| 5. Solve Complex Constraints | • Constraint Satisfaction: Find time slots satisfying all constraints (Kat's schedule, 1 hour, 2 weeks, in-person) |
| 6. Handle Scheduling Conflicts | • Conflict Resolution: Resolve conflicts by identifying which 1:1s/lunches can be rescheduled |
| 7. Find Meeting Room | • Resource Booking: Book conference room for in-person meeting with required capacity |
| 8. Generate Meeting Proposal | • Recommendation Engine: Propose optimal solution with alternatives if primary option unavailable |
| 9. Create Calendar Event | • Calendar Event Creation: Create meeting with all details (attendees, time, location, room) |
| 10. Coordinate Multi-Party | • Multi-party Coordination/Negotiation: Handle scheduling negotiations if no perfect slot exists |
  
**7) Collaborate-1: "Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks."**  

| Steps | Atomic Agent Capabilities |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand Agenda Requirements | • Natural Language Understanding: Extract agenda structure requirements and discussion topics |
| 2. Find Project Alpha Meetings | • Calendar Events Retrieval: Find existing/upcoming Project Alpha meetings with product and marketing teams |
| 3. Retrieve Meeting Materials | • Document/Content Retrieval: Retrieve related documents (previous notes, action items, project plans, blockers) |
| 4. Gather Background Intelligence | • Research/Intelligence Gathering: Gather project context, current status, milestones, known blockers |
| 5. Identify Priority Topics | • Priority/Preference Matching: Identify most important agenda topics based on user's stated goals |
| 6. Structure Agenda | • Agenda Generation/Structuring: Create structured meeting agenda with sections for progress, confirmation, blocking issues |
| 7. Generate Formatted Agenda | • Document Generation/Formatting: Generate formatted agenda document for distribution |
  
**8) Collaborate-2: "Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses."**  

| Steps | Atomic Agent Capabilities |
| -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand Preparation Requirements | • Natural Language Understanding: Extract multi-part preparation request (review, summarize, anticipate objections, prepare responses) |
| 2. Identify Senior Leadership | • Attendee/Contact Resolution: Identify who qualifies as "senior leadership" to find the correct meeting |
| 3. Find Senior Leadership Meeting | • Calendar Events Retrieval: Find the specific meeting with senior leadership |
| 4. Extract Meeting Metadata | • Meeting Metadata Extraction: Extract meeting context (attendees, agenda, organizer, purpose) |
| 5. Retrieve All Materials | • Document/Content Retrieval: Retrieve all meeting materials (attachments, presentations, reports, previous notes) |
| 6. Gather Intelligence | • Research/Intelligence Gathering: Gather background on attendees, topics, company priorities, strategic initiatives |
| 7. Synthesize to Three Points | • Document Generation/Formatting: Summarize materials into 3 main discussion points with executive-level clarity |
| 8. Anticipate Objections | • Objection/Risk Anticipation: Predict potential concerns or pushback from senior leadership |
| 9. Generate Effective Responses | • Document Generation/Formatting: Create response strategies with data/evidence for each anticipated objection |
| 10. Assess Meeting Importance | • Meeting Importance Assessment: Confirm high-stakes nature and identify critical success factors |
  
**9) Collaborate-3: "Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company."**  

| Steps | Atomic Agent Capabilities |
| -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand Brief Requirements | • Natural Language Understanding: Extract preparation requirements (brief, individual dossiers, topic interests, company background) |
| 2. Find Customer Beta Meeting | • Calendar Events Retrieval: Find the specific meeting with customer Beta |
| 3. Extract Meeting Details | • Meeting Metadata Extraction: Extract meeting context (attendees, agenda, organizer, purpose, location) |
| 4. Resolve Customer Attendees | • Attendee/Contact Resolution: Resolve customer attendee identities to full profiles |
| 5. Retrieve Meeting Materials | • Document/Content Retrieval: Retrieve all related content (previous notes, emails, presentations, contracts) |
| 6. Research Customer Company | • Research/Intelligence Gathering: Gather comprehensive background (company info, attendee profiles, topics of interest, relationship history) |
| 7. Create Individual Dossiers | • Document Generation/Formatting: Generate attendee dossiers with profiles, topics of interest, decision authority |
| 8. Generate Company Background | • Document Generation/Formatting: Create company background section (overview, industry, news, relationship history) |
| 9. Compile Meeting Brief | • Document Generation/Formatting: Assemble comprehensive brief (overview, company background, dossiers, talking points) |
  
   
  
 ++[JZ1][@Qi He](mailto:qhe@microsoft.com)++ ++[@Chin-Yew Lin](mailto:cyl@microsoft.com)++ updated the table based on the new report  
 ++[CL2][@Joy](mailto:jingyingzeng@microsoft.com)++, changed to 25 to reflect the latest update.  
 ++[CL3][@Qi](mailto:qhe@microsoft.com)++ I added the new hero prompts analysis.  
 ++[CL4][@Joy](mailto:jingyingzeng@microsoft.com)++, FYI, I have added the new hero prompt analysis.  
