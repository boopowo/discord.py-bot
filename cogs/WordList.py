import discord 
import datetime 
import json
import os

from discord.ext import commands
from discord.ext import tasks

from datetime import datetime

f_name = 'WordList.json'
backup_folder = './backups/'
update_time = 300

def current_time():
    return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

class WordList(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.word_list = {}
        self.update.start()
    
    @commands.Cog.listener()
    async def on_ready(self):
        print('WordList ready {}'.format(current_time()))
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return 
        elif message.content.startswith('/'):
            return
        m = message.content.lower()
        msplt = m.split()
        for i in range(len(msplt)):
            s =""
            for j in range(len(msplt[i])):
                if msplt[i][j].isalnum():
                    s += msplt[i][j]
            if len(s) == 0:
                pass
            elif s in self.word_list:
                self.word_list[s] += 1
            else:
                self.word_list[s] = 1
        
    @commands.command()
    async def show_word(self, ctx, word):
        word = word.lower()
        if word in self.word_list:
            await ctx.send('{} has appeared: {} times'.format(word, self.word_list[word]))
        else:
            await ctx.send('Cannot find message with {} '.format(word))

    @commands.command()
    async def show_wordlist(self, ctx):
        sorted_wordlist = dict(sorted(self.word_list.items(), key = lambda x:x[1], reverse = True))
        output = ""
        count = 0
        for word in sorted_wordlist:
            output += '{}: {} times\n '.format(word, sorted_wordlist[word])
            count+= 1
            if count >= 25:
                break
        await ctx.send('```Top 25 words:\n {}```'.format(output))
            
    @commands.command()
    async def clear_wordlist(self, ctx):
        await ctx.send('Yeah right')
        # print("CLEARING WORD LIST FILE {}".format(current_time()))
        # await ctx.send("CLEARING WORD LIST FILE")
        # lst = []
        # with open(f_name, 'w') as f:
        #     json.dump(lst, f)
        # self.word_list.clear()
        # print("WORD LIST FILE CLEARED {}".format(current_time()))
        # await ctx.send('WORD LIST FILE CLEARED SUCCESSFULLY')
    
    @commands.command()
    async def create_backup_wordlist(self, ctx):
        print("CREATING BACKUP {}".format(current_time()))
        await ctx.send("CREATING BACKUP")
        backup = []
        for word in self.word_list:
            item = {
                "word": word,
                "value": self.word_list[word]
            }
            backup.append(item)
        with open('{}backup_{}'.format(backup_folder,f_name), 'w') as f:
            json.dump(backup, f)
        print("BACKUP SUCCESSFUL {}".format(current_time()))
        await ctx.send("BACKUP SUCCESSFUL")

    @tasks.loop(seconds = update_time)
    async def update(self):
        print("Updating Word List file automatically {}".format(current_time()))
        lst = []
        for word in self.word_list:
            item = {
                "word": word,
                "value": self.word_list[word]
            }
            lst.append(item)
        with open(f_name, 'w') as f:
            json.dump(lst, f)
        print("Update Word List file successful {}".format(current_time()))

    @update.before_loop
    async def before_update(self):
        if os.path.exists(f_name):
            print('Read Word List file {}'.format(current_time()))
            with open(f_name) as f:
                word_data = json.load(f)
            for words in word_data:
                self.word_list[words['word']] = words['value']
            print("Read Word List file successful {}".format(current_time()))
        else:
            print('{} does not exist. Creating file {}'.format(f_name, current_time()))
            with open(f_name, 'w') as f:
                json.dump([], f)
            print('{} created {}'.format(f_name, current_time()))
        await self.client.wait_until_ready()

def setup(client):
    client.add_cog(WordList(client))