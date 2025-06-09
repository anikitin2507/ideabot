"""LLM client for generating decision advice (supports OpenRouter and OpenAI)."""

import asyncio
import httpx

import openai
import structlog
from openai import AsyncOpenAI

from src.config import Config

logger = structlog.get_logger()


class LLMClient:
    """Client for interacting with LLM APIs to generate decision advice."""

    def __init__(self, config: Config):
        """Initialize the LLM client."""
        self.config = config
        
        # Configure OpenAI client with appropriate base URL and API key
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.api_base if config.api_type == "openrouter" else None
        )

    async def get_decision_advice(
        self,
        options: list[str],
        context: str | None = None,
        vote_results: dict[str, int] | None = None,
    ) -> str | None:
        """
        Generate decision advice for given options.

        Args:
            options: List of options to choose from
            context: Additional context from user (future feature)
            vote_results: Voting results from group chat (v1.1 feature)

        Returns:
            Decision advice string or None if failed
        """
        try:
            prompt = self._build_prompt(options, context, vote_results)

            logger.info(
                "Requesting decision advice from LLM",
                api_type=self.config.api_type,
                model=self.config.model,
                options_count=len(options),
            )

            # Build request parameters
            params = {
                "model": self.config.model,
                "messages": [
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt},
                ],
                "max_tokens": 150,
                "temperature": 0.7,
                "timeout": self.config.response_timeout,
            }
            
            # Add OpenRouter specific headers if needed
            headers = {}
            if self.config.api_type == "openrouter":
                headers = {
                    "HTTP-Referer": "https://github.com/anikitin2507/ideabot",
                    "X-Title": "Decision Bot"
                }
                params["headers"] = headers

            response = await self.client.chat.completions.create(**params)

            if not response.choices:
                logger.error("No choices in LLM response")
                return None

            advice = response.choices[0].message.content
            if not advice:
                logger.error("Empty content in LLM response")
                return None

            advice = advice.strip()

            logger.info(
                "Generated decision advice successfully",
                advice_length=len(advice),
                tokens_used=response.usage.total_tokens if response.usage else None,
            )

            return advice

        except openai.RateLimitError as e:
            logger.error("LLM rate limit exceeded", error=str(e))
            return "🚫 Извините, превышен лимит запросов к AI. Попробуйте позже."

        except openai.APIError as e:
            logger.error("LLM API error", error=str(e))
            return "🚫 Ошибка AI сервиса. Попробуйте позже."

        except httpx.TimeoutException:
            logger.error("LLM request timeout")
            return "⏰ Превышено время ожидания ответа AI. Попробуйте позже."

        except asyncio.TimeoutError:
            logger.error("LLM request timeout")
            return "⏰ Превышено время ожидания ответа AI. Попробуйте позже."

        except Exception as e:
            logger.error("Unexpected error in LLM client", error=str(e), error_type=type(e).__name__)
            return "🚫 Произошла ошибка при генерации совета. Попробуйте позже."

    def _get_system_prompt(self) -> str:
        """Get the system prompt for the AI assistant."""
        return """Ты помощник для принятия решений. Твоя задача - помочь пользователю выбрать один из предложенных вариантов.

Требования к ответу:
1. Выбери ОДИН конкретный вариант из предложенных
2. Дай 1-2 кратких предложения с обоснованием выбора
3. Будь лаконичен и конкретен
4. Используй дружелюбный тон
5. Отвечай на русском языке

Формат ответа: "Рекомендую [выбранный вариант]. [Краткое обоснование]."
"""

    def _build_prompt(
        self,
        options: list[str],
        context: str | None = None,
        vote_results: dict[str, int] | None = None,
    ) -> str:
        """Build the user prompt for decision making."""
        prompt_parts = []

        # Add options
        prompt_parts.append("Помоги выбрать из следующих вариантов:")
        for i, option in enumerate(options, 1):
            prompt_parts.append(f"{i}. {option}")

        # Add voting results if available (v1.1 feature)
        if vote_results:
            prompt_parts.append("\nРезультаты голосования друзей:")
            total_votes = sum(vote_results.values())
            for option, votes in sorted(
                vote_results.items(), key=lambda x: x[1], reverse=True
            ):
                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                prompt_parts.append(f"• {option}: {votes} голосов ({percentage:.1f}%)")

        # Add context if provided
        if context:
            prompt_parts.append(f"\nДополнительный контекст: {context}")

        return "\n".join(prompt_parts)


# For backward compatibility
OpenAIClient = LLMClient
