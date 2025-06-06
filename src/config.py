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

    # OpenAI API Key
    openai_api_key: str = Field(..., env="OPENAI_API_KEY", description="OpenAI API Key")

    # OpenAI Model Configuration
    openai_model: str = Field(default="gpt-4.1-mini", env="OPENAI_MODEL")

    # Database Configuration (for v1.1)
    database_url: str | None = Field(default=None, env="DATABASE_URL")

    # Logging Configuration
    log_level: str = Field(default="INFO", env="LOG_LEVEL")

    # Bot Configuration
    max_options: int = Field(default=5, env="MAX_OPTIONS")
    response_timeout: int = Field(default=30, env="RESPONSE_TIMEOUT")

    @field_validator("bot_token")
    @classmethod
    def validate_bot_token(cls, v: str) -> str:
        """Validate Telegram Bot Token format."""
        if not v or len(v) < 40:
            raise ValueError("Invalid BOT_TOKEN format. Should be from @BotFather")
        return v

    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_key(cls, v: str) -> str:
        """Validate OpenAI API Key format."""
        if not v or not v.startswith(("sk-", "sk-proj-")):
            raise ValueError("Invalid OPENAI_API_KEY format. Should start with 'sk-'")
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
                elif field_name == "openai_api_key":
                    missing_vars.append("OPENAI_API_KEY - Get it from platform.openai.com/api-keys")
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
