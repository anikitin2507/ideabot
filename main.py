"""Main entry point for the Decision Bot."""

import asyncio
import logging

import structlog
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import web
from dotenv import load_dotenv

from src.config import create_config
from src.handlers.decision_handler import DecisionHandler


async def health_check(request):
    """Health check endpoint for Railway."""
    return web.json_response({"status": "healthy", "service": "decision-bot"})


async def create_app() -> web.Application:
    """Create aiohttp application with health check."""
    app = web.Application()
    app.router.add_get("/health", health_check)
    return app


async def main() -> None:
    """Initialize and start the bot."""
    # Load environment variables
    load_dotenv()

    # Configure logging
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logger = structlog.get_logger()

    # Initialize configuration with better error handling
    config = create_config()

    # Initialize bot and dispatcher
    bot = Bot(
        token=config.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    # Register handlers
    decision_handler = DecisionHandler()
    dp.include_router(decision_handler.router)

    # Create web app for health checks
    app = await create_app()

    logger.info("Starting Decision Bot", version="1.0.0")

    try:
        # Start both bot and web server concurrently
        from aiohttp.web import _run_app

        async def start_bot():
            await dp.start_polling(bot)

        async def start_web():
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", 8000)
            await site.start()
            logger.info("Health check server started on port 8000")
            # Keep the server running
            while True:
                await asyncio.sleep(1)

        # Run both concurrently
        await asyncio.gather(start_bot(), start_web())

    except Exception as e:
        logger.error("Bot crashed", error=str(e))
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
