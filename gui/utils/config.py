"""
Flask Application Configuration Module

This module provides configuration management for the Research Paper Aggregator GUI.
It demonstrates proper configuration patterns for academic web applications.

Educational Notes:
- Configuration as Code: External configuration for different environments
- Security Best Practices: Secure handling of sensitive configuration
- Environment Separation: Clear distinction between dev/test/production
- Academic Standards: Configuration suited for research environments

Design Patterns Applied:
- Strategy Pattern: Different configurations for different environments
- Factory Pattern: Configuration creation based on environment
- Singleton Pattern: Single configuration instance per environment
"""

import os
from typing import Dict, Any


class Config:
    """
    Base configuration class with common settings.

    Educational Notes:
    - Inheritance: Base class provides common configuration
    - Environment Variables: Uses OS environment for deployment flexibility
    - Security: Secret key management and secure defaults
    """

    # Flask core configuration
    SECRET_KEY = (
        os.environ.get("SECRET_KEY") or "academic-research-development-key-2025"
    )

    # Academic application settings
    APPLICATION_NAME = "Research Paper Aggregator"
    APPLICATION_VERSION = "1.0.0"
    APPLICATION_DESCRIPTION = "Professional GUI for Academic Research"

    # UI/UX configuration for academic users
    UI_CONFIG = {
        "theme": "academic-professional",
        "accessibility_enabled": True,
        "progressive_disclosure": True,
        "user_journey_tracking": True,
        "citation_formats": ["APA", "MLA", "Chicago", "Harvard"],
        "visualization_types": ["sunburst", "treemap", "network", "timeline"],
        "evidence_quality_metrics": ["confidence", "relevance", "strength", "context"],
        "dashboard_widgets": [
            "session_summary",
            "recent_activity",
            "progress_metrics",
            "timeline",
            "quick_actions",
        ],
    }

    # File paths and directories
    UPLOAD_FOLDER = "uploads"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file uploads

    # Academic research configuration
    RESEARCH_CONFIG = {
        "max_search_results": 100,
        "default_quality_threshold": 0.7,
        "session_timeout_minutes": 120,  # 2 hours for research sessions
        "auto_save_interval_seconds": 300,  # 5 minutes
        "max_evidence_per_concept": 50,
        "citation_cache_size": 1000,
    }

    # Performance settings optimized for academic use
    PERFORMANCE_CONFIG = {
        "enable_caching": True,
        "cache_timeout": 3600,  # 1 hour
        "compress_responses": True,
        "lazy_load_visualizations": True,
        "pagination_size": 25,
    }


class DevelopmentConfig(Config):
    """
    Development environment configuration.

    Educational Notes:
    - Development Features: Debug mode, detailed logging, hot reload
    - Academic Development: Settings optimized for research tool development
    - Security: Relaxed settings appropriate for development only
    """

    DEBUG = True
    TESTING = False

    # Development-specific settings
    EXPLAIN_TEMPLATE_LOADING = True

    # Logging configuration for development
    LOG_LEVEL = "DEBUG"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Development database (if using one)
    DATABASE_URL = os.environ.get("DEV_DATABASE_URL") or "sqlite:///dev_research.db"


class TestingConfig(Config):
    """
    Testing environment configuration.

    Educational Notes:
    - Test Isolation: Settings that ensure test independence
    - Academic Testing: Configuration for research tool testing
    - Mock Services: Using test doubles for external dependencies
    """

    TESTING = True
    DEBUG = False

    # Testing-specific settings
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing

    # Test database
    DATABASE_URL = "sqlite:///:memory:"  # In-memory database for tests

    # Reduced timeouts for faster tests
    RESEARCH_CONFIG = Config.RESEARCH_CONFIG.copy()
    RESEARCH_CONFIG.update(
        {
            "session_timeout_minutes": 5,
            "auto_save_interval_seconds": 10,
            "max_evidence_per_concept": 10,
        }
    )


class ProductionConfig(Config):
    """
    Production environment configuration.

    Educational Notes:
    - Security First: Production-hardened security settings
    - Performance: Optimized for academic production environments
    - Monitoring: Enhanced logging and error tracking
    """

    DEBUG = False
    TESTING = False

    # Production security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

    # Production logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Production database
    DATABASE_URL = os.environ.get("DATABASE_URL")

    # Enhanced performance for production
    PERFORMANCE_CONFIG = Config.PERFORMANCE_CONFIG.copy()
    PERFORMANCE_CONFIG.update(
        {
            "cache_timeout": 7200,  # 2 hours in production
            "pagination_size": 50,  # Larger pages for better performance
        }
    )


class AcademicInstitutionConfig(ProductionConfig):
    """
    Configuration for academic institution deployment.

    Educational Notes:
    - Institutional Integration: Settings for university/research environments
    - Compliance: Configuration meeting academic institution requirements
    - Scalability: Settings for multi-user academic environments
    """

    # Institution-specific settings
    INSTITUTION_NAME = os.environ.get("INSTITUTION_NAME", "Academic Institution")
    INSTITUTION_LOGO = os.environ.get("INSTITUTION_LOGO_URL")

    # Academic authentication (if using SSO)
    SAML_ENABLED = os.environ.get("SAML_ENABLED", "False").lower() == "true"
    LDAP_ENABLED = os.environ.get("LDAP_ENABLED", "False").lower() == "true"

    # Enhanced research configuration for institutions
    RESEARCH_CONFIG = ProductionConfig.RESEARCH_CONFIG.copy()
    RESEARCH_CONFIG.update(
        {
            "max_search_results": 200,  # Higher limits for institutional use
            "session_timeout_minutes": 240,  # 4 hours for extended research
            "max_evidence_per_concept": 100,
            "citation_cache_size": 5000,
        }
    )

    # Multi-user features
    MULTIUSER_CONFIG = {
        "enable_user_accounts": True,
        "enable_collaboration": True,
        "enable_sharing": True,
        "enable_export_restrictions": False,
    }


# Configuration factory
config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "academic": AcademicInstitutionConfig,
}


def get_config(config_name: str = None) -> Config:
    """
    Factory function to get configuration by environment name.

    Args:
        config_name: Environment name ('development', 'testing', 'production', 'academic')

    Returns:
        Configuration instance for the specified environment

    Educational Notes:
    - Factory Pattern: Creates appropriate configuration based on environment
    - Default Handling: Sensible defaults for development
    - Type Safety: Returns typed configuration objects
    """

    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    config_class = config_by_name.get(config_name, DevelopmentConfig)
    return config_class()


def validate_config(config: Config) -> Dict[str, Any]:
    """
    Validate configuration settings for academic application requirements.

    Args:
        config: Configuration instance to validate

    Returns:
        Dictionary with validation results

    Educational Notes:
    - Configuration Validation: Ensures settings meet application requirements
    - Academic Standards: Validates academic-specific configuration
    - Error Prevention: Catches configuration issues early
    """

    validation_results = {"valid": True, "warnings": [], "errors": []}

    # Validate required settings
    if not config.SECRET_KEY or config.SECRET_KEY == "your-secret-key-here":
        validation_results["errors"].append(
            "SECRET_KEY must be set to a secure value in production"
        )
        validation_results["valid"] = False

    # Validate academic configuration
    if config.RESEARCH_CONFIG["max_search_results"] < 10:
        validation_results["warnings"].append(
            "max_search_results is very low - may limit research effectiveness"
        )

    if config.RESEARCH_CONFIG["session_timeout_minutes"] < 30:
        validation_results["warnings"].append(
            "session_timeout_minutes is low - may interrupt research sessions"
        )

    # Validate UI configuration
    required_citation_formats = ["APA", "MLA"]
    if not all(
        fmt in config.UI_CONFIG["citation_formats"] for fmt in required_citation_formats
    ):
        validation_results["errors"].append(
            "APA and MLA citation formats are required for academic use"
        )
        validation_results["valid"] = False

    return validation_results
