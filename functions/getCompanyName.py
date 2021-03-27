import requests_html
from bs4 import BeautifulSoup as BS


session = requests_html.HTMLSession()

def getName(CIN):
    if CIN.isalnum() and len(CIN)==21:
        header = session.headers
        header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
        header['Referer'] = 'http://www.mca.gov.in/mcafoportal/viewPublicDocumentsFilter.do'
        url = 'http://www.mca.gov.in/mcafoportal/viewDocuments.do'
        data = {"companyOrllp":"C",
                "cartType":"",
                "__checkbox_companyChk":"true",
                "cinChk":"true",
                "__checkbox_cinChk":"true",
                "cinFDetails":CIN,
                "__checkbox_llpChk":"true",
                "__checkbox_llpinChk":"true",
                "__checkbox_regStrationNumChk":"true",
                "countryOrigin":"INDIA",
                "__checkbox_stateChk":"true",
                "displayCaptcha":"false",
                "companyID":""}
            
        output = session.post(url, data=data, headers=header)    
        soup=BS(output.text,'lxml')
        table=soup.find('table',{'id':'results'})
        resultlist=[]
        for row in table.findAll('tr'):
            for data in row.findAll('td'):
                resultlist.append(data.text.strip())
        return resultlist[2]
    else:
        return 'FAILED'
