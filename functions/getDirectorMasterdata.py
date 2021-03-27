import requests_html
import pandas as pd
import pickle


def getDirectorMasterdata(DIN):
    with open('_temp/session', 'rb') as f:
        session = pickle.load(f)
    ValidationUrl = 'http://www.mca.gov.in/mcafoportal/findCompanyForDirector.do'
    data = {'dinNo': DIN}
    DirectorPage = session.post(ValidationUrl,data =data)
    if 'errMsg' in DirectorPage.html.text.lower():
        print(DirectorPage.html.text)
    else:
        print(DirectorPage.html.text)
        CompanyPageUrl = 'http://www.mca.gov.in/mcafoportal/showCompanyResults.do'
        CompaniesPage = session.get(CompanyPageUrl)
        htmlTables = CompaniesPage.html.find('table')
        DirectorsInterestTable=pd.read_html(htmlTables[4].html)[0]
        DirectorsInterestTable.columns = DirectorsInterestTable.iloc[0]
        DirectorsInterestTable = DirectorsInterestTable.drop(index=0)
        return DirectorsInterestTable
