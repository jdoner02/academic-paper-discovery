"""
Domain entities package.

Entities are objects that have identity and a lifecycle. They are distinguished
by their identity rather than their attributes. In our domain, the primary
entity is the ResearchPaper.

Educational Note:
- Entities have identity (usually an ID) that persists over time
- Two entities are equal if they have the same identity, even if other attributes differ
- Entities encapsulate business rules and invariants
- They should contain behavior, not just data (avoid anemic domain model)
"""
