#import requests_html
#from bs4 import BeautifulSoup as BS
import pandas as pd
import numpy as np



#session = requests_html.HTMLSession()

def findForm(form_info, addForm='',addDesc=''):
    form_id={'SERIOUS COMPLAINT FORM': 'FORM SCP', 'Application for extension of Time': 'FORM NDH-2', 'Form for filing financial statement and other documents with the Registrar': 'FORM AOC-4',
    'Simplified Proforma for Incorporating Company Electronically (SPICe) - with mandatory PAN & TAN application included.': 'SPICE', 'Information by auditor to Registrar': 'FORM 23B',
     'Form for submission of documents with the Registrar.': 'FORM GNL-2', 'Addendum for rectification of defects or incompleteness.': 'FORM GNL-4',
     'Form for filing Addendum for Rectification of Defects or Incompleteness': 'FORM RD GNL-5', 'Half Yearly Return': 'FORM NDH-3',
     'Form of intimation of appointment of cost auditor by the company to Central Government.': 'FORM CRA-2',
     'Filing Profit and Loss account and otherdocuments with the Registrar': 'FORM 23ACA', 'eArticles of Association (SPICe AoA)': 'SPICE AOA',
     'One Person Company- Application for Conversion': 'FORM INC-6', 'Form for filing Cost Audit Report with the Central Government.': 'FORM CRA-4',
     'Statement regarding deposits existing on the commencement of the Act': 'FORM DPT-4',
     'Application for allotment of Director Identification Number in existing company': 'FORM DIR-3',
     'Information Memorandum': 'FORM PAS-2', 'Applications made to Registrar of Companies': 'FORM GNL-1', 
     'Form for filing XBRL document in respect of financial statement and other documents with the Registrar': 'FORM AOC-4(XBRL)', 
     'Application for requesting refund of fees paid.': 'FORM REFUND', 'Private Placement Offer Letter': 'FORM PAS-4',
      'Application for declaration as Nidhi Company and for updation of status by Nidhis': 'FORM NDH-4', 
      'Form for filing application or documents with Central Government': 'FORM CG-1', 
      'Application by company to ROC for removing its name from register of Companies': 'FORM STK-2', 
      'Notice of Resignation by the Auditor': 'FORM ADT-3', 'Return of appointment of Managin Director/Whole Time Director/Manager': 'FORM MR-1', 
      'A Report by a company to ROC for intimating the disqualification of the director': 'FORM DIR-9',
       'Intimation of Director Identification Number by the company to the Registrar DIN services': 'FORM DIR-3C', 
       'Application for surrender of Director Identification Number': 'FORM DIR-5', 'Return of dormant companies': 'FORM MSC-3', 
       'Filing financial statement and other documents with the Registrar': 'FORM 23AC', 'Return of allotment': 'FORM PAS-3', 
       'Circular or circular in the form of advertisement inviting deposits': 'FORM DPT-1', 
       'Filing of Resolutions and agreements to the Registrar': 'FORM MGT-14', 
       'Notice of situation or change of situation of registered office': 'FORM INC-22', 
       'Form for filing XBRL document in respect of financial statement and other documents with the Registrar.': 'FORM 23AC (XBRL)', 
       'Annual Return of a Foreign company': 'FORM FC-4', 
       'Application to Regional Director for approval to shift the Registered Office from one state to another state or from jurisdiction of one Registrar to another Registrar within the same State': 'FORM INC-23',
        'Application for registration of creation or modification of charge for debentures or rectification of particulars filed in respect of creation or modification of charge for debentures': 'FORM CHG-9', 
        'Letter of offer': 'FORM SH-8', 'Application for Goods and services tax Identification number, employees state Insurance corporation registration pLus Employees provident fund organisation registration (AGILE)': 'AGILE', 
        'Form for filing consolidated financial statements and other documents with the Registrar': 'FORM AOC-4(CFS)', 
        'Information by cost auditor to Central Government': 'FORM 23D', 'Memorandum of Appeal': 'FORM ADJ', 
        'Return of alteration in the documents filed for registration by foreign company': 'FORM FC-2', 
        'Notice of appointment or cessation of receiver or manager': 'FORM CHG-6', 
        'Application for KYC of Director': 'FORM DIR-3 KYC', 'Application for removal of auditor(s) from his/their office before expiry of term': 'FORM ADT-2', 
        'Application for approval of Central Government for change of name': 'FORM INC-24', 
        'Notice of Order of the Court or any other competent authority': 'FORM INC-28', 
        'Notice of situation or change of situation or discontinuation of situation,of place where foreign register shall be kept': 'FORM MGT-3', 
        'Declaration for commencement of business': 'FORM INC-20A', 'Form for filing XBRL document inrespect of cost audit report andother documents with the CentralGovernment': 'FORM I-XBRL', 
        'One Person Company- Intimation of exceeding threshold': 'FORM INC-5', 'Application for seeking status of active company': 'FORM MSC-4',
        'Application by a company for registration under section 366': 'FORM URC-1', 'Information to be filed by foreign company': 'FORM FC-1',
        'Application for registration of creation, modification of charge (other than those related to debentures)': 'FORM CHG-1',
        'Form of application for removal of disqualification of directors': 'FORM DIR-10',
        'Application for grant of License under section 8': 'FORM INC-12', 'Return of Statutory Compliances': 'FORM NDH-1',
        'Details of persons/directors/charged/specified': 'FORM GNL-3', 'Return in respect of buy-back of securities': 'FORM SH-11',
        'Particulars for satisfaction of charge thereof': 'FORM CHG-4',
        'Form of application to the Central Government for approval of appointment or reappointment and remuneration or increase in remuneration or waiver for excess or over payment to managing director or whole time director or manager and commission or remuneration to directors': 'FORM MR-2',
        'Particulars of appointment of Director and the key managerial personnel and the changes among them': 'FORM DIR-12',
        'Intimation to Registrar of revocation/surrender of license issued under section 8': 'FORM INC-20', 'Particulars of annual return for the company not having share capital': 'FORM-21A',
        'Form of application to the Central Government for appointment of cost auditor.': 'FORM 23C', 'Declaration of Solvency': 'FORM SH-9',
        'Application to Regional director for conversion of section 8 company into company of any other kind': 'FORM INC-18',
        'Application to Registrar for obtaining the status of dormant company': 'FORM MSC-1', 'INVESTOR COMPLAINT FORM': 'FORM ICP',
        'Conversion of public company into private company or private company into public company': 'FORM INC-27', 'eMemorandum of Association (SPICe MoA)': 'SPICE MOA', 'Annual accounts along with the list of all principal places of business in India established by foreign company': 'FORM FC-3', 'Form for filing Report on Annual General Meeting': 'FORM MGT-15', 'Filing annual return by a companyhaving a share capital with the Registrar.': 'FORM-20B (Companies Act 1956)', 
        'Return to the Registrar in respect of declaration under section 90': 'FORM BEN-2',
         'Active Company Tagging Identities and Verification (ACTIVE)': 'FORM INC-22A', 
        'Return of deposits': 'FORM DPT-3', 
        'Applications made to Regional Director': 'FORM RD-1', 'One Person Company- Change in Member/Nominee': 'FORM INC-4', 
        'Application to Central Government for extension of time for filing particulars of registration of creation / modification / satisfaction of charge OR for rectification of omission or misstatement of any particular in respect of creation/ modification/ satisfaction of charge': 'FORM CHG-8', 
       'One Person Company- Nominee consent form': 'FORM INC-3', 
       'Form for filing annual return by a company.': 'FORM MGT-7',
        'Reply To Call for Information on CSR': 'FORM CFI(CSR)', 
       'Persons not holding beneficial interest in shares': 'FORM MGT-6', 
       'Information to the Registrar by company regarding the number of layers of subsidiaries.': 'FORM CRL-1', 
       'Information to the Registrar by Company for appointment of Auditor': 'FORM ADT-1',
        'Form for submission of compliance certificate with the Registrar': 'FORM 66', 
       'Intimation of change in particulars of Director to be given to the Central Government': 'FORM DIR-6', 
       'Form for filing XBRL document in respect of Profit and Loss account and other documents with the Registrar.': 'FORM 23ACA (XBRL)', 
       'Notice to Registrar of any alteration of share capital': 'FORM SH-7',
        'Form for filing XBRL document inrespect of compliance report andother documents with the CentralGovernment': 'FORM A XBRL', 
       'Application for striking off the name of company under the Fast Track Exit(FTE) Mode': 'FORM FTE', 
       'Notice of address at which books of account are maintained': 'FORM AOC-5', 
       'Form for furnishing half yearly return with the registrar in respect of outstanding payments to Micro or Small Enterprise.': 'FORM MSME', 
       'Notice of resignation of a director to the Registrar': 'FORM DIR-11'}
    Syn_dict=dict.fromkeys(['annual filing','annual returns' 'financial statement','annual report','balance sheet','pnl','profit and loss'],"financial statement")
    Syn_dict.update(dict.fromkeys(['director','directrr','directar','directr','directors'],'director'))
    Syn_dict.update(dict.fromkeys(['din'],'director identification number'))               
    form_data=(pd.DataFrame(list(form_id.items()))).rename(columns={0:"Description",1:"Form"})
    stop_words = ['form','for','filing','is','was','be','when','how']
    responseDict={}
    if str(form_info).replace(' ','').replace('-','').isalpha():
        query=form_info.lower().split(' ') 
        for x in query:
            try:
                if  x in stop_words:
                    word_ix=query.index(x)
                    query.pop(word_ix)
                    continue
                word_ix=query.index(x)
                query[word_ix]=Syn_dict[x]
            except Exception:
                continue
        indexlist=(form_data[np.logical_and.reduce([(form_data['Description'].str.lower()).str.contains(word) for word in query])]).index.tolist()
        loop_counter=0
        for x in indexlist:
            loop_counter+=1
            tempDict={}
            tempDict['form']=[form_data['Form'].iloc[x]]
            tempDict['description']=form_data['Description'].iloc[x]
            responseDict['Status']='Success'
            responseDict[loop_counter]=tempDict
        return responseDict
   
    elif str(form_info.replace('-','')).replace(' ','').isnumeric() or str(form_info).replace('-','').replace(' ','').isalnum():
        query=form_info.lower()
        def CA1956(text):
            CA1956=('FORM 23AC','FORM 23AC (XBRL)','FORM 21A','FORM 66','FORM 23ACA(XBRL)','FORM 23B','FORM 23ACA')
            if text in CA1956:
                return " (Companies Act, 1956)"
            else:
                return ''
        try:
            query=query.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~=_+"}).upper()
            responseDict={}
            if query.lower().find('form')!=0:
                query='FORM '+ (query.replace('FORM',''))
            tempDict={}
            tempDict['form']=query+CA1956(query)
            tempDict['description']=form_data.loc[(form_data['Form']==query),'Description'].iloc[0]
            responseDict['Status']='Success'
            responseDict[1]=tempDict
            return responseDict
        except IndexError:
            indexlist=(form_data[np.logical_and.reduce([form_data['Form'].str.contains(word) for word in query])]).index.tolist()
            responseDict['Status']='Partial Match/No Match'
            loop_counter=0
            for x in indexlist:
                loop_counter+=1
                tempDict={}
                tempDict['form']=form_data['Form'].iloc[x]+CA1956(query)
                tempDict['description']=form_data['Description'].iloc[x]
                responseDict[loop_counter]=tempDict
            return responseDict
