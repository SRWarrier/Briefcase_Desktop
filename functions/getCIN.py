import requests_html
import re

session = requests_html.HTMLSession()
CLEAN = re.compile('\s+')

def getHeader():
    
    return header

def getCIN(name,masterdata=False):
        master_response={}
        header = session.headers
        header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
        header['Referer'] = 'http://www.mca.gov.in/mcafoportal/viewCompanyMasterData.do'
        url = 'http://www.mca.gov.in/mcafoportal/cinLookup.do'
        data = {
            'companyname': name
        }
        
        try:
            response = session.post(url, data=data, headers=header)
        except Exception:
            master_response['Status']='failed'
            master_response['data']="Invalid Query"
            return master_response
        if response.json()['success'] == 'true':
            response_data=response.json()
            return_dict={}
            for x in range(len(response_data['companyList'][:10])):
                tempdict={}
                for key in response_data['companyList'][x].keys():
                    if key == 'companyID':
                        tempdict['CIN'] = response_data['companyList'][x][key]
                    elif key == 'companyName':
                        tempdict['Name'] = response_data['companyList'][x][key]
                return_dict[x+1]=tempdict
            if len(return_dict)==1:
                master_response['Status']='Success'
                master_response['data']=return_dict
            elif len(return_dict)>1:    
                master_response['Status']='Selection'
                master_response['data']=return_dict
            else:
                master_response['Status']='failed'
                master_response['data']="No Matches found for existing name."
        elif response.json()['success'] == 'false':
            master_response['Status']='failed'
            master_response['data']="No Matches found for existing name."
        return master_response
