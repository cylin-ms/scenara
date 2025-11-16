# ACRUE based Assertion and Rubrics

By: STCA Time and Place Team

This is an initial version of implementation for two-stage assertion generation

**Query pattern**: What will be discussed in this <event> meeting? Focus on the top 3 or 4 points. And why does it matter? Should I attend or what happens if I skip?

**Utterance**: What will be discussed in this Solutions Architecture & Security Governance Pipeline Review meeting? Focus on the top 3 or 4 points. And why does it matter? Should I attend or what happens if I skip?


## Assertions
- text: The answer states the meeting title exactly as "Solutions Architecture & Security Governance Pipeline Review."
  - level: critical
  - dimension: Accuracy

- text: The response lists the start time as July 28 2025 10: 00 AM (local Pacific time) and the end time as 11: 00 AM.
  - level: critical
  - dimension: Accuracy

- text: The answer uses future-oriented wording such as "will discuss" or "is planned to cover," not past tense.
  - level: critical
  - dimension: Accuracy

- text: Exactly 3 or 4 discussion points are presented – no more, no less.
  - level: critical
  - dimension: Completeness
- text: Each discussion point is grounded in the invite body or the attached file pipeline_review_agenda.docx (e.g., "final Jenkins pipeline enhancement review," "audit-artifact retention policy," "RSD alignment sign-off").
  - level: critical
  - dimension: Accuracy

- text: The answer explicitly references the two pre-reads: pipeline_review_agenda.docx and rsd_pipeline_alignment.docx.
  - level: expected
  - dimension: Completeness
- text: The answer names at least Terina Hafen and Shari Jatho as key stakeholders, matching the RequiredAttendees list.
  - level: expected
  - dimension: Accuracy

- text: Under "why it matters," the answer links the topics to compliance sign-off (FedRAMP / audit) and production rollout readiness, reflecting language in rsd_pipeline_alignment.docx.
  - level: expected
  - dimension: Accuracy
- text: The response recommends that Nila should attend because she owns open action items (e.g., coordinating Solutions Architecture sign-off noted in CI_CD_Integration_Details.xlsx ActionItem AI-002) and is the organiser.
  - level: critical
  - dimension: Accuracy

- text: Consequences of skipping include missing the final sign-off and delaying compliance approval, pulled from event body that it is a "final review"
  - level: expected
  - dimension: Completeness
- text: The answer offers a mitigation if skipping, such as delegating to Terina Hafen or asking for the meeting recording and updated RSD doc.
  - level: expected
  - dimension: Completeness

- text: The answer notes the meeting is today in less than 24 hours and flags urgency for any last-minute preparation.
  - level: expected
  - dimension: Usefulness
- text: Preparation actions include reviewing "pipeline_review_agenda.docx" and "rsd_pipeline_alignment.docx" before attending.
  - level: expected
  - dimension: Usefulness

- text: The content is organised into clear sections: Top Points, Why It Matters, and Attendance Recommendation.
  - level: expected
  - dimension: Usefulness
- text: Each discussion point is numbered or bulleted and limited to two lines, supporting scannability.
  - level: aspirational
  - dimension: Usefulness

- text: No unrelated meetings or general company updates appear in the answer.
  - level: critical
  - dimension: Relevance
- text: The response avoids speculation beyond what is in the invite or attached docs (e.g., does not predict new agenda items).
  - level: critical
  - dimension: Relevance

- text: If the answer indicates any uncertainty (e.g., "agenda may change"), it labels it clearly as tentative.
  - level: aspirational
  - dimension: Accuracy
- text: The answer cites the organizer (Nila Tanguma) or "your meeting" to establish provenance.
  - level: expected
  - dimension: Accuracy

- text: The answer gives a short executive summary sentence at the top capturing the meeting's criticality.
  - level: aspirational
  - dimension: Exceptional
- text: Risk level of skipping is characterised (e.g., "High risk to project timeline if you are absent".
  - level: expected
  - dimension: Usefulness

- text: Topics are prioritised in order of importance (e.g., #1 Final pipeline sign-off, #2 Compliance traceability, etc.).
  - level: expected
  - dimension: Usefulness
- text: The answer mentions that the meeting is the final gate before production pipeline changes, tying importance to imminent deadlines.
  - level: expected
  - dimension: Completeness

- text: No more than 4 discussion points are listed, satisfying the "focus on top 3–4" instruction.
  - level: critical
  - dimension: Relevance
- text: "Why it matters" explanations are linked to compliance approval and production readiness rather than generic statements.
  - level: critical
  - dimension: Relevance

- text: The response refrains from making any unsupported commitments or promises (e.g., it does not guarantee audit approval).
  - level: expected
  - dimension: Accuracy
- text: If the answer cites document links, it uses the correct file names (pipeline_review_agenda.docx, rsd_pipeline_alignment.docx) as per attachments.
  - level: expected
  - dimension: Accuracy

- text: The answer mentions that the meeting is today (or "later today" making it time-aware.
  - level: expected
  - dimension: Relevance
- text: The language is direct and avoids generic phrases like "important topics" instead using concrete phrases ("final Jenkins pipeline enhancement review".
  - level: aspirational
  - dimension: Usefulness

- text: The answer avoids redundant repetition of points across sections.
  - level: expected
  - dimension: Usefulness
- text: If the answer suggests a delegate, it proposes someone on the attendee list (e.g., Terina Hafen) or explains what profile would be suitable.
  - level: aspirational
  - dimension: Usefulness

- text: Any mention of follow-up steps if skipping includes reviewing the meeting recording or minutes post-meeting.
  - level: aspirational
  - dimension: Usefulness
- text: If confidence/uncertainty is expressed (e.g., "High confidence based on attached agenda", it is tied to specific sources.
  - level: aspirational
  - dimension: Exceptional

- text: The answer remains concise and avoids excessive formatting not supported by simple display.
  - level: expected
  - dimension: Usefulness
- text: The response uses neutral, professional tone without assigning blame.
  - level: expected
  - dimension: Usefulness

- text: If the answer includes project or compliance names (e.g., FedRAMP, SI-10), they are spelled correctly and match source documents.
  - level: expected
  - dimension: Accuracy
- text: The answer does not include information about any other recurring series – refers only to this single instance.
  - level: expected
  - dimension: Accuracy

- text: The answer does not contradict any details in the invite (e.g., does not claim the meeting is 2 hours long).
  - level: critical
  - dimension: Accuracy

- text: The response offers a brief post-meeting checklist if skipping (e.g., review minutes, confirm action items).
  - level: aspirational
  - dimension: Exceptional

### Distribution
For this utterance, the distribution of all generated assertions
#### ACRUE
Accuracy : 14 (35.9%) 
Usefulness : 12 (30.8%)
Completeness : 5 (12.8%)
Relevance: 5 (12.8%)
Exceptional : 3 (7.7%) 
#### level
expected : 20 (51.3%) 
critical: 11 (28.2%)
aspirational: 8 (20.5%)

## Rubrics
### Accuracy
- Meeting title exactly matches the title in the invite or calendar entry.
- Meeting date, start/end time, and timezone are correctly identified and consistent with the invite.
- Correctly identifies whether the meeting is in the past, today, or future relative to the current date.
- Uses appropriate tense and phrasing based on timing (future: “will discuss”; past: “was discussed”; today: “is expected today”).
- Pulls the most recent agenda revision; does not rely on outdated drafts.
- Top 3–4 points are grounded in verified sources (agenda/pre-reads/organizer notes) and, when available, prior minutes/recordings/transcripts and relevant emails/chats.
- If the meeting already occurred, the listed points match what was actually discussed per minutes/recording.
- Stated decisions (e.g., approvals, sign-offs) match agenda language or pre-read objectives.
- Stakeholders/attendees named (if included) match the invite or attendee roster.
- Project names, dependencies, acronyms, and figures cited match current materials.
- “Why it matters” statements accurately reflect business impact, deadlines, or compliance requirements stated in artifacts.
- References to documents (titles/links) are correct, accessible, and point to the latest versions with revision date noted.
- Includes dates on cited sources or last-checked time to demonstrate recency.
- Identifies the organizer or source of the agenda to establish provenance.
- Distinguishes confirmed information from assumptions and labels assumptions explicitly.
- If asked about follow-ups, includes updates since the meeting only up to the current date (no future speculation).
- Recognizes recurring series and references the upcoming instance’s specific agenda rather than generic series descriptions.
- No contradictions exist between the response and cited meeting artifacts.
- The attendance recommendation accurately reflects whether the user’s presence is required (e.g., approval authority).
- Any uncertainty (e.g., tentative agenda) is explicitly labeled and not presented as confirmed.
- No unsupported promises or commitments are made; claims are backed by cited sources.
- If importance or relevance is unclear from available artifacts, frames the attend/skip guidance as conditional and avoids subjective assertions.

### Completeness
- Provides exactly 3 or 4 top discussion points (no fewer, no more).
- Each discussion point includes a brief “why it matters” explanation tied to outcomes, risks, or deadlines.
- Each point notes the expected action or decision (decide, align, review, inform) where applicable.
- Includes a clear attend or skip recommendation for the user.
- Describes specific consequences of skipping tied to each top point (e.g., loss of influence on X decision).
- Offers mitigation options if skipping (delegate, submit input asynchronously, review notes/recording).
- Identifies required pre-work or pre-reads and indicates whether they are complete or pending.
- Highlights key stakeholders expected to attend if relevant to the user’s decision.
- Notes time sensitivity (deadlines, milestones) associated with the topics.
- Provides pointers to source artifacts (agenda doc, invite, prior minutes) when available.
- States any known information gaps and how to resolve them (e.g., “agenda not published; check link by <date>”).
- If the meeting is past yet the question asks “will be discussed,” clarifies the meeting has concluded and summarizes actual outcomes.
- Provides conditions under which the attendance recommendation would change (e.g., contingent on stakeholder attendance or document availability).
- Specifies what happens if no one from the user’s team attends and how to mitigate that outcome (e.g., assign delegate, submit written input).

### Relevance
- Focuses strictly on the specified meeting; excludes unrelated meetings or general company updates.
- Limits content to the top 3–4 priority topics rather than the full agenda.
- “Why it matters” explanations are tied to this meeting’s objectives, decisions, or risks.
- Attendance recommendation is linked to the user’s role/responsibilities when known, or framed generically when unknown.
- Uses time-aware framing appropriate to the meeting date (future agenda vs. past outcomes vs. today’s expectations).
- Avoids speculation beyond what is supported by the invite, agenda, pre-reads, minutes, or organizer notes.
- Excludes extraneous background that does not affect the attend/skip decision.
- Consequences of skipping are specific to this meeting’s content, not generic boilerplate.
- Avoids premature speculation for distant future meetings; focuses on known agenda and prep plan.
- References the upcoming instance’s agenda for recurring meetings rather than a generic series description.

### Usefulness
- Prioritizes the topics clearly (e.g., numbered list from highest to lower priority).
- Provides a concise, scannable summary suitable for quick reading.
- Presents a decisive attend/skip recommendation with rationale.
- Assigns a clear overall risk level to skipping (e.g., low/medium/high) with justification, or per topic where relevant.
- Lists concrete actions if attending (specific pre-reads, data to bring, talking points).
- Lists concrete actions if skipping (delegate selection, send notes/questions, request minutes/recording).
- Suggests an appropriate delegate profile or specific person if available.
- Indicates whether the meeting requires the user’s presence for approvals or commitments.
- Identifies the most relevant stakeholders to engage with during or after the meeting.
- Suggests follow-up steps to stay aligned if skipping (review notes/recording, debrief from delegate).
- Emphasizes last-minute prep and attendance urgency if the meeting is imminent (today or within 24 hours).
- Presents the top 3–4 points as succinct bullets with parallel structure for readability.
- Organizes content into at least these core sections: top discussion points, why the meeting matters, and attendance recommendation (with consequences of skipping where relevant).
- Uses direct, unambiguous language; defines necessary terms or acronyms.
- Keeps the response concise; avoids heavy formatting incompatible with simple display.
- Uses clear action verbs for recommendations and next steps (e.g., “send,” “review,” “decide”).
- Ensures scannability: each bullet ≤2 lines for clarity.
- Avoids generic phrases (e.g., “important topics”); uses specific, verifiable wording.
- Maintains a neutral, professional tone; avoids blame language.
- Avoids duplication across sections (no repeated points or rationale).

### Exceptional
- Connects topics to strategic initiatives, OKRs, or critical deadlines to underscore impact.
- Explains how the meeting matters to the user specifically by aligning topics to their work, goals, or objectives (when known).
- Identifies decisions at risk if the user skips and offers contingency plans.
- Uses insights from prior related meetings or threads to refine expected discussion points.
- Provides a one-sentence executive summary capturing the meeting’s criticality.
- Tailors advice to the user’s role/objectives when known, or asks one targeted clarifying question to tailor if not.
- Flags prerequisites or dependencies (e.g., data needed, stakeholder alignment) and suggests pre-meeting actions to resolve them.
- Indicates confidence levels for each point and cites the basis/source for that confidence.
- Offers a brief post-meeting follow-up checklist (what to review, who to ping) if skipping.
- Surfaces emergent risks or opportunities inferred from source materials without inventing facts.
- Suggests sample talking points or questions the user could raise to influence outcomes.
