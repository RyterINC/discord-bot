# bot.py
import os
from dotenv import load_dotenv
from discord.ext import commands
# import cogs
from cogs import greetings, util


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

bot.add_cog(greetings.Greetings(bot))
bot.add_cog(util.Utility(bot))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


bot.run(TOKEN)
