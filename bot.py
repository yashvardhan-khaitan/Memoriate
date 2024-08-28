import os

from dotenv import load_dotenv
from discord.ext import commands
import discord

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("online")

@bot.command(name='add-story')
async def addStory(ctx):
    await ctx.send("Greatness from small beginnings")

bot.run(TOKEN)