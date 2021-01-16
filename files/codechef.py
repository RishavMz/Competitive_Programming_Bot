import requests
import urllib.error , urllib.parse , urllib.request
from bs4 import BeautifulSoup

####################################################################################################


def ccContestList():
    fhand = requests.get("https://www.codechef.com/contests").content
    soup = BeautifulSoup(fhand , 'lxml')

    tables = soup.find_all("table",{"class":"dataTable"})
    present = tables[0].find("tbody").find_all("tr")
    s = '====================================='
    s = s + '\n\n=== PRESENT CONTESTS ===\n'
    for data in present:
        detail = data.find_all("td")
        s = s + 'Contest Name   : '+str(detail[1].text).lstrip()
        s = s + 'Start time     : '+str(detail[2].text)+'\n'
        s = s + 'End time       : '+str(detail[3].text)+'\n\n'
    s = s + '\n\n'
    future = tables[1].find("tbody").find_all("tr")
    s = '\n\n=== FUTURE CONTESTS ===\n'
    for data in future:
        detail = data.find_all("td")
        s = s + 'Contest Name   : '+str(detail[1].text).lstrip()
        s = s + 'Start time     : '+str(detail[2].text)+'\n'
        s = s + 'End time       : '+str(detail[3].text)+'\n\n'    
    s = s +  '====================================='    
    return s    

####################################################################################################
