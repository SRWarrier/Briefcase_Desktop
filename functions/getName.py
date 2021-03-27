import requests_html
import pandas as pd


session = requests_html.HTMLSession()

def searchname(name1,name2='',name3='',name4='',name5='',name6='',activity1='',activity2=''):
    namedata={}
    try:
        header = session.headers
        header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
        header['Referer'] = 'Referer: http://www.mca.gov.in/mcafoportal/checkCompanyName.do'
        url = 'http://www.mca.gov.in/mcafoportal/checkCompanyName.do'
        data = {
            'counter': '1',
            'name1':name1,
            'name2': name2, 
            'name3': name3, 
            'name4': name4, 
            'name5': name5, 
            'name6': name6, 
            'activityType1':activity1,  
            'activityType2':activity2,  
            'displayCaptcha':   'false'
        } 
        output = session.post(url, data=data, headers=header)
        print(output.html.status_code)
        if output.html.status_code = 200:
            html_res=output.html.find("#companyList",first=True)
            try:
                Comp_table=pd.read_html(html_res.html)[0]
                Comp_table=Comp_table.rename(columns={'LLPIN/CIN/Form INC-1 Ref No':'LLPIN/CIN','Company / LLP Name':'Name','Company Name Status':'Status'})
                Comp_table=Comp_table[['LLPIN/CIN','Name','Status']]
            except AttributeError:
                namedata['Status']='Message'
                namedata['data'] = "No Similar names found.if activity given, please try without activity or widen your search before confirming"
                return namedata

            CINlist=Comp_table['LLPIN/CIN'].tolist()
            Namelist=Comp_table['Name'].tolist()
            Statuslist=Comp_table['Status'].tolist()
            responseData={}
            for x in range(len(CINlist)):
                tempDict={}
                tempDict['CIN']=CINlist[x]
                tempDict['Name']=Namelist[x]
                tempDict['Status']=Statuslist[x]
                responseData[x+1]=tempDict
            namedata['Status']='Success'
            namedata['data'] = responseData
            return namedata
        except IndexError:
            namedata['Status']='Failed'
            namedata['data'] = 'Error Occurred'
            return namedata
