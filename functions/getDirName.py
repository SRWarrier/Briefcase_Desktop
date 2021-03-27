import requests_html
from bs4 import BeautifulSoup as BS


session = requests_html.HTMLSession()
header = session.headers
header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
def getDirName(Query):
    NameData={}
    if str(Query).isnumeric() and len(Query)==8:
        session.get('http://www.mca.gov.in/mcafoportal/showEnquireDIN.do',headers=header)
        requestHeader = header
        requestHeader['Accept']= 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        requestHeader['Accept-Encoding']= 'gzip, deflate'
        requestHeader['Content-Type']= 'application/x-www-form-urlencoded'
        requestHeader['Referer']= 'http://www.mca.gov.in/mcafoportal/showEnquireDIN.do'
        url = 'http://www.mca.gov.in/mcafoportal/enquireDIN.do'
        data = {"DIN":Query,
                "displayCaptcha":"false"}   
        try:
            output = session.post(url, data=data, headers=requestHeader)
        except Exception:
            NameData['Status'] = 'Failed'
            NameData['data'] = 'Error Occured | DIN not Found'
            return NameData
        soup = BS(output.text,'lxml')
        table = soup.find('table',{'id':'enquireDINDetailsId'})
        dindata=[]
        for tr in table.findAll('tr'):
            templist=[]
            for td in tr.findAll('td'):
                templist.append(td.text.strip())
            dindata.append(templist)
        dinDict={}
        for item in dindata:
            if len(item)>1:
                dinDict[item[0]]=item[1]
        NameData['Status'] = 'Success'
        NameData['data'] = dinDict
        return NameData
