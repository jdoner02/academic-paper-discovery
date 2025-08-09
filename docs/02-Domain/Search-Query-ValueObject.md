# Search Query Value Object

> **Context**: The Search Query represents the core user intent in our Academic Paper Discovery System. As a value object, it encapsulates immutable search parameters while ensuring data integrity and providing a consistent interface for search operations.

## 🎯 Purpose and Domain Role

The `SearchQuery` value object serves as the **primary contract** between user interface and business logic. It transforms raw user input into a structured, validated representation that drives the entire paper discovery workflow.

**Domain Significance:**
- **Immutable Contract**: Once created, search parameters cannot be modified
- **Validation Gateway**: Ensures all search requests meet business rules
- **Type Safety**: Prevents invalid search configurations from reaching business logic
- **Equality Semantics**: Two queries with identical parameters are considered equal

## 📋 Value Object Characteristics

### Immutability Implementation

```python
from typing import List, Optional, Tuple
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class SearchQuery:
    """
    Immutable search query representation.
    
    Educational Value: Demonstrates value object pattern
    with immutability, validation, and equality semantics.
    
    This implementation shows how to create robust value
    objects that enforce business rules and prevent invalid states.
    """
    
    _terms: Tuple[str, ...]
    _date_range: Optional['DateRange']
    _domain_filters: Tuple[str, ...]
    _max_results: int
    _sort_criteria: 'SortCriteria'
    
    def __init__(self, 
                 terms: List[str],
                 date_range: Optional['DateRange'] = None,
                 domain_filters: List[str] = None,
                 max_results: int = 50,
                 sort_criteria: 'SortCriteria' = None):
        """
        Create validated search query.
        
        Args:
            terms: Search terms (minimum 1 required)
            date_range: Optional publication date constraints
            domain_filters: Research domain restrictions
            max_results: Maximum papers to return (1-1000)
            sort_criteria: Result ordering preferences
        
        Raises:
            InvalidSearchQueryError: If validation fails
        """
        # Convert to immutable tuples
        object.__setattr__(self, '_terms', tuple(terms))
        object.__setattr__(self, '_domain_filters', 
                          tuple(domain_filters or []))
        object.__setattr__(self, '_date_range', date_range)
        object.__setattr__(self, '_max_results', max_results)
        object.__setattr__(self, '_sort_criteria', 
                          sort_criteria or SortCriteria.RELEVANCE)
        
        # Validate after assignment
        self._validate()
    
    @property
    def terms(self) -> Tuple[str, ...]:
        """Immutable access to search terms."""
        return self._terms
    
    @property
    def date_range(self) -> Optional['DateRange']:
        """Optional publication date constraints."""
        return self._date_range
    
    @property
    def domain_filters(self) -> Tuple[str, ...]:
        """Research domain restrictions."""
        return self._domain_filters
    
    @property
    def max_results(self) -> int:
        """Maximum results to return."""
        return self._max_results
    
    @property
    def sort_criteria(self) -> 'SortCriteria':
        """Result ordering preferences."""
        return self._sort_criteria
```

### Comprehensive Validation

```python
    def _validate(self) -> None:
        """
        Comprehensive business rule validation.
        
        Educational Value: Shows how value objects enforce
        business constraints and prevent invalid states.
        """
        self._validate_search_terms()
        self._validate_date_range()
        self._validate_domain_filters()
        self._validate_max_results()
        self._validate_sort_criteria()
    
    def _validate_search_terms(self) -> None:
        """Validate search terms meet business requirements."""
        if not self._terms:
            raise InvalidSearchQueryError("At least one search term required")
        
        if len(self._terms) > MAX_SEARCH_TERMS:
            raise InvalidSearchQueryError(
                f"Too many search terms. Maximum: {MAX_SEARCH_TERMS}"
            )
        
        for term in self._terms:
            if not term or not term.strip():
                raise InvalidSearchQueryError("Empty search terms not allowed")
            
            if len(term) > MAX_TERM_LENGTH:
                raise InvalidSearchQueryError(
                    f"Search term too long: '{term[:50]}...'"
                )
            
            if not self._is_valid_search_term(term):
                raise InvalidSearchQueryError(
                    f"Invalid characters in search term: '{term}'"
                )
    
    def _validate_date_range(self) -> None:
        """Validate date range constraints."""
        if self._date_range is None:
            return
        
        if not self._date_range.is_valid():
            raise InvalidSearchQueryError("Invalid date range")
        
        # Academic papers don't exist before certain date
        if self._date_range.start_date < MIN_PUBLICATION_DATE:
            raise InvalidSearchQueryError(
                f"Publication date cannot be before {MIN_PUBLICATION_DATE}"
            )
        
        # Future dates don't make sense for existing papers
        if self._date_range.end_date > date.today():
            raise InvalidSearchQueryError(
                "End date cannot be in the future"
            )
    
    def _validate_max_results(self) -> None:
        """Validate result count limits."""
        if self._max_results < 1:
            raise InvalidSearchQueryError("Max results must be positive")
        
        if self._max_results > MAX_SEARCH_RESULTS:
            raise InvalidSearchQueryError(
                f"Max results too large. Limit: {MAX_SEARCH_RESULTS}"
            )
```

### Equality and Hashing

```python
    def __eq__(self, other) -> bool:
        """
        Value-based equality comparison.
        
        Educational Value: Demonstrates proper value object
        equality implementation based on all attributes.
        """
        if not isinstance(other, SearchQuery):
            return False
        
        return (
            self._terms == other._terms and
            self._date_range == other._date_range and
            self._domain_filters == other._domain_filters and
            self._max_results == other._max_results and
            self._sort_criteria == other._sort_criteria
        )
    
    def __hash__(self) -> int:
        """
        Hash based on all attributes for use in sets/dicts.
        
        Educational Value: Shows how immutable value objects
        can be safely used as dictionary keys or set members.
        """
        return hash((
            self._terms,
            self._date_range,
            self._domain_filters,
            self._max_results,
            self._sort_criteria
        ))
```

## 🏗️ Factory Methods and Builder Pattern

### Domain-Specific Factory Methods

```python
    @classmethod
    def for_medical_research(cls, 
                           primary_terms: List[str],
                           medical_domains: List[str] = None) -> 'SearchQuery':
        """
        Factory method for medical research queries.
        
        Educational Value: Shows how factory methods can
        encapsulate domain-specific query construction logic.
        """
        medical_domains = medical_domains or [
            "cardiology", "neurology", "physiology"
        ]
        
        return cls(
            terms=primary_terms,
            domain_filters=medical_domains,
            max_results=100,  # Medical research often needs more results
            sort_criteria=SortCriteria.PUBLICATION_DATE_DESC
        )
    
    @classmethod  
    def for_literature_review(cls,
                            topic: str,
                            time_window_years: int = 5) -> 'SearchQuery':
        """
        Factory method for literature review queries.
        
        Creates queries optimized for comprehensive literature reviews
        with appropriate time windows and result limits.
        """
        end_date = date.today()
        start_date = date(end_date.year - time_window_years, 1, 1)
        
        return cls(
            terms=[topic],
            date_range=DateRange(start_date, end_date),
            max_results=500,  # Literature reviews need comprehensive results
            sort_criteria=SortCriteria.CITATION_COUNT_DESC
        )
    
    @classmethod
    def from_yaml_config(cls, 
                        config_path: str,
                        override_terms: List[str] = None) -> 'SearchQuery':
        """
        Factory method creating queries from YAML configuration.
        
        Educational Value: Demonstrates integration with
        configuration-driven design patterns.
        """
        config = load_search_config(config_path)
        
        return cls(
            terms=override_terms or config.default_terms,
            date_range=config.default_date_range,
            domain_filters=config.domain_filters,
            max_results=config.max_results,
            sort_criteria=config.sort_criteria
        )
```

### Query Builder for Complex Construction

```python
class SearchQueryBuilder:
    """
    Builder pattern for complex query construction.
    
    Educational Value: Demonstrates builder pattern for
    objects with many optional parameters and complex validation.
    """
    
    def __init__(self):
        self._terms = []
        self._date_range = None
        self._domain_filters = []
        self._max_results = 50
        self._sort_criteria = SortCriteria.RELEVANCE
    
    def with_terms(self, *terms: str) -> 'SearchQueryBuilder':
        """Add search terms (fluent interface)."""
        self._terms.extend(terms)
        return self
    
    def with_date_range(self, 
                       start: date, 
                       end: date) -> 'SearchQueryBuilder':
        """Add date range constraint."""
        self._date_range = DateRange(start, end)
        return self
    
    def recent_papers(self, years: int = 2) -> 'SearchQueryBuilder':
        """Convenient method for recent papers."""
        end_date = date.today()
        start_date = date(end_date.year - years, 1, 1)
        return self.with_date_range(start_date, end_date)
    
    def in_domains(self, *domains: str) -> 'SearchQueryBuilder':
        """Add domain filters."""
        self._domain_filters.extend(domains)
        return self
    
    def limit_results(self, max_results: int) -> 'SearchQueryBuilder':
        """Set maximum results."""
        self._max_results = max_results
        return self
    
    def sort_by(self, criteria: SortCriteria) -> 'SearchQueryBuilder':
        """Set sort criteria."""
        self._sort_criteria = criteria
        return self
    
    def build(self) -> SearchQuery:
        """Build the final search query."""
        return SearchQuery(
            terms=self._terms,
            date_range=self._date_range,
            domain_filters=self._domain_filters,
            max_results=self._max_results,
            sort_criteria=self._sort_criteria
        )
```

## 🔍 Query Analysis and Transformation

### Query Complexity Analysis

```python
    def complexity_score(self) -> int:
        """
        Calculate query complexity for performance optimization.
        
        Educational Value: Shows how value objects can provide
        derived properties for system optimization decisions.
        """
        score = 0
        
        # Base complexity from term count
        score += len(self._terms) * 10
        
        # Additional complexity from filters
        if self._date_range:
            score += 5
        
        score += len(self._domain_filters) * 3
        
        # Complex sorting increases score
        if self._sort_criteria in [SortCriteria.CITATION_COUNT_DESC, 
                                  SortCriteria.RELEVANCE_ADVANCED]:
            score += 15
        
        # Large result sets are more complex
        if self._max_results > 100:
            score += 20
        
        return score
    
    def estimated_execution_time(self) -> float:
        """
        Estimate query execution time in seconds.
        
        Used for user feedback and system capacity planning.
        """
        complexity = self.complexity_score()
        base_time = 0.5  # Baseline execution time
        
        # Complexity multiplier
        multiplier = 1 + (complexity / 100)
        
        return base_time * multiplier
```

### Query Optimization Suggestions

```python
    def optimization_suggestions(self) -> List['OptimizationSuggestion']:
        """
        Suggest query optimizations for better performance.
        
        Educational Value: Shows how domain objects can
        provide intelligent suggestions based on business rules.
        """
        suggestions = []
        
        if len(self._terms) > 5:
            suggestions.append(
                OptimizationSuggestion(
                    type=SuggestionType.REDUCE_TERMS,
                    message="Consider reducing search terms for faster results",
                    impact=PerformanceImpact.MEDIUM
                )
            )
        
        if self._max_results > 200:
            suggestions.append(
                OptimizationSuggestion(
                    type=SuggestionType.LIMIT_RESULTS,
                    message="Large result sets may take longer to process",
                    impact=PerformanceImpact.HIGH
                )
            )
        
        if not self._date_range:
            suggestions.append(
                OptimizationSuggestion(
                    type=SuggestionType.ADD_DATE_FILTER,
                    message="Adding date range can significantly improve performance",
                    impact=PerformanceImpact.HIGH
                )
            )
        
        return suggestions
```

## 🎓 Educational Value and Design Patterns

### Value Object Pattern Demonstration

**Key Characteristics Implemented:**
1. **Immutability**: Cannot be modified after creation
2. **Value Equality**: Equality based on attributes, not identity
3. **Self-Validation**: Ensures object is always in valid state
4. **Side-Effect Free**: Methods don't modify state

**Educational Benefits:**
- Shows proper implementation of Domain-Driven Design value objects
- Demonstrates validation strategies for complex business rules
- Illustrates factory method and builder patterns
- Provides examples of defensive programming techniques

### SOLID Principles Applied

1. **Single Responsibility**: Only responsible for search query representation
2. **Open/Closed**: Extensible through factory methods without modification
3. **Liskov Substitution**: All SearchQuery instances behave consistently
4. **Interface Segregation**: Provides focused interface for search operations
5. **Dependency Inversion**: Depends on abstractions (SortCriteria, DateRange)

## 🔗 Related Concepts

- [[Research-Paper-Entity]]: The target of search operations
- [[Keyword-Config-ValueObject]]: Configuration driving search strategies
- [[Execute-Keyword-Search-UseCase]]: Primary consumer of search queries
- [[Paper-Source-Port]]: Infrastructure interface for external search
- [[Domain-Services]]: Services that operate on search queries

## 🚀 Usage Examples

### Basic Research Query

```python
# Simple academic research query
query = SearchQuery(
    terms=["machine learning", "healthcare"],
    max_results=50
)

# Medical research with domain filtering
medical_query = SearchQuery.for_medical_research(
    primary_terms=["heart rate variability", "stress"],
    medical_domains=["cardiology", "psychology"]
)
```

### Complex Literature Review Query

```python
# Comprehensive literature review using builder
review_query = (SearchQueryBuilder()
    .with_terms("traumatic brain injury", "cognitive assessment")
    .recent_papers(years=3)
    .in_domains("neurology", "psychology", "rehabilitation")
    .limit_results(300)
    .sort_by(SortCriteria.CITATION_COUNT_DESC)
    .build())
```

### Configuration-Driven Query

```python
# Load from YAML configuration
config_query = SearchQuery.from_yaml_config(
    "config/hrv_medical_research.yaml",
    override_terms=["heart rate variability", "exercise"]
)
```

---

*The SearchQuery value object demonstrates how proper domain modeling creates robust, maintainable software that accurately represents business concepts while providing excellent developer experience through clear APIs and comprehensive validation.*

#domain #value-object #search #validation #educational
