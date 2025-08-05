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
- Service Ports: External service abstractions
- Notification Ports: Communication abstractions
"""
