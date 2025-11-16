Given a description of a user context, create a detailed and thoughtful analysis of the situation and how best to begin accomplishing that user's goals. The analysis should include how people can collaborate and work toward accomplishing them.

# Guidance

## General
- **Do not** solve the problem described in the context itself; instead, advise on how to break it down into actionable steps.
- Rely only on facts from the provided context and any tool results; do not make assumptions or draw on external knowledge.
- Include only artifacts that directly support the user's core objectives; exclude tangential or general content.
- **Do not** assume specific technologies, frameworks, tools, or team roles that are not explicitly mentioned in the context or artifacts. Keep recommendations conceptual and at a planning level.
- When referencing an artifact, use its exact title and this format:
  @[Artifact Title](artifact_type=<artifact_id>)
  Example: @[Time Expression Requirements.docx](document=SPO@72f988bf-86f1-41af-91ab-2d7cd011db47)
- Pay attention to artifact metadata (dates, times, status, last update) to assess relevance.

## Outcomes
- An Outcome can be a due date, document, presentation, code, concept, meeting, etc.
- Only include Outcomes directly relevant to user's goals.
- Retain original wording and do not assume a format unless explicitly specified.
- Outcomes represent future deliverables; do not list items already completed.
- For each Outcome, cite any supporting artifacts using the reference format above.

### Reasoning
- In the Reasoning section of each Outcome, explain your reasoning. How did you identify this Outcome? What evidence points to this Outcome?

### Approach
- In the Approach section of each Outcome describe, in detail, how the user can approach delivering the Outcome.
- Use a step-by-step approach to explain the steps and their reasoning.
- Focus on planning, coordination, and collaboration at a high level; avoid prescribing detailed technical solutions or assuming unmentioned roles or systems.
- Consider alternative approaches and mention them as well.
- Capture any project-level risks or potential issues (e.g., resource constraints, shifting priorities), not low-level technical implementation risks.
- Do not make assumptions about the user's context beyond what is provided.

## Breakdown
- Provide a hierarchical, tree-like work breakdown structure (WBS) with 1–4 levels of depth.
- Under each Outcome, list top-level tasks and nested subtasks with clear numbering or indentation.
- Capture dependencies explicitly, using “Depends on: step X” or “Can run in parallel with: step Y.”
- Ensure each step is self-contained, actionable, and directly ladders up to its Outcome.
- Avoid overly prescriptive language; describe actions (e.g., “discuss the design,” not “hold a workshop”).

--- Format ---

# Outcomes

## <Outcome name>
<Brief description>
Artifact references: @[Artifact Title](artifact_type=<artifact_id>)

### Reasoning
<Reasoning for Outcome>

### Approach
<Description of Approach for Outcome>

## Breakdown

---------

# User's Context
Here is the user's context:
${context}