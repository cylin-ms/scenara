## Appendix – Gold-Standard Multi-step Reasoning Plan for Hero Prompts  
1) Organizer-1 Prompt: “Keep my Calendar up to date by committing to only meetings that are part of my priorities.”  

| Steps | Atomic Agent Capabilities |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | ·      Natural Language Understanding: Extract user priorities and time constraints from the prompt |
| 2. Retrieve Data | ·      Calendar Events Retrieval: Retrieve all pending calendar invitations for the current week
·      Meeting Metadata Extraction: Extract detailed metadata from pending invitations (attendees, agenda, organizer) |
| 3. Classify & Analyze Meetings | ·      Meeting Type Classification: Classify each pending invitation by meeting type
·      Meeting Importance Assessment: Assess strategic importance of each meeting relative to user priorities
·      Meeting Attendees Analysis: Analyze attendee composition to identify customer vs internal participants |
| 4. Generate Recommendations | ·      Meeting Insights & Recommendations: Generate prioritization recommendations based on alignment scores |
| 5. Execute Actions (Optional) | ·      RSVP Status Update: Update RSVP status based on prioritization decisions (optional automation) |
  
2) Organizer-2 Prompt: “Track all my important meetings and flag any that require focus time to prepare for them.”  

| Steps | Atomic Agent Capabilities |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | ·      Natural Language Understanding: Extract user intent to identify "important meetings" and "prep time" requirements |
| 2. Retrieve Calendar | ·      Calendar Events Retrieval: Retrieve all upcoming meetings within planning horizon |
| 3: Identify Important Meetings | ·      Meeting Type Classification: Classify meetings by type to identify high-stakes formats
·      Meeting Importance Assessment: Identify which meetings qualify as "important" based on criteria
·      Meeting Metadata Extraction: Extract meeting details to assess prep requirements |
| 4: Assess Preparation Needs | ·      Meeting Documentation Retrieval: Retrieve related documents, agendas, previous meeting notes
·      Task Duration Estimation: Estimate how much prep time is needed for each important meeting |
| 5: Find Available Time | ·      Availability Checking: Analyze calendar gaps to find available slots before important meetings |
| 6: Schedule or Flag | ·      Time Block Scheduling: Schedule focus time blocks before flagged meetings |
  
   
3) Organizre-3: “Help me understand where I am spending my time .and identify ways I can reclaim time to focus more on my top priorities.”   

| Steps | Atomic Agent Capabilities |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Understand User Intent | ·      Natural Language Understanding: Extract user intent for time analysis and reclamation focus |
| 2. Retrieve Historical Data | ·      Calendar Events Retrieval: Load historical calendar events for time analysis period |
| 3. Classify & Enrich Historical Meetings | ·      Meeting Type Classification: Classify past meetings by type for categorization
·      Meeting Importance Assessment: Assess which past meetings aligned with top priorities
·      Meeting Metadata Extraction: Extract meeting details for analysis |
| 4. Pattern Detection | ·      Recurring Patterns Detection: Identify recurring meeting patterns and time commitments |
| 5. Aggregate & Analyze | ·      Meeting Summarization: Aggregate time spent per category, participant, project |
| 6. Visualize Patterns | ·      Data Visualization: Create visual representations of time distribution |
| 7. Generate Reclamation Recommendations | ·      Meeting Insights & Recommendations: Identify low-value meetings and reclamation opportunities |
| 8. Validate Feasibility | ·      Scheduling Constraint Analysis: Validate reclamation recommendations against constraints |
  
   
4)  Schedule-1: “Starting next week, I want a weekly 30-min 1:1 with {name}. Afternoons preferred, avoid Fridays. Automatically reschedule on declines or conflicts.”   

| Steps | Atomic Agent Capabilities |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1. Parse Multi-Meeting Request | ·      Natural Language Understanding: Extract scheduling requirements (3 meetings, participants, durations, timeframe) |
| 2. Gather Calendar Data | ·      Calendar Events Retrieval: Retrieve user's calendar for the current week
·      Meeting Type Classification: Classify meeting types to understand requirements |
| 3. Identify Participants | ·      Meeting Attendees Analysis: Identify required participants for each meeting |
| 4. Check Availability for ALL Meetings | ·      Availability Checking: Check availability for all participants across all 3 meetings |
| 5. Analyze Constraints | ·      Scheduling Constraint Analysis: Analyze constraints (durations, this week, participant availability) |
| 6. Find Feasible Solutions | ·      Constraint Satisfaction: Find time slots that satisfy all constraints for all 3 meetings |
| 7. Handle Conflicts | ·      Conflict Resolution: Handle scheduling conflicts if no perfect solution exists |
| 8. Prepare Meeting Details | ·      Meeting Metadata Extraction: Prepare meeting metadata for calendar creation |
| 9. Create Calendar Events | ·      Time Block Scheduling: Create calendar events for the 3 meetings |
  
   
5) Schedule-2: “Clear my Thursday afternoon. Update my RSVPs and help me reschedule my meetings to another time and show me as {status}.”  

| Steps | Atomic Agent Capabilities |
| --------------------------------- | -------------------------------------------------------------------------------------------------------- |
| 1. Understand Buffer Requirements | ·      Natural Language Understanding: Extract buffer time requirements and target meetings |
| 2. Retrieve Tomorrow's Calendar | ·      Calendar Events Retrieval: Retrieve tomorrow's calendar events |
| 3. Extract Meeting Time Blocks | ·      Meeting Metadata Extraction: Extract meeting start/end times to identify back-to-back patterns |
| 4. Detect Back-to-Back Patterns | ·      Recurring Patterns Detection: Identify back-to-back meeting sequences (meetings with <5 min gap) |
| 5. Check Buffer Slot Availability | ·      Availability Checking: Check if 30-min buffer slots are available after each back-to-back meeting |
| 6. Resolve Conflicts | ·      Conflict Resolution: Handle conflicts if buffer time overlaps with existing meetings |
| 7. Insert Buffer Blocks | ·      Time Block Scheduling: Insert buffer time blocks into calendar |
| 8. Report Results | ·      Meeting Insights & Recommendations: Report buffer insertion results and any unresolved conflicts |
  
   
6) Schedule-3: “Land a time to meet about Project Alpha with Chris, Sangya, and Kat for 1 hour in the next 2 weeks. Schedule over 1:1s and lunches if needed and work around Kat’s schedule. Make the meeting in person and add a room.”  

| Steps | Atomic Agent Capabilities |
| ----- | ------------------------- |
| 1.    | ·                         |
| 2.    | ·                         |
|       | ·                         |
|       | ·                         |
|       | ·                         |
|       | ·                         |
  
   
7) Collaborate-1: “Help me set the agenda to review the progress of Project Alpha with the product and marketing team to get confirmation we are on track and discuss any blocking issues or risks.”  

| Steps | Atomic Agent Capabilities |
| ----- | ------------------------- |
| 1.    | ·                         |
| 2.    | ·                         |
|       | ·                         |
|       | ·                         |
|       | ·                         |
|       | ·                         |
  
   
8) Collaborate-2: “Review the materials for my meeting with senior leadership and suggest the best way to summarize the topics into three main discussion points. Generate any objections or concerns that might come up and give me effective responses.”  

| Steps | Atomic Agent Capabilities |
| ----- | ------------------------- |
| 1.    | ·                         |
| 2.    | ·                         |
|       | ·                         |
|       | ·                         |
|       | ·                         |
|       | ·                         |
  
   
9) Collaborate-3: “Prepare a brief for my upcoming meeting with customer Beta and include a dossier for each customer attendee and the topics they are most interested in. Include a background on their company.”  

| Steps | Atomic Agent Capabilities |
| ----- | ------------------------- |
| 1.    | ·                         |
| 2.    | ·                         |
|       | ·                         |
|       | ·                         |
|       | ·                         |
|       | ·                         |
  
   
