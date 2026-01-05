import glob
import io
import re

import discord
import matplotlib.pyplot as plt
from discord.ext import commands

from .database import store_messages
from .helpers.permissions import (
    get_user_permissions,
    grant_command,
    is_anshu,
    requires_permission,
    revoke_command,
)
from .helpers.safety import (
    RateLimitError,
    TimeoutError,
    check_code_safety,
    get_safe_exec_globals,
    rate_limit,
    timeout,
    validate_sql_query,
)
from .mcserver import restart_server, start_server, stop_server

intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    if bot.user:
        print(f"Logged in as {bot.user.name} - {bot.user.id}")


@bot.command(name="ping")
async def ping(ctx):
    # sends an embed message with pong! and the bot's latency
    embed = discord.Embed(
        title="Pong!",
        description=f"Latency: {bot.latency * 1000:.2f} ms",
        color=0x00FF00,
    )
    await ctx.send(embed=embed)


@bot.command(name="mcserver")
async def mcserver(ctx, *, arg):
    match arg:
        case "start":
            await ctx.send("Starting Minecraft server...")
            await start_server(ctx)
        case "stop":
            await ctx.send("Stopping Minecraft server...")
            await stop_server(ctx)
        case "restart":
            await ctx.send("Restarting Minecraft server...")
            await restart_server(ctx)
        case "config":
            await ctx.send("Config is yet to be implemented")
        case _:
            await ctx.send("Invalid argument.")


@bot.command(name="archive")
@is_anshu()
async def archive(ctx):
    # Goes through all messsages in the current channel and stores all data into a sqllite database
    await ctx.send("Storing messages to SQLite. This may take a while...")
    count = await store_messages(ctx)
    await ctx.send(f"Stored {count} messages to SQLite database.")


@bot.command(name="grant")
@is_anshu()
async def grant(ctx, user: discord.User, command_name: str):
    """
    Grant a user permission to run a specific command.
    Usage: !grant @user command_name
    Example: !grant @john runsql
    """
    if grant_command(str(user.id), command_name):
        await ctx.send(
            f"✅ Granted `{user.name}` permission to use `!{command_name}` command."
        )
    else:
        await ctx.send("❌ Failed to grant permission.")


@bot.command(name="revoke")
@is_anshu()
async def revoke(ctx, user: discord.User, command_name: str):
    """
    Revoke a user's permission to run a specific command.
    Usage: !revoke @user command_name
    Example: !revoke @john runsql
    """
    if revoke_command(str(user.id), command_name):
        await ctx.send(
            f"✅ Revoked `{user.name}`'s permission to use `!{command_name}` command."
        )
    else:
        await ctx.send("❌ Failed to revoke permission.")


@bot.command(name="permissions")
@is_anshu()
async def permissions(ctx, user: discord.User | None = None):
    """
    View permissions for a user or all users.
    Usage: !permissions [@user]
    """
    if user:
        # Show permissions for specific user
        perms = get_user_permissions(str(user.id))
        if perms:
            perms_list = ", ".join([f"`!{cmd}`" for cmd in perms])
            await ctx.send(f"**{user.name}** can run: {perms_list}")
        else:
            await ctx.send(f"**{user.name}** has no special command permissions.")
    else:
        # Show all permissions
        from .helpers.permissions import COMMAND_PERMISSIONS

        if not COMMAND_PERMISSIONS:
            await ctx.send("No command permissions have been granted yet.")
            return

        embed = discord.Embed(
            title="Command Permissions",
            color=0x00FF00,
        )

        for command_name, user_ids in COMMAND_PERMISSIONS.items():
            if user_ids:
                users = []
                for user_id in user_ids:
                    try:
                        u = await bot.fetch_user(int(user_id))
                        users.append(u.name)
                    except Exception:
                        users.append(f"<@{user_id}>")
                embed.add_field(
                    name=f"!{command_name}",
                    value=", ".join(users),
                    inline=False,
                )

        await ctx.send(embed=embed)


@bot.command(name="matplotlib")
@requires_permission("matplotlib")
@rate_limit(calls=5, period=60)  # 5 plots per minute
async def matplotlib(ctx, *, code: str = ""):
    """
    Executes matplotlib code and returns the generated plot as an image.
    Accepts Python code in text or from attached .txt/.py file.

    Example code input:
    ```python
    plt.plot([1, 2, 3], [4, 5, 6])
    plt.title("Sample Plot")
    ```

    """
    # Check if there's an attachment
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]

        # Download and read the attachment content
        try:
            content_bytes = await attachment.read()
            code = content_bytes.decode("utf-8")
        except Exception as e:
            await ctx.send(f"❌ Error reading attachment: {e}")
            return

    # If no code after checking attachment, send error
    if not code or code.strip() == "":
        await ctx.send(
            "❌ No Python code provided. Either type code or attach a .txt/.py file."
        )
        return

    # Extract code from code block if present
    code_block_pattern = r"```(?:python)?\s*\n?(.*?)\n?```"
    match = re.search(code_block_pattern, code, re.DOTALL | re.IGNORECASE)

    if match:
        code = match.group(1).strip()

    # Check code safety
    is_safe, warning = check_code_safety(code)
    if not is_safe:
        await ctx.send(f"❌ Unsafe code detected: {warning}")
        return

    # Use restricted globals for safety
    safe_globals = get_safe_exec_globals()
    local_scope = {}

    @timeout(5)  # 5 second timeout
    def execute_code():
        exec(code, safe_globals, local_scope)

    try:
        # Execute the provided matplotlib code with timeout
        execute_code()

        # Save the current figure to a BytesIO object
        img_bytes = io.BytesIO()
        plt.savefig(img_bytes, format="png")
        img_bytes.seek(0)

        # Create a Discord file object
        discord_file = discord.File(img_bytes, filename="plot.png")

        # Send the image file in the channel
        await ctx.send(file=discord_file)

        # Clear the current figure to avoid overlap in future plots
        plt.clf()

    except TimeoutError:
        await ctx.send("❌ Code execution timed out (5 second limit)")
        plt.clf()
    except RateLimitError as e:
        await ctx.send(f"⏱️ {e}")
    except Exception as e:
        await ctx.send(f"❌ Error executing matplotlib code: {e}")
        plt.clf()


@bot.command(name="runsql")
@requires_permission("runsql")
@rate_limit(calls=10, period=60)  # 10 queries per minute
async def runsql(ctx, *, query: str = ""):
    """
    Runs a SQL query on the database file in the current directory.
    Accepts SQL in code blocks like: ```sql SELECT * FROM messages```
    Can also read SQL from attached .txt file.
    Returns results as a .txt file.
    """
    # Check if there's an attachment
    if ctx.message.attachments:
        attachment = ctx.message.attachments[0]

        # Download and read the attachment content
        try:
            content_bytes = await attachment.read()
            query = content_bytes.decode("utf-8")
        except Exception as e:
            await ctx.send(f"❌ Error reading attachment: {e}")
            return

    # If no query after checking attachment, send error
    if not query or query.strip() == "":
        await ctx.send(
            "❌ No SQL query provided. Either type a query or attach a .txt file."
        )
        return

    # Extract SQL from code block if present
    code_block_pattern = r"```(?:sql)?\s*\n?(.*?)\n?```"
    match = re.search(code_block_pattern, query, re.DOTALL | re.IGNORECASE)

    if match:
        query = match.group(1).strip()

    # Validate query safety
    is_valid, error_msg = validate_sql_query(query)
    if not is_valid:
        await ctx.send(f"❌ Query validation failed: {error_msg}")
        return

    # Find any database file (not channel-specific)
    pattern = "*_messages.db"
    matching_files = glob.glob(pattern)

    if not matching_files:
        await ctx.send("❌ No database files found. Run `!archive` first.")
        return

    # Get the most recent file (sorted by name, which includes timestamp)
    db_path = sorted(matching_files)[-1]

    try:
        # Run query with timeout wrapper
        @timeout(10)  # 10 second timeout for queries
        def execute_query():
            import sqlite3

            conn = sqlite3.connect(db_path, timeout=5.0)
            # Register custom SQL functions
            from .database import (
                is_tracked,
                real_name,
                sentiment_label,
                sentiment_polarity,
                sentiment_subjectivity,
                word_count,
            )

            conn.create_function("sentiment_polarity", 1, sentiment_polarity)
            conn.create_function("sentiment_subjectivity", 1, sentiment_subjectivity)
            conn.create_function("sentiment_label", 1, sentiment_label)
            conn.create_function("word_count", 1, word_count)
            conn.create_function("real_name", 1, real_name)
            conn.create_function("is_tracked", 1, is_tracked)

            c = conn.cursor()
            c.execute(query)
            results = c.fetchall()
            conn.close()
            return results

        results = execute_query()

        if not results:
            response = "Query executed successfully, but no results to display."
        else:
            result_str = "\n".join([str(row) for row in results])
            response = f"Query Results:\n{result_str}"

        # Create a text file with the results
        file_content = f"SQL Query:\n{query}\n\n{'=' * 60}\n\nResults:\n{response}"
        file_bytes = io.BytesIO(file_content.encode("utf-8"))
        file_bytes.seek(0)

        # Create Discord file object
        discord_file = discord.File(file_bytes, filename="query_results.txt")

        # Send only the file, no preview
        await ctx.send(file=discord_file)

    except TimeoutError:
        await ctx.send("❌ Query execution timed out (10 second limit)")
    except RateLimitError as e:
        await ctx.send(f"⏱️ {e}")
    except Exception as e:
        await ctx.send(f"❌ Error executing query: {e}")


@bot.event
async def on_command_error(ctx, error):
    """Handle command errors, particularly permission errors."""
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "❌ You don't have permission to use this command. Administrator access required."
        )
    elif isinstance(error, commands.CommandInvokeError):
        if isinstance(error.original, discord.Forbidden):
            await ctx.send(
                "❌ I don't have permission to perform that action in this channel."
            )
        elif isinstance(error.original, (TimeoutError, RateLimitError)):
            # These are already handled
            pass
        else:
            await ctx.send(f"❌ An error occurred: {error.original}")
    else:
        # Re-raise other errors for debugging
        raise error
