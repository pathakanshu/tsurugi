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
        config_path = os.path.join(os.path.dirname(__file__), "server_info.json")

        try:
            with open(config_path, "r") as f:
                _config = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(
                "Server configuration file not found." + config_path
            )
    return _config


def _get_start_cmd():
    """Build the start command from config."""
    config = _load_config()

    return f"cd {
        os.path.expanduser(config['minecraft']['path'])
    } && java -Xms12G -Xmx16G -jar {
        os.path.expanduser(
            config['minecraft']['path'] + config['minecraft']['jar_file_name']
        )
    } nogui"


def server_is_running():
    """Check if the screen session is already active"""
    result = subprocess.run(["screen", "-list"], capture_output=True, text=True)
    return SCREEN_NAME in result.stdout


async def start_server(ctx):
    # Notify user if waiting for lock
    if LOCK.locked():
        wait_msg = await ctx.send("⏳ Waiting for current operation to complete...")
    else:
        wait_msg = None

    async with LOCK:
        if wait_msg:
            await wait_msg.delete()

        if server_is_running():
            await ctx.send("Minecraft server is already running!")
            return

        msg = await ctx.send("Starting Minecraft server...")
        print(_get_start_cmd())
        try:
            # Start the Minecraft server in a screen session
            subprocess.run(
                ["screen", "-dmS", SCREEN_NAME, "bash", "-c", _get_start_cmd()],
                check=True,
            )

            await msg.edit(content="Minecraft server started successfully!")
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to start Minecraft server: {e}")


async def stop_server(ctx):
    # Notify user if waiting for lock
    if LOCK.locked():
        wait_msg = await ctx.send("⏳ Waiting for current operation to complete...")
    else:
        wait_msg = None

    async with LOCK:
        if wait_msg:
            await wait_msg.delete()

        if not server_is_running():
            await ctx.send("Minecraft server is not running!")
            return
        msg = await ctx.send("Stopping Minecraft server...")
        try:
            # Send "stop" to the server console inside the screen session
            # "stuff" is an actual command to send text to the screen session
            # In this case, we're sending the "stop" command to minecraft server console
            subprocess.run(
                ["screen", "-S", SCREEN_NAME, "-X", "stuff", "stop\n"], check=True
            )
            await msg.edit(content="Minecraft server stopped successfully!")
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to stop Minecraft server: {e}")


async def restart_server(ctx):
    # Notify user if waiting for lock
    if LOCK.locked():
        wait_msg = await ctx.send("⏳ Waiting for current operation to complete...")
    else:
        wait_msg = None

    async with LOCK:
        if wait_msg:
            await wait_msg.delete()

        if not server_is_running():
            await ctx.send("Minecraft server is not running!")
            return

        # Stop the server
        msg = await ctx.send("Stopping Minecraft server...")
        try:
            subprocess.run(
                ["screen", "-S", SCREEN_NAME, "-X", "stuff", "stop\n"], check=True
            )
            await msg.edit(content="Server stopped. Waiting before restart...")
            await asyncio.sleep(5)  # Wait for clean shutdown
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to stop server: {e}")
            return

        # Start the server
        await msg.edit(content="Starting Minecraft server...")
        try:
            subprocess.run(
                ["screen", "-dmS", SCREEN_NAME, "bash", "-c", _get_start_cmd()],
                check=True,
            )
            await msg.edit(content="Minecraft server restarted successfully!")
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to start server: {e}")
