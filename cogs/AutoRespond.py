import discord
import datetime

from discord.ext import commands

from datetime import datetime

def current_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

class AutoRespond(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('AutoRespond ready {}'.format(current_time()))
    
def setup(client):
    client.add_cog(AutoRespond(client))