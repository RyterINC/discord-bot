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

    @commands.command(name='roll.dice', help='Rolls X dice with Y sides')
    async def roll(self, ctx, number_of_dice: int, number_of_sides: int):
        dice = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await ctx.send(', '.join(dice))


    @commands.command(name='give.nuts', help='Give a member a kupo nut! (Karma points)')
    async def give_nuts(self, ctx, member: discord.Member):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if str(member.id) not in data["member-general"].keys():
            data["member-general"][str(member.id)] = {}
            data["member-general"][str(member.id)]["nuts"] = 0

        data["member-general"][str(member.id)]["nuts"] += 1
        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        total = data["member-general"][str(member.id)]["nuts"]
        message = "<@" + str(member.id) + ">" + " You received a kupo nut from " + ctx.message.author.name + "! You have **" + str(total) + "** kupo nuts!"
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)           
        await ctx.send(message)


    @commands.command(name='list.nuts', help='Find out how many kupo nuts a member has')
    async def list_nuts(self, ctx, member: discord.Member):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if str(member.id) not in data["member-general"].keys():
            data["member-general"][str(member.id)] = {}
            data["member-general"][str(member.id)]["nuts"] = 0
            message = "<@" + str(member.id) + ">" + " has **0** kupo nuts. Be the first to give them a kupo nut, kupo!."
            await ctx.send(message)
        else:
            total = data["member-general"][str(member.id)]["nuts"]
            message = "<@" + str(member.id) + ">" + " has **" + str(total) + "** kupo nuts"
            await ctx.send(message)
