import discord
import os
from dotenv import load_dotenv
from files.codeforces import *
from files.codechef import *

####################################################################################################

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
        if message.content.startswith('$cfcontests'):
            msg = cfContestList()
            await message.channel.send(msg)
        elif message.content.startswith('$cfrating'):
            msg = message.content.split()
            res = cfRatingChange(msg[1])
            await message.channel.send(res)
        elif message.content.startswith('$cfuser'):
            msg = message.content.split()
            res = cfUserInfo(msg[1:])
            await message.channel.send(res)
        elif message.content.startswith('$cfranklist'):
            msg = message.content.split()
            res = cfRanklist(msg[1] , msg[2:])
            await message.channel.send(res)  
        elif message.content.startswith('$cccontests'):
            msg = ccContestList()
            await message.channel.send(msg) 
        elif message.content.startswith('$ccuser'):
            msg = message.content.split()
            res = ccUserInfo(msg[1])
            await message.channel.send(res)                 
    except:
        await message.channel.send('Sorry, there is some error in your syntax') 

load_dotenv()
client.run(os.getenv("TOKEN"))

####################################################################################################
