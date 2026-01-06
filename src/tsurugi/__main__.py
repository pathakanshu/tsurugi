import logging

from .bot import bot
from .config.config import DISCORD_TOKEN


def main():
    """Entry point for the Tsurugi Discord bot."""
    # Configure logging to show INFO level messages
    logging.basicConfig(
        level=logging.INFO,
        format="[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Type narrowing - DISCORD_TOKEN is guaranteed to be str after config validation
    assert isinstance(DISCORD_TOKEN, str)
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
