import discord 
import datetime 
import json
import os

from discord.ext import commands
from discord.ext import tasks

from datetime import datetime

f_name = 'UserList.json'
backup_folder = './backups/'
update_time = 300

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
        user = str(message.author)
        if user in self.user_list:
            self.user_list[user] += 1
        else:
            self.user_list[user] = 1

    @commands.command()
    async def show_user(self, ctx, user):
        user = user.capitalize()
        if user in self.user_list:
            await ctx.send('{} has: {} messages'.format(user, self.user_list[user]))
        else:
            await ctx.send('Cannot find user {}'.format(user))
    
    @commands.command()
    async def show_userlist(self, ctx):
        sorted_userlist = dict(sorted(self.user_list.items(), key=lambda x:x[1], reverse = True))
        output = ""
        count = 0
        for user in sorted_userlist:
            output += "{}: {} messages\n ".format(user, sorted_userlist[user])
            count += 1
            if count >= 25:
                break
        
        await ctx.send('```Top chatters:\n {}```'.format(output))

    @commands.command()
    async def clear_userlist(self, ctx):
        await ctx.send('Yeah right')
        # print("CLEARING USER FILE {}".format(current_time()))
        # await ctx.send('CLEARING USER FILE')
        # lst = []
        # with open(f_name, 'w') as f:
        #     json.dump(lst, f)
        # self.user_list.clear()
        # print("USER FILE CLEARED {}".format(current_time()))
        # await ctx.send('USER FILE CLEARED SUCCESSFULLY')
    
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
    
    @tasks.loop(seconds = update_time)
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
        if os.path.exists(f_name):
            print('Read User file {}'.format(current_time()))
            with open(f_name) as f:
                user_data = json.load(f)
            for users in user_data:
                self.user_list[users['name']] = users['value']
            print("Read User file successful {}".format((current_time())))
        else:
            print('{} does not exist. Creating file {}'.format(f_name, current_time()))
            with open(f_name, 'w') as f:
                json.dump([], f)
            print('{} created {}'.format(f_name, current_time()))
        
        await self.client.wait_until_ready()
    
def setup(client):
    client.add_cog(UserList(client))