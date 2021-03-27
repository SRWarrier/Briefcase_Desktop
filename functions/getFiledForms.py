import requests_html
from bs4 import BeautifulSoup as BS
import datetime
from functions.getCIN import getCIN
from functions.getCompanyName import getName
import time


session = requests_html.HTMLSession()

def getFileDocuments(Name=False,CIN=False,FINYEAR=datetime.datetime.now().year,CAT='All'):
    if CIN and not Name:
        Name=getName(CIN)
        if Name['Status']=='Failed':
            return Name
        elif Name['Status']=='Selection':
            return Name
        else:
            Name=Name['data'][1]['Name']
        
    elif Name and not CIN:
        CINdata=getCIN(Name)
        if CINdata['Status']=='Failed':
            return CINdata
        elif CINdata['Status']=='Selection':
            return CINdata
        else:
            CIN=CINdata['data'][1]['CIN']
            Name=(CINdata['data'][1]['Name']).replace(' ','+')
    else:
        return 'Invalid values given'
    CategoryDict={'certificates':'CETF',
                  'directors':'CDRD',
                  'incorporation':'INCD',
                  'charge':'CRGD',
                  'annual':'ARBE',
                  'llp':'LLPF',
                  'otherD':'OTRE',
                  'attachments':'OTRA'}
    url = 'http://www.mca.gov.in/mcafoportal/vpdDocumentCategoryDetails.do'
    header = session.headers
    header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
    #covert to List
    if isinstance(FINYEAR,int):
        FINYEAR=[FINYEAR]
    if CAT=='All':
        CAT=CategoryDict.values()
    elif isinstance(CAT,str):
        CAT=[CAT]
    
    #Defaul Dict
    Mother={}
    Daughter={}
    Son={}
    for Year in FINYEAR:
        if 2006<int(Year)<(datetime.datetime.now().year)+1:
            for categ in CAT:
                if categ.lower() in CategoryDict.keys() or categ in CategoryDict.values():
                    if categ.lower() in CategoryDict.keys():
                        categ=CategoryDict[categ]
                    data = {"cinFDetails":CIN,
                            "companyName":Name,
                            "cartType":"",
                            "categoryName":categ,
                            "finacialYear":str(Year)}
                    try:
                        response=session.post(url, headers=header, data = data)
                    except requests_html.requests.exceptions.ConnectionError:
                        for x in range(3):
                            try:
                                time.sleep(1)
                                response=session.post(url, headers=header, data = data)
                                break
                            except :
                                continue
                    try:
                        if response.status_code==200:
                            test='Pass'
                        else:
                            test='Fail'
                    except:
                        test='Fail'

                    print
                    try:
                        if test=='Pass':
                            soup = BS(response.text,'lxml')
                            table = soup.find('table',{'id':'results'})
                            theaders=[]
                            for tr in table.findAll('tr'):
                                    for th in tr.findAll('th'):
                                            theaders.append(th.get_text().strip())

                            
                            loop_counter=1
                            for tr in table.findAll('tr'):
                                    allRows=tr.findAll('td')
                                    tempDict={}
                                    for x in range(len(allRows)):
                                            tempDict[theaders[x]]=allRows[x].text.strip()
                                    if len(tempDict)>0:
                                            Son[loop_counter]=tempDict
                                            loop_counter+=1
                    except AttributeError:
                        Son={1:{"No Forms Filed in the year"}}
                
                Daughter[categ]=Son
                time.sleep(3)
            Mother[Year]=Daughter
    return Mother
