import discord
import os
import urllib.request , urllib.parse, urllib.error
import json
from datetime import datetime
from dotenv import load_dotenv


####################################################################################################

def contestList():
    fhand = urllib.request.urlopen('https://codeforces.com/api/contest.list').read().decode()
    try:
        js = json.loads(fhand)
        if(js['status']=='OK'):
            if(len(js['result'])>0):
                contests = []
                for data in js['result']:
                    if(data['phase']=='BEFORE'):
                        contests.append(data)
                st = ''
                st = st+"= UPCOMING CONTESTS ON CODEFORCES =\n"
                for data in contests:
                    time = data['startTimeSeconds']
                    st = st + "==================================\n"
                    st = st + "Contest ID   : "+str(data['id'])+"\n"
                    st = st + "Contest Name : "+str(data['name'])+"\n"
                    st = st + "Start Time   : "+str( datetime.utcfromtimestamp(time))+"\n"
                    st = st + "End Time     : "+str(datetime.utcfromtimestamp(time + data['durationSeconds']))+"\n"
                    st = st + "==================================\n" 
                return st
            else:
                return "===No Contest in near future. Please check again later.==="        
    except:
        return '====Failed to load data===='

###########################################################################################################

def ratingChange(handle):
    handle = urllib.request.urlopen('https://codeforces.com/api/user.rating?handle='+handle)
    fhand = handle.read().decode()
    try:
        js = json.loads(fhand)
        if(js['status']=='OK'):
            st = ''
            st = st + "==================================\n" 
            st = st + "=    Last round participated : "+str(js['result'][-1]['contestName'])+"\n"
            st = st + "=    Old Rating              : "+str(js['result'][-1]['oldRating'])+"\n"
            st = st + "=    New Rating              : "+str(js['result'][-1]['newRating'])+"\n"
            st = st + "=    Rank                    : "+str(js['result'][-1]['rank'])+"\n"
            st = st + "==================================\n"
            return st
    except:
        return "====Failed to load data===="

##################################################################################################################

def userInfo(li):
    s = ';'.join(li)
    handle = urllib.request.urlopen('https://codeforces.com/api/user.info?handles='+s)
    fhand = handle.read().decode()
    try:
        js = json.loads(fhand)
        if(js['status']=='OK'):
            st = ''
            for data in js['result'] :
                st = st + "==================================\n"
                st = st + "=    Handle         : "+str(data['handle'])+'\n'
                st = st + "=    Max Rank       : "+str(data['maxRank'])+'\n'
                st = st + "=    Max Rating     : "+str(data['maxRating'])+'\n'
                st = st + "=    Current Rank   : "+str(data['rank'])+'\n'
                st = st + "=    Current Rating : "+str(data['rating'])+'\n'
                st = st + "==================================\n"
            return st    
    except:
        return "====Failed to load data===="   
#############################################################################################################

def ranklist(contestid , competitors):
    ranklist = []
    s = ';'.join(competitors)
    handle = urllib.request.urlopen('https://codeforces.com/api/contest.standings?contestId='+contestid+'&from=1&handles='+s)
    fhand = handle.read().decode()
    try:
        js = json.loads(fhand)
        if(js['status']=='OK'):
            rank = 1
            st = ''
            st = st + "==================================\n"
            st = st + "==       Custom Ranklist        ==\n"
            st = st + "==================================\n\n"
            st = st + " Sl.  Points       Handle\n"
            for data in js['result']['rows'] :
                st = st + "=>   "+str(rank)+'        '+str(int(data['points']))+'         '+(data['party']['members'][0]['handle'])+'\n' 
                rank += 1   
            return st                

    except:
        return "====Failed to load data===="         

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
        if message.content.startswith('$contests'):
            msg = contestList()
            await message.channel.send(msg)
        elif message.content.startswith('$rating'):
            msg = message.content.split()
            res = ratingChange(msg[1])
            await message.channel.send(res)
        elif message.content.startswith('$user'):
            msg = message.content.split()
            res = userInfo(msg[1:])
            await message.channel.send(res)
        elif message.content.startswith('$ranklist'):
            msg = message.content.split()
            res = ranklist(msg[1] , msg[2:])
            await message.channel.send(res)            
    except:
        await message.channel.send('Sorry, there is some error in your syntax') 

load_dotenv()
client.run(os.getenv("TOKEN"))

    ####################################################################################################
  ########################################################################################################
############################################################################################################
  ########################################################################################################
    ####################################################################################################