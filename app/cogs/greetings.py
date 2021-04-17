from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
      await member.create_dm()
      await member.dm_channel(
          f'Hey {member.name}, you\'re finally awake. Welcome to the Auh! Discord server!'
      )
