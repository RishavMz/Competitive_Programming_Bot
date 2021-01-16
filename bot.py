import discord
import os
from dotenv import load_dotenv
from files.codeforces import *
from files.codechef import *
from discord.ext import commands, tasks

####################################################################################################

client = discord.Client()                           #initializing bot

@tasks.loop(hours=24)                               # Loop runs every 24 hours 
async def called_once_a_day(message):               # Sets remainder about upcoming contests
    msg1 = cfContestList()
    await message.channel.send(msg1)
    msg2 = ccContestList()
    await message.channel.send(msg2)

@client.event
async def on_ready():                               #check if bot loaded(ready)
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):                      #check if message recieved(read by bot)
    if message.author == client.user:               
        return                                      #if message was sent by itself
    try:
        if message.content.startswith('$cfcontests'):   #Following command list
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
        called_once_a_day.start(message)      
    except:
        await message.channel.send('Sorry, there is some error in your syntax') 

load_dotenv()
client.run(os.getenv("TOKEN"))                          # 

####################################################################################################
