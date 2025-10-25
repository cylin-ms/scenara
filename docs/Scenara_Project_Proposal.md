# Scenara: AI-Native Unit Test Generator & Evaluator
Purpose
Chin-Yew Lin, Haidong Zhang, and Copilot
## This proposal outlines a future-looking framework for Scenara, an AI-native Unit Test generator and evaluator for AI-native apps and services.

1. Conceptual Transfer: From Unit Test to AI-Native Unit Test
## Traditional Unit Test: Checks if a software function behaves as expected for given inputs, with clear pass/fail criteria.
## AI-Native Unit Test: Evaluates if an AI system (e.g., Copilot, LLM agent) correctly handles a real-world scenario, decomposing it into sub-scenarios, generating test cases, and scoring outputs using rubrics and completion metrics.

2. End-to-End Process for Scenara
## Scenario Intake: User provides a scenario (e.g., “Prepare for a customer meeting with pre-reads and attendee dossiers”).
## Scenario Analysis & Decomposition: Scenara analyzes the scenario, referencing a taxonomy (like meeting types) to identify archetypes and break down into sub-scenarios.
## Test Point & Edge Case Generation: For each sub-scenario, Scenara identifies key steps, required context, and possible edge cases. Defines what needs to be checked.
## Context/Background Setup: Determines what synthetic or real data is needed and sets up a test tenant or sandbox with representative data.
## Variant Test Case Generation: Produces N variants of the scenario for broad and specific coverage.
## Model Evaluation: Runs the AI-native model on each test case and collects outputs.
## Rubric-Based Scoring & Task Completion Verification: Applies rubrics to score outputs and uses a checklist to verify task completion. Logs results and scores.
## Iterative Improvement: Uses results to refine prompt templates, agent behaviors, and test coverage.

3. Analogy: Screenplay Writer from Novel
## Like a screenwriter adapting a novel, Scenara fills in action details, props, and sequences, ensuring all critical beats are covered and anticipating edge cases.

4. Key Features
## Taxonomy-Driven: Uses a robust taxonomy to classify and decompose scenarios.
## Templatized Prompts: Leverages machine-readable templates for each scenario archetype.
## Automated Test Tenant: Deploys a sandbox with synthetic data for safe, repeatable testing.
## Rubric & Checklist Evaluation: Combines qualitative (rubric) and quantitative (completion) metrics.
## Variant Generation: Supports broad and specific scenario coverage.
## Continuous Learning: Refines itself based on test outcomes and rubric feedback.

5. Example: Meeting Prep Scenario
User Scenario: “Prepare for a weekly engineering standup with deck audit and owner reminders.”
Identifies scenario as “Team Status Update.”
## Breaks down into: deck audit, owner mapping, reminder drafting, escalation.
## Sets up synthetic deck with missing/unclear slides.
## Generates test cases: all slides updated, some missing, unclear owners, deadline passed.
## Runs Copilot on each case, collects outputs.
Scores: Did it identify missing slides? Draft correct reminders? Escalate as needed?
## Logs results, updates templates if gaps found.

6. Concrete Scenario Walkthroughs
### Walkthrough 1: Customer Briefing with Attendee Dossiers
Scenario: “Prepare a brief for my meeting with customer Beta; include attendee dossiers and company background.”
**Sub-scenarios:**
Company background synthesis
Attendee dossier generation
Brief formatting and delivery
**Test Points:**
Are all dossier fields populated?
Is the background sourced from correct repositories?
Is the brief NDA-safe?
**Edge Cases:**
Missing attendee info
Conflicting company data
Sensitive content leakage
### Walkthrough 2: Leadership Sync with Objection Handling
Scenario: “Summarize into 3 main points; anticipate objections and responses.”
**Sub-scenarios:**
Point synthesis
Objection prediction
Response drafting
**Test Points:**
Are points aligned with strategic priorities?
Are objections realistic and responses data-backed?
Is the tone confident and concise?

7. Rubric Templates
**Rubric Dimensions:**
Coverage: Does the output include all required elements?
Accuracy: Are facts and references correct?
Contextual Relevance: Is the output tailored to the scenario?
Usability: Can the output be directly used by the end user?
Taxonomy Alignment: Does the output match the scenario archetype?
Leakage & RAI (Responsible AI) Concerns:
Leakage: Does the output avoid exposing confidential, sensitive, or NDA-protected information?
RAI: Does the output comply with Responsible AI principles (fairness, transparency, privacy, safety, inclusiveness, accountability)?
### Sample Rubric (5-point scale)

8. Automation Blueprint
**Components:**
## Scenario Parser: Converts user input into structured scenario.
## Sub-scenario Mapper: Uses taxonomy to identify components.
## Test Case Generator: Produces variants and edge cases.
## Test Tenant Orchestrator: Sets up synthetic data and environment.
## Evaluator Engine: Runs model, applies rubric, logs results.
## Feedback Loop: Refines prompts and templates based on scores.

9. Benefits & Strategic Impact
## Objective Benchmarking: Standardizes how AI-native workflows are evaluated.
## Scalable & Repeatable: Enables continuous, automated regression testing as models evolve.
## Traceable & Actionable: Every test is logged, scored, and linked to improvement actions.
## Domain-Extensible: While meetings are the first domain, the approach generalizes to any AI-native workflow (e.g., document drafting, code review, customer support).
## Strategic Differentiator: Positions Microsoft as a leader in AI-native engineering quality assurance.
## Enterprise Readiness: Supports compliance, governance, and Responsible AI at scale.

10. Next Steps
## Formalize the taxonomy and template schema for all target domains.
## Build the test tenant automation pipeline.
## Develop rubric and checklist libraries for each scenario archetype.
## Integrate with model evaluation dashboards for continuous monitoring.
## Pilot with internal Copilot scenarios and expand to partner teams.

