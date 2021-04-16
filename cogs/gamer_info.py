from discord.ext import commands
import discord
import boto3
import json

class GamerInfo(commands.Cog):
    def __init__(self, bot, stateFilePath, BUCKET_NAME, filename, GUILD):
        self.bot = bot
        self.stateFilePath = stateFilePath
        self.BUCKET_NAME = BUCKET_NAME
        self.filename = filename
        self.s3 = boto3.resource('s3')
        self.guildName = GUILD

    @commands.command(name='twitch_set', help='Update gamer info with Twitch username')
    async def twitch_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["twitch"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "Twitch username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='psn_set', help='Update gamer info with PSN username')
    async def psn_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["PSN"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "PSN username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='switch_set', help='Update gamer info with Switch username')
    async def switch_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["Switch"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "Switch username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='steam_set', help='Update gamer info with Steam username')
    async def steam_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["Steam"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "Steam username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='switch_friend_code_set', help='Update gamer info with Switch friend code')
    async def switch_friend_code_set(self, ctx, friend_code):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["Switch-friend-code"] = friend_code

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "Switch friend code **" + friend_code + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='xbox_set', help='Update gamer info with Xbox username')
    async def xbox_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["Xbox"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "Xbox username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='battlenet_set', help='Update gamer info with Battle.net username')
    async def battlenet_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["Battle-net"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "Battle.net username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='origin_set', help='Update gamer info with Origin username')
    async def origin_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["Origin"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "Origin username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='epic_set', help='Update gamer info with Epic username')
    async def epic_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["Epic"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "Epic username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)


    @commands.command(name='rockstar_set', help='Update gamer info with RockStar username')
    async def rockstar_set(self, ctx, username):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        member_id = str(ctx.message.author.id)
        if member_id not in data["gamer-info"]:
            data["gamer-info"][member_id] = {}
        data["gamer-info"][member_id]["RockStar"] = username

        with open(self.stateFilePath, 'w') as outfile:
            json.dump(data, outfile, sort_keys=True, indent=4)
        self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        message = "RockStar username **" + username + "** updated in **" + ctx.message.author.name + "** gamer info!"
        await ctx.send(message)
