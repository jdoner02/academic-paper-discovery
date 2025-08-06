"""
Ports package - Dependency Inversion interfaces.

Ports define the contracts that the application layer needs from external systems.
They represent the boundaries of our application and follow the Dependency
Inversion Principle by defining what we need, not how it's implemented.

Educational Notes:
- Ports are abstract interfaces (ABC in Python)
- Infrastructure layer implements these ports (adapters)
- This allows easy testing with mock implementations
- Enables swapping implementations without changing application logic

Hexagonal Architecture:
Ports are the "hexagon edges" - they define how the application
communicates with the external world without being coupled to it.

Types of Ports:
- Repository Ports: Data access abstractions
- Source Ports: Multi-source data access abstractions
- Service Ports: External service abstractions
- Notification Ports: Communication abstractions

Multi-Source Evolution:
The addition of PaperSourcePort demonstrates how Clean Architecture
enables evolution. We extend existing abstractions (PaperRepositoryPort)
without breaking existing code, adding multi-source capabilities while
maintaining backward compatibility.
"""

from src.application.ports.paper_repository_port import PaperRepositoryPort
from src.application.ports.paper_source_port import PaperSourcePort

__all__ = [
    "PaperRepositoryPort",
    "PaperSourcePort",
]
