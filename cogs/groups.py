from discord.ext import commands
import discord
import boto3
import json

class Groups(commands.Cog):

    def __init__(self, bot, stateFilePath, BUCKET_NAME, filename, GUILD):
        self.bot = bot
        self.stateFilePath = stateFilePath
        self.BUCKET_NAME = BUCKET_NAME
        self.filename = filename
        self.s3 = boto3.resource('s3')
        self.guildName = GUILD


    @commands.command(name='group_create', help='Creates a notification group')
    async def group_create(self, ctx, group_name):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if group_name in data["groups"]:
            message = "Group **" + group_name + "** already exists!"
        else:
            data["groups"][group_name] = []
            with open(self.stateFilePath, 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
            message = "Group **" + group_name + "** created!"
            self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        await ctx.send(message)


    @commands.command(name='group_delete', help='Deletes a notification group')
    async def group_delete(self, ctx, group_name):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if group_name not in data["groups"]:
            message = "Group **" + group_name + "** doesn't exist!"
        else:
            del data["groups"][group_name]
            with open(self.stateFilePath, 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
            message = "Group **" + group_name + "** deleted!"
            self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)

        await ctx.send(message)


    @commands.command(name='group_list', help='List all notification groups')
    async def group_list(self, ctx):
        message = '❗Current notification groups❗\n>>> '
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        for group in data["groups"].keys():
            message = message + group + '\n'

        await ctx.send(message)


    @commands.command(name='group_member_add', help='Adds a member to a notification group')
    async def group_member_add(self, ctx, group_name, member_name):

        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        for guild in self.bot.guilds:
            if guild.name == self.guildName:
                break

        if group_name not in data["groups"]:
            message = "Group **" + group_name + "** doesn't exist. To view current groups, use command !group_list"
            await ctx.send(message)

        if member_name in data["groups"][group_name]:
            message = "Discord member **" + member_name + "** is already in group + **" + group_name + "**"
            await ctx.send(message)

        if guild.get_member_named(member_name) == None:
            message = "**" + member_name + "** is not a member is the **" + self.guildName + "** Discord server."
            await ctx.send(message)
        else:
            data["groups"][group_name].append(member_name)
            with open(self.stateFilePath, 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
            message = "Member **" + member_name + "** has been added to the **" + group_name + "** notification group!"
            self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)
            await ctx.send(message)
 

    @commands.command(name='group_member_remove', help='Removes a member from a notification group')
    async def group_member_remove(self, ctx, group_name, member_name):

        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if group_name not in data["groups"]:
            message = "Group **" + group_name + "** doesn't exist. To view current groups, use command !group_list"
            await ctx.send(message)

        if member_name not in data["groups"][group_name]:
            message = "Discord member **" + member_name + "** isn't in group + **" + group_name + "**"
            await ctx.send(message)
        else:
            data["groups"][group_name].remove(member_name)
            with open(self.stateFilePath, 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
            message = "Member **" + member_name + "** has been removed from notification group **" + group_name + "**!"
            self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)
            await ctx.send(message)


