from discord.ext import commands
import boto3
import discord
import json
import random

class Utility(commands.Cog):
    def __init__(self, bot, stateFilePath, BUCKET_NAME, filename, GUILD):
        self.bot = bot
        self.stateFilePath = stateFilePath
        self.BUCKET_NAME = BUCKET_NAME
        self.filename = filename
        self.s3 = boto3.resource('s3')
        self.guildName = GUILD

    @commands.command(name='roll_dice', help='Rolls X dice with Y sides')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))


    @commands.command(name='give_korok_seed', help='Give a member a Korok seed! (Karma points)')
    async def give_korok_seed(self, ctx, member: discord.Member):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if str(member.id) not in data["member-general"].keys():
            data["member-general"][str(member.id)] = {}
            data["member-general"][str(member.id)]["koroks"] = 0

        data["member-general"][str(member.id)]["koroks"] += 1
        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        message = "<@" + str(member.id) + ">" + "You received a Korok seed! Yahaha!\n http://gph.is/2Flp8en"
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)           
        await ctx.send(message)


    @commands.command(name='list_korok_seeds', help='Find out how many korok seeds a member has')
    async def list_korok_seeds(self, ctx, member: discord.Member):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if str(member.id) not in data["member-general"].keys():
            data["member-general"][str(member.id)] = {}
            data["member-general"][str(member.id)]["koroks"] = 0
            message = "<@" + str(member.id) + ">" + " has **0** korok seeds. Why don't you give them a seed you monster."
            await ctx.send(message)
        else:
            total = data["member-general"][str(member.id)]["koroks"]
            message = "<@" + str(member.id) + ">" + " has **" + str(total) + "** korok seeds"
            await ctx.send(message)
