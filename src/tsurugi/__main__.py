from .bot import bot
from .config import DISCORD_TOKEN

if __name__ == "__main__":
    # Type narrowing - DISCORD_TOKEN is guaranteed to be str after config validation
    assert isinstance(DISCORD_TOKEN, str)
    bot.run(DISCORD_TOKEN)
