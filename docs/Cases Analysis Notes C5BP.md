Here is the Markdown conversion of “[GPEval][CasesAnalysis]C5BP-HaidongZhang.docx”:

---

# Calendar.AI  
Golden Prompts Evaluation

# Cases Analysis Notes: C5BP

**By:** Haidong Zhang

| **ID**   | C5BP |
|----------|------|
| **Scenario** | Meeting with Purpose: People |
| **Prompt**   | Who is attending this /meeting and what are their roles |

## Cases

| **Case #** | **Prompt** | **Model** | **Run on** |
|------------|------------|-----------|------------|
| 1 | who is attending upcoming Bi-weekly DKI LT Meeting and what are their roles | GPT-5 | Sept 27, 2025 |
| 2 | who is attending "Meeting Prep STCA Sync" meeting next Tue and what are their roles | GPT-5 | Sept 27, 2025 |
| 3 | who is attending next "Meeting Prep STCA Sync" meeting and what are their roles | GPT-5 | Sept 27, 2025 |

---

## Summary

## Details

### **Case 1:** _who is attending upcoming Bi-weekly DKI LT Meeting and what are their roles_

DevUI Link: [Copilot DevUI](https://devui.sdf-devui.substrate-turing-enterprisedevui.eastus-sdf.cosmic-ppe.office.net/?sharedSessionId=0f4dcb0b-442e-426c-b923-11648d0b83be&entryPoint=shareCommand) (round #1)

#### Identify meeting
- **Is it triggered**: Yes
- **How about the quality**: The meeting was identified correctly.

#### Identify attendees
- **Is it triggered**: Yes
- **How about the quality**:  
  Observations:
  - Jian-Guang Lou should be listed here: although Jian-Guang Lou was initially added when this meeting series was created, they left Microsoft a month ago.

  ![][image_pT2NFNerpBNAbkjRYjy5fg==]

#### Describe attendee roles
- **Is it triggered**: Yes
- **How about the quality**:  
  Observations:
  - The description of roles mixed job title such as Principal Architect, and very general/vague role such as “technical leadership role”.
  - For the roles in the meeting: only mentioned Dongmei as the organizer, but for other attendees, their roles for the meeting is not clear.

---

### **Case 2:** _who is attending "Meeting Prep STCA Sync" meeting next Tue and what are their roles_

DevUI Link: [Copilot DevUI](https://devui.sdf-devui.substrate-turing-enterprisedevui.eastus-sdf.cosmic-ppe.office.net/?sharedSessionId=0f4dcb0b-442e-426c-b923-11648d0b83be&entryPoint=shareCommand) (round #2)

#### Identify meeting
- **Is it triggered**: Yes
- **How about the quality**:  
  - The meeting was not identified correctly.
  - Looking into further – I asked this query on 9/27, LU resolved "next Tue" as 10/7, but I expected 9/30.

#### Identify attendees
- **Is it triggered**: Yes
- **How about the quality**:  
  - All attendees are listed.

  ![][image_XOEgGxD05P2hCzbzZItg/g==]

#### Describe attendee roles
- **Is it triggered**: Yes
- **How about the quality**:  
  Observations:
  - Organizer and Attendees were separately listed, which is good.
  - The role descriptions are too general. Some are incorrect, e.g., Caroline, Drew, Balaji.
  - For the attendees, there are no descriptions of their roles specific to this meeting.

---

### **Case 3:** _who is attending next "Meeting Prep STCA Sync" meeting and what are their roles_

DevUI Link: [Copilot DevUI](https://devui.sdf-devui.substrate-turing-enterprisedevui.eastus-sdf.cosmic-ppe.office.net/?sharedSessionId=3007b514-1425-424e-a643-c554b25edf39&entryPoint=shareCommand)

#### Identify meeting
- **Is it triggered**: Yes
- **How about the quality**: The meeting was identified correctly.

#### Identify attendees
- **Is it triggered**: Yes
- **How about the quality**: (No further details provided.)

#### Describe attendee roles
- **Is it triggered**: Yes
- **How about the quality**:  
  - It told me "The calendar entry does not include explicit job titles or roles for these attendees. Would you like me to look up their roles within the organization and provide that information?"

---

## Discussions

- For "roles" in the prompt, users may expect their job roles, or maybe their roles in the meeting. In current answers, seems it is more about the job roles, but not consistent (e.g., for "Mark" in case 2, it provides their role in the meeting as organizer but not listed their job role).
- List all attendees vs. those who accepted the meeting?
- I am also curious if I asked about an "All-Hands meeting", what the answers will be.

---

## Rubric

### Generating the rubric:

By asking Copilot questions like “who is attending this meeting and what are their roles”, the user’s goal is to identify who will be in the meeting and their roles/affiliations, including any background context on those people that’s useful (e.g., new client, your boss, key decision-maker), and the expectations for Copilot response: Lists all attendees by name and title/role (especially those the user might not know). If many, focus on key ones (like presenters, decision-makers). Please come up with a rubric for evaluating how good Copilot fulfill such task.

### Generated Rubric:

**Meeting Attendee Analysis Evaluation Rubric**  
Framework: PRIME (0-3 Scale)

<u>P - Participant Identification & Prioritization</u>  
Measures: Complete attendee listing with appropriate focus on key individuals  
Scoring:
- 3 (Excellent): All attendees listed with names and titles; clearly prioritizes key participants (decision-makers, presenters, stakeholders); appropriately handles large attendee lists by focusing on most important individuals
- 2 (Good): Most attendees identified with titles; good prioritization of important participants; minor gaps in less critical attendees
- 1 (Fair): Basic attendee list with some titles; limited prioritization; some important participants may lack sufficient detail
- 0 (Poor): Incomplete attendee list or missing titles; no clear prioritization of key vs. peripheral participants

<u>R - Role & Title Accuracy</u>  
Measures: Precision and completeness of role/title information, especially for unfamiliar attendees  
Scoring:
- 3 (Excellent): Accurate, specific job titles and organizational roles provided for all key attendees; particularly thorough for participants user might not know well
- 2 (Good): Most roles/titles accurate and specific; minor gaps or slight imprecision in some descriptions
- 1 (Fair): Basic role information provided but lacks specificity or has some inaccuracies; generic descriptions (e.g., "senior leader")
- 0 (Poor): Missing or inaccurate role information; vague or unhelpful descriptions that don't aid user understanding

<u>I - Important Stakeholder Intelligence</u>  
Measures: Clear identification and contextualization of decision-makers and key stakeholders  
Scoring:
- 3 (Excellent): Decision-makers and key stakeholders clearly identified with context about their authority, influence, and relevance to meeting topics (e.g., "Sarah Chen, VP Engineering - has final budget approval authority")
- 2 (Good): Most important stakeholders identified with some authority/influence context; generally clear about who holds decision-making power
- 1 (Fair): Basic identification of senior roles but limited context about their specific authority or importance in meeting context
- 0 (Poor): Fails to identify or inadequately explains the importance of key decision-makers and stakeholders

<u>M - Meaningful Background Context</u>  
Measures: Provision of relevant relationship, historical, and contextual information  
Scoring:
- 3 (Excellent): Rich, actionable context provided (e.g., "Your direct manager," "New client from Q3 acquisition," "Led the project you'll be presenting on"); helps user understand relationships and anticipate dynamics
- 2 (Good): Useful background context for key participants; provides most relationship information needed for effective engagement
- 1 (Fair): Some background context but may miss important relationships or historical interactions
- 0 (Poor): Little to no meaningful background context; purely transactional listing without relationship intelligence

<u>E - External & New Participant Emphasis</u>  
Measures: Clear flagging and contextualization of external participants or first-time attendees  
Scoring:
- 3 (Excellent): All external participants and new attendees clearly marked with comprehensive context (e.g., "John Smith (Client CTO from ABC Corp) - first time joining, key decision-maker for contract renewal")
- 2 (Good): External and new participants identified with good context; minor gaps in background information
- 1 (Fair): Basic identification of external/new participants but limited context about their significance or background
- 0 (Poor): Fails to clearly identify external participants or new attendees; risk of user being caught unprepared

Composite Scoring & Performance Levels  
- Overall Score Calculation:  
  Total Score = (P + R + I + M + E) / 5

Performance Bands:
- 🌟 Exceptional (2.6-3.0): Meeting Mastery
- ✅ Proficient (2.0-2.5): Well-Prepared
- ⚠️ Developing (1.4-1.9): Basic Awareness
- ❌ Needs Improvement (0.8-1.3): Minimal Value
- 🚫 Inadequate (0.0-0.7): Preparation Failure

Critical Success Indicators:
- Complete Coverage: All attendees identified, with focus on those user might not know
- Authority Clarity: Decision-makers and key stakeholders clearly highlighted
- Context Richness: Meaningful background that helps user understand relationships and anticipate needs
- External Awareness: Clear flagging of external participants or first-time attendees
- Strategic Value: Information directly supports more effective meeting engagement and preparation

Failure Modes to Avoid:
- Generic role descriptions that don't help user understand importance
- Missing external participant identification leading to surprises
- Lack of decision-maker context causing missed engagement opportunities
- Absent relationship intelligence preventing strategic preparation
- Focus on peripheral attendees while missing key stakeholders

---

### Scoring of Case 1:

**PRIME Rubric Evaluation Results**

**P - Participant Identification & Prioritization: 2/3 (Good)**
- **Strengths:**
  - Complete attendee identification: All 6 participants listed by name (Dongmei Zhang, Chin-Yew Lin, Qingwei Lin, Shi Han, Haidong Zhang, Jian-Guang Lou)
  - Meeting size manageable, so all attendees appropriately included rather than needing prioritization
  - Organizer clearly identified with leadership context
- **Gaps:**
  - No clear prioritization or emphasis on who are the most important participants for the user to focus on
  - Equal treatment of all attendees without highlighting key stakeholders or decision-makers
  - Limited guidance on which participants deserve most preparation attention

**R - Role & Title Accuracy: 1/3 (Fair)**
- **Strengths:**
  - Accurate identification of user's role ("Principal Architect")
  - Correct identification of Dongmei Zhang as organizer and "LT lead"
  - Basic organizational context provided
- **Critical Deficiencies:**
  - Missing specific titles for 67% of attendees: Chin-Yew Lin, Qingwei Lin, Shi Han, and Jian-Guang Lou lack actual job titles
  - Vague, unhelpful descriptions: "Senior leader in the DKI LT group," "Technical leadership role," "Engineering or research leadership"
  - Generic language that doesn't help user understand what these people actually do
  - Particularly problematic since user specifically asked about roles, and these are people they "might not know"

**I - Important Stakeholder Intelligence: 1/3 (Fair)**
- **Strengths:**
  - Identified Dongmei Zhang as organizer and likely decision-maker
  - Recognized her as user's manager (from profile context)
- **Major Gaps:**
  - No hierarchy or authority context beyond the organizer
  - No decision-making authority explained – unclear who has influence over what decisions
  - Missing stakeholder importance – no indication of who the user should pay special attention to
  - Lack of influence mapping – no context about each person's area of responsibility or authority level in DKI LT

**M - Meaningful Background Context: 1/3 (Fair)**
- **Strengths:**
  - Identified manager relationship (Dongmei Zhang)
  - Some attendees noted as frequent collaborators
- **Severe Shortcomings:**
  - Failed to leverage available rich context: User memory shows extensive collaboration history with Chin-Yew Lin on Meeting Prep evaluation, M.Arena, and rubric development projects
  - Missed critical relationships: No mention that "You've been working closely with Chin-Yew Lin on Meeting Prep since September"
  - No project context: Despite available data about ongoing collaborations, no background provided
  - Generic relationship descriptions without specific interaction history or working context

**E - External & New Participant Emphasis: 2/3 (Good)**
- **Strengths:**
  - Correctly identified all participants as internal Microsoft employees
  - No external participants, so no risk of missing external attendee flags
  - Internal meeting context clearly established
- **Minor Gaps:**
  - Jian-Guang Lou shows "None" RSVP status but no explanation of whether they're new to this recurring series
  - No context about whether meeting composition has changed recently
  - Missing information about first-time attendees to this specific meeting series

**Overall PRIME Score**: 1.4/3 (47%) – Developing Performance  
Performance Band: Developing (1.4-1.9) – Basic Awareness

**Interpretation:** Fundamental attendee information provided but lacks depth needed for effective meeting preparation.

---

**Critical Analysis:**

🎯 **What Worked:**
- Successfully identified all meeting participants
- Provided basic meeting logistics and structure
- Correctly established internal Microsoft context
- Identified key organizer relationship

❌ **Critical Failures:**
- Missing Job Titles: 4 out of 6 attendees lack specific, actionable role information
- Underutilized Available Data: Rich collaboration history with Chin-Yew Lin completely ignored
- Weak Authority Intelligence: No clear guidance on decision-making hierarchy or stakeholder importance
- Generic Context: Vague descriptions instead of specific, useful background information

**Impact on User Preparation:**
- Limited Strategic Value: User remains largely unprepared for individual participant dynamics
- Missed Relationship Intelligence: No leverage of known working relationships for meeting context
- Inadequate Role Understanding: Vague role descriptions don't help user tailor engagement approach
- No Decision-Maker Clarity: Uncertain about who has authority or influence in meeting discussions

**Specific Evidence of Missed Opportunities:**
Based on available user context data, the response should have included:
- "Chin-Yew Lin – You've been collaborating with them on Meeting Prep evaluation and M.Arena since September"
- "Zhitao Hou – Part of your Meeting Prep rubric development team" (noted in user's recent collaborators)
- Specific job titles available through directory lookup
- Authority levels within DKI Leadership Team structure

**Key Recommendations for Improvement:**
- Enhanced Directory Integration: Automatic lookup of specific job titles for all attendees
- Memory Context Activation: Surface relevant collaboration history and project relationships
- Authority Mapping: Clear identification of decision-making hierarchy and influence levels
- Strategic Preparation Guidance: Specific insights about each attendee's likely focus areas and expertise

**Conclusion:**  
While the system provided basic meeting roster information, it failed to deliver the strategic intelligence needed for effective leadership meeting preparation. The response functioned as a simple attendee list rather than comprehensive preparation intelligence, missing critical opportunities to leverage available relationship and collaboration data.

---

**Note:**  
- The images referenced (e.g., `![][image_pT2NFNerpBNAbkjRYjy5fg==]`) are placeholders for screenshots or figures in the original document. If you need these images included, please provide them separately or let me know if you want to extract text only.

---

If you’d like this Markdown as a downloadable file or want it added to your Canvas Page, just let me know!