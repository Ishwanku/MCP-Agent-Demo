"""
Configuration settings for the MCP Agent.

This module provides configuration management for the MCP agent system using Pydantic.
It handles loading settings from environment variables and .env files.

Key Features:
- Environment variable loading
- .env file support
- Type validation
- Default values
- Case-sensitive settings

Example:
    ```python
    from mcp.core.config import settings
    
    # Access settings
    port = settings.DEMO_AGENT_PORT
    api_key = settings.DEMO_AGENT_API_KEY
    outlook_path = settings.OUTLOOK_PATH
    ```

Dependencies:
    - pydantic_settings: For settings management
    - python-dotenv: For .env file support
"""

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Settings for the MCP Agent.
    
    This class defines all configuration settings for the MCP agent system.
    It uses Pydantic for validation and type checking.
    
    Attributes:
        DEMO_AGENT_PORT: Port to run the demo agent on
        DEMO_AGENT_API_KEY: API key for authentication
        OUTLOOK_PATH: Path to the Outlook executable
        LOG_LEVEL: Logging level for the application
        
    Configuration:
        The settings can be configured through:
        - Environment variables
        - .env file
        - Default values (if not specified)
    """
    
    # Demo Agent settings
    DEMO_AGENT_PORT: int = 8000
    DEMO_AGENT_API_KEY: Optional[str] = None
    
    # Outlook settings
    OUTLOOK_PATH: Optional[str] = None
    
    # Logging settings
    LOG_LEVEL: str = "INFO"
    
    class Config:
        """Pydantic configuration.
        
        This class configures how Pydantic loads and validates settings.
        
        Attributes:
            env_file: Path to the .env file
            case_sensitive: Whether to be case-sensitive with environment variables
        """
        env_file = ".env"
        case_sensitive = True

# Create a global settings instance
settings = Settings() 