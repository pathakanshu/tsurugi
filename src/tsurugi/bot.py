import glob
import io
import re

import discord
import matplotlib.pyplot as plt
from discord.ext import commands

from .database import run_sql_query, store_messages
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
@commands.has_permissions(administrator=True)
async def archive(ctx):
    # Goes through all messsages in the current channel and stores all data into a sqllite database
    await ctx.send("Storing messages to SQLite. This may take a while...")
    count = await store_messages(ctx)
    await ctx.send(f"Stored {count} messages to SQLite database.")


@bot.command(name="matplotlib")
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

    # Prepare a local scope for executing the code
    # This is done to limit the available variables and functions

    local_scope = {"plt": plt}

    try:
        # Execute the provided matplotlib code
        exec(code, {}, local_scope)

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

    except Exception as e:
        await ctx.send(f"❌ Error executing matplotlib code: {e}")


@bot.command(name="runsql")
@commands.has_permissions(administrator=True)
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

    # Find any database file (not channel-specific)
    pattern = "*_messages.db"
    matching_files = glob.glob(pattern)

    if not matching_files:
        await ctx.send("❌ No database files found. Run `!archive` first.")
        return

    # Get the most recent file (sorted by name, which includes timestamp)
    db_path = sorted(matching_files)[-1]

    try:
        response = await run_sql_query(db_path, query)

        # Create a text file with the results
        file_content = f"SQL Query:\n{query}\n\n{'=' * 60}\n\nResults:\n{response}"
        file_bytes = io.BytesIO(file_content.encode("utf-8"))
        file_bytes.seek(0)

        # Create Discord file object
        discord_file = discord.File(file_bytes, filename="query_results.txt")

        # Send only the file, no preview
        await ctx.send(file=discord_file)

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
        else:
            await ctx.send(f"❌ An error occurred: {error.original}")
    else:
        # Re-raise other errors for debugging
        raise error
