import discord
import datetime

from discord.ext import commands
from datetime import datetime

def current_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

class ErrorHandling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('ErrorHandling Ready {}'.format(current_time()))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            #print('Command not found {}'.format(current_time()))
            await ctx.send('Command not found')
        else:
            print('{} {}'.format(error, current_time()))

def setup(client):
    client.add_cog(ErrorHandling(client))