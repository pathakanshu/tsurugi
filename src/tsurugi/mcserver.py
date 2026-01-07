import asyncio
import json
import os
import subprocess

SCREEN_NAME = "mcserver"
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "server_info.json")

try:
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
except FileNotFoundError:
    raise FileNotFoundError("Server configuration file not found." + CONFIG_PATH)

MINECRAFT_PATH = config["minecraft"]["path"]
JAR_PATH = os.path.join(MINECRAFT_PATH, config["minecraft"]["jar_file_name"])
CPU_QUOTA = config["minecraft"].get("cpu_quota", 60)  # Default to 60% if not specified
MEMORY_LIMIT_GB = config["minecraft"].get(
    "memory_limit_gb", 12
)  # Default to 12GB if not specified
LOG_FILE = os.path.join(MINECRAFT_PATH, "logs", "latest.log")


START_CMD: list[str] = [
    "java",
    f"-Xms{MEMORY_LIMIT_GB}G",
    f"-Xmx{MEMORY_LIMIT_GB}G",
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

            # Use systemd-run to escape bot's cgroup memory limits
            # CPUQuota limits the server CPU usage (configurable in server_info.json)
            systemd_cmd = [
                "sudo",
                "systemd-run",
                "--scope",
                "--unit=minecraft-server",
                f"--property=CPUQuota={CPU_QUOTA}%",
                f"--property=MemoryMax={MEMORY_LIMIT_GB}G",
                "--setenv=HOME=/home/ubuntu",
                "--uid=ubuntu",
                "--gid=ubuntu",
                "screen",
                "-dmS",
                SCREEN_NAME,
                "bash",
                "-c",
                cmd,
            ]

            subprocess.run(systemd_cmd, check=True)
            await asyncio.sleep(1)

            if server_is_running():
                await msg.edit(content="Screen session started...")
            else:
                await msg.edit(
                    content="Screen session created but server may not be running. Check logs."
                )
        except subprocess.CalledProcessError as e:
            await msg.edit(content=f"Failed to start Minecraft server: {e}")
    except Exception as e:
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
        await ctx.send(f"Unexpected error: {e}")


async def restart_server(ctx):
    if not server_is_running():
        await ctx.send("Minecraft server is not running!")
        return

    await stop_server(ctx)
    await ctx.send("Waiting 5s for clean shutdown...")
    await asyncio.sleep(5)  # Wait for clean shutdown
    await start_server(ctx)


async def console_command(ctx, command: str):
    """
    Execute a console command in the Minecraft server.
    Only works if the server is running.
    Captures and returns the console output.
    """
    if not server_is_running():
        await ctx.send("❌ Minecraft server is not running!")
        return

    try:
        # Get current log file size to know where to start reading
        log_size_before = os.path.getsize(LOG_FILE) if os.path.exists(LOG_FILE) else 0

        # Send the command to the screen session
        subprocess.run(
            ["screen", "-S", SCREEN_NAME, "-X", "stuff", f"{command}\n"],
            check=True,
        )

        # Wait a bit for the command to execute and log
        await asyncio.sleep(0.5)

        # Read new log entries
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                f.seek(log_size_before)
                new_logs = f.read()

            # Extract relevant output (filter out some noise)
            lines = new_logs.strip().split("\n")
            relevant_lines = []
            for line in lines:
                # Skip empty lines and DiscordSRV chat echoes
                if line and "INFO]:" in line and "[DiscordSRV]" not in line:
                    # Extract just the message part after timestamp
                    parts = line.split("INFO]: ", 1)
                    if len(parts) > 1:
                        relevant_lines.append(parts[1])

            if relevant_lines:
                output = "\n".join(relevant_lines[:5])  # Limit to 5 lines
                await ctx.send(f"```\n{output}\n```")
            else:
                await ctx.send(f"✅ Command sent: `{command}`")
        else:
            await ctx.send(f"✅ Command sent: `{command}` (log file not found)")

    except subprocess.CalledProcessError as e:
        await ctx.send(f"❌ Failed to send command: {e}")
    except Exception as e:
        await ctx.send(f"❌ Error reading output: {e}")
