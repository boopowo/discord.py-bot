import json
import discord
import os
import datetime

from discord.ext import commands
from datetime import datetime

client = commands.Bot(command_prefix = '/')
cog_dir = './cogs'
token = 'token'

def current_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

@client.event
async def on_ready():
    print('Bot ready {}'.format(current_time()))

#Load extension
@client.command()
async def load_cog(ctx, extension):
    client.load_extension('cogs.{}'.format(extension))
    print('{} loaded {}'.format(extension, current_time()))
    await ctx.send('{} loaded'.format(extension))

#Unload extension
@client.command()
async def unload_cog(ctx, extension):
    client.unload_extension('cogs.{}'.format(extension))
    print('{} unloaded {}'.format(extension, current_time()))
    await ctx.send('{} unloaded'.format(extension))

#Loads cogs in path
print('Loading cogs {}'.format(current_time()))
for f in os.listdir(cog_dir):
    if f.endswith('.py'):
        client.load_extension('cogs.{}'.format(f[:-3]))
        print("Loaded {} {}".format(f, current_time()))

client.run(token)
