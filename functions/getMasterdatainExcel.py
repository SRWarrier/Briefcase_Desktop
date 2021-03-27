import requests_html
from bs4 import BeautifulSoup as BS
try:
    from functions.getCompanyName import getName
    from functions.getCIN import getCIN
except:
    from getCompanyName import getName
    from getCIN import getCIN
import os
import pandas as pd
from io import BytesIO


session = requests_html.HTMLSession()

def getMasterdataExcel(CIN=False, Name = False,filename = None,Save = False):
    MasterData={}
    header = session.headers
    header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
    header['Referer'] = 'http://www.mca.gov.in/mcafoportal/companyLLPMasterData.do'
    if Name and not CIN:
        data= getCIN(Name,True)
        print(data)
        if data['Status']=='Success':
            CIN = data['data'][1]['CIN']
            name = data['data'][1]['Name']
            hasPassed = True
        elif data['Status'] == 'Selection':
            return data
        else:
            MasterData['Status']='Failed'
            MasterData['data']=''
            return MasterData
    elif CIN and not Name and len(CIN)==21 and CIN.isalnum():
        name = getName(CIN)
        if name!='FAILED':
            hasPassed = True
        else:
            MasterData['Status']='Failed'
            MasterData['data']=''
            return MasterData

    elif CIN and Name:
        name = Name
        hasPassed = True
    if hasPassed:
        data = {
            'altScheme': 'CIN',
            'companyID': CIN,
            'companyName': name
            }
        url = 'http://www.mca.gov.in/mcafoportal/exportCompanyMasterData.do'
        try:
            response = session.post(url, data=data, headers=header)
        except:
            MasterData={}
            MasterData['Status']='Failed'
            MasterData['data']='Error Occured. Please check internet connectivity or try again later.'
            return MasterData
        if response.status_code==200:
            if Save:
                if filename == None:
                    filename = CIN+f' ({name}).xlsx'
                with open(filename,'wb') as f:
                    f.write(response.content)
                    f.close()
                return {'Status':'Success','data':f'Masterdata saved to \n{os.path.abspath(filename)}'}
            masterdata=pd.read_excel(BytesIO(response.content))
            #Index
            chargeIndex = masterdata.loc[masterdata['Company Master Data']=='Charges'].index[0]
            SignatoryIndex = masterdata.loc[masterdata['Company Master Data']=='Directors/Signatory Details'].index[0]
            MasterData = masterdata[0:chargeIndex]
            MasterData=(MasterData.rename(columns={'Company Master Data':'key','Unnamed: 2':'value'}))
            MasterData=MasterData[['key','value']]
            MasterData_dict=dict(MasterData.values.tolist())
            Charges=masterdata[chargeIndex:SignatoryIndex-1].fillna('-')
            Charges.columns=Charges.iloc[1]
            Charges=Charges.iloc[2:].reindex()
            Charheader=Charges.columns.tolist()
            ChargesDict={}
            charge_counter=0
            for x in Charges.values.tolist():
                charge_counter=charge_counter+1
                temp_dict={}
                for z,y in zip(Charheader,x):
                    temp_dict[z]=y
                ChargesDict[charge_counter]=temp_dict
            
            Signatories=masterdata[SignatoryIndex:].fillna('-')
            Signatories.columns=Signatories.iloc[1]
            Signatories=Signatories.iloc[2:].reindex()
            Signatories=Signatories.rename(columns={'Begin date ':'BD','End date':'ED'})
            SigHeader=Signatories.columns.tolist()
            SigDict={}
            loop_counter=0
            for x in Signatories.values.tolist():
                loop_counter+=1
                temp_dict={}
                for z,y in zip(SigHeader,x):
                    if str(y).isnumeric():
                            y=y[-8:]
                    temp_dict[z]=y
                SigDict[loop_counter]=temp_dict
            MasterData={}
            ParsedData={}
            MasterData['Status']='Success'
            ParsedData['Masterdata']=MasterData_dict
            ParsedData['Charges']=ChargesDict
            ParsedData['Signatories']=SigDict
            MasterData['data']=ParsedData
            return MasterData
        else:
            MasterData['Status']='Failed'
            MasterData['data']=''
            return MasterData

