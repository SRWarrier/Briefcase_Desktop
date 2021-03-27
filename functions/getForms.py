import requests
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile
from io import BytesIO
import os
import time


session = requests.Session()


def getForm(Forms_dict,FormName,CompanyName,Purpose):
    MCA_root = 'http://www.mca.gov.in'
    Rq_header = session.headers
    Rq_header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    Rq_header['Referer'] = 'http://www.mca.gov.in/'
    Rq_header['Upgrade-Insecure-Requests'] = '1'
    # Get Forms
    Form_url = Forms_dict[FormName]
    form_zip = session.get(Form_url, headers=Rq_header)
    if form_zip.status_code == 200:
        with ZipFile(BytesIO(form_zip.content)) as zipObj:
            listOfFileNames = zipObj.namelist()
            Tx = CompanyName.split()
            FileNamePdf = Tx[0]+'_'+Tx[1]+'_'+FormName+'_'+Purpose.replace(' ','_')+'.pdf'
            for fileName in listOfFileNames:
                if fileName.endswith(f'{FormName}.pdf'):
                    if not os.path.exists(CompanyName):
                        os.makedirs(os.path.join(CompanyName,Purpose))
                    with open(os.path.join(CompanyName,Purpose, FileNamePdf), 'wb') as f:
                        f.write(zipObj.read(fileName))
                        os.startfile(os.path.join(CompanyName, Purpose,FileNamePdf))
                elif fileName.endswith(f'{FormName.replace("Form_","Form ")}.pdf'):
                    if not os.path.exists(CompanyName):
                        os.makedirs(os.path.join(CompanyName,Purpose))
                    with open(os.path.join(CompanyName,Purpose, FileNamePdf), 'wb') as f:
                        f.write(zipObj.read(fileName))
                        os.startfile(os.path.join(CompanyName,Purpose,FileNamePdf))
                    
