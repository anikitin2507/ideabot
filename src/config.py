"""Configuration module for the Decision Bot."""

import sys
from typing import Any

import structlog
from pydantic import Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

logger = structlog.get_logger()


class Config(BaseSettings):
    """Configuration settings for the bot."""

    # Telegram Bot Token
    bot_token: str = Field(..., env="BOT_TOKEN", description="Telegram Bot Token from @BotFather")

    # LLM API Configuration
    api_type: str = Field(default="openrouter", env="API_TYPE")
    api_key: str = Field(..., env="API_KEY", description="API Key (OpenRouter or OpenAI)")
    api_base: str = Field(default="https://openrouter.ai/api/v1", env="API_BASE", description="API Base URL")
    
    # Model Configuration
    model: str = Field(default="gpt-4.1-mini", env="MODEL")

    # Database Configuration (for v1.1)
    database_url: str | None = Field(default=None, env="DATABASE_URL")

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Bot Configuration
    max_options: int = Field(default=5, env="MAX_OPTIONS")
    response_timeout: int = Field(default=30, env="RESPONSE_TIMEOUT")
    
    # Deployment Configuration
    use_webhook: bool = Field(default=False, env="USE_WEBHOOK")
    webhook_url: str | None = Field(default=None, env="WEBHOOK_URL")
    webhook_path: str = Field(default="/webhook", env="WEBHOOK_PATH")

    @field_validator("bot_token")
    @classmethod
    def validate_bot_token(cls, v: str) -> str:
        """Validate Telegram Bot Token format."""
        if not v or len(v) < 40:
            raise ValueError("Invalid BOT_TOKEN format. Should be from @BotFather")
        return v

    @field_validator("api_key")
    @classmethod
    def validate_api_key(cls, v: str) -> str:
        """Validate API Key format."""
        if not v or len(v) < 10:
            raise ValueError("Invalid API_KEY format")
        return v

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


def create_config() -> Config:
    """Create configuration with detailed error handling."""
    try:
        return Config()
    except ValidationError as e:
        logger.error("Configuration validation failed")
        
        # Extract missing fields and provide helpful error messages
        missing_vars = []
        invalid_vars = []
        
        for error in e.errors():
            field_name = error["loc"][0] if error["loc"] else "unknown"
            error_type = error["type"]
            
            if error_type == "missing":
                if field_name == "bot_token":
                    missing_vars.append("BOT_TOKEN - Get it from @BotFather in Telegram")
                elif field_name == "api_key":
                    missing_vars.append("API_KEY - Get it from openrouter.ai/keys")
                else:
                    missing_vars.append(f"{field_name.upper()}")
            else:
                invalid_vars.append(f"{field_name.upper()}: {error['msg']}")
        
        error_msg = "❌ Configuration Error!\n\n"
        
        if missing_vars:
            error_msg += "Missing required environment variables:\n"
            for var in missing_vars:
                error_msg += f"  • {var}\n"
            error_msg += "\n"
        
        if invalid_vars:
            error_msg += "Invalid environment variables:\n"
            for var in invalid_vars:
                error_msg += f"  • {var}\n"
            error_msg += "\n"
        
        error_msg += "Please set these variables in Railway:\n"
        error_msg += "1. Go to your Railway project dashboard\n"
        error_msg += "2. Open 'Variables' tab\n"
        error_msg += "3. Add the missing variables\n"
        error_msg += "4. Redeploy the application\n\n"
        error_msg += "See QUICK_DEPLOY.md for detailed instructions."
        
        print(error_msg)
        logger.error("Configuration error", error=error_msg)
        sys.exit(1)
    except Exception as e:
        logger.error("Unexpected configuration error", error=str(e))
        print(f"❌ Unexpected configuration error: {e}")
        sys.exit(1)
