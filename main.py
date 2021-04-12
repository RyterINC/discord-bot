import os
from dotenv import load_dotenv
from discord.ext import commands
import boto3
from botocore.exceptions import ClientError
from cogs import greetings, util


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BUCKET_NAME = os.getenv('DISCORD_S3_BUCKET')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

bot.add_cog(greetings.Greetings(bot))
bot.add_cog(util.Utility(bot))

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


s3 = boto3.resource('s3')
filename = GUILD + "_" + "state.json"
bucket = s3.Bucket(BUCKET_NAME)
objs = list(bucket.objects.filter(Prefix=filename))
path = "./state/"

if os.path.isdir(path) == False:
    os.mkdir("./state")

if any([w.key == filename for w in objs]):
    print("State file exists for " + GUILD + " Discord server...")
    if os.path.isfile(path + filename):
        os.remove(path + filename)

    s3.meta.client.download_file(BUCKET_NAME, filename, path + filename)
else:
    print("State file does not exist for " + GUILD + " Discord server, creating...")
    f = open(path + filename, 'w')
    f.write('{}')
    s3.meta.client.upload_file(path + filename, BUCKET_NAME, filename)



bot.run(TOKEN)
