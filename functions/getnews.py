import requests
from bs4 import BeautifulSoup as bs
import re
import datetime
import unicodedata
from io import BytesIO
import os
import feedparser

session=requests.Session()
headers=session.headers
headers['User-Agent']='Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0'

def getMCAUpdates(last_update):
    url="http://www.mca.gov.in"
    response=session.get(url,headers=headers)
    mod_date=datetime.datetime.strptime(response.headers['Last-Modified'],"%a, %d %b %Y %H:%M:%S GMT")
    if (datetime.datetime.now()-datetime.timedelta(days=2))<mod_date:
        soup=bs(response.text,'lxml')
        updates=soup.find('div',{'id':'MyDivName'})
        news=updates.findAll('li',{'class':'ImpInfoLi'})
        if len(news)>20:
            news=news[:20]
        NewsList=[]
        for item in range(len(news)):
            newsdict={}
            if len(news[item].findAll('a')):
                description=unicodedata.normalize('NFKC',news[item].text).replace(re.findall('\(\d.*?B\)',news[item].text)[0],'').replace('\n',' ').replace('â\x80\x93',' ')
                if description==last_update:
                    break
                newsdict['description']=description
                newsdict['pdf']=url+news[item].find('a')['href']
                NewsList.append(newsdict)
            else:
                description=unicodedata.normalize('NFKC',news[item].text).encode('latin-1').decode().replace('\n',' ').replace('â\x80\x93',' ')
                if description==last_update:
                        break
                newsdict['description']=description
                newsdict['pdf']=''
                NewsList.append(newsdict)
        return NewsList

def getITUpdates(last_update):
    url="https://www.incometaxindia.gov.in/Pages/default.aspx"
    response=session.get(url,headers=headers)
    mod_date=datetime.datetime.strptime(response.headers['Last-Modified'],"%a, %d %b %Y %H:%M:%S GMT")
    if (datetime.datetime.now()-datetime.timedelta(days=2))<mod_date:
        soup=bs(response.text,'lxml')
        updates=soup.find('div',{'class':'latest_news'})
        newsection=updates.find('ul',{'class':'scrollbarDIT'})
        news=newsection.findAll('li')
        if len(news)>20:
            news=news[:20]
        NewsList=[]
        for item in range(len(news)):
            newsdict={}
            if len(news[item].findAll('a')):
                if 'onclick' in news[item].find('a').attrs:
                    js_link=news[item].find('a')['onclick']
                    filename=(js_link[js_link.find("('"):js_link.find("')")+1]).replace("('",'').replace("')",'')
                    description=(news[item].find('a')['title']).replace('\u200b','').replace('\n',' ')
                    if description==last_update:
                        break
                    newsdict['description']=description
                    
                    newsdict['pdf']=filename.replace("'","")
                    NewsList.append(newsdict)
            else:
                description=news[item].text.replace('\n',' ')
                newsdict['description']=description
                newsdict['pdf']=''
                NewsList.append(newsdict)
        return NewsList

def getIBBCUpdates(last_update):
    base_url='https://ibbi.gov.in'
    url="https://ibbi.gov.in/whats-new"
    response=session.get(url,headers=headers)
    soup=bs(response.text,'lxml')
    updates=soup.find('table')
    tablebody=soup.find('tbody')
    NewsList=[]
    trlist=tablebody.findAll('tr')
    if len(trlist)>20:
        trlist=trlist[:20]
    for item in range(len(trlist)):
        newsdict={}
        tdlist=trlist[item].findAll('td')
        if datetime.datetime.strptime(tdlist[0].text.replace('\r\n','').replace('st','').replace('nd','').replace('rd','').replace('th','').strip(),'%d %B, %Y')>(datetime.datetime.now()-datetime.timedelta(days=2)):
            #newsdict['date']=tdlist[0].text.replace('\r\n','').strip()
            newsdict['description']=tdlist[1].find('a').text.strip()
            url=tdlist[1].find('a')['href']
            if url[:4]=='http':
                newsdict['pdf']=tdlist[1].find('a')['href']
            else:
                newsdict['pdf']=base_url+tdlist[1].find('a')['href']
            NewsList.append(newsdict)
    return NewsList
        
def getNews():
    url = 'https://www.livemint.com/rss/news'
    Feed = feedparser.parse(url)
    entries = Feed['entries']
    Deck = []
    counter = 0
    for entry in entries:
        Title = entry['title']
        Summary = entry['summary']
        Text = '<b>'+Title+'</b>'+'<br>'+Summary
        Deck.append({'description':Text, 'pdf':entry['link']})
        counter+=1
        if counter==20:
            break
    return Deck

def downloadPDF(url,folder,filename):
    pdf_data=session.get(url,headers=headers)
    with open(os.path.join(folder,filename),'wb') as f:
        f.write(pdf_data.content)
        f.close()
    
