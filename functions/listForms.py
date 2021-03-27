import requests
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile
from io import BytesIO
import os
import time


session = requests.Session()
def getForm():
    MCA_root = 'http://www.mca.gov.in'
    Rq_header = session.headers
    Rq_header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0'
    Rq_header['Referer'] = 'http://www.mca.gov.in/'
    Rq_header['Upgrade-Insecure-Requests'] = '1'
    # Get Forms
    forms_page = 'http://www.mca.gov.in/MinistryV2/companyformsdownload.html'
    response = session.get(forms_page, headers=Rq_header)
    soup = bs(response.text, 'lxml')
    main_content = soup.find('div', {'id': 'skipMain'})
    form_links = main_content.findAll('a')
    _forms = []
    for link in form_links:
        if link['href'][-9:] != '_help.zip':
            if link['href'][-3:] == 'zip':
                _forms.append(MCA_root+link['href'])
    Forms_dict = {}
    for form in _forms:
        key = os.path.split(form)[-1].strip('.zip')
        Forms_dict[key] = form
    return Forms_dict
