import os
from dotenv import load_dotenv
from discord.ext import commands
import discord
from db import insertStory, summarizeDB

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("online")

@bot.command(name='add-story')
async def addStory(ctx):
    
    # need userID, userName, serverID, serverName, message
    user_id = ctx.author.id
    user_name = ctx.author.name
    server_id = ctx.guild.id if ctx.guild else "Direct Message"
    server_name = ctx.guild.name if ctx.guild else "Direct Message"
    message_id = ctx.message.id
    message = ctx.message.content.replace("/add-story ", '')

    print(
        f'User ID: {user_id}\n'
        f'User Name: {user_name}\n'
        f'Server ID: {server_id}\n'
        f'Server Name: {server_name}\n'
        f'Message ID: {message_id}'
    )

    # send story to weaviate db
    storyDBID = insertStory(message, message_id, user_id, user_name, server_id, server_name)

    # depending on success, send inserted/not inserted message

    # TODO: Catch exceptions/error codes
    if (storyDBID == None):
        await ctx.send("There was an error when adding your story. Please try again!")
    else:
        await ctx.send(f"Story added! Here is the UUID of the message: {storyDBID}")

@bot.command(name='summarize')
async def summarize(ctx):
    message = ctx.message.content.replace("/summarize ", '')
    summary = summarizeDB(message)
    await ctx.send(summary)

bot.run(TOKEN)