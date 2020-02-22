import discord
import datetime

from discord.ext import commands
from datetime import datetime

def current_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

class Ping(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('Ping ready {}'.format(current_time()))

    @commands.command()
    async def ping(self, ctx):
        print('pong {}ms {}'.format(round(self.client.latency * 1000), current_time()))
        await ctx.send('pong {}ms'.format(round(self.client.latency * 1000)))

def setup(client):
    client.add_cog(Ping(client))