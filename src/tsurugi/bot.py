import discord
from discord.ext import commands

from .config import DISCORD_TOKEN
from .database import store_messages

intents = discord.Intents.default()
intents.message_content = True  # Enable access to message content

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
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


@bot.command(name="storeMongo")
async def storeMongo(ctx):
    # Goes through all messsages in the current channel and stores all data into a MongoDB database
    # MongoDB connection details are stored in environment variables
    # 
    # This command should be used with caution as it may take a long time to complete
    
    await ctx.send("Storing messages to MongoDB. This may take a while...")
    count = await store_messages(ctx)
    await ctx.send(f"Stored {count} messages to MongoDB.")


if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
