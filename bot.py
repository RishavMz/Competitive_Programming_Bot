import discord
import os
from dotenv import load_dotenv
from files.codeforces import *
from files.codechef import *
from discord.ext import commands, tasks
from discord.ext.commands import Bot


####################################################################################################

helpmessage = '\n\n===================\n'
helpmessage = helpmessage + '    COMMAND LIST\n'
helpmessage = helpmessage + '\n\n===================\n'
helpmessage = helpmessage + '$$cfcontests \n'
helpmessage = helpmessage + 'Displays a list of upcoming contests on codeforces \n\n'
helpmessage = helpmessage + '$$cfrating [userhandle] \n'
helpmessage = helpmessage + 'Displays rating change for the last round of the given user on codeforces \n\n'
helpmessage = helpmessage + '$$cfuser [userhandle1] [userhandle2]......\n'
helpmessage = helpmessage + 'Displays user details(rank , rating , maxrating etc of the given users) on codeforces \n\n'
helpmessage = helpmessage + '$$cfranklist [contestid] [userhandle1] [userhandle2].... \n'
helpmessage = helpmessage + 'Displays a custom ranklist using the given users on codeforces \n\n'
helpmessage = helpmessage + '$$cccontests \n'
helpmessage = helpmessage + 'Displays a list of upcoming rated contests on codechef \n\n'
helpmessage = helpmessage + '$$ccuser [userhandle] \n'
helpmessage = helpmessage + 'Displays user details(star , rating , maxrating etc of the given user) on codechef \n\n'
helpmessage = helpmessage + '$$startbotnotifier \n'
helpmessage = helpmessage + 'The bot would check for present and upcoming contests (in both codeforces and codechef) every 24 hours and notify the server members(starting from the moment this command is given)\n\n'
helpmessage = helpmessage + '$$stopbotnotifier \n'
helpmessage = helpmessage + 'Turn off the timed message feature which repeats every 24 hours. \n\n'
helpmessage = helpmessage + '$$ccdbusers  \n'
helpmessage = helpmessage + 'Displays a ranklist from users whose handles are stored in database(for codechef) \n\n'
helpmessage = helpmessage + '$$ccdbadd [userhandle] \n'
helpmessage = helpmessage + 'Adds the user with given handle(username) to the database(for codechef) \n'
helpmessage = helpmessage + '$$cfdbusers  \n'
helpmessage = helpmessage + 'Displays a ranklist from users whose handles are stored in database(for codeforces) \n\n'
helpmessage = helpmessage + '$$cfdbadd [userhandle] \n'
helpmessage = helpmessage + 'Adds the user with given handle(username) to the database(for codeforces) \n'
helpmessage = helpmessage + '$$help \n'
helpmessage = helpmessage + 'Get command list\n.\n\n\n\n'

######################################################################################################

client = discord.Client()                           #initializing bot

loop = 0


@tasks.loop(hours=24)                               # Loop runs every 24 hours 
async def called_once_a_day(message):               # Sets remainder about upcoming contests
    msg1 = cfContestList()
    msg2 = ccContestList()
    await embed(message.channel,(msg1+"\n.\n.\n.\n.\n."+msg2))
    ccUpdateDatabase()
    cfUpdateDatabase()


#@tasks.loop(seconds=600)                               # Loop runs every 60 seconds 
#async def stay_awake():                                # keeps the bot awake
#    print("#")


bot = Bot("!")
@bot.command()
async def embed(channel,text):
    embed=discord.Embed( description=text, color=discord.Color.blue())
    await channel.send(embed=embed)

@client.event
async def on_ready():                               #check if bot loaded(ready)
    print('We have logged in as {0.user}'.format(client))
    #.await stay_awake()

@client.event
async def on_message(message):                      #check if message recieved(read by bot)
    global loop
    if message.author == client.user:               
        return                                      #if message was sent by itself
    try:
        if message.content.startswith('$$cfcontests'):   #Following command list
            msg = cfContestList()
            await embed(message.channel,msg)

        elif message.content.startswith('$$cfrating'):
            msg = message.content.split()
            res = cfRatingChange(msg[1])
            await embed(message.channel,res)

        elif message.content.startswith('$$cfuser'):
            msg = message.content.split()
            res = cfUserInfo(msg[1:])
            await embed(message.channel,res)

        elif message.content.startswith('$$cfranklist'):
            msg = message.content.split()
            res = cfRanklist(msg[1] , msg[2:])
            await embed(message.channel,res)  

        elif message.content.startswith('$$cccontests'):
            msg = ccContestList()
            await embed(message.channel,msg)

        elif message.content.startswith('$$ccuser'):
            msg = message.content.split()
            res = ccUserInfo(msg[1])
            await embed(message.channel,res)

        elif message.content.startswith('$$help'):
            await embed(message.channel,helpmessage)           

        elif message.content.startswith('$$startbotnotifier'):   
            if loop == 0 :    
                loop = 1             
                called_once_a_day.start(message) 
            else:
                await embed(message.channel,'Notifier already set for this channel') 

        elif message.content.startswith('$$stopbotnotifier'):
            if(loop == 1):
                loop = 0
                called_once_a_day.stop()
            else:
                await embed(message.channel,'This feature cannot be disabled as it has not been enabled')

        elif message.content.startswith('$$ccdbusers'):
            res = ccGetUsersFromDatabase(message.guild.id)
            await message.channel.send(res)

        elif message.content.startswith('$$cfdbusers'):
            res = cfGetUsersFromDatabase(message.guild.id)
            await message.channel.send(res)

        elif message.content.startswith('$$cfdbadd'):
            msg = message.content.split()
            res = cfAddUser(msg[1],message.guild.id)
            await message.channel.send(res)                    
        elif message.content.startswith('$$ccdbadd'):
            msg = message.content.split()
            res = ccAddUser(msg[1],message.guild.id)
            await message.channel.send(res)
    except:
        await message.channel.send('Sorry, there is some error in your syntax') 

load_dotenv()
client.run(os.getenv("TOKEN"))                          # 

####################################################################################################
