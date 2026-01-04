import json
import os

from discord.ext import commands

# Load user mappings
USER_MAPPINGS_DATA = {}
USER_MAPPINGS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "user_mappings.json"
)

try:
    with open(USER_MAPPINGS_PATH, "r") as f:
        USER_MAPPINGS_DATA = json.load(f)
except FileNotFoundError:
    print(f"Warning: User mappings file not found at {USER_MAPPINGS_PATH}")
except Exception as e:
    print(f"Warning: Could not load user mappings: {e}")


def get_anshu_user_ids() -> set[str]:
    """
    Returns a set of all Discord user IDs belonging to Anshu.
    Used for permission checks on sensitive commands.
    """
    anshu_ids = set()
    if "users" in USER_MAPPINGS_DATA and "anshu" in USER_MAPPINGS_DATA["users"]:
        for account in USER_MAPPINGS_DATA["users"]["anshu"]["accounts"]:
            anshu_ids.add(account["user_id"])
    return anshu_ids


def is_anshu():
    """Custom check to ensure only Anshu can run certain commands."""

    async def predicate(ctx):
        anshu_ids = get_anshu_user_ids()
        if str(ctx.author.id) not in anshu_ids:
            await ctx.send("❌ This command can only be used by Anshu.")
            return False
        return True

    return commands.check(predicate)
