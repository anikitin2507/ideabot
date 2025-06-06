"""Configuration module for the Decision Bot."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Configuration settings for the bot."""

    # Telegram Bot Token
    bot_token: str = Field(..., env="BOT_TOKEN")

    # OpenAI API Key
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")

    # OpenAI Model Configuration
    openai_model: str = Field(default="gpt-4.1-mini", env="OPENAI_MODEL")

    # Database Configuration (for v1.1)
    database_url: str | None = Field(default=None, env="DATABASE_URL")

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Bot Configuration
    max_options: int = Field(default=5, env="MAX_OPTIONS")
    response_timeout: int = Field(default=30, env="RESPONSE_TIMEOUT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
