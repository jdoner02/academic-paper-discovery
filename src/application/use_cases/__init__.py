"""
Use cases package.

Use cases represent single business operations that the application can perform.
They orchestrate domain objects to fulfill specific business requirements.

Educational Notes:
- Each use case should do one thing well (Single Responsibility Principle)
- Use cases depend on domain objects and ports, not concrete implementations
- They contain application-specific business logic, not domain business logic
- Use cases are the entry points for external requests into the application

Pattern: Command Pattern
Each use case implements a specific command that can be executed by the application.
This makes the system more modular and testable.
"""
