"""
Configuration settings for the Astronaut Health Simulation Engine.
"""

import os
from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    host: str = "localhost"
    port: int = 5432
    database: str = "ahse_db"
    username: str = "ahse_user"
    password: str = "ahse_password"
    
    @property
    def connection_string(self) -> str:
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class APIConfig:
    """API configuration settings."""
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False
    cors_origins: list = None
    
    def __post_init__(self):
        if self.cors_origins is None:
            self.cors_origins = ["*"]


@dataclass
class DashboardConfig:
    """Dashboard configuration settings."""
    host: str = "localhost"
    port: int = 8501
    theme: str = "light"
    layout: str = "wide"


@dataclass
class SimulationConfig:
    """Simulation engine configuration."""
    default_accuracy_threshold: float = 0.85
    max_simulation_days: int = 1000
    prediction_interval_days: int = 7
    confidence_threshold: float = 0.7
    
    # Model parameters
    muscle_atrophy_rate: float = 0.001
    bone_loss_rate: float = 0.0008
    cardiovascular_decline_rate: float = 0.0002
    immune_decline_rate: float = 0.0001
    cognitive_decline_rate: float = 0.0001
    dna_damage_rate: float = 0.0001
    stress_accumulation_rate: float = 0.0001
    sleep_decline_rate: float = 0.00005


@dataclass
class RecommendationConfig:
    """Recommendation engine configuration."""
    max_recommendations: int = 10
    benefit_weight: float = 0.4
    feasibility_weight: float = 0.3
    cost_weight: float = 0.2
    timeline_weight: float = 0.1
    
    # Risk thresholds
    high_risk_threshold: float = 0.7
    medium_risk_threshold: float = 0.4
    low_risk_threshold: float = 0.1


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: str = "logs/ahse.log"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5


class Config:
    """Main configuration class."""
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.api = APIConfig()
        self.dashboard = DashboardConfig()
        self.simulation = SimulationConfig()
        self.recommendation = RecommendationConfig()
        self.logging = LoggingConfig()
        
        # Load environment variables
        self._load_env_vars()
    
    def _load_env_vars(self):
        """Load configuration from environment variables."""
        # Database
        self.database.host = os.getenv("DB_HOST", self.database.host)
        self.database.port = int(os.getenv("DB_PORT", self.database.port))
        self.database.database = os.getenv("DB_NAME", self.database.database)
        self.database.username = os.getenv("DB_USER", self.database.username)
        self.database.password = os.getenv("DB_PASSWORD", self.database.password)
        
        # API
        self.api.host = os.getenv("API_HOST", self.api.host)
        self.api.port = int(os.getenv("API_PORT", self.api.port))
        self.api.debug = os.getenv("API_DEBUG", "false").lower() == "true"
        
        # Dashboard
        self.dashboard.host = os.getenv("DASHBOARD_HOST", self.dashboard.host)
        self.dashboard.port = int(os.getenv("DASHBOARD_PORT", self.dashboard.port))
        
        # Logging
        self.logging.level = os.getenv("LOG_LEVEL", self.logging.level)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "database": {
                "host": self.database.host,
                "port": self.database.port,
                "database": self.database.database,
                "username": self.database.username,
                "password": "***"  # Hide password
            },
            "api": {
                "host": self.api.host,
                "port": self.api.port,
                "debug": self.api.debug,
                "cors_origins": self.api.cors_origins
            },
            "dashboard": {
                "host": self.dashboard.host,
                "port": self.dashboard.port,
                "theme": self.dashboard.theme,
                "layout": self.dashboard.layout
            },
            "simulation": {
                "default_accuracy_threshold": self.simulation.default_accuracy_threshold,
                "max_simulation_days": self.simulation.max_simulation_days,
                "prediction_interval_days": self.simulation.prediction_interval_days,
                "confidence_threshold": self.simulation.confidence_threshold
            },
            "recommendation": {
                "max_recommendations": self.recommendation.max_recommendations,
                "benefit_weight": self.recommendation.benefit_weight,
                "feasibility_weight": self.recommendation.feasibility_weight,
                "cost_weight": self.recommendation.cost_weight,
                "timeline_weight": self.recommendation.timeline_weight
            },
            "logging": {
                "level": self.logging.level,
                "format": self.logging.format,
                "file_path": self.logging.file_path
            }
        }


# Global configuration instance
config = Config()


def get_config() -> Config:
    """Get the global configuration instance."""
    return config


def update_config(**kwargs) -> None:
    """Update configuration settings."""
    global config
    
    for section, values in kwargs.items():
        if hasattr(config, section):
            section_config = getattr(config, section)
            for key, value in values.items():
                if hasattr(section_config, key):
                    setattr(section_config, key, value)


# Environment-specific configurations
class DevelopmentConfig(Config):
    """Development environment configuration."""
    
    def __init__(self):
        super().__init__()
        self.api.debug = True
        self.logging.level = "DEBUG"
        self.simulation.default_accuracy_threshold = 0.8


class ProductionConfig(Config):
    """Production environment configuration."""
    
    def __init__(self):
        super().__init__()
        self.api.debug = False
        self.logging.level = "WARNING"
        self.simulation.default_accuracy_threshold = 0.9


class TestingConfig(Config):
    """Testing environment configuration."""
    
    def __init__(self):
        super().__init__()
        self.api.debug = True
        self.logging.level = "ERROR"
        self.database.database = "ahse_test_db"
        self.simulation.default_accuracy_threshold = 0.7


def get_environment_config(env: str = None) -> Config:
    """Get configuration for specific environment."""
    if env is None:
        env = os.getenv("ENVIRONMENT", "development")
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    config_class = config_map.get(env, DevelopmentConfig)
    return config_class()

