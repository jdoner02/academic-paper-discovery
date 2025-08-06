# Research Paper Discovery Platform - Source Module

"""
Interactive Research Paper Discovery Platform Source Module.

This module contains the complete Clean Architecture implementation for
transforming academic paper collections into interactive visual concept maps.

Educational Notes:
This package demonstrates professional software architecture patterns including:
- Clean Architecture with strict layer separation
- Domain-Driven Design with rich business models
- Test-Driven Development with comprehensive coverage
- Design patterns applied to real-world academic problems

Package Structure:
- domain/: Pure business logic (entities, value objects, services)
- application/: Use cases and abstract ports
- infrastructure/: External dependencies and adapters
- interface/: User interfaces and API endpoints

The architecture emphasizes:
1. Dependency Inversion: Inner layers define interfaces, outer layers implement
2. Single Responsibility: Each component has one clear purpose
3. Open/Closed Principle: Extensible without modification
4. Interface Segregation: Small, focused interfaces
5. Liskov Substitution: Implementations are interchangeable

Real-World Application:
Academic researchers need tools that bridge technical capabilities with
intuitive user experiences. This platform demonstrates how to build
sophisticated ML-powered applications with maintainable, educational code.
"""

__version__ = "0.1.0"
__author__ = "Jessica Doner"
__email__ = "jdoner02@gmail.com"
__description__ = "Interactive research paper discovery with visual concept mapping"

# Educational Note: Version information helps with reproducible builds
# and dependency management across development environments
