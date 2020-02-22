import discord 
import datetime 
import json

from discord.ext import commands
from discord.ext import tasks

from datetime import datetime

f_name = 'UserList.json'
backup_folder = './backups/'

def current_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

class UserList(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.user_list = {}
        self.update.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("UserList ready {}".format(current_time()))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        user = message.author
        if user in self.user_list:
            self.user_list[user] += 1
        else:
            self.user_list[user] = 1

    @commands.command()
    async def show_user(self, ctx, user):
        user = user.capitalize()
        if user in self.user_list:
            await ctx.send('{} has: {}'.format(user, self.user_list[user]))
        else:
            await ctx.send('User does not exist')
    
    @commands.command()
    async def show_userlist(self, ctx):
        output = ""
        for user in self.user_list:
            output += '{}: {}\n '.format(user, self.user_list[user])
        await ctx.send('```This is the list of all users and the times they have sent a message:\n {}```'.format(output))
    
    @commands.command()
    async def clear_userlist(self, ctx):
        print("CLEARING USER FILE {}".format(current_time()))
        await ctx.send('CLEARING USER FILE')
        lst = []
        with open(f_name, 'w') as f:
            json.dump(lst, f)
        self.user_list.clear()
        print("USER FILE CLEARED {}".format(current_time()))
        await ctx.send('USER FILE CLEARED SUCCESSFULLY')
    
    @commands.command()
    async def create_backup_userlist(self, ctx):
        print("CREATING BACKUP {}".format(current_time()))
        await ctx.send("CREATING BACKUP")
        backup = []
        for user in self.user_list:
            item = {
                "name": user,
                "value": self.user_list[user]
            }
            backup.append(item)
        with open('{}backup_{}'.format(backup_folder,f_name), 'w') as f:
            json.dump(backup, f)
        print("BACKUP SUCCESSFUL {}".format(current_time()))
        await ctx.send("BACKUP SUCCESSFUL")
    
    @tasks.loop(seconds = 300)
    async def update(self):
        print("Updating User file automatically {}".format(current_time()))
        lst = []
        for user in self.user_list:
            item = {
                "name": user,
                "value": self.user_list[user]
            }
            lst.append(item)
        with open(f_name, 'w') as f:
            json.dump(lst, f)
        print("Update User file successful {}".format(current_time()))
    
    @update.before_loop
    async def before_update(self):
        print('Read User file {}'.format(current_time()))
        with open(f_name) as f:
            user_data = json.load(f)
        for users in user_data:
            self.user_list[users['name']] = users['value']
        print("Read User file successful {}".format((current_time())))
        await self.client.wait_until_ready()
    
def setup(client):
    client.add_cog(UserList(client))