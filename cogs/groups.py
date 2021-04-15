from botocore.exceptions import ClientError
from discord.ext import commands
import boto3
import json

class Groups(commands.Cog):

    def __init__(self, bot, stateFilePath, BUCKET_NAME, filename):
        self.bot = bot
        self.stateFilePath = stateFilePath
        self.BUCKET_NAME = BUCKET_NAME
        self.filename = filename
        self.s3 = boto3.resource('s3')


    @commands.command(name='group_create', help='Creates a notification group')
    async def roll(self, ctx, group_name):
        with open(self.stateFilePath) as infile:
            data = json.load(infile)
        
        if group_name in data["groups"]:
            message = "Group \"" + group_name + "\" already exists!"
        else:
            data["groups"][group_name] = []
            with open(self.stateFilePath, 'w') as outfile:
                json.dump(data, outfile, sort_keys=True, indent=4)
            message = "Group \"" + group_name + "\" created!"
            self.s3.meta.client.upload_file(self.stateFilePath, self.BUCKET_NAME, self.filename)
        await ctx.send(message)
