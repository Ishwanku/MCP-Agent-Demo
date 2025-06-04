"""
Configuration management for the Demo MCP Agent.

This module centralizes configuration using Pydantic settings.
It handles environment variables and provides type-safe, validated settings.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Main settings class for the Demo MCP Agent."""
    
    model_config = SettingsConfigDict(env_prefix="")

    # Demo Agent settings
    DEMO_AGENT_PORT: int = Field(default=8000)
    DEMO_AGENT_API_KEY: str = Field(default="demo-secret-key")

    # Logging settings
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

# Create global settings instance
settings = Settings()

# Export settings for use in other modules
DEMO_AGENT_PORT = settings.DEMO_AGENT_PORT
DEMO_AGENT_API_KEY = settings.DEMO_AGENT_API_KEY

__all__ = [
    "settings",
    "DEMO_AGENT_PORT",
    "DEMO_AGENT_API_KEY"
]
