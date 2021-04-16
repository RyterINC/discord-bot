from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='twitch_set', help='Post your twitch username for people to see')
    async def twitch_set(self, ctx, username):
            
        await ctx.send()
