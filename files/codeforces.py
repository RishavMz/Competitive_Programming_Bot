import os
import urllib.request , urllib.parse, urllib.error
import json
from datetime import datetime


####################################################################################################

def timeConvert(date):                                              # Convert from GMT to UTC(+5:30)
    date = str(datetime.utcfromtimestamp(date)).split()
    dat = date[0].split('-')
    modify = date[1].split(':')
    modify[0] = int(modify[0])+5
    modify[1] = int(modify[1]) + 30
    if(modify[1]>=60):
        modify[0] = str(modify[0] + modify[1] // 60)
        modify[1] = str(modify[1] % 60)
        if len(modify[0]) == 1 :
            modify[0] = '0'+modify[0]
        if len(modify[1]) == 1 :
            modify[1] = '0'+modify[1]    
    strdate = str(dat[2]) + '-' + str(dat[1]) + '-' + str(dat[0]) + '  '+ str(modify[0]) + ':' + str(modify[1]) + ':' + str(modify[2]); 
    return strdate

####################################################################################################
def cfContestList():
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
                st = st+"=== UPCOMING + PRESENT CONTESTS ON CODEFORCES ===\n"
                for data in contests:
                    time = data['startTimeSeconds'] 
                    st = st + "==================================\n"
                    st = st + "Contest ID   : "+str(data['id'])+"\n"
                    st = st + "Contest Name : "+str(data['name'])+"\n"
                    st = st + "Start Time   : "+timeConvert(time)+"\n"
                    st = st + "End Time     : "+timeConvert(time + data['durationSeconds'])+"\n"
                    st = st + "==================================\n\n" 
                return st
            else:
                return "===No Contest in near future. Please check again later.==="        
    except:
        return '====Failed to load data===='

###########################################################################################################

def cfRatingChange(handle):
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

def cfUserInfo(li):
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

def cfRanklist(contestid , competitors):
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


