"""Decision handler for processing user messages and generating advice."""

import structlog
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from src.config import create_config
from src.services.openai_client import OpenAIClient
from src.services.option_parser import OptionParser

logger = structlog.get_logger()


class DecisionHandler:
    """Handler for decision-making requests."""

    def __init__(self):
        """Initialize the decision handler."""
        self.router = Router()
        self.config = create_config()
        self.option_parser = OptionParser(max_options=self.config.max_options)
        self.openai_client = OpenAIClient(self.config)

        # Register message handlers
        self.router.message(Command("start"))(self.start_command)
        self.router.message(Command("help"))(self.help_command)
        self.router.message(F.text)(self.handle_decision_request)

    async def start_command(self, message: Message) -> None:
        """Handle /start command."""
        welcome_text = (
            "👋 Привет! Я бот-помощник для принятия решений.\n\n"
            "Просто отправь мне варианты, между которыми сомневаешься, "
            "и я помогу выбрать лучший!\n\n"
            "Примеры:\n"
            "• Пицца или суши?\n"
            "• Посмотреть фильм, почитать книгу или поиграть в игру\n"
            "• 1. Пойти в спортзал\n2. Остаться дома\n\n"
            "Отправь /help для получения дополнительной информации."
        )

        await message.answer(welcome_text)

        logger.info(
            "User started bot",
            user_id=message.from_user.id if message.from_user else None,
            username=message.from_user.username if message.from_user else None,
        )

    async def help_command(self, message: Message) -> None:
        """Handle /help command."""
        help_text = (
            "🤖 <b>Как пользоваться ботом:</b>\n\n"
            "1️⃣ Отправь мне сообщение с вариантами выбора\n"
            "2️⃣ Я проанализирую их и дам совет\n\n"
            "<b>Поддерживаемые форматы:</b>\n"
            "• Через «или»: <i>Пицца или суши?</i>\n"
            "• Через запятую: <i>Кино, театр, дом</i>\n"
            "• По строкам:\n"
            "<i>Кофе\n"
            "Чай\n"
            "Какао</i>\n"
            "• Нумерованный список:\n"
            "<i>1. Утренняя пробежка\n"
            "2. Йога дома</i>\n\n"
            "<b>Ограничения:</b>\n"
            f"• Минимум 2 варианта\n"
            f"• Максимум {self.config.max_options} вариантов\n\n"
            "Просто напиши свои варианты, и я помогу выбрать! 🎯"
        )

        await message.answer(help_text, parse_mode="HTML")

    async def handle_decision_request(self, message: Message) -> None:
        """Handle user message with decision request."""
        if not message.text:
            return

        user_id = message.from_user.id if message.from_user else None
        username = message.from_user.username if message.from_user else None

        logger.info(
            "Processing decision request",
            user_id=user_id,
            username=username,
            message_length=len(message.text),
        )

        # Send "thinking" reaction
        await message.react("🤔")

        # Parse options from message
        options = self.option_parser.parse_options(message.text)

        if not options:
            error_text = (
                "🤷‍♂️ Не могу найти варианты для выбора в твоём сообщении.\n\n"
                "Попробуй написать так:\n"
                "• Пицца или суши?\n"
                "• Кино, театр или дом\n"
                "• 1. Вариант А\n2. Вариант Б\n\n"
                "Отправь /help для получения примеров."
            )
            await message.answer(error_text)
            return

        if len(options) < 2:
            await message.answer(
                "🤷‍♂️ Нужно минимум 2 варианта для выбора. " "Добавь ещё один вариант!"
            )
            return

        # Generate advice using OpenAI
        try:
            advice = await self.openai_client.get_decision_advice(options)

            if advice:
                # Format the response
                response_text = f"🎯 {advice}"
                await message.answer(response_text)

                logger.info(
                    "Decision advice sent successfully",
                    user_id=user_id,
                    options_count=len(options),
                    advice_length=len(advice),
                )
            else:
                # Fallback response if OpenAI fails
                fallback_advice = self._generate_fallback_advice(options)
                await message.answer(f"🎯 {fallback_advice}")

                logger.warning(
                    "Used fallback advice due to OpenAI failure",
                    user_id=user_id,
                    options_count=len(options),
                )

        except Exception as e:
            logger.error(
                "Error processing decision request", user_id=user_id, error=str(e)
            )

            await message.answer(
                "😅 Произошла ошибка при обработке запроса. "
                "Попробуй ещё раз через несколько секунд."
            )

    def _generate_fallback_advice(self, options: list[str]) -> str:
        """Generate simple fallback advice when OpenAI is unavailable."""
        import random

        chosen_option = random.choice(options)
        fallback_reasons = [
            "Иногда лучше положиться на интуицию!",
            "Этот вариант кажется наиболее универсальным.",
            "Попробуй этот - а если не понравится, всегда можно выбрать другой!",
            "Мой случайный выбор - но он может оказаться самым правильным!",
            "Этот вариант выглядит интересно, почему бы не попробовать?",
        ]

        reason = random.choice(fallback_reasons)
        return f"Рекомендую {chosen_option}. {reason}"
