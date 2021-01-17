import requests
import urllib.error , urllib.parse , urllib.request
from bs4 import BeautifulSoup

####################################################################################################

def getpropertime(st):
    st = st.split(' ')
    month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    for i in month:
        if(st[1]==i):
            st[1] = (1 + month.index(i))
    print (st[2],st[1],st[0],st[3]  )   

###################################################################################################

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

####################################################################################################
def ccContestList():
    fhand = requests.get("https://www.codechef.com/contests").content
    soup = BeautifulSoup(fhand , 'lxml')

    tables = soup.find_all("table",{"class":"dataTable"})
    present = tables[0].find("tbody").find_all("tr")
    s = '\n\n=================================='
    s = s + '\n\n=== CODECHEF PRESENT CONTESTS ===\n'
    for data in present:
        detail = data.find_all("td")
        s = s + 'Contest Name   : '+str(detail[1].text).lstrip()
        s = s + 'Start time     : '+str(detail[2].text)+'\n'
        s = s + 'End time       : '+str(detail[3].text)+'\n\n'
    s = s + '\n\n'
    future = tables[1].find("tbody").find_all("tr")
    s = '\n\n=== CODECHEF FUTURE CONTESTS ===\n'
    for data in future:
        detail = data.find_all("td")
        sj = str(detail[1].text).lstrip()
        if cckeywordAI(sj):
            s = s + 'Contest Name   : '+str(detail[1].text).lstrip()
            s = s + 'Start time     : '+str(detail[2].text)+'\n'
            s = s + 'End time       : '+str(detail[3].text)+'\n\n'    
    s = s +  '==================================\n\n'    
    return s    

####################################################################################################

def ccUserInfo(handle):
    try:
        req = 'https://www.codechef.com/users/'+str(handle)
        fhand = requests.get(req).content
        soup = BeautifulSoup(fhand,'lxml')
        s = '\n'
        s = s +  '===============================\n' 
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
            s = s +  '=================================='   
            s = s + '\n'
            return s
    except:
        return "== No user found ==\n"

####################################################################################################

