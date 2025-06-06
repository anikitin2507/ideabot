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


async def webhook_handler(request):
    """Handle webhook updates from Telegram."""
    import structlog

    logger = structlog.get_logger()

    bot = request.app["bot"]
    dp = request.app["dispatcher"]

    try:
        data = await request.json()
        from aiogram.types import Update

        update = Update(**data)
        await dp.feed_update(bot, update)
        return web.Response(status=200)
    except Exception as e:
        logger.error("Webhook error", error=str(e))
        return web.Response(status=500)


async def create_app(bot=None, dp=None, config=None) -> web.Application:
    """Create aiohttp application with health check and webhook."""
    app = web.Application()
    app.router.add_get("/health", health_check)

    if bot and dp and config and config.use_webhook:
        app["bot"] = bot
        app["dispatcher"] = dp
        app.router.add_post(config.webhook_path, webhook_handler)

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

    logger.info(
        "Starting Decision Bot",
        version="1.0.0",
        mode="webhook" if config.use_webhook else "polling",
    )

    try:
        # Check for existing bot instances first
        try:
            me = await bot.get_me()
            logger.info("Bot authenticated", username=me.username, id=me.id)
        except Exception as e:
            logger.error("Failed to authenticate bot", error=str(e))
            raise

        # Create web app with or without webhook
        app = await create_app(bot, dp, config)

        if config.use_webhook:
            # Webhook mode - no conflicts possible
            if not config.webhook_url:
                logger.error("WEBHOOK_URL is required when USE_WEBHOOK=true")
                raise ValueError("WEBHOOK_URL is required for webhook mode")

            # Set webhook
            webhook_url = f"{config.webhook_url.rstrip('/')}{config.webhook_path}"
            await bot.set_webhook(
                url=webhook_url,
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"],
            )
            logger.info("Webhook set", url=webhook_url)

            # Start only web server
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, "0.0.0.0", 8000)
            await site.start()
            logger.info("Webhook server started on port 8000")

            # Keep running
            while True:
                await asyncio.sleep(1)
        else:
            # Polling mode - with conflict handling
            # Clear any pending updates to avoid conflicts
            try:
                await bot.delete_webhook(drop_pending_updates=True)
                logger.info("Cleared webhook and pending updates")
            except Exception as e:
                logger.warning("Could not clear webhook", error=str(e))

            # Start both bot and web server concurrently
            async def start_bot():
                retry_count = 0
                max_retries = 5

                while retry_count < max_retries:
                    try:
                        logger.info("Starting bot polling", attempt=retry_count + 1)
                        await dp.start_polling(
                            bot,
                            polling_timeout=10,
                            handle_as_tasks=False,
                            drop_pending_updates=True,
                        )
                        break
                    except Exception as e:
                        if "terminated by other getUpdates request" in str(e):
                            retry_count += 1
                            wait_time = min(30, 5 * retry_count)
                            logger.warning(
                                "Bot conflict detected, retrying",
                                error=str(e),
                                retry=retry_count,
                                wait_time=wait_time,
                            )
                            if retry_count >= max_retries:
                                logger.error(
                                    "🚨 POLLING CONFLICTS DETECTED! 🚨\n"
                                    "Multiple bot instances are running with the same token.\n\n"
                                    "SOLUTIONS:\n"
                                    "1. USE WEBHOOK MODE (recommended):\n"
                                    "   Add to Railway Variables:\n"
                                    "   USE_WEBHOOK=true\n"
                                    "   WEBHOOK_URL=https://your-domain.railway.app\n\n"
                                    "2. STOP OTHER DEPLOYMENTS:\n"
                                    "   Railway Dashboard → Deployments → Stop All → Redeploy one\n\n"
                                    "3. CREATE NEW BOT TOKEN:\n"
                                    "   @BotFather → /mybots → Revoke & Generate new token\n\n"
                                    "See URGENT_FIX.md for detailed instructions."
                                )
                                raise
                            await asyncio.sleep(wait_time)
                        else:
                            logger.error("Bot polling error", error=str(e))
                            raise

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

    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down gracefully")
    except Exception as e:
        logger.error("Bot crashed", error=str(e))
        raise
    finally:
        try:
            await bot.session.close()
            logger.info("Bot session closed")
        except Exception as e:
            logger.error("Error closing bot session", error=str(e))


if __name__ == "__main__":
    asyncio.run(main())
