# bot.py
import os
import random
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel(
      f'Hey {member.name}, you\'re finally awake. Welcome to the Auh! Discord server!'
  )

bot.run(TOKEN)
