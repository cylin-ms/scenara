## Document Structure
Execution plan is a JSON document, starting with a root entity of type "Document".

## Standard Fields
These are standard fields names and types:
- "id": Unique, immutable id of an entity. Immutable. Preferred format is ```<entity-moniker>-XXX```. (e.g. task-001).
- "name": Short, user-friendly name for an entity. Immutable.
- "details": Detailed freeform, textual description, notes or history of the entity. This should be updated as necessary as more details are learned. This is the notes that you want to keep around internally.
- "history": Array of history entities related an entity. Immutable (appended by external systems).
- "draft": boolean field indicating whether an entity is currently being edited/added as part of this session or not. whenever a new entity is added, it needs to be marked as draft=true.

### Document
This is the root entity for the document.
Fields:
- name
- details
- draft
- participants: Array of Participant entities.
- references: Array of Reference entities.
- deliverables: Array of Deliverable entities.
- tasks: Array of task entities.
- history

### Participant
Represents a participant in the plan. The current user is an implicit partipant and can be referenced with keyword `you`. The system is also an implicit participant and can be referenced with keyword `system`.
Fields:
- name
- email: Email address of the user (string).
- details
- draft

### Reference
Represents a reference to an external entity. This entity captures the details. To use the reference in text, or in other fields, use the string form "@ref[<type>]/<id>" (e.g. "@ref[word]/abc").
Fields:
- name
- type: type of reference. email|chat|event|meeting|word|excel|powerpoint|...
- id
- history
- draft

### Deliverable
Represents a deliverable artifact. This entity captures the details. To use the reference in text, or in other fields, use the string form "@deliverable[<type>]/<id>" (e.g. "@deliverable[word]/abc").
Fields:
- name
- type: type of artifact. word|excel|powerpoint|...
- id
- draft
- history


### Task
Represents a task in the plan. A task can be assigned to one or more participant, including the user "you" or "system" Each task represents a concrete, actionable item.
Fields:
- id
- name
- draft
- details
- dependencies: array of ids of tasks that this task is dependent on.
- co-dependencies: array of ids of tasks that this task is co-dependent on.
- state: state of the task. One of: not-started|started|completed|abandoned|blocked.
- due-by: datetime by which this task must be completed. Optional.
- assignees: array of email addresses, or "you" or "system" that this task is assigned to.
- deliverables: array of Deliverable reference that this task is related to.
- references: array of Reference references that this task is related to.
- history

### History
Represents an entry that captures a log of activity that happened externally. **Do not edit** these. They are supplied by the external system.
Fields:
- date
- details



## Examples

──────────────────────────────────────────────────────────
Example 1
──────────────────────────────────────────────────────────
{
  "id": "document-001",
  "name": "Short Plan",
  "participants": [
    {
      "name": "Alice",
      "email": "alice@example.com"
    }
  ],
  "tasks": [
    {
      "id": "task-001",
      "name": "Draft Outline"
    }
  ]
}


──────────────────────────────────────────────────────────
Example 2
──────────────────────────────────────────────────────────
{
  "id": "document-002",
  "name": "Extended Plan",
  "participants": [
  {
    "name": "Bob",
    "email": "bob@example.com"
  },
  {
    "name": "Carol",
    "email": "carol@example.com"
  }
  ],
  "references": [
  {
    "name": "Design Spec",
    "type": "word",
    "id": "doc-001"
  }
  ],
  "deliverables": [
  {
    "name": "Project Report",
    "type": "word",
    "id": "report-001"
  }
  ],
  "tasks": [
  {
    "id": "task-001",
    "name": "Review Specs",
    "references": [
      "@ref[word]/doc-001"
    ],
    "state": "started"
  },
  {
    "id": "task-002",
    "name": "Write Report",
    "dependencies": [
      "task-001"
    ],
    "deliverables": [
      "@deliverable[word]/report-001"
    ],
    "assignees": [
      "carol@example.com"
    ],
    "due-by": "2024-02-01T09:00:00Z",
    "state": "not-started"
 }
]
}



