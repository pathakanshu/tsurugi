# Permission System

The Tsurugi bot has a flexible permission system that allows Anshu to grant specific users access to sensitive commands.

## Overview

- **Anshu** (owner) has full access to all commands
- Anshu can grant/revoke permissions for specific commands to other users
- Permissions are stored in `src/tsurugi/data/command_permissions.json`

## Commands

### For Anshu Only

#### `!lock`
Lock the bot. Only Anshu can use commands when locked.

**Example:**
```
!lock
```

When locked:
- All users except Anshu are blocked from using any commands
- Anshu can still use all commands normally
- Useful for maintenance or emergency situations

#### `!unlock`
Unlock the bot. Normal permissions resume.

**Example:**
```
!unlock
```

#### `!grant <user> <command_name>`
Grant a user permission to run a specific command.

**Example:**
```
!grant @john runsql
!grant @alice matplotlib
```

#### `!revoke <user> <command_name>`
Revoke a user's permission to run a specific command.

**Example:**
```
!revoke @john runsql
!revoke @alice matplotlib
```

#### `!permissions [user]`
View permissions for a specific user or all users.

**Examples:**
```
!permissions           # Show all command permissions
!permissions @john     # Show permissions for specific user
```

#### `!archive`
Archive all messages in the current channel to SQLite database. This command is restricted to Anshu only and cannot be granted to other users.

## Lockdown Mode

The bot can be put into lockdown mode where only Anshu can execute commands.

**When locked:**
- All commands with `@requires_permission` decorator are blocked for non-Anshu users
- Anshu's commands (`!lock`, `!unlock`, `!grant`, `!revoke`, `!permissions`, `!archive`) remain accessible to Anshu
- Users attempting to run commands receive: "🔒 Bot is locked. Only Anshu can use commands."

**Use cases:**
- Emergency maintenance
- Preventing command usage during debugging
- Temporarily disabling bot functionality

**Commands:**
- `!lock` - Enable lockdown mode
- `!unlock` - Disable lockdown mode

## Protected Commands

The following commands require explicit permission from Anshu:

- **`!runsql`** - Execute SQL queries on archived message databases
- **`!matplotlib`** - Execute matplotlib code to generate plots

## Permission File Format

Permissions are stored in `src/tsurugi/data/command_permissions.json`:

```json
{
  "runsql": ["user_id_1", "user_id_2"],
  "matplotlib": ["user_id_1"]
}
```

## Implementation Details

### Helper Functions

Located in `src/tsurugi/helpers/permissions.py`:

- `grant_command(user_id, command_name)` - Grant permission
- `revoke_command(user_id, command_name)` - Revoke permission
- `has_command_permission(user_id, command_name)` - Check permission
- `get_user_permissions(user_id)` - Get all commands user can run
- `get_anshu_user_ids()` - Get Anshu's Discord user IDs

### Decorators

- `@is_anshu()` - Restrict command to Anshu only (always works, even in lockdown)
- `@requires_permission("command_name")` - Require permission for command (respects lockdown mode)

### Usage in Bot Commands

```python
@bot.command(name="runsql")
@requires_permission("runsql")
async def runsql(ctx, *, query: str = ""):
    # Command implementation
    pass
```

## Security Notes

- Anshu's user IDs are read from `user_mappings.json`
- Anshu always has permission to run all commands (even when locked)
- The `!archive` command cannot be delegated (Anshu only)
- Permission changes are saved immediately to disk
- If `command_permissions.json` doesn't exist, it's created automatically
- Lockdown state is in-memory only (resets on bot restart)
- Lockdown blocks all `@requires_permission` commands for non-Anshu users