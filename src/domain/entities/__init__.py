"""
Domain entities package.

Entities are objects that have identity and a lifecycle. They are distinguished
by their identity rather than their attributes. In our domain, the primary
entities are ResearchPaper, Concept, and PaperConcepts.

Educational Note:
- Entities have identity (usually an ID) that persists over time
- Two entities are equal if they have the same identity, even if other attributes differ
- Entities encapsulate business rules and invariants
- They should contain behavior, not just data (avoid anemic domain model)
"""

from .research_paper import ResearchPaper
from .concept import Concept
from .paper_concepts import PaperConcepts

__all__ = ["ResearchPaper", "Concept", "PaperConcepts"]
