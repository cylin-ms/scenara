# Me Notes Access Guide
Based on me_notes_one_pager.md documentation

## Issue Found
- aka.ms/pint redirects to feedback portal, not actual Me Notes data
- Need to use alternative access methods from documentation

## Next Steps to Try

### 1. MPS Canvas: Personalization V1 (SDFv2)
- Visit Microsoft SharePoint personalization sites
- Look for "Personalization V1" section
- Navigate to Me Notes dashboard/canvas

### 2. PowerShell Script Method
- Find: me_journal_v1.ps1 
- Requires: MSIT access, DAT tool, AzVPN
- Allows: LLM API interaction with notes

### 3. API Methods (DEV debugging only)
- IQAPI: Direct API access
- AnnotationStore: readMePeopleNotesFromAS.http
- Substrate Query: Person-specific queries  
- EntityServe: Search with "People Notes" type
- AugLoop: Skills/plugins integration

### 4. File Search Needed
- Look for: "How to test Me Notes.loop" file
- Find: me_journal_v1.ps1 script
- Find: readMePeopleNotesFromAS.http file
- Find: Integration examples and utils

## Me Notes Object Structure
When accessed properly, each note contains:
- **note**: The insight text
- **category**: Type (FOLLOW_UPS, WORK_RELATED, etc.)
- **title**: Short description  
- **temporal_durability**: Duration (TEMPORAL_SHORT_LIVED, etc.)

## Expected Data Volume
- P50: 12 notes per week
- P95: 40 notes per week
- Rich user-to-user knowledge
