import asyncio
import logging
import os
from datetime import datetime

import discord
from discord.ext import commands
from dotenv import load_dotenv


def main():
    """
    Main entry point for the bot
    """
    load_dotenv()

    intents = discord.Intents.default()
    bot: discord.ext.commands.AutoShardedBot = commands.AutoShardedBot(
        intents=intents,
        command_prefix="",
        help_command=None,
        description="Qubot is a discord bot for Quantum computing",
        shard_count=4,
    )

    if not os.path.exists("logs"):
        os.makedirs("logs")

    handler = logging.FileHandler(
        filename=f'logs/discord_{datetime.now().strftime("%Y_%m_%d_%H_%M")}.log',
        encoding="utf-8",
        mode="w",
    )
    log_format = logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    discord.utils.setup_logging(
        handler=handler,
        formatter=log_format,
        level=logging.DEBUG if os.getenv("DEBUG") == "True" else logging.INFO,
        root=False,
    )
    logger = logging.getLogger("discord")

    logger.info("Starting Bot...")

    asyncio.run(run(bot, logger))


async def run(bot: commands.AutoShardedBot, logger: logging.Logger):
    """Loads all the cogs and start the bot

    :param bot: The bot
    :param logger: The logging object
    """
    logger.info("Loading cogs....")
    for filename in os.listdir("cogs"):
        if filename.endswith("py") and filename != "__init__.py":
            await bot.load_extension(f"qubot.cogs.{filename[:-3]}")

    logger.info("Cogs successfully loaded!")

    async with bot:
        await bot.start(os.getenv("TOKEN"))


if __name__ == "__main__":
    main()
