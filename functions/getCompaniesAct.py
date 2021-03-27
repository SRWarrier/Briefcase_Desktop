import requests_html
from bs4 import BeautifulSoup as BS
import re
import sqlite3

session = requests_html.HTMLSession()
CLEAN = re.compile('\s+')


def getHeader():
    header = session.headers
    header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
    return header


def alphatonum(x):
    alphadict={'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
               'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17, 'r': 18, 's': 19,
               't': 20, 'u': 21, 'v': 22, 'w': 23, 'x': 24, 'y': 25, 'z': 26, 'aa': 27, 'ab': 28, 'ac': 29, 'ad': 30,
               'ae': 31, 'af': 32, 'ag': 33, 'ah': 34, 'ai': 35, 'aj': 36, 'ak': 37, 'al': 38, 'am': 39, 'an': 40, 'ao': 41,
               'ap': 42, 'aq': 43, 'ar': 44, 'as': 45, 'at': 46, 'au': 47, 'av': 48, 'aw': 49, 'ax': 50, 'ay': 51, 'az': 52,
               'ba': 53, 'bb': 54,'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11,
               'L': 12, 'M': 13, 'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24,
               'Y': 25, 'Z': 26, 'AA': 27, 'AB': 28, 'AC': 29, 'AD': 30, 'AE': 31, 'AF': 32, 'AG': 33, 'AH': 34, 'AI': 35, 'AJ': 36,
               'AK': 37, 'AL': 38, 'AM': 39, 'AN': 40, 'AO': 41, 'AP': 42, 'AQ': 43, 'AR': 44, 'AS': 45, 'AT': 46, 'AU': 47, 'AV': 48,
               'AW': 49, 'AX': 50, 'AY': 51, 'AZ': 52, 'BA': 53, 'BB': 54}
    return alphadict[x]

def findSection(Section='',SubSection='',Clause='',Proviso='',Explanation='',replyDict={},json=False):
    url="http://www.mca.gov.in/SearchableActs/Section"+str(Section)+'.htm'
    searchHeader = getHeader()
    try:
        response=session.get(url,headers=searchHeader)
    except:
        return {'Status':'Failed', 'Message':'You may not be connected to Internet.Please Check and try again'}
    soup=BS(response.text,'lxml')
    SecTitle=(soup.find('div',{'class':'WordSection1'})).findChild("p").text.replace('\n',' ')
    SecText=soup.text[soup.text.find('\n('):].replace("","<b>").replace("","</b>")
    Sectionsplit=SecText.replace('sub-section\n','sub-section').replace('subsection\n','subsection').split("\n(")
    sec_string=''
    for x in Sectionsplit:
        if x!='':
                if x[0].isnumeric():
                        sec_string=sec_string+"||"+x.replace('\n',' ').replace('Provided','@Provided').replace('Explanation','~Explanation')+'\n'
                if x[0].isalpha():
                        sec_string=sec_string+"#"+x.replace('\n',' ').replace('Provided','@Provided').replace('Explanation','~Explanation')+'\n'
    if SubSection!='' and Clause=='' and Proviso=='' and Explanation=='':           
         SubSectionText=sec_string.split('||')[int(SubSection)].replace('#','\n\n').replace('@','\n\n').replace('~','\n\n')
         result=SubSectionText.replace('#',"\n\n").replace('\x97',':')
         replyDict['Section Title']=SecTitle
         replyDict['Section Number']=str(Section)
         replyDict['Sub Section']=str(SubSection)
         replyDict['Section Text']=result
         
    elif Clause!='' and Proviso=='' and Explanation=='':
        if Clause.isalpha():
            _Clause=alphatonum(Clause)
        ClauseText=(sec_string.split('||')[int(SubSection)]).split('#')[_Clause].replace('@','\n\n').replace('~','\n\n')
        result=ClauseText.replace('\x97',':').replace('\x92',"'")
        replyDict['Section Title']=SecTitle
        replyDict['Section Number']=str(Section)
        replyDict['Sub Section']=str(SubSection)
        replyDict['Clause']=str(Clause)
        replyDict['Section Text']=result  

    elif Proviso!=''and Explanation=='':
        if Clause.isalpha():
            _Clause=alphatonum(Clause)
        if Clause=='':
            ProvisoText=(sec_string.split('||')[int(SubSection)]).split('@')[int(Proviso)]
        else:    
            ProvisoText=(sec_string.split('||')[int(SubSection)]).split('#')[int(_Clause)].split('@')[int(Proviso)]
        result=ProvisoText.replace('\x97',':').replace('\x92',"'")
        replyDict['Section Title']=SecTitle
        replyDict['Section Number']=str(Section)
        replyDict['Sub Section']=str(SubSection)
        replyDict['Clause']=str(Clause)
        replyDict['Proviso']=str(Proviso)
        replyDict['Section Text']=result      
    
    elif Proviso==''and Explanation!='':
        if Clause.isalpha():
            _Clause=alphatonum(Clause)
        if Clause=='':
            ExplText=(sec_string.split('||')[int(SubSection)]).split('~')[int(Explanation)]
        else:    
            ExplText=(sec_string.split('||')[int(SubSection)]).split('#')[int(_Clause)].split('~')[int(Explanation)]
        result=ExplText.replace('\x97',':').replace('\x92',"'")
        replyDict['Section Title']=SecTitle
        replyDict['Section Number']=str(Section)
        replyDict['Sub Section']=str(SubSection)
        replyDict['Clause']=str(Clause)
        replyDict['Explanation']=str(ExplText)
        replyDict['Section Text']=result     
        
    else:
        SectionText=''
        for x in sec_string:
            SectionText=SectionText+((x.replace('@','\n\n')).replace('#','\n\t')).replace('~','\n').replace("","<b>").replace("","</b>")
        resultString=SectionText.replace('||','\n\n')
        if resultString=='':
            fString=(soup.find('div',{'class':'WordSection1'}))
            Rtitle=SecTitle.replace('<b>','').replace('</b>','')
            resultString=fString.text[fString.find('\n'):].replace('\n',' ').replace(Rtitle,"\n")
        replyDict['Section Title']=str(SecTitle)
        replyDict['Section Text']=str(resultString)
    ResultDict={}
    if len(replyDict)>0:
        if json==True:
            ResultDict['Status']='Success'
            ResultDict['result']=replyDict
        else:
            replyString=''
            replyString=replyString+replyDict['Section Title']+'\n'
            if 'Section Number' in replyDict.keys():
                replyString=replyString+'Sec.: '+replyDict['Section Number']
            if 'Sub Section' in replyDict.keys():
                replyString=replyString+', '+'Sub.:'+replyDict['Sub Section']
            if 'Clause' in replyDict.keys():
                replyString=replyString+', '+'Cl.:'+replyDict['Clause']
            if 'Proviso' in replyDict.keys():
                replyString=replyString+', '+'Pro.:'+replyDict['Proviso']
            if 'Explanation' in replyDict.keys():
                replyString=replyString+', '+'Ex.:'+replyDict['Explanation']
            replyString=replyString+'\n'+'*'*50+'\n'+replyDict['Section Text']+'\n'
            if 'FootNote' in replyDict.keys():
                replyString=replyString+'\n'+'*'*50+'\n'+replyDict['FootNote']
            return '\n'+replyString
    else:
        ResultDict['Status']='Failed'
    return ResultDict


    
        
def to_superscript(num,reverse=False):
    if reverse==False:
        transl = str.maketrans(dict(zip('1234567890', '¹²³⁴⁵⁶⁷⁸⁹⁰')))
        return num.translate(transl)
    elif reverse==True:
        transl = str.maketrans(dict(zip('¹²³⁴⁵⁶⁷⁸⁹⁰','1234567890')))
        return num.translate(transl)

def WhatIs(Section='',SubSection='',Clause='',Proviso='',Explanation='',replyDict={},json=False, debug=False):
    if Section=='':
        return {'Status':'Failed','data':'Secton Required'}
    if SubSection=='' and Clause!='':
        return {'Status':'Failed','data':'Sub Secton Required'}
    reqheader=session.headers
    reqheader['User-Agent']='Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
    reqheader['Referer']='https://indiacode.nic.in/handle/123456789/1362/simple-search?nccharset=24B44923&query=companies+act&btngo=&searchradio=acts'
    reqheader['Accept']='text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    reqheader['Accept-Encoding']= 'gzip, deflate, br'
    reqheader['Accept-Language']='en-US,en;q=0.5'
    reqheader['Upgrade-Insecure-Requests']= '1'
    dbfilepath = 'Database/C3_DataBase.db'
    conn = sqlite3.connect(dbfilepath)
    cur = conn.cursor()
    SectionData = cur.execute(f'SELECT * from CompaniesAct WHERE Section = "{Section}"').fetchall()
    print(SectionData)
    SecTitle = SectionData[0][1]
    Securl = SectionData[0][2]
    try:
        sectionresponse=session.get(Securl,headers=reqheader)
        sectiontext=sectionresponse.json()
    except Exception as e:
        exception_name = type(e).__name__
        if debug:
            print(exception_name, e)
        if exception_name=='IndexError':
            return {'Status':'Failed', 'Message':'Unable to find the specified section'}
        else:
            return {'Status':'Failed/QSR', 'Message':'Server did not respond. Would you like to do a Quick Search.\nPlease note that Quick Searches are not up to date.'}
    footnote=''
    try:
        footnote="Footnote:\n"+BS(sectiontext['footnote'],'lxml').text.replace('\r\n','\n')
    except KeyError:
        pass
    fSectext=sectiontext['content'].replace('<sup>','^<sup>')
    suText=(re.sub('\<sup>\s*(\d+)', lambda m: to_superscript(m[1]), fSectext)).replace('</sup>','').split('\\r\\n')
    sec_string=''
    for txt in suText:
        pre_text=BS(txt,'lxml').text.replace('\n\r\n','|').split('|')
        for x in pre_text:
            if x!='':
                x=x.replace('\r\n',' ')
                if x[0]=='^':
                    y=x[3:]
                else:
                    y=x
                if y[0]=='(':
                    if y[1].isnumeric():
                        sec_string=sec_string+'||'+x
                    elif y[1].isalpha():
                        sec_string=sec_string+'#'+x
                elif y[0:8].lower()=='provided':
                    sec_string=sec_string+'@'+x
                elif y[0:11].lower()=='explanation':
                    sec_string=sec_string+'~'+x
                else:
                    sec_string=sec_string+" "+x
    if SubSection!='' and Clause=='' and Proviso=='' and Explanation=='':           
         SubSectionText=sec_string.split('||')[int(SubSection)].replace('#','\n\n').replace('@','\n\n').replace('~','\n\n')
         result=SubSectionText.replace('#',"\n\n").replace('\x97',':')
         replyDict['Section Title']=SecTitle
         replyDict['Section Number']=str(Section)
         replyDict['Sub Section']=str(SubSection)
         replyDict['Section Text']=result
         replyDict['FootNote']=footnote

    elif Clause!='' and Proviso=='' and Explanation=='':
        if Clause.isalpha():
            _Clause=alphatonum(Clause)
        ClauseText=(sec_string.split('||')[int(SubSection)]).split('#')[int(_Clause)].replace('@','\n\n').replace('~','\n\n')
        result=ClauseText.replace('\x97',':').replace('\x92',"'")
        replyDict['Section Title']=SecTitle
        replyDict['Section Number']=str(Section)
        replyDict['Sub Section']=str(SubSection)
        replyDict['Clause']=str(Clause)
        replyDict['Section Text']=result
        replyDict['FootNote']=footnote
        

    elif Proviso!=''and Explanation=='':
        if Clause.isalpha():
            _Clause=alphatonum(Clause)
        if Clause=='':
            ProvisoText=(sec_string.split('||')[int(SubSection)]).split('@')[int(Proviso)].replace('~','\n\n')
        else:    
            ProvisoText=(sec_string.split('||')[int(SubSection)]).split('#')[int(_Clause)].split('@')[int(Proviso)].replace('~','\n\n')
        result=ProvisoText.replace('\x97',':').replace('\x92',"'").replace("","<b>").replace("","</b>")
        replyDict['Section Title']=SecTitle
        replyDict['Section Number']=str(Section)
        replyDict['Sub Section']=str(SubSection)
        replyDict['Clause']=str(Clause)
        replyDict['Proviso']=str(Proviso)
        replyDict['Section Text']=result
        replyDict['FootNote']=footnote
    
    elif Proviso==''and Explanation!='':
        if Clause.isalpha():
            _Clause=alphatonum(Clause)
        if Clause=='':
            ExplText=(sec_string.split('||')[int(SubSection)]).split('~')[int(Explanation)].replace('@','\n\n')
        else:    
            ExplText=(sec_string.split('||')[int(SubSection)]).split('#')[int(_Clause)].split('~')[int(Explanation)]
        result=ExplText.replace('\x97',':').replace('\x92',"'")
        replyDict['Section Title']=SecTitle
        replyDict['Section Number']=str(Section)
        replyDict['Sub Section']=str(SubSection)
        replyDict['Clause']=str(Clause)
        replyDict['Explanation']=str(Explanation)
        replyDict['Section Text']=result
        replyDict['FootNote']=footnote
        
    else:
        SectionText=''
        for x in sec_string:
            SectionText=SectionText+((x.replace('@','\n\n')).replace('#','\n\t')).replace('~','\n').replace("","<b>").replace("","</b>")
        resultString=SectionText.replace('||','\n\n')
        if resultString!='':
            replyDict['Section Title']=SecTitle
            replyDict['Section Text']=str(resultString)
            replyDict['FootNote']=footnote
    ResultDict={}
    if len(replyDict)>0:
        if json==True:
            ResultDict['Status']='Success'
            ResultDict['result']=replyDict
        else:
            replyString=''
            replyString=replyString+replyDict['Section Title']+'\n'
            if 'Section Number' in replyDict.keys():
                replyString=replyString+'Sec.: '+replyDict['Section Number']
            if 'Sub Section' in replyDict.keys():
                replyString=replyString+', '+'Sub.:'+replyDict['Sub Section']
            if 'Clause' in replyDict.keys():
                replyString=replyString+', '+'Cl.:'+replyDict['Clause']
            if 'Proviso' in replyDict.keys():
                replyString=replyString+', '+'Pro.:'+replyDict['Proviso']
            if 'Explanation' in replyDict.keys():
                replyString=replyString+', '+'Ex.:'+replyDict['Explanation']
            replyString=replyString+'\n'+'*'*50+'\n'+replyDict['Section Text']+'\n'
            if 'FootNote' in replyDict.keys():
                replyString=replyString+'\n'+'*'*50+'\n'+replyDict['FootNote']
            return '\n'+replyString
    else:
        ResultDict['Status']='Failed'
    return ResultDict


