import json
import os

from discord.ext import commands

# Load user mappings
USER_MAPPINGS_DATA = {}
USER_MAPPINGS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "user_mappings.json"
)

# Command permissions
COMMAND_PERMISSIONS = {}
COMMAND_PERMISSIONS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "data", "command_permissions.json"
)

try:
    with open(USER_MAPPINGS_PATH, "r") as f:
        USER_MAPPINGS_DATA = json.load(f)
except FileNotFoundError:
    print(f"Warning: User mappings file not found at {USER_MAPPINGS_PATH}")
except Exception as e:
    print(f"Warning: Could not load user mappings: {e}")

try:
    with open(COMMAND_PERMISSIONS_PATH, "r") as f:
        COMMAND_PERMISSIONS = json.load(f)
except FileNotFoundError:
    # Create default permissions file
    COMMAND_PERMISSIONS = {}
    os.makedirs(os.path.dirname(COMMAND_PERMISSIONS_PATH), exist_ok=True)
    with open(COMMAND_PERMISSIONS_PATH, "w") as f:
        json.dump(COMMAND_PERMISSIONS, f, indent=2)
    print(f"Created default command permissions file at {COMMAND_PERMISSIONS_PATH}")
except Exception as e:
    print(f"Warning: Could not load command permissions: {e}")


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


def save_command_permissions():
    """Save command permissions to disk."""
    try:
        with open(COMMAND_PERMISSIONS_PATH, "w") as f:
            json.dump(COMMAND_PERMISSIONS, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving command permissions: {e}")
        return False


def grant_command(user_id: str, command_name: str) -> bool:
    """
    Grant a user permission to run a specific command.
    Returns True if successful, False otherwise.
    """
    user_id = str(user_id)
    if command_name not in COMMAND_PERMISSIONS:
        COMMAND_PERMISSIONS[command_name] = []

    if user_id not in COMMAND_PERMISSIONS[command_name]:
        COMMAND_PERMISSIONS[command_name].append(user_id)
        return save_command_permissions()
    return True  # Already has permission


def revoke_command(user_id: str, command_name: str) -> bool:
    """
    Revoke a user's permission to run a specific command.
    Returns True if successful, False otherwise.
    """
    user_id = str(user_id)
    if (
        command_name in COMMAND_PERMISSIONS
        and user_id in COMMAND_PERMISSIONS[command_name]
    ):
        COMMAND_PERMISSIONS[command_name].remove(user_id)
        return save_command_permissions()
    return True  # Didn't have permission anyway


def has_command_permission(user_id: str, command_name: str) -> bool:
    """
    Check if a user has permission to run a specific command.
    Anshu always has permission.
    """
    user_id = str(user_id)

    # Anshu always has permission
    if user_id in get_anshu_user_ids():
        return True

    # Check if user is in the allowed list for this command
    return (
        command_name in COMMAND_PERMISSIONS
        and user_id in COMMAND_PERMISSIONS[command_name]
    )


def get_user_permissions(user_id: str) -> list[str]:
    """Get all commands a user has permission to run."""
    user_id = str(user_id)
    permissions = []

    for command_name, allowed_users in COMMAND_PERMISSIONS.items():
        if user_id in allowed_users:
            permissions.append(command_name)

    return permissions


def is_anshu():
    """Custom check to ensure only Anshu can run certain commands."""

    async def predicate(ctx):
        anshu_ids = get_anshu_user_ids()
        if str(ctx.author.id) not in anshu_ids:
            await ctx.send("❌ This command can only be used by Anshu.")
            return False
        return True

    return commands.check(predicate)


def requires_permission(command_name: str):
    """
    Custom check to ensure user has permission to run a specific command.
    Anshu always has permission.
    """

    async def predicate(ctx):
        if has_command_permission(str(ctx.author.id), command_name):
            return True

        await ctx.send(
            f"❌ You don't have permission to use the `!{command_name}` command."
        )
        return False

    return commands.check(predicate)
