# Test if .env file is loaded and DISCORD_TOKEN is set
def test_discord_token_loaded():
    from tsurugi.config import DISCORD_TOKEN

    assert DISCORD_TOKEN is not None
    assert isinstance(DISCORD_TOKEN, str)
    assert len(DISCORD_TOKEN) > 0
    assert DISCORD_TOKEN != "your_token_here"  # Ensure it's not a placeholder


# Test if bot can be instantiated without errors
def test_bot_instantiation():
    from tsurugi.bot import bot

    assert bot is not None
    assert hasattr(bot, "run")
    assert hasattr(bot, "add_cog")
