import asyncio
import json
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

SCREEN_NAME = "mcserver"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "server_info.json")

try:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Server configuration file not found." + CONFIG_PATH)

MINECRAFT_PATH = config["minecraft"]["path"]
JAR_PATH = os.path.join(MINECRAFT_PATH, config["minecraft"]["jar_file_name"])


START_CMD: list[str] = [
    "java",
    "-Xms12G",
    "-Xmx16G",
    "-jar",
    str(JAR_PATH),
    "nogui",
]


def server_is_running():
    """Check if the screen session is already active"""
    result = subprocess.run(["screen", "-list"], capture_output=True, text=True)
    return SCREEN_NAME in result.stdout


async def start_server(ctx):
    try:
        if server_is_running():
            await ctx.send("Minecraft server is already running!")
            return

        msg = await ctx.send("Starting Minecraft server...")

        try:
            # Build command that changes directory before starting server
            cmd = f"cd {MINECRAFT_PATH} && {' '.join(START_CMD)}"
            logger.info(f"Starting Minecraft server with command: {cmd}")
            logger.info(f"MINECRAFT_PATH: {MINECRAFT_PATH}")
            logger.info(f"JAR_PATH: {JAR_PATH}")
            logger.info(f"START_CMD: {START_CMD}")

            # Use systemd-run to escape bot's cgroup memory limits
            # --scope creates a transient scope unit
            # --user runs as the current user (not system-wide)
            systemd_cmd = [
                "systemd-run",
                "--user",
                "--scope",
                "--unit=minecraft-server",
                "screen",
                "-dmS",
                SCREEN_NAME,
                "bash",
                "-c",
                cmd,
            ]
            logger.info(f"Full subprocess call: {' '.join(systemd_cmd)}")

            result = subprocess.run(
                systemd_cmd,
                capture_output=True,
                text=True,
                check=True,
            )
            logger.info(f"Subprocess stdout: {result.stdout}")
            logger.info(f"Subprocess stderr: {result.stderr}")

            # Give screen a moment to start
            await asyncio.sleep(1)

            # Check if it's actually running
            if server_is_running():
                await msg.edit(content="Minecraft server started successfully!")
            else:
                await msg.edit(
                    content="Screen session created but server may not be running. Check logs."
                )
        except subprocess.CalledProcessError as e:
            logger.error(f"CalledProcessError: {e}")
            logger.error(f"Error stdout: {e.stdout}")
            logger.error(f"Error stderr: {e.stderr}")
            await msg.edit(content=f"Failed to start Minecraft server: {e}")
    except Exception as e:
        logger.exception("Unexpected error in start_server")
        await ctx.send(f"Unexpected error: {e}")


async def stop_server(ctx):
    try:
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
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to stop Minecraft server: {e}")
    except Exception as e:
        logger.exception("Unexpected error in stop_server")
        await ctx.send(f"Unexpected error: {e}")


async def restart_server(ctx):
    try:
        if not server_is_running():
            await ctx.send("Minecraft server is not running!")
            return

        # Stop the server
        msg = await ctx.send("Stopping Minecraft server...")
        try:
            subprocess.run(
                ["screen", "-S", SCREEN_NAME, "-X", "stuff", "stop\n"], check=True
            )
            await asyncio.sleep(5)  # Wait for clean shutdown
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to stop server: {e}")
            return

        # Start the server
        await msg.edit(content="Starting Minecraft server...")
        try:
            # Build command that changes directory before starting server
            cmd = f"cd {MINECRAFT_PATH} && {' '.join(START_CMD)}"
            logger.info(f"Restarting Minecraft server with command: {cmd}")

            # Use systemd-run to escape bot's cgroup memory limits
            systemd_cmd = [
                "systemd-run",
                "--user",
                "--scope",
                "--unit=minecraft-server",
                "screen",
                "-dmS",
                SCREEN_NAME,
                "bash",
                "-c",
                cmd,
            ]

            subprocess.run(
                systemd_cmd,
                check=True,
            )
            await msg.edit(content="Minecraft server restarted successfully!")
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to start server: {e}")
    except Exception as e:
        logger.exception("Unexpected error in restart_server")
        await ctx.send(f"Unexpected error: {e}")
