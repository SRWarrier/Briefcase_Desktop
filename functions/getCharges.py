from bs4 import BeautifulSoup as BS
try:
    from functions.getCaptcha import getMCA_Captcha
    from functions.getCompanyName import getName
    
except:
    from getCaptcha import getMCA_Captcha
    from getCompanyName import getName
import pandas as pd


def getCharges(session,CIN,captcha=''):
    MasterResponse = {}
    Name = getName(CIN)
    if captcha =='':
        getMCA_Captcha(session,True)
        captcha = input('Enter Captcha:\n')
    try:
        header = session.headers
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        header['Referer']='http://www.mca.gov.in/mcafoportal/showIndexOfCharges.do'
        url='http://www.mca.gov.in/mcafoportal/viewIndexOfCharges.do'
        data={"companyName":Name.replace(' ','+'),
             "companyID":CIN,
             "displayCaptcha":"true",
             "userEnteredCaptcha":captcha}
        if len(CIN) == 21:
            response = session.post(url, data=data, headers=header)
            if response.status_code==200:
                chargeTable = response.html.find('#charges',first=True)
                if chargeTable!=None:
                    table = pd.read_html(chargeTable.html)[0]
                    table.columns = list(range(len(list(table.columns))))
                    table = table.drop(columns=1)
                    chargeValues = table.to_json(orient='values')
                    baseList = []
                    for col in eval(chargeValues):
                        tempList = []
                        for val in col:
                                if not isinstance(val,str):
                                        val = str(val)
                                tempList.append(val.replace('\\',''))
                        baseList.append(tempList)
                    MasterResponse['Status'] = 'Success'
                    MasterResponse['data'] = baseList
                    return MasterResponse
                else:
                    MasterResponse['Status'] = 'NoCharges'
                    MasterResponse['data'] = "No Charges Registered"
                    return MasterResponse
    
    except Exception as e:
            MasterResponse['Status'] = 'Failed'
            MasterResponse['data'] = e
            return MasterResponse

def getCapImage():
    ImageData=getMCA_Captcha(session,False)
    return ImageData
    
