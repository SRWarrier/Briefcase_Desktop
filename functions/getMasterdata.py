import requests_html
from bs4 import BeautifulSoup as BS
try:
    from functions.getCIN import getCIN
except:
    from getCIN import getCIN
import pandas as pd
import re

session = requests_html.HTMLSession()
CLEAN = re.compile('\s+')
def getMasterData(CINorName,forMasterdata=True):
    GetCookie = session.get("http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do")
    MasterData={}
    hasPassed = False
    try:
        header = session.headers
        header['Host']= 'www.mca.gov.in'
        header['User-Agent']= 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv=76.0) Gecko/20100101 Firefox/76.0'
        header['Accept']= 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        header['Accept-Language']= 'en-US,en;q=0.5'
        header['Accept-Encoding']= 'gzip, deflate'
        header['Content-Type']= 'application/x-www-form-urlencoded'
        header['Origin']= 'http=//www.mca.gov.in'
        header['Connection']= 'keep-alive'
        header['Referer']= 'http=//www.mca.gov.in/mcafoportal/viewCompanyMasterData.do'
        header['Upgrade-Insecure-Requests']= '1'
        if CINorName.find(" ")!=-1 or CINorName.isalpha():
            data=getCIN(CINorName,forMasterdata)
            if data['Status']=='Success':
                CIN = data['data'][1]['CIN']
                hasPassed = True
            elif data['Status'] == 'Selection':
                return data
            else:
                return data
            
        elif CINorName.isalnum() and len(CINorName)==21:
            CIN=CINorName
            hasPassed = True
        else:
            return "Invalid CIN/Name"
        if hasPassed:
            captcha=''
            CName=''
            data={
                    'companyName': CName,
                    'companyID': CIN,
                    'displayCaptcha': 'false',
                    'userEnteredCaptcha': captcha
                    }
            url='http://www.mca.gov.in/mcafoportal/companyLLPMasterData.do'
            response = session.post(url, data=data, headers=header)
            print(response)
            soup=BS(response.content,'lxml')
            if soup.find('ul',{'class':'errorMessage'}):
                if soup.find('ul',{'class':'errorMessage'}).text.strip('\n') == 'Enter valid Letters shown.':
                    print('Captcha Error')
                    time.sleep(2)

            else:
                MasterDatatable=soup.find('table',{'id':'resultTab1'})
                MDtable=[]
                for tr in MasterDatatable.findAll("tr"):
                    tablecontents =[CLEAN.sub(' ', x.text).strip() for x in tr.findAll("td")]
                    MDtable.append(tablecontents)
                _MasterData = (pd.DataFrame(MDtable)).reset_index(drop=True)
                _MasterData=_MasterData.rename(columns={0:'key',1:'value'})
                MasterDataKeys = ['company_cin','company_name','company_roc','company_registration_number','company_category',
                                       'company_subcategory','company_class','company_authorized_capital','company_paidup_capital',
                                       'company_no_of_members','company_date_of_incorporation','company_registered_address','company_other_than_regsitered_office',
                                       'company_email_id','company_listed','company_active_status',
                                       'company_suspended','company_date_of_last_agm','company_date_of_balance_sheet',
                                       'company_status']
                MasterData_dict=dict(_MasterData.values.tolist())
                MasterData_dict = dict(zip(MasterDataKeys,list(MasterData_dict.values())))
                Chargedtable=soup.find('table',{'id':'resultTab5'})
                CHtable=[]
                for tr in Chargedtable.findAll("tr"):
                    tableheaders=[CLEAN.sub(' ', x.text).strip() for x in tr.findAll("th")]
                    tablecontents =[CLEAN.sub(' ', x.text).strip() for x in tr.findAll("td")]
                    CHtable.append(tableheaders)
                    CHtable.append(tablecontents)
                Charges = (pd.DataFrame(CHtable))
                Charges = Charges.dropna(how='all') 
                Charges = Charges.fillna('NA')
                Charges.columns=Charges.iloc[0]
                Charges=Charges.drop(index=0).dropna().reset_index(drop=True)
                if Charges.empty:
                    Charges=Charges.append({'Assets under charge':"No Charges Exists for Company/LLP"},ignore_index=True)                       
                Charheader=['charge_assets','charge_amount','charge_creation_date','charge_modification_date','charge_status']
                ChargesDict={}
                loop_counter=0
                for x in Charges.values.tolist():
                    loop_counter+=1
                    tempDict={}
                    for z,y in zip(Charheader,x):
                        tempDict[z]=y
                    ChargesDict[loop_counter]=tempDict
                Signatoriestable=soup.find('table',{'id':'resultTab6'})
                SItable=[]
                for tr in Signatoriestable.findAll("tr"):
                    tableheaders=[CLEAN.sub(' ', x.text).strip() for x in tr.findAll("th")]
                    tablecontents =[CLEAN.sub(' ', x.text).strip() for x in tr.findAll("td")]
                    SItable.append(tableheaders)
                    SItable.append(tablecontents)
                Signatories = (pd.DataFrame(SItable))
                Signatories.columns=Signatories.iloc[0]
                Signatories=Signatories.drop(index=0).dropna().reset_index(drop=True)
                del Signatories['Surrendered DIN']
                SigHeader=['director_din','director_name','director_appointment_date','director_cessation_date']
                SigDict={}
                loop_counter=0
                for x in Signatories.values.tolist():
                    loop_counter+=1
                    tempDict={}
                    for z,y in zip(SigHeader,x):
                        if y.isnumeric():
                                y=y[-8:]
                        tempDict[z]=y
                    SigDict[loop_counter]=tempDict
                ParsedData={}
                MasterData['Status']='Success'
                ParsedData['Masterdata']=MasterData_dict
                ParsedData['Charges']=ChargesDict
                ParsedData['Signatories']=SigDict
                MasterData['data']=ParsedData
                return MasterData
    except IndexError as e:
        print(e)
        MasterData['Status']='Failed'
        MasterData['data']=''
        return MasterData
