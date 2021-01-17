import requests
import urllib.error , urllib.parse , urllib.request
from bs4 import BeautifulSoup

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
        s = s +  '===============================' 
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
