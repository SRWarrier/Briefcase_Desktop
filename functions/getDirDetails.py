import requests_html
from bs4 import BeautifulSoup as BS
from functions.getDIN import getDIN
import itertools

session = requests_html.HTMLSession()

def getDirdetails(Query,datafilter=None):
    DirDetailsDict={}
    test = 'Fail'
    header = session.headers
    header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
    header['Referer'] = 'http://www.mca.gov.in/mcafoportal/viewDirectorMasterData.do'
    url = 'http://www.mca.gov.in/mcafoportal/showdirectorMasterData.do'
    data = {
        'directorName': '',
        'din':  '',
        'displayCaptcha': 'false'
    }
    if str(Query).isnumeric() and len(Query)==8:
        data['din']=str(Query)
        test='Pass'
    elif str(Query).replace(" ","").replace(",","").isalpha():
        if len(Query)>2:
            response = getDIN(Query)
            if response['Status']=='Failed':
                test='Fail'  

            elif response['Status']=='Success':
                if len(response['data'])>1:
                    DirDetailsDict['Status']='UserSelectionRequired'
                    DirDetailsDict['data']=response['data']
                    return DirDetailsDict
                
                else:
                    name=response['data'][0]['Name']
                    din=response['data'][0]['DIN']
                    data['directorName']=name
                    data['din']=din
                    test="Pass"##        if check  

        else:
            DirDetailsDict['Status']='Failed'
            DirDetailsDict['data']='Invalid Input, please enter atlease 3 characters'
            return DirDetailsDict
    else:
        DirDetailsDict['Status']='Failed'
        DirDetailsDict['data']='Operation failed'
        return DirDetailsDict
    if test=='Pass':
        try:
            output = session.post(url, data=data, headers=header)
        except Exception as e:
            print(e)
            return['Operation Failed']
        Dirdata = output.html.element('table#directorData').text().split('\n')
        Dirinfo = dict(itertools.zip_longest(*[iter(Dirdata)] * 2, fillvalue=""))
        DirectorMaster={}
        Directinfo={}
        try:
            tablehead = ['cin_LLPIN','aso_company_name','begin_date','end_date','active_complicance']#output.html.xpath('.//table[@id="companyData"]/thead/tr')[0].text.split('\n')
            info_table=output.html.xpath('.//table[@id="companyData"]/tr')
            for x in range(len(info_table)):
                tabledata = output.html.xpath('.//table[@id="companyData"]/tr')[x].text.split('\n')
                tempDict={}
                for colno in range(len(tablehead)):
                    try:
                        tempDict[tablehead[colno]]=tabledata[colno]
                    except:
                        continue
                Directinfo[x+1]=tempDict
        except NameError:    
            DirectorMaster['Status']='Failed'
            DirectorMaster['data']='No data found'
            return DirectorMaster
    if datafilter==None:
            DirectorMaster['Status']='Success'
            DirectorMaster['data']=Directinfo
            return DirectorMaster
    elif datafilter.lower()=='company':
        response={}
        for x in range(len(Directinfo)):
            tempDict={}
            tempDict[Directinfo[x+1]['CIN/FCRN']]=Directinfo[x+1]['Company Name']
            response[x+1]=tempDict
        DirectorMaster['Status']='Success'
        DirectorMaster['data']=response
        return DirectorMaster
    else:
        DirectorMaster['Status']='Failed'
        DirectorMaster['data']='No data found'
        return DirectorMaster
