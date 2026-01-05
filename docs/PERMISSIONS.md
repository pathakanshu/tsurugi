# Permission System

The Tsurugi bot has a flexible permission system that allows Anshu to grant specific users access to sensitive commands.

## Overview

- **Anshu** (owner) has full access to all commands
- Anshu can grant/revoke permissions for specific commands to other users
- Permissions are stored in `src/tsurugi/data/command_permissions.json`

## Commands

### For Anshu Only

#### `!lock`
Lock the bot. **All commands are disabled** when locked (except `!unlock`).

**Example:**
```
!lock
```

When locked:
- **All users including Anshu** are blocked from using any commands
- Only `!unlock` can be used to restore access
- Useful for emergency shutdowns or maintenance

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

The bot can be put into complete lockdown mode where **all commands are disabled**.

**When locked:**
- **All commands are blocked for everyone** (including Anshu)
- Only `!unlock` command works (Anshu only)
- All users attempting to run commands receive: "🔒 Bot is locked. Use !unlock to restore access."

**Use cases:**
- Emergency shutdown
- Preventing all command usage during critical maintenance
- Complete bot functionality disable

**Commands:**
- `!lock` - Enable lockdown mode (disables everything except unlock)
- `!unlock` - Disable lockdown mode (only works when locked)

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

- `@is_anshu()` - Restrict command to Anshu only (blocked during lockdown unless `allow_when_locked=True`)
- `@is_anshu(allow_when_locked=True)` - Restrict to Anshu only, works even when locked (used for `!unlock`)
- `@requires_permission("command_name")` - Require permission for command (blocked during lockdown)

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
- Anshu has permission to run all commands **except when bot is locked**
- The `!archive` command cannot be delegated (Anshu only)
- Permission changes are saved immediately to disk
- If `command_permissions.json` doesn't exist, it's created automatically
- Lockdown state is in-memory only (resets on bot restart)
- **Lockdown blocks ALL commands for ALL users** (only `!unlock` works)