import requests_html
from bs4 import BeautifulSoup as BS
import pandas as pd
session = requests_html.HTMLSession()



def calcfee(form,CIN=False,AC=False,PURPS=False,NOM=False,DOE=False,TNV=False,SC=False,IC=False,RNOM=False,Charge=False,isAuthorised='N',isSection8='N',isSmallCo='N',isOPC='N'):
    form_dict={'Reserve Unique Name': 'ZI01', 'Form INC-3': 'ZI03', 'Form INC-4': 'ZI04', 'Form INC-5': 'ZI05', 'Form INC-6': 'ZI06',
               'Form INC-12': 'ZI12', 'Form INC-18': 'ZI18', 'Form INC-20': 'ZI20', 'Form INC-20 A': 'Z20A', 'Form INC-22': 'ZI22',
               'Form INC-22A ACTIVE': 'Z22A', 'Form INC-23': 'ZI23', 'Form INC-24': 'ZI24', 'Form INC-27': 'ZI27', 'Form INC-28': 'ZI28',
               'SPICe(INC-32)': 'ZI29', 'Form PAS-2': 'ZPA2', 'Form PAS-3': 'ZPA3', 'Form PAS-6': 'ZPA6', 'Form SH-7': 'ZS07', 'Form SH-8': 'ZS08',
               'Form SH-9': 'ZS09', 'Form SH-11': 'ZS11', 'Form DPT-1': 'ZDP1', 'Form DPT-3': 'ZDP3', 'Form DPT-4': 'ZDP4', 'Form CHG-1': 'ZCH1', 'Form CHG-4': 'ZCH4',
               'Form CHG-6': 'ZCH6', 'Form CHG-8': 'ZCH8', 'Form CHG-9': 'ZCH9', 'Form MGT-3': 'ZM03', 'Form MGT-6': 'ZM06', 'Form MGT-7': 'ZM07', 'Form MGT-10': 'ZM10',
               'Form MGT-14': 'ZM14', 'Form MGT-15': 'ZM15', 'Form-IEPF-1': 'ZIE1', 'Form-IEPF-2': 'ZIE2', 'Form-IEPF-3': 'ZIE3', 'Form-IEPF-4': 'ZIE4', 'Form-IEPF-5': 'ZIE5',
               'Form-IEPF-6': 'ZIE6', 'Form AOC-4': 'ZA04', 'Form AOC-5': 'ZA05', 'Form AOC-4(XBRL)': 'ZA4X', 'Form AOC-4(CFS)': 'ZA4C', 'Form CRA-2': 'ZCR2', 'Form CRA-4': 'ZCR4',
               'Form ADT-1': 'ZAD1', 'Form ADT-2': 'ZAD2', 'Form ADT-3': 'ZAD3', 'Form DIR-3': 'ZD03', 'Form DIR-3 KYC': 'ZD3K', 'Form DIR-5': 'ZD05', 'Form DIR-6': 'ZD06',
               'Form DIR-9': 'ZD09', 'Form DIR-10': 'ZD10', 'Form DIR-11': 'ZD11', 'Form DIR-12': 'ZD12', 'Form DIR-3C': 'ZD3C', 'Form MR-1': 'ZMR1', 'Form MR-2': 'ZMR2',
               'Form STK-2': 'ZST2', 'Form URC-1': 'ZU01', 'Form FC-1': 'ZF01', 'Form FC-2': 'ZF02', 'Form FC-3': 'ZF03', 'Form FC-4': 'ZF04', 'Form GNL-1': 'ZGN1', 'Form GNL-2': 'ZGN2',
               'Form GNL-3': 'ZGN3', 'Form GNL-4': 'ZGN4', 'Form NDH-1': 'ZN01', 'Form NDH-2': 'ZN02', 'Form NDH-3': 'ZN03', 'Form NDH4': 'ZN04', 'Form ADJ': 'ZADJ', 'Form MSC-1': 'ZMS1',
               'Form MSC-3': 'ZMS2', 'Form MSC-4': 'ZMS3', 'Form CG-1': 'ZCG1', 'Form RD-1': 'ZRD1', 'Refund Form': 'ZREF'}
    SPICe_purpose={'other':'PRIC','OPC/Small company':'OPCC'}
    SH_7_purpose={'independently': 'ISCI','Increase in members':'INOM','Government order':'ISCC',
                  'Consolidation or division':'CSDS','Redemption of redeemable preference shares':'RRPS'}
    INC_6_purpose={'Voluntary conversion':'OPC','Mandatory conversion':'PUB'}
    INC_20_purpose={'Revocation of license':'ONDI','Voluntary surrender':'VOLN'}
    INC_22_purpose={'Notice of Situation of Registered Office of the New Company':'22RONC','Notice of Situation of Registered Office of the New Company (Subsequent upon incorporation)':'NWCM','Notice of Change of Registered Office address':'ESCM'}
    INC_27_purpose={'Conversion of private company into public company':'CPBC','Conversion of public company into private company':'CPPC'}
    MGT_14_purpose={'Filing of Resolutions and agreements to the Registrar':'RESL','Filing of the proposed resolution u/s 94(1)':'NONE','Postal ballot resolution(s) under section 110':'PBRL'}
    AOC_4_purpose={'Filing of Provisional unadopted financial statements by private or public company':'OUFS','Filing of Adopted financial statements by private or public company':'AOFS',
                   'Filing of financial statements by One person company':'AOFO','Filing of revised financial statements u/s 130 or 131':'RVSD'}
    CRA_2_purpose={'Intimation of appointment of cost auditor (Original filing)':'ORGN','Intimation of appointment of cost auditor in case of casual vacancy':'FDAD',
                   'Intimation of appointment of cost auditor in case of amalgamation. demerger':'FACV','Intimation of appointment of cost auditor (others)':'OTRS'}
    DIR_12_purpose={'Incorporation':'ESCM','Change':'NWCM'}
    GNL_1_purpose={'Application for Compounding of offences':'ACOO','Application for Extension of AGM up to 3 months':'EAGM',
                   'Application for Scheme of arrangement. amalgamation of Non Govt. company':'AFAO','Application for Scheme of arrangement. amalgamation of Govt. company':'AFAG',
                   'Others':'OTHS'}
    Statecode={'ANDAMAN AND NICOBAR ISLANDS': 'AN', 'ANDHRA PRADESH': 'AP', 'ARUNACHAL PRADESH': 'AR', 'ASSAM': 'AS', 'BIHAR': 'BR',
               'CHANDIGARH': 'CH', 'CHHATTISGARH': 'CT', 'DADAR NAGAR HAVELI': 'DN', 'DAMAN AND DIU': 'DD', 'DELHI': 'DL', 'GOA': 'GA',
               'GUJARAT': 'GJ', 'HARYANA': 'HR', 'HIMACHAL PRADESH': 'HP', 'JAMMU AND KASHMIR': 'JK', 'JHARKHAND': 'JH', 'KARNATAKA': 'KA',
               'KERALA': 'KL', 'LAKSHADWEEP': 'LD', 'MADHYA PRADESH': 'MP', 'MAHARASHTRA': 'MH', 'MANIPUR': 'MN', 'MEGHALAYA': 'ML', 'MIZORAM': 'MZ',
               'NAGALAND': 'NL', 'ORISSA': 'OR', 'PONDICHERRY': 'PY', 'PUNJAB': 'PB', 'RAJASTHAN': 'RJ', 'SIKKIM': 'SK', 'TAMIL NADU': 'TN',
               'TELANGANA': 'TG', 'TRIPURA': 'TR', 'UTTAR PRADESH': 'UP', 'UTTARAKHAND': 'UR', 'WEST BENGAL': 'WB'}

    ReqCIN=('Form INC-4','Form INC-5','Form INC-6','Form INC-23','Form INC-28',
            'Form PAS-2','Form PAS-3','Form INC-20','Form INC-20 A','Form INC-22',
            'Form DPT-1','Form DPT-3','Form DPT-4','Form CHG-1','Form CHG-4','Form CHG-6'
            ,'Form INC-27','Form PAS-6','Form SH-7','Form SH-8','Form SH-9','Form SH-11',
            'Form CHG-8','Form CHG-9','Form MGT-3','Form MGT-6''Form MGT-7''Form MGT-10','Form MGT-14'
            ,'Form MGT-15','Form-IEPF-1','Form-IEPF-3','Form-IEPF-4','Form-IEPF-6','Form AOC-4',
            'Form AOC-5','Form AOC-4(XBRL)','Form AOC-4(CFS)','Form CRA-2','Form CRA-4','Form ADT-1',
            'Form ADT-2','Form ADT-3','Form DIR-9','Form DIR-10','Form DIR-11','Form DIR-12','Form DIR-3C',
            'Form MR-1','Form MR-2','Form FC-1','Form FC-2','Form FC-3','Form FC-4','Form GNL-1',
            'Form GNL-2','Form GNL-3','Form NDH-1','Form NDH-2','Form NDH-3','Form ADJ','Form MSC-1',
            'Form MSC-3','Form MSC-4','Form CG-1','Form RD-1')
    ReqPURPS=('Form INC-6','Form INC-20 A','Form INC-20','Form SH-7','Form INC-22','Form MGT-14'
                'Form INC-27','Form INC-32','SPICe(INC-32)',
                'Form AOC-4','Form CRA-2','Form DIR-12','Form GNL-1')
    ReqTNV=('Form PAS-3','Form PAS-6')
    ReqIC=('Form SH-7')
    ReqAC=('Form INC-22','Form DIR-12','Form URC-1','SPICe(INC-32)',)
    ReqNOM=('Form SH-7')
    ReqDOE=('Form INC-4','Form INC-5','Form INC-6','Form INC-20','Form INC-20 A',
                'Form INC-22','Form INC-27','Form PAS-3','Form PAS-6','Form SH-7',
                'Form SH-11','Form DPT-3','Form DPT-4','Form CHG-1','Form CHG-4',
                'Form CHG-6','Form SH-7''Form CHG-9','Form MGT-3','Form MGT-6','Form MGT-7',
            'Form MGT-10','Form MGT-14','Form MGT-15','Form-IEPF-3','Form AOC-4','Form AOC-5',
            'Form AOC-4(XBRL)','Form AOC-4(CFS)','Form CRA-2','Form CRA-4','Form ADT-1','Form ADT-3',
            'Form DIR-11','Form DIR-12','Form DIR-3C','Form MR-1','Form FC-1','Form FC-2',
            'Form FC-3','Form FC-4','Form GNL-3','Form NDH-1','Form NDH-3')
    ReqSC=('Form FC-1','SPICe(INC-32)')
    ReqRNOM=('Form SH-7')
    ReqCharge=('Form CHG-1','Form CHG-9')


    checkCIN=form in ReqCIN
    checkIC=form in ReqIC
    checkAC=form in ReqAC
    checkPURPS=form in ReqPURPS
    checkNOM=form in ReqNOM
    checkDOE=form in ReqDOE
    checkTNV=form in ReqTNV
    checkSC=form in ReqSC
    checkRNOM=form in ReqNOM
    checkCharge=form in ReqCharge

    def getPurpose(PURPS,form):
        if form.lower()=='spice(inc-32)':
            return SPICe_purpose[PURPS]
        if form.lower()=='form dir-12':
            return DIR_12_purpose[PURPS]

    def State(SC):
        SC_list=Statecode.items()
        for x in SC_list:
            if x[0].find(SC.upper())!=-1:
                return x[1]
        
    disq='Require: '

    if checkPURPS:
        if PURPS!=False:
            PURPS=getPurpose(PURPS,form)
        elif PURPS==False:
            disq=disq+"Purpose of filing and "
            
        
    if checkCIN:
        if CIN!=False:
            if len(CIN)==21 and ' ' not in CIN:
                CIN=CIN
            else:
                CIN=getCIN(CIN)[0]  
        elif PURPS != False:
            if PURPS not in ('ESCM'):
                disq=disq+"CIN and "
            
    if checkIC:
        if PURPS in ('ISCI','ISCC'):
            if IC==False:
                disq=disq+"Increased Authorised Capital and "
                
    if checkAC:
        if PURPS in ('ZD12','22RONC','PRIC','OPCC','NWCM','ESCM'):
            if AC!=False:
                isAuthorized='Y'
            else:
                disq=disq+"Authorised Capital and "

    if checkRNOM:
        if PURPS in ('INOM'):
            if RNOM==False:
                disq=disq+"Increased Number of Members and "
            
        

       
    if checkRNOM:
        if RNOM==False:
            disq=disq+"Number of Members and "


    if checkDOE:
        if DOE==False or PURPS not in ('FACV','NONE'):
            if DOE==False:
                if PURPS!=False:
                    if PURPS not in ('ESCM'):
                        disq=disq+"Date of Event and "

    if checkTNV:
        if TNV==False:
            disq=disq+"Total Nominal Value and "

    if checkSC:
        if PURPS==('PRIC','OPCC'):
            if SC==False:
                disq=disq+"State and "
        if SC==False:
            disq=disq+"State and "
        else:
            SC=State(SC)
           
    if checkCharge:
        if Charge==False:
            disq=disq+"Amount of Charge and "

    if not disq=='Require: ':
        return disq.strip('and ')
    else:
        if CIN==False:
            CIN=''
        if AC==False:
            AC=''
        if PURPS==False:
            PURPS=''
        if NOM==False:
            NOM=''
        if DOE==False:
            DOE=''
        if TNV==False:
            TNV=''
        if SC==False:
            SC='none'
        if RNOM==False:
            RNOM=''
        if Charge==False:
            Charge=''
        if IC==False:
            IC=''
        #find Form id
        form_id=form_dict[form]

        
        header = session.headers
        header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
        header['Referer'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
        url="http://www.mca.gov.in/mcafoportal/showCompanyFeePostLogin.do"
        data={
            'formSelected': form_id,
            'companyid' :CIN,
            'authorizedCapital': AC ,   
            'dateOfEvent':  DOE,
            'totalNominalValue':TNV,
            'stateCode': SC,
            'increasedContribution' :IC,
            'revisedNumberOfMembers': RNOM, 
            }
         

       
        if form_id in ('ZI04','ZI05','ZI06','ZI12','ZI18','ZI20','ZI22','ZI24','ZI28','ZI29'):
            data['numberOfMembers']=''
            data['amountOfChargeSecured']=''
            if form_id in ('ZI05','ZI12','ZI18'):
                data['prelogin']=''
            if PURPS in ('OPC','ONDI','PUB','VOLN','22RONC','CPBC','CPPC'):
                data['selectedPurpose']=PURPS
            if PURPS in ('PUB','VOLN','NWCM'):
                data['prelogin']=''
            if PURPS in ('22RONC','NWCM','PRIC'):
                data['isAuthorizedCapital']=isAuthorised
                data['lastTimeCapitalIncreasedDate']=''
                if isAuthorised=='N':
                    data.pop('authorizedCapital')
                    data['prelogin']=''
        if form_id in ('Z123'):
            data.pop('companyid')
            data['isAuthorizedCapital']=isAuthorised
            data['lastTimeCapitalIncreasedDate']=''
            data['numberOfMembers']=NOM
            data['isOpcCompany']=isOPC
            data['isSection8Company']=isSection8
            if isAuthorised=='N':
                    data.pop('authorizedCapital')
                    data['prelogin']=''
            if isOPC=='N':
                data['isSmallCompany']=isSmallCo
                data['prelogin']=''
        if form_id in ('ZI29'):
            data['selectedPurpose']=PURPS
            data['isSection8Company']=isSection8
            if PURPS in ('OPCC'):
                data.pop('isSection8Company')
                data['prelogin']=''
        print(data)             
        url='http://www.mca.gov.in/mcafoportal/showCompanyFeePostLogin.do'
        output = session.post(url, data=data, headers=header)
        soup=BS(output.text,'lxml')
        table=soup.find('table',{'id':'feeresult'})
        tabledata=table.findAll('tr')
        records = []
        for tr in tabledata:
            td=tr.find_all('td')
            row=[tr.text.replace('\n','').replace('\t','').replace('\r','') for tr in td]
            records.append(row)
        feedetails=pd.DataFrame(records)
        feedetails=feedetails.rename(columns=feedetails.iloc[0])
        feedetails=feedetails[2:]
        return feedetails
