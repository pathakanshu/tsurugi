import asyncio
import json
import os
import subprocess

LOCK = asyncio.Lock()
SCREEN_NAME = "mcserver"
_config = None


def _load_config():
    """Lazy load server configuration."""
    global _config
    if _config is None:
        config_path = os.path.join(
            os.path.dirname(__file__), "data", "server_info.jsonc"
        )
        try:
            with open(config_path, "r") as f:
                # Read file and remove comments for JSONC support
                content = f.read()
                # Simple JSONC comment removal (doesn't handle all edge cases)
                lines = [line.split("//")[0] for line in content.split("\n")]
                _config = json.loads("\n".join(lines))
        except FileNotFoundError:
            _config = {"minecraft": {"path": "", "jar_file_name": ""}}
    return _config


def _get_start_cmd():
    """Build the start command from config."""
    config = _load_config()
    jar_full_path = config["minecraft"]["path"] + config["minecraft"]["jar_file_name"]
    return [
        "screen",
        "-dmS",
        SCREEN_NAME,
        "java",
        "-Xms12G",  # Minimum memory allocation
        "-Xmx16G",  # Maximum memory allocation
        "-jar",
        jar_full_path,
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
            subprocess.run(_get_start_cmd(), check=True)
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
