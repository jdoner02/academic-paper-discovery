"""
Tests for Keyword Configuration Value Objects.

This test module demonstrates comprehensive testing of domain value objects,
including configuration loading, validation, and business logic testing.
It shows TDD principles applied to configuration-driven functionality.

Educational Notes:
- Tests value object immutability and validation
- Tests factory method for loading configuration
- Tests business logic encapsulated in value objects
- Demonstrates edge case testing for configuration systems

Testing Patterns:
- Arrange-Act-Assert: Clear test structure
- Given-When-Then: BDD-style test organization
- Edge Case Testing: Invalid configurations and boundary conditions
- Fixture Usage: Reusable test data setup
"""

import pytest
import tempfile
import yaml
from pathlib import Path
from datetime import datetime

from src.domain.value_objects.keyword_config import (
    KeywordConfig,
    SearchStrategy,
    SearchConfiguration,
)


class TestSearchStrategy:
    """Test SearchStrategy value object creation and behavior."""

    def test_create_valid_search_strategy(self):
        """Test creating a valid search strategy with required fields."""
        # Given: Valid strategy configuration
        strategy = SearchStrategy(
            name="test_strategy",
            description="Test strategy for unit testing",
            required_terms=["heart rate variability"],
            optional_terms=["HRV", "RMSSD"],
            max_results=25,
        )

        # Then: Strategy is created successfully
        assert strategy.name == "test_strategy"
        assert strategy.description == "Test strategy for unit testing"
        assert strategy.required_terms == ["heart rate variability"]
        assert strategy.optional_terms == ["HRV", "RMSSD"]
        assert strategy.max_results == 25

    def test_strategy_immutability(self):
        """Test that SearchStrategy is immutable after creation."""
        # Given: A search strategy
        strategy = SearchStrategy(
            name="test_strategy",
            description="Test description",
            required_terms=["term1"],
        )

        # When/Then: Attempting to modify raises AttributeError
        with pytest.raises(AttributeError):
            strategy.name = "modified_name"

    def test_strategy_validation_empty_name(self):
        """Test validation rejects empty strategy name."""
        # When/Then: Creating strategy with empty name raises ValueError
        with pytest.raises(ValueError, match="Search strategy must have a name"):
            SearchStrategy(
                name="", description="Test description", required_terms=["term1"]
            )

    def test_strategy_validation_empty_description(self):
        """Test validation rejects empty description."""
        # When/Then: Creating strategy with empty description raises ValueError
        with pytest.raises(ValueError, match="Search strategy must have a description"):
            SearchStrategy(
                name="test_strategy", description="", required_terms=["term1"]
            )

    def test_strategy_validation_empty_required_terms(self):
        """Test validation rejects empty required terms."""
        # When/Then: Creating strategy with no required terms raises ValueError
        with pytest.raises(
            ValueError, match="Search strategy must have at least one required term"
        ):
            SearchStrategy(
                name="test_strategy", description="Test description", required_terms=[]
            )

    def test_strategy_validation_negative_max_results(self):
        """Test validation rejects negative max results."""
        # When/Then: Creating strategy with negative max_results raises ValueError
        with pytest.raises(ValueError, match="max_results must be positive"):
            SearchStrategy(
                name="test_strategy",
                description="Test description",
                required_terms=["term1"],
                max_results=-1,
            )

    def test_get_all_terms(self):
        """Test getting all terms from all categories."""
        # Given: Strategy with terms in multiple categories
        strategy = SearchStrategy(
            name="comprehensive_strategy",
            description="Strategy with all term types",
            required_terms=["hrv", "required"],
            optional_terms=["optional1", "optional2"],
            alternative_terms=["alt1"],
            technology_terms=["tech1", "tech2"],
            clinical_terms=["clinical1"],
        )

        # When: Getting all terms
        all_terms = strategy.get_all_terms()

        # Then: All unique terms are returned
        expected_terms = [
            "hrv",
            "required",
            "optional1",
            "optional2",
            "alt1",
            "tech1",
            "tech2",
            "clinical1",
        ]
        assert len(all_terms) == len(expected_terms)
        for term in expected_terms:
            assert term in all_terms

    def test_get_all_terms_removes_duplicates(self):
        """Test that get_all_terms removes duplicate terms."""
        # Given: Strategy with duplicate terms across categories
        strategy = SearchStrategy(
            name="duplicate_strategy",
            description="Strategy with duplicate terms",
            required_terms=["hrv", "duplicate"],
            optional_terms=["duplicate", "optional"],
            alternative_terms=["hrv"],
        )

        # When: Getting all terms
        all_terms = strategy.get_all_terms()

        # Then: Duplicates are removed
        assert len(all_terms) == 3  # hrv, duplicate, optional
        assert "hrv" in all_terms
        assert "duplicate" in all_terms
        assert "optional" in all_terms

    def test_build_search_query_required_only(self):
        """Test building search query with only required terms."""
        # Given: Strategy with only required terms
        strategy = SearchStrategy(
            name="simple_strategy",
            description="Simple strategy",
            required_terms=["heart rate variability", "HRV"],
        )

        # When: Building search query
        query = strategy.build_search_query()

        # Then: Query contains properly formatted required terms
        assert '"heart rate variability"' in query
        assert '"HRV"' in query
        assert " AND " in query

    def test_build_search_query_with_optional_terms(self):
        """Test building search query with optional terms."""
        # Given: Strategy with required and optional terms
        strategy = SearchStrategy(
            name="complex_strategy",
            description="Complex strategy",
            required_terms=["heart rate variability"],
            optional_terms=["RMSSD", "pNN50"],
        )

        # When: Building search query
        query = strategy.build_search_query()

        # Then: Query contains required terms and optional terms with OR logic
        assert '"heart rate variability"' in query
        assert '"RMSSD"' in query
        assert '"pNN50"' in query
        assert " AND " in query
        assert " OR " in query


class TestSearchConfiguration:
    """Test SearchConfiguration value object creation and validation."""

    def test_create_valid_search_configuration(self):
        """Test creating valid search configuration."""
        # Given: Valid configuration parameters
        config = SearchConfiguration(
            default_strategy="broad_hrv",
            citation_threshold=5,
            start_year=2020,
            end_year=2025,
            exclude_terms=["animal study"],
            include_preprints=True,
            max_concurrent_searches=3,
        )

        # Then: Configuration is created successfully
        assert config.default_strategy == "broad_hrv"
        assert config.citation_threshold == 5
        assert config.start_year == 2020
        assert config.end_year == 2025
        assert config.exclude_terms == ["animal study"]
        assert config.include_preprints is True
        assert config.max_concurrent_searches == 3

    def test_configuration_validation_negative_citation_threshold(self):
        """Test validation rejects negative citation threshold."""
        # When/Then: Creating config with negative threshold raises ValueError
        with pytest.raises(ValueError, match="Citation threshold cannot be negative"):
            SearchConfiguration(
                default_strategy="test",
                citation_threshold=-1,
                start_year=2020,
                end_year=2025,
            )

    def test_configuration_validation_invalid_year_range(self):
        """Test validation rejects invalid year range."""
        # When/Then: Creating config with start year after end year raises ValueError
        with pytest.raises(ValueError, match="Start year cannot be after end year"):
            SearchConfiguration(
                default_strategy="test",
                citation_threshold=0,
                start_year=2025,
                end_year=2020,
            )

    def test_configuration_validation_future_end_year(self):
        """Test validation rejects unrealistic future end year."""
        # Given: Current year plus more than one year
        future_year = datetime.now().year + 2

        # When/Then: Creating config with far future end year raises ValueError
        with pytest.raises(
            ValueError, match="End year cannot be more than one year in the future"
        ):
            SearchConfiguration(
                default_strategy="test",
                citation_threshold=0,
                start_year=2020,
                end_year=future_year,
            )

    def test_configuration_validation_zero_concurrent_searches(self):
        """Test validation rejects zero concurrent searches."""
        # When/Then: Creating config with zero concurrent searches raises ValueError
        with pytest.raises(
            ValueError, match="max_concurrent_searches must be positive"
        ):
            SearchConfiguration(
                default_strategy="test",
                citation_threshold=0,
                start_year=2020,
                end_year=2025,
                max_concurrent_searches=0,
            )


class TestKeywordConfig:
    """Test KeywordConfig value object and YAML loading functionality."""

    @pytest.fixture
    def sample_yaml_config(self):
        """Fixture providing sample YAML configuration data."""
        return {
            "hrv_core_terms": ["heart rate variability", "HRV"],
            "medical_conditions": ["TBI", "concussion"],
            "methodologies": ["ECG", "PPG"],
            "clinical_applications": ["prognosis", "biomarker"],
            "search_strategies": {
                "broad_hrv": {
                    "description": "Broad HRV research",
                    "required_terms": ["heart rate variability"],
                    "optional_terms": ["HRV"],
                    "max_results": 50,
                },
                "tbi_focused": {
                    "description": "TBI-focused HRV research",
                    "required_terms": ["heart rate variability", "TBI"],
                    "max_results": 30,
                },
            },
            "search_configuration": {
                "default_strategy": "broad_hrv",
                "citation_threshold": 5,
                "publication_date_range": {"start_year": 2020, "end_year": 2025},
                "exclude_terms": ["animal study"],
                "include_preprints": True,
                "max_concurrent_searches": 3,
            },
        }

    def test_create_valid_keyword_config(self, sample_yaml_config):
        """Test creating valid KeywordConfig from components."""
        # Given: Valid configuration components
        strategies = {}
        for name, strategy_data in sample_yaml_config["search_strategies"].items():
            strategies[name] = SearchStrategy(
                name=name,
                description=strategy_data["description"],
                required_terms=strategy_data["required_terms"],
                optional_terms=strategy_data.get("optional_terms", []),
                max_results=strategy_data["max_results"],
            )

        search_config_data = sample_yaml_config["search_configuration"]
        search_config = SearchConfiguration(
            default_strategy=search_config_data["default_strategy"],
            citation_threshold=search_config_data["citation_threshold"],
            start_year=search_config_data["publication_date_range"]["start_year"],
            end_year=search_config_data["publication_date_range"]["end_year"],
            exclude_terms=search_config_data["exclude_terms"],
            include_preprints=search_config_data["include_preprints"],
            max_concurrent_searches=search_config_data["max_concurrent_searches"],
        )

        # When: Creating KeywordConfig
        config = KeywordConfig(
            hrv_core_terms=sample_yaml_config["hrv_core_terms"],
            medical_conditions=sample_yaml_config["medical_conditions"],
            methodologies=sample_yaml_config["methodologies"],
            clinical_applications=sample_yaml_config["clinical_applications"],
            search_strategies=strategies,
            search_configuration=search_config,
        )

        # Then: Configuration is created successfully
        assert config.hrv_core_terms == ["heart rate variability", "HRV"]
        assert config.medical_conditions == ["TBI", "concussion"]
        assert len(config.search_strategies) == 2
        assert "broad_hrv" in config.search_strategies
        assert "tbi_focused" in config.search_strategies

    def test_load_from_yaml_file(self, sample_yaml_config):
        """Test loading KeywordConfig from YAML file."""
        # Given: Temporary YAML file with configuration
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_yaml_config, f)
            temp_path = Path(f.name)

        try:
            # When: Loading configuration from file
            config = KeywordConfig.from_yaml_file(temp_path)

            # Then: Configuration is loaded correctly
            assert config.hrv_core_terms == ["heart rate variability", "HRV"]
            assert config.medical_conditions == ["TBI", "concussion"]
            assert len(config.search_strategies) == 2
            assert config.search_configuration.default_strategy == "broad_hrv"
            assert config.search_configuration.citation_threshold == 5
        finally:
            # Cleanup: Remove temporary file
            temp_path.unlink()

    def test_load_from_nonexistent_file(self):
        """Test loading from nonexistent file raises appropriate error."""
        # Given: Path to nonexistent file
        nonexistent_path = Path("/nonexistent/config.yaml")

        # When/Then: Loading raises FileNotFoundError
        with pytest.raises(FileNotFoundError, match="Configuration file not found"):
            KeywordConfig.from_yaml_file(nonexistent_path)

    def test_load_from_invalid_yaml(self):
        """Test loading from invalid YAML raises appropriate error."""
        # Given: Temporary file with invalid YAML
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("invalid: yaml: content: [")
            temp_path = Path(f.name)

        try:
            # When/Then: Loading raises ValueError
            with pytest.raises(ValueError, match="Invalid YAML configuration"):
                KeywordConfig.from_yaml_file(temp_path)
        finally:
            # Cleanup: Remove temporary file
            temp_path.unlink()

    def test_get_strategy_by_name(self, sample_yaml_config):
        """Test getting specific strategy by name."""
        # Given: KeywordConfig with multiple strategies
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_yaml_config, f)
            temp_path = Path(f.name)

        try:
            config = KeywordConfig.from_yaml_file(temp_path)

            # When: Getting strategy by name
            strategy = config.get_strategy("tbi_focused")

            # Then: Correct strategy is returned
            assert strategy.name == "tbi_focused"
            assert strategy.description == "TBI-focused HRV research"
            assert "heart rate variability" in strategy.required_terms
            assert "TBI" in strategy.required_terms
        finally:
            temp_path.unlink()

    def test_get_default_strategy(self, sample_yaml_config):
        """Test getting default strategy when no name specified."""
        # Given: KeywordConfig with default strategy
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_yaml_config, f)
            temp_path = Path(f.name)

        try:
            config = KeywordConfig.from_yaml_file(temp_path)

            # When: Getting strategy without specifying name
            strategy = config.get_strategy()

            # Then: Default strategy is returned
            assert strategy.name == "broad_hrv"
            assert strategy.description == "Broad HRV research"
        finally:
            temp_path.unlink()

    def test_get_nonexistent_strategy(self, sample_yaml_config):
        """Test getting nonexistent strategy raises appropriate error."""
        # Given: KeywordConfig with known strategies
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_yaml_config, f)
            temp_path = Path(f.name)

        try:
            config = KeywordConfig.from_yaml_file(temp_path)

            # When/Then: Getting nonexistent strategy raises ValueError
            with pytest.raises(ValueError, match="Strategy 'nonexistent' not found"):
                config.get_strategy("nonexistent")
        finally:
            temp_path.unlink()

    def test_get_all_terms(self, sample_yaml_config):
        """Test getting all terms from all categories."""
        # Given: KeywordConfig with terms in multiple categories
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_yaml_config, f)
            temp_path = Path(f.name)

        try:
            config = KeywordConfig.from_yaml_file(temp_path)

            # When: Getting all terms
            all_terms = config.get_all_terms()

            # Then: All unique terms from all categories are returned
            expected_terms = [
                "heart rate variability",
                "HRV",
                "TBI",
                "concussion",
                "ECG",
                "PPG",
                "prognosis",
                "biomarker",
            ]
            assert len(all_terms) == len(expected_terms)
            for term in expected_terms:
                assert term in all_terms
        finally:
            temp_path.unlink()

    def test_list_strategies(self, sample_yaml_config):
        """Test listing available strategy names."""
        # Given: KeywordConfig with multiple strategies
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_yaml_config, f)
            temp_path = Path(f.name)

        try:
            config = KeywordConfig.from_yaml_file(temp_path)

            # When: Listing strategies
            strategies = config.list_strategies()

            # Then: All strategy names are returned
            assert len(strategies) == 2
            assert "broad_hrv" in strategies
            assert "tbi_focused" in strategies
        finally:
            temp_path.unlink()

    def test_validation_empty_hrv_terms(self, sample_yaml_config):
        """Test validation rejects empty HRV core terms."""
        # Given: Configuration with empty HRV core terms
        sample_yaml_config["hrv_core_terms"] = []

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_yaml_config, f)
            temp_path = Path(f.name)

        try:
            # When/Then: Loading raises ValueError
            with pytest.raises(ValueError, match="HRV core terms cannot be empty"):
                KeywordConfig.from_yaml_file(temp_path)
        finally:
            temp_path.unlink()

    def test_validation_missing_default_strategy(self, sample_yaml_config):
        """Test validation rejects when default strategy doesn't exist."""
        # Given: Configuration with invalid default strategy
        sample_yaml_config["search_configuration"][
            "default_strategy"
        ] = "nonexistent_strategy"

        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            yaml.dump(sample_yaml_config, f)
            temp_path = Path(f.name)

        try:
            # When/Then: Loading raises ValueError
            with pytest.raises(
                ValueError, match="Default strategy 'nonexistent_strategy' not found"
            ):
                KeywordConfig.from_yaml_file(temp_path)
        finally:
            temp_path.unlink()
