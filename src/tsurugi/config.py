import os

import dotenv

# Load environment variables from a .env file
dotenv.load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
if not DISCORD_TOKEN:
    raise RuntimeError("DISCORD_BOT_TOKEN not set")
