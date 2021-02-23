import os
import urllib.request , urllib.parse, urllib.error
import json
from datetime import datetime
import time
import psycopg2
from os import environ



####################################################################################################


#################   Utility function to obtain time in required format

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

################# Displays list of present and upcoming contests

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
                tm = datetime.timestamp(datetime.now())
                count = 0
                for data in contests:
                    time = data['startTimeSeconds'] 
                    #if(int(time-tm) <= 259200):
                    count += 1
                    st = st + "=============================\n"
                    st = st + "Contest ID   : "+str(data['id'])+"\n"
                    st = st + "Contest Name : "+str(data['name'])+"\n"
                    st = st + "Start Time   : "+timeConvert(time)+"\n"
                    st = st + "End Time     : "+timeConvert(time + data['durationSeconds'])+"\n"
                    st = st + "=============================\n\n" 
                    if(count == 0):
                        return '==\nNo event today or tomorrow\n==\n'    
                return st
            else:
                return "=No Contest in near future. Please check again later.="        
    except:
        return '====Failed to load data===='

#################   Displays the change in rating for a  given user

def cfRatingChange(handle):
    handle = urllib.request.urlopen('https://codeforces.com/api/user.rating?handle='+handle)
    fhand = handle.read().decode()
    try:
        js = json.loads(fhand)
        if(js['status']=='OK'):
            st = ''
            st = st + "=============================\n" 
            st = st + "=    Last round participated : "+str(js['result'][-1]['contestName'])+"\n"
            st = st + "=    Old Rating              : "+str(js['result'][-1]['oldRating'])+"\n"
            st = st + "=    New Rating              : "+str(js['result'][-1]['newRating'])+"\n"
            st = st + "=    Rank                    : "+str(js['result'][-1]['rank'])+"\n"
            st = st + "=============================\n"
            return st
    except:
        return "==Failed to load data=="

#################   Displays details about a given user

def cfUserInfo(li):
    s = ';'.join(li)
    handle = urllib.request.urlopen('https://codeforces.com/api/user.info?handles='+s)
    fhand = handle.read().decode()
    try:
        js = json.loads(fhand)
        if(js['status']=='OK'):
            st = ''
            for data in js['result'] :
                st = st + "=============================\n"
                st = st + "=    Handle         : "+str(data['handle'])+'\n'
                st = st + "=    Max Rank       : "+str(data['maxRank'])+'\n'
                st = st + "=    Max Rating     : "+str(data['maxRating'])+'\n'
                st = st + "=    Current Rank   : "+str(data['rank'])+'\n'
                st = st + "=    Current Rating : "+str(data['rating'])+'\n'
                st = st + "=============================\n"
            return st    
    except:
        return "====Failed to load data===="   

#################   Displays a custom ranklist with the provided users

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
            st = st + "==============================n"
            st = st + "==     Custom Ranklist     ==\n"
            st = st + "=============================\n\n"
            st = st + " Sl.  Points       Handle\n"
            for data in js['result']['rows'] :
                st = st + "=>   "+str(rank)+'        '+str(int(data['points']))+'         '+(data['party']['members'][0]['handle'])+'\n' 
                rank += 1   
            return st                

    except:
        return "==Failed to load data=="         



###################################################################################################
#######################        Database Functionality               ###############################
###################################################################################################

DATABASE_URL = environ.get('DATABASE_URL')

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
print("Database opened successfully")

cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS CODEFORCES(ID SERIAL PRIMARY KEY ,SERVER INTEGER, HANDLE VARCHAR(50) UNIQUE , RATING INTEGER, MAXRATING INTEGER)")

################    Shows all user details (handle and rating) as a ranklist

def cfGetUsersFromDatabase(server):
    cur.execute("SELECT HANDLE,RATING FROM CODEFORCES ORDER BY RATING DESC WHERE SERVER =?",(server,))
    rows = cur.fetchall()
    if(len(rows)==0):
        return "\nNo Records"
    s = "\n"
    rank = 1
    for row in rows:
        s+= str(rank) + "    "+str(row[0]) +"    "+ str(row[1])+'\n'
        rank += 1
    return s    

#################   Checks if user details already present in database

def cfSearchDatabase(handle,server):
    cur.execute("SELECT * FROM CODEFORCES WHERE HANDLE = ? AND SERVER=? ",(handle,server,))
    row = cur.fetchone()
    if row is None:
        return 0
    else:
        return 1    

#################   Adds details of a new user into the database

def cfAddUser(handle,server):
    try:
        if(cfSearchDatabase(handle,server)):
            return "== User already added to database =="
        handle = urllib.request.urlopen('https://codeforces.com/api/user.info?handles='+handle)
        fhand = handle.read().decode()
        js = json.loads(fhand)
        if(js['status']=='OK'):
            if(len(js['result'])==0):
                return "== No user found ==\n"
            for data in js['result'] :
                cur.execute("INSERT INTO CODEFORCES (SERVER,HANDLE, RATING, MAXRATING) VALUES (?, ? , ? , ? )",(server,data['handle'],data['rating'],data['maxRating'],))
                conn.commit()
                return "User successfully added to database"
        else:
            return "API request limit exceeded. Please wait for some time before making another request"  
    except:
        return "== No user found ==\n"

#################   Updates the data from database

def cfUpdateDatabase():
    cur.execute("SELECT * FROM CODEFORCES")
    rows = cur.fetchall()
    for row in rows:
        time.sleep(2)
        handle = urllib.request.urlopen('https://codeforces.com/api/user.info?handles='+str(row[1]))
        fhand = handle.read().decode()
        try:
            js = json.loads(fhand)
            if(js['status']=='OK'):
                for data in js['result'] :
                    cur.execute("UPDATE CODEFORCES SET RATING = ? , MAXRATING = ? WHERE ID = ",(data['rating'],data['maxRating'],row[0],))
                    conn.commit()
                    return "User successfully added to database"
            else:
                return "API request limit exceeded. Please wait for some time before making another request"  
        except:
            return "== No user found ==\n"
