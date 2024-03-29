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


    @commands.command(name='group.create', help='Creates a notification group')
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


    @commands.command(name='group.delete', help='Deletes a notification group')
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


    @commands.command(name='group.list', help='List all notification groups')
    async def group_list(self, ctx):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        if len(data["groups"]) == 0:
            message = "There are currently no notification groups" 
            await ctx.send(message)
            return
        message = '❗Current notification groups❗\n>>> '
        for group in data["groups"].keys():
            message = message + group + '\n'

        await ctx.send(message)


    @commands.command(name='member.add', help='Adds a member to a notification group')
    async def group_member_add(self, ctx, group_name, member: discord.Member):

        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if group_name not in data["groups"]:
            message = "Group **" + group_name + "** doesn't exist. To view current groups, use command !group_list"
            await ctx.send(message)
            return

        if member.id in data["groups"][group_name]:
            message = "Discord member **" + member.name + "** is already in group + **" + group_name + "**"
            await ctx.send(message)
            return

        if ctx.guild.get_member(member.id) == None:
            message = "**" + member.name + "** is not a member in the **" + self.guildName + "** Discord server."
            await ctx.send(message)
            return
        else:
            data["groups"][group_name].append(member.id)
            with open(self.stateFilePath, 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
            message = "Member **" + member.name + "** has been added to the **" + group_name + "** notification group!"
            self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)
            await ctx.send(message)
 

    @commands.command(name='member.remove', help='Removes a member from a notification group')
    async def group_member_remove(self, ctx, group_name, member: discord.Member):

        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if group_name not in data["groups"]:
            message = "Group **" + group_name + "** doesn't exist. To view current groups, use command !group_list"
            await ctx.send(message)

        if member.id not in data["groups"][group_name]:
            message = "Discord member **" + member.name + "** isn't in group + **" + group_name + "**"
            await ctx.send(message)
        else:
            data["groups"][group_name].remove(member.id)
            with open(self.stateFilePath, 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
            message = "Member **" + member.name + "** has been removed from notification group **" + group_name + "**!"
            self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)
            await ctx.send(message)


    @commands.command(name='member.list', help='Lists all members in a notification group')
    async def group_member_list(self, ctx, group_name):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if group_name not in data["groups"]:
            message = "Group **" + group_name + "** doesn't exist. To view current groups, use command !group_list"
            await ctx.send(message)
            return

        if len(data["groups"][group_name]) == 0:
            message = "There are no members in the notification group **" + group_name + "**."
            await ctx.send(message)
        else:
            message = "❗Current members in **" + group_name + "** notification group❗\n>>> "
            for m_id in data["groups"][group_name]:
                member = ctx.guild.get_member(m_id)
                message = message + member.name + '\n'
            await ctx.send(message)


    @commands.command(name='notify', help='Sends a message to all members of a notification group - EX: !group_notify raid-one')
    async def group_notify(self, ctx, group_name):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)

        if group_name not in data["groups"]:
            message = "Group **" + group_name + "** doesn't exist. To view current groups, use command !group_list"
            await ctx.send(message)

        if len(data["groups"][group_name]) == 0:
            message = "There are no members in the notification group **" + group_name + "**."
            await ctx.send(message)
        else:
            message = ":mega: " + "Notifying " + group_name + " :mega:\n"
            for member in data["groups"][group_name]:
                message = message + "<@" + str(member) + "> "
            await ctx.send(message)
