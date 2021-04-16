from cogs import greetings, util, groups
from discord.ext import commands
import discord
from dotenv import load_dotenv
from shutil import copyfile
import boto3
import json
import os

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BUCKET_NAME = os.getenv('DISCORD_S3_BUCKET')
GUILD = os.getenv('DISCORD_GUILD')

path = "./state/"
filename = GUILD + "_" + "state.json"
stateFilePath = path + filename
templateFilePath = "./templates/state-template.json"
s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)
objs = list(bucket.objects.filter(Prefix=filename))
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)
template_update = False

bot.add_cog(greetings.Greetings(bot))
bot.add_cog(util.Utility(bot))
bot.add_cog(groups.Groups(bot, stateFilePath, BUCKET_NAME, filename, GUILD))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


if os.path.isdir(path) == False:
    os.mkdir("./state")

if any([w.key == filename for w in objs]):
    print("State file exists for " + GUILD + " Discord server...")
    if os.path.isfile(stateFilePath):
        os.remove(stateFilePath)
    s3.meta.client.download_file(BUCKET_NAME, filename, stateFilePath)
    with open(stateFilePath) as s_infile:
        state_data = json.load(s_infile)
    with open(templateFilePath) as t_infile:
        template_data = json.load(t_infile)
    for key in template_data.keys():
        if key not in state_data.keys():
            state_data[key] = []
            template_update = True
    if template_update:
        with open(stateFilePath, 'w') as s_outfile:
            json.dump(state_data, s_outfile, sort_keys=True, indent=4)
        s3.meta.client.upload_file(stateFilePath, BUCKET_NAME, filename)

else:
    print("State file does not exist for " + GUILD + " Discord server, creating...")

    copyfile(templateFilePath, stateFilePath)
    s3.meta.client.upload_file(stateFilePath, BUCKET_NAME, filename)


bot.run(TOKEN)
