import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

class Settings(BaseSettings):
    """
    Application configuration class using Pydantic Settings Management
    Supports different environment configurations
    """
    # Database Configuration
    MONGODB_STRING: str

    # Model config to load environment variables
    model_config = SettingsConfigDict(
        env_file=".env",  # Default env file
        env_file_encoding="utf-8",
        extra="ignore"  # Ignore extra environment variables
    )

    # Method to load specific environment configuration
    @classmethod
    def get_settings(cls, env_file: str = ".env"):
        """
        Load settings from a specific environment file
        
        :param env_file: Path to the environment configuration file
        :return: Configured Settings instance
        """
        # Expand environment variables in .env file
        load_dotenv(env_file)
        return cls()

# Example of dynamic environment loading
def get_environment_settings():
    """
    Dynamically load environment settings based on deployment context
    
    :return: Configured Settings instance
    """
    # Detect environment
    env = os.getenv("ENV", "development")
    
    # Load appropriate environment file
    if env == "production":
        return Settings.get_settings(".env.production")
    else:
        return Settings.get_settings(".env")
