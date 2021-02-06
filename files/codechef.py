import requests
import urllib.error , urllib.parse , urllib.request
from bs4 import BeautifulSoup
import sqlite3
import time


####################################################################################################

#################   Utility function to get time in required format

def getpropertime(st):
    st = st.split(' ')
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in month:
        if(st[1]==i):
            st[1] = (1 + month.index(i))
    print (st[2],st[1],st[0],st[3]  )   

#################   Utility function to check if a contest is rated

def cckeywordAI(st):
    st = st.split()
    if(len(st)>1):
        if((st[1] == 'Challenge') and len(st)==3):
            return 1
    for data in st:
        if(data == 'Lunchtime'):
            return 1
        elif(data == 'Cook-Off'):
            return 1
        elif((data == 'Rated') or (data == '(Rated')):
            return 1
    return 0            

#################   Shows a list of present and upcoming contests

def ccContestList():
    fhand = requests.get("https://www.codechef.com/contests").content
    soup = BeautifulSoup(fhand , 'lxml')

    tables = soup.find_all("table",{"class":"dataTable"})
    present = tables[0].find("tbody").find_all("tr")
    s = '\n\n============================'
    s = s + '\n\n= CODECHEF PRESENT CONTESTS =\n'
    for data in present:
        detail = data.find_all("td")
        sj = str(detail[1].text).lstrip()
        if cckeywordAI(sj):
            s = s + 'Contest Name   : '+str(detail[1].text).lstrip()
            s = s + 'Start time     : '+str(detail[2].text)+'\n'
            s = s + 'End time       : '+str(detail[3].text)+'\n\n'    
    s = s +  '=============================\n\n'    
    future = tables[1].find("tbody").find_all("tr")
    s = s + '\n\n= CODECHEF FUTURE CONTESTS =\n'
    for data in future:
        detail = data.find_all("td")
        sj = str(detail[1].text).lstrip()
        if cckeywordAI(sj):
            s = s + 'Contest Name   : '+str(detail[1].text).lstrip()
            s = s + 'Start time     : '+str(detail[2].text)+'\n'
            s = s + 'End time       : '+str(detail[3].text)+'\n\n'    
    s = s +  '=============================\n\n'    
    return s    

#################   Shows information about a user

def ccUserInfo(handle):
    try:
        req = 'https://www.codechef.com/users/'+str(handle)
        fhand = requests.get(req).content
        soup = BeautifulSoup(fhand,'lxml')
        s = '\n'
        s = s +  '==========================\n' 
        info = soup.find_all("div",{"class":"user-details-container plr10"})
        if(len(str(info)) < 1):
            return "== No user found ==\n"
        else:
            name = soup.find("div",{"class":"user-details-container plr10"}).find_all("header")
            name = name[0].find_all("h2")
            s = s + 'User Name          : ' + str(name[0].text + '\n')
            rating = soup.find_all("div",{"class":"rating-number"})
            s = s + 'Current Rating     : ' + str(rating[0].text) + '\n'

            star = soup.find_all("div",{"class":"rating-star"})
            st = 0
            for data in star[0].find_all('span'):
                st += 1
            s = s + 'Current stars      : ' + str(st) + '\n'  
            s = s +  '============================='   
            s = s + '\n'
            return s
    except:
        return "== No user found ==\n"


###################################################################################################
#######################        Database Functionality               ###############################
###################################################################################################

conn = sqlite3.connect('database/COMPPROG.db')
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS CODECHEF(ID INTEGER AUTO_INCREMENT PRIMARY KEY , HANDLE VARCHAR(50) UNIQUE , NAME VARCHAR(50) , RATING INTEGER)")

################    Shows all user details (handle and rating) as a ranklist

def ccGetUsersFromDatabase():
    cur.execute("SELECT HANDLE,RATING FROM CODECHEF ORDER BY RATING DESC")
    rows = cur.fetchall()
    s = "\n"
    rank = 1
    for row in rows:
        s+= str(rank) + "    "+str(row[0]) +"    "+ str(row[1])+'\n'
        rank += 1
    return s    

#################   Checks if user details already present in database

def ccSearchDatabase(handle):
    cur.execute("SELECT * FROM CODECHEF WHERE HANDLE = ? ",(handle,))
    row = cur.fetchone()
    if row is None:
        return 0
    else:
        return 1    

#################   Adds details of a new user into the database

def ccAddUser(handle):
    try:
        if(ccSearchDatabase(handle)):
            return "== User already added to database =="
        req = 'https://www.codechef.com/users/'+str(handle)
        fhand = requests.get(req).content
        soup = BeautifulSoup(fhand,'lxml')
        info = soup.find_all("div",{"class":"user-details-container plr10"})
        if(len(str(info)) < 1):
            return "== No user found ==\n"
        else:
            name = soup.find("div",{"class":"user-details-container plr10"}).find_all("header")
            name = name[0].find_all("h2")
            vname = name[0].text
            rating = soup.find_all("div",{"class":"rating-number"})
            vrating = int(rating[0].text)
            cur.execute("INSERT INTO CODECHEF (HANDLE, NAME, RATING) VALUES (? , ? , ?)",(handle,vname,vrating,))
            conn.commit()
            return "User successfully added to database"
    except:
        return "== No user found ==\n"

#################   Updates the data from database

def ccUpdateDatabase():
    cur.execute("SELECT * FROM CODECHEF")
    rows = cur.fetchall()
    for row in rows:
        time.sleep(2)
        req = 'https://www.codechef.com/users/'+str(row[1])
        fhand = requests.get(req).content
        soup = BeautifulSoup(fhand,'lxml')
        info = soup.find_all("div",{"class":"user-details-container plr10"})
        if(len(str(info)) < 1):
            pass
        else:
            name = soup.find("div",{"class":"user-details-container plr10"}).find_all("header")
            name = name[0].find_all("h2")
            vname = name[0].text
            rating = soup.find_all("div",{"class":"rating-number"})
            vrating = int(rating[0].text)
            cur.execute("UPDATE CODECHEF SET NAME = ? , RATING = ?  WHERE ID = ?",(vname, vrating,row[0],))
            conn.commit()    

