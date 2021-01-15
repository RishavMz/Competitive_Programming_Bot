import urllib.request , urllib.parse, urllib.error
import json
from datetime import datetime

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
                print("=== UPCOMING CONTESTS ON CODEFORCES ===")
                for data in contests:
                    time = data['startTimeSeconds']
                    print('========================================================================')
                    print("=    Contest ID   : ",data['id'])
                    print("=    Contest Name : ",data['name'])
                    print("=    Start Time   : ", datetime.utcfromtimestamp(time))
                    print("=    End Time     : ",datetime.utcfromtimestamp(time + data['durationSeconds']))
                    print('========================================================================')  
                    print()  
            else:
                print("===No Contest in near future. Please check again later.===")        
    except:
        print('====Failed to load data====')    

###########################################################################################################

def ratingchange(handle):
    handle = urllib.request.urlopen('https://codeforces.com/api/user.rating?handle='+handle)
    fhand = handle.read().decode()
    try:
        js = json.loads(fhand)
        if(js['status']=='OK'):
            print("===============================================================================")   
            print("=    Last round participated : ",js['result'][-1]['contestName'])
            print("=    Old Rating              : ",js['result'][-1]['oldRating'])
            print("=    New Rating              : ",js['result'][-1]['newRating'])
            print("=    Rank                    : ",js['result'][-1]['rank'])
            print("================================================================================")
            print()
    except:
        print("====Failed to load data / Handle not found ====")

##################################################################################################################

def userInfo(li):
    s = ';'.join(li)
    handle = urllib.request.urlopen('https://codeforces.com/api/user.info?handles='+s)
    fhand = handle.read().decode()
    try:
        js = json.loads(fhand)
        if(js['status']=='OK'):
            for data in js['result'] :
                try:
                    print("=============================================================================")
                    print("=    Handle         : ",data['handle'])
                    print("=    Max Rank       : ",data['maxRank'])
                    print("=    Max Rating     : ",data['maxRating'])
                    print("=    Current Rank   : ",data['rank'])
                    print("=    Current Rating : ",data['rating'])
                    print("=============================================================================")
                    print()
                except:
                    print("No matching data for ",data['handle'])
    except:
        print("====Failed to load data / Handle not found ====")            

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
            print(js['result']['rows'][0])
            print("===============================================================")
            print("==                 Custom Ranklist                           ==")
            print("===============================================================")
            print()
            print(" Custom Rank     Points         Handle")
            for data in js['result']['rows'] :
                print()
                print("=>   ",rank,'        ',int(data['points']),'         ',(data['party']['members'][0]['handle'])) 
                rank += 1               

    except:
        print("====Failed to load data====")         

####################################################################################################

print("****************************************************************** *")
print("*                                                                  *")
print("* Hello , I'm noob bot.                                            *")
print("* Currently I use codeforces API to fetch data requested by users  *")
print("*                                                                  *")
print("* Interact with me :                                               *")
print("* 1        => Get list of future contests                          *")
print("*                                                                  *")
print("* 2 [user_handle] => Get rating change for a user's last contest   *")
print("* Example :  2 Noobmaster69                                        *")
print("*                                                                  *")
print("* 3 [user_handle1  user_handle2 ......] => Get data about users    *")
print("* Example :  3 Noobmaster69 HAMMERTHOR RABBIT                      *")
print("*                                                                  *")
print("* 4 [contest_id] [user_handle1  user_handle2...] => Get ranklist   *")
print("* Example :  4 Noobmaster69 HAMMERTHOR RABBIT                      *")
print("*                                                                  *")
print("****************************************************************** *")

while(True):
    inp = input().split()
    if(inp[0] == '1'):
        contestList()
    elif(inp[0]=='2' and len(inp)==2):
        ratingchange(inp[1])
    elif(inp[0]=='3'):
        userInfo(inp[1:]) 
    elif(inp[0]=='4'):
        ranklist(inp[1],inp[2:])       
    else:
        pass    
