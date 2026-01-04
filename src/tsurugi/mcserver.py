import asyncio
import json
import subprocess

with open("server_info.json", "r") as f:
    config = json.load(f)


LOCK = asyncio.Lock()
SCREEN_NAME = "mcserver"
JAR_FULL_PATH = config["minecraft"]["path"] + config["minecraft"]["jar_file_name"]
START_CMD = [
    "screen",
    "-dmS",
    SCREEN_NAME,
    "java",
    "-Xms12G",  # Minimum memory allocation
    "-Xmx16G",  # Maximum memory allocation
    "-jar",
    JAR_FULL_PATH,
    "nogui",
]


def server_is_running():
    """Check if the screen session is already active"""
    result = subprocess.run(["screen", "-list"], capture_output=True, text=True)
    return SCREEN_NAME in result.stdout


async def start_server(ctx):
    async with LOCK:
        if server_is_running():
            await ctx.send("Minecraft server is already running!")
            return
        msg = await ctx.send("Starting Minecraft server...")
        try:
            subprocess.run(START_CMD, check=True)
            await msg.edit(content="Minecraft server started successfully!")
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to start Minecraft server: {e}")


async def stop_server(ctx):
    async with LOCK:
        if not server_is_running():
            await ctx.send("Minecraft server is not running!")
            return
        msg = await ctx.send("Stopping Minecraft server...")
        try:
            # Send "stop" to the server console inside the screen session
            # "stuff" is an actual command to send text to the screen session
            subprocess.run(
                ["screen", "-S", SCREEN_NAME, "-X", "stuff", "stop\n"], check=True
            )
            await msg.edit(content="Minecraft server stopped successfully!")
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to stop Minecraft server: {e}")


async def restart_server(ctx):
    async with LOCK:
        await stop_server(ctx)
        await start_server(ctx)
