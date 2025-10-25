I've converted your document “[GPEval][CasesAnalysis]C3BP-HaidongZhang.docx” into Markdown format as requested. However, there was a connection issue when trying to create the Markdown doc as an interactive Page. 

**Here is the Markdown content you can copy and use:**

---

# Calendar.AI  
Golden Prompts Evaluation

# Cases Analysis Notes: C3BP

**By:** Haidong Zhang

| **ID** | C3BP |
|--------|------|
| **Scenario** | Meeting with Purpose: Track |
| **Prompt** | What happened in the last /meeting any decisions and action items |

## Cases

| **Case #** | **Prompt** | **Model** | **Run on** |
|------------|------------|-----------|------------|
| 1 | what happened in the last Meeting Prep STCA Sync meeting, any decisions and action items | GPT-5 | Sept 29, 2025 |
| 2 | what happened in the last Bi-weekly DKI LT Meeting, any decisions and action items | GPT-5 | Sept 29, 2025 |

---

## Summary

## Details

### **Case 1:** _what happened in the last Meeting Prep STCA Sync meeting, any decisions and action items_

DevUI Link: https://devui.sdf-devui.substrate-turing-enterprisedevui.eastus-sdf.cosmic-ppe.office.net/?sharedSessionId=06cd6a0d-ad07-4418-8171-c219d7d5c619&entryPoint=shareCommand

#### Identify meeting
- **Is it triggered**: Yes
- **How about the quality**
  - Although I only asked about the last one, the last two instances of this recurring meeting were identified, and corresponding decisions and action items were provided. It is not precisely targeting my question, but I think it is ok.

#### Identify decisions
- **Is it triggered**: Yes
- **How about the quality**
  - ![][image_7fSRQJ9cMeRTEsnkgyFNAg==]
  - Observations:
    - The response summarized key discussion points, which are overall completed, and well captured what we have discussed.
    - Regarding the decisions, I am not sure about the first one “Ship V3 with insights and related files, excluding Topics” and the second one “Adopt simplified UX”. They look like the decisions which already have been made before this meeting. For the third one, “Continue refining prompts to balance relevancy vs. latency”, it can be viewed as an item everyone agreed on.

#### Identify action items
- **Is it triggered**: Yes
- **How about the quality**
  - ![][image_CPqodCaugPV0p6LHMQslew==]
  - Observations:
    - Overall, the action items from this meeting were captured well.
    - One action item was missed: Haidong & Zhitao to follow up with Rakesh to help prompt optimization

Rate:

---

### **Case 2:** _what happened in the last Bi-weekly DKI LT Meeting, any decisions and action items_

DevUI Link: https://devui.sdf-devui.substrate-turing-enterprisedevui.eastus-sdf.cosmic-ppe.office.net/?sharedSessionId=06cd6a0d-ad07-4418-8171-c219d7d5c619&entryPoint=shareCommand

#### Identify meeting
- **Is it triggered**: Yes
- **How about the quality**
  - The meeting was identified correctly as the most recent instance of the meeting series as of the date I run the query.

#### Identify decisions and action items
- **Is it triggered**: Yes
- **How about the quality**
  - ![][image_9L2mEARNnzl4VMDo6be2gQ==]
  - It mentioned that it cannot summarize decisions and action items due to lacking of meeting transcript or detailed notes. I think it is a reasonable answer.

---

## Discussions

- For "roles" in the prompt, users may expect their job roles, or maybe their roles in the meeting. In current answers, seems it is more about the job roles, but not consistent (e.g., for "Mark" in case 2, it provides his role in the meeting as organizer but not listed his job role).
- List all attendees vs. those who accepted the meeting?
- I am also curious if I asked about an "All-Hands meeting", what the answers will be.

---

## Rubric

### Generating the rubric:

By asking Copilot questions like “what happened in the last meeting, any decisions or action items”, the user’s goal is to get a recap of a previous meeting, and the user expects Copilot to summarize its key points: decisions made, topics covered, and actions assigned (especially those assigned to the user or still open). The response should be kept concise and factual, possibly in bullet form for each point, so the user gets a quick refresher.  
Please come up with a rubric for measuring how good Copilot fulfills such task.

### Generated Rubric:

**Meeting Recap Rubric (RECAP)**  
0-3 Scale

<u>Relevance</u>
- 0: No relevant info; off-topic
- 1: Some relevant info, but key points missing
- 2: Most key points included, minor gaps
- 3: All key points (decisions, topics, actions) are relevant and included

<u>Exactness</u>
- 0: Major factual errors or omissions
- 1: Some inaccuracies or vague statements
- 2: Mostly accurate, minor errors
- 3: Fully accurate, precise, and specific

<u>Conciseness</u>
- 0: Excessive detail or rambling
- 1: Some unnecessary detail
- 2: Mostly concise, minor verbosity
- 3: Very concise, only essential info, easy to scan

<u>Actionability</u>
- 0: No action items identified
- 1: Some actions mentioned, unclear or incomplete
- 2: Most actions clear, some missing details
- 3: All action items clearly listed, with owners/status if possible

<u>Presentation</u>
- 0: Disorganized, hard to read
- 1: Some structure, but not clear
- 2: Mostly well-structured, minor issues
- 3: Well-structured, clear bullets or sections, easy to read

To aggregate the score across dimensions:
- Assign a score (0–3) for each dimension.
- Add up the scores for all dimensions.
- Divide the total by the number of dimensions to get the average score.

### Rate of Case 1:

---

**Note:**  
- The images referenced (e.g., `![][image_7fSRQJ9cMeRTEsnkgyFNAg==]`) are placeholders for screenshots or figures in the original document. If you need these images included, please provide them separately or let me know if you want to extract text only.
