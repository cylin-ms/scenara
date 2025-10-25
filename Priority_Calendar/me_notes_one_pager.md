People Notes About Me—One Pager
I am I, because I remember.
Reza Bonyadi, Feb. 2025

Extracted from user communications within M365—one of the largest repositories of people-communications data on the planet—Me Notes provides a rich, continually updated, open-ended textual representation of the user ("Me") at varying levels of abstraction, while remaining private to the user. At its simplest, it captures clear, factual insights drawn directly from daily interactions (Level 1 notes), such as "Reza is working on Project Atlas." At a deeper level, it synthesizes information scattered across multiple interactions over time, forming nuanced insights (Level 2 notes capturing habits, preferences, and styles), such as "Reza carefully analyzes options before making critical decisions."
Current status of Me Notes: Today, Me Notes are extracted from emails, chats, and meeting transcripts, which can be extended to other 1P and 3P data sources as needed. The notes include the note snippet, classification tag, and a title. Me Notes is available in MSIT and indexed by Entity Serve, and is planned to go WW during 25Q3. Check out your me notes in personalization canvas and in the pint portal (available to SDF users only). Note that, if you are in Europe, Me Notes is turned off by default for you. Please contact us to help you on-board. See details here: aka.ms/peoplenotes.
# Why Me Notes Matters:
Individual productivity: With a comprehensive understanding of "Me," M365 services, including the Microsoft agentic and Copilot ecosystem, can deliver responses tailored to individual needs, preferences, priorities, and contexts.
Business productivity: Many businesses—such as law firms, consultancies, and online professional services—rely on an up-to-date picture of each team member’s skills, interests, and accomplishments to assign the right tasks to the right people. Me Notes captures this information in near‑real time and can enable the user to select and share them broadly and safely.
Concrete Example (Illustrative Scenario): Sarah, a senior consultant at a global consultancy firm, has her "Me Notes" automatically updated daily from her work-related communications and meetings.
At the individual productivity level, Microsoft's Copilot proactively surfaces an important client opportunity buried in yesterday's lengthy email thread Sarah didn't have time to fully review. Copilot does this because Me Notes captured Sarah’s ongoing interests and focuses in sustainability projects.
At the business productivity level, Sarah’s manager is staffing a critical sustainability consulting project. With Sarah’s consent through a privacy-preserving interface, her manager quickly sees recent updates from her Me Notes about her recent successful engagements and current interests in sustainability. This helps the manager confidently assign Sarah to the new high-impact project, improving efficiency and project fit.
Me notes capabilities and opportunities: Microsoft is uniquely positioned to bring Me Notes and its impact to millions of users, offering unrivaled personal context in a safe and compliant manner. With an unmatched global footprint in enterprise data and the trust we’ve earned from countless user interactions, we can shape the most complete representation of users on the planet, used to add value back to our users. No other company on the planet can achieve the same depth of user understanding while maintaining privacy and security. By applying index-time deep reasoning to communications across the M365 ecosystem, Me Notes aspires to become the most comprehensive and living expression of each user’s story—an open-ended resource that remains ever-current and readily available.
# How to access Me Notes
Quick summary (see details here: How to test Me Notes.loop):
For viewing Me Notes and light interactions:
Use "aka.ms/pint" (SDFv2 only)
Use MPS canvas: Personalization V1 (SDFv2)
Use this shell script that allows interacting with any notes using LLM API: me_journal_v1.ps1 (MSIT, use DAT tool and AzVPN for auth and secure connection)
For integrations [ FOR DEV debugging only – Reach out to talk about Prod]
Use IQAPI: LINK with pre-filled query
Use AnnotationStore: readMePeopleNotesFromAS.http - Repos
Use Substrate query (instructions here, see section “for a specific person”)
Use EntityServe (Search), Pick People Notes as “Type” in ES explorer
Use AugLoop skills/plugins (utils are here, an integration example, DocumentRelevance, here)
# Me Notes object
When you query Me Notes through any of the methods mentioned above, you receive an object (in JSON fromat or any other format, depending on the endpoint you use), which contains:
The Note: A piece of text that describes a noteworthy knowledge about me, the user.
Category of the Note: What is the type of the snippet (e.g., FOLLOW_UPS, WORK_RELATED), see details here: [Partner] Available People Note Categories - Overview.
Title of the Note: Describes the note in a few words.
Temporal durability: Is the snippet a likely temporal knowledge or more durable (e.g., TEMPORAL_SHORT_LIVED), see details here: [Partner] Available People Note Categories - Overview.
# Me Notes distribution
Here is the distribution of Me Notes:


User-to-user knowledge is almost always rich. Distribution of Me Notes (per week in MSIT): 12 notes (per week) at P50, and 40 notes (per week) at P95.
# Scenarios and examples
From personalized document and meeting summarization to context-aware digital agents, Me Notes enables next-level productivity for knowledge workers and businesses. There was a large effort during the past years in terms of collecting scenarios, demos, showing value of personalization using me data, etc. Here are some prototypes using Me Notes:
Using Me Notes to Discover impact opportunities in your emails: Discovery Agent: Your Personal Agent to Discover Where You Matter
Using Me Notes to write your connect automatically: "Connect" Declarative Agent
Using Me Notes in an adaptive personalization scheme: March 2024 - Copilot Adaptive Personalization
Using Me Notes for personalization and accessibility: March 2024 - Copilot Accessibility Personalization
Lots of examples using Me Notes for personalization (document summary, email triage, finding surprising discoveries, and more): sydney_PN.pptx
Using Me Notes through Sydney plug-ins for personalization: Personalizing Copilot with Adaptive User Representation, and 2024-11-21 Everything is a People Notes plugin.pptx, 2025-02-04 FAST Personalization Show and Tell.pptx
To be continued…



