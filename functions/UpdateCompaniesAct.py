import requests_html
from bs4 import BeautifulSoup as BS
import re
import sqlite3 as lite
session = requests_html.HTMLSession()


def refreshDataBase():
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS CompaniesAct('Section' TEXT UNIQUE, 'Title' TEXT, 'link' TEXT)" )
    reqheader=session.headers
    reqheader['User-Agent']='Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'
    reqheader['Referer']='https://indiacode.nic.in/handle/123456789/1362/simple-search?nccharset=24B44923&query=companies+act&btngo=&searchradio=acts'
    reqheader['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    reqheader['Accept-Encoding']= 'gzip, deflate, br'
    reqheader['Accept-Language']='en-US,en;q=0.5'
    reqheader['Upgrade-Insecure-Requests']= '1'
    sectionDict={}
    SecTitleDict={}
    acturl='https://indiacode.nic.in/handle/123456789/2114?sam_handle=123456789/1362'
    actpage=session.get(acturl,headers=reqheader,timeout =400)
    soup=BS(actpage.text,'lxml')
    TableBody=(soup.find('table',{'id':'myTableActSection'})).find('tbody')
    if len(TableBody)>400:
        hreflinks=TableBody.findAll('a',{'class','sectionTitle'})
        if len(hreflinks)<2:
            hreflinks=TableBody.findAll('a',{'class','title'})
        SectionDict = {}
        for x in hreflinks:
            Tid = x.attrs['id'].split('#')
            SecTitle = x.text.strip().split('\xa0')[1].strip()
            actid=Tid[0]
            sectionID=Tid[1]
            Securl="https://indiacode.nic.in/SectionPageContent?actid="+actid+"&sectionID="+sectionID
            SectionNo = x.text.strip().split('\xa0')[0].replace('Section ','').replace('.','')
            SectionData =tuple([SectionNo,SecTitle,Securl])
            cur.execute("INSERT OR REPLACE INTO CompaniesAct VALUES"+str(SectionData))
    cur.close()
    con.commit()
    con.close()
    return True
