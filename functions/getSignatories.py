from bs4 import BeautifulSoup as BS
try:
    from functions.getCaptcha import getMCA_Captcha
except:
    from getCaptcha import getMCA_Captcha


def getSignatory(session,CIN,captcha_switch=True,captcha=''):
    MasterResponse = {}
    if captcha =='':
        getMCA_Captcha(session,True)
        captcha = input('Enter Captcha:\n')
    try:
        header = session.headers
        header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
        header['Referer']='http://www.mca.gov.in/mcafoportal/viewSignatoryDetails.do'
        url='http://www.mca.gov.in/mcafoportal/viewSignatoryDetailsAction.do'
        if captcha_switch==False:
            captcha=''
        data={
            'companyID': CIN,
            'displayCaptcha': 'true',
            'userEnteredCaptcha': captcha,
            'submitBtn': 'Submit'
            }
        if len(CIN) == 21:
            response = session.post(url, data=data, headers=header)
            if len(response.html.xpath('.//ul[@class="errorMessage"]'))>0:
                if response.html.xpath('.//ul[@class="errorMessage"]/li')[0].text == 'Enter valid Letters shown.':
                    MasterResponse['Status'] = 'Failed'
                    MasterResponse['data'] = 'Enter valid Letters shown.'
                    return MasterResponse
            else:
                tablehead=response.html.xpath('.//table[@id="signatoryDetails"]/thead/tr')[0].text.split('\n')
                tablelen=len(response.html.xpath('.//table[@id="signatoryDetails"]/tr[@class="table-row"]'))
                masterSig = {}
                loop_counter = 1
                for i in range(tablelen):
                    tabledata = response.html.xpath('.//table[@id="signatoryDetails"]/tr[@class="table-row"]')[i].text.split('\n')
                    tempDict = {}
                    for key, item in zip(tablehead,tabledata):
                        if 'address' in key.lower():
                            item.title()
                        tempDict[key] = item
                    masterSig[loop_counter] = tempDict
                    loop_counter +=1
                MasterResponse['Status'] = 'Success'
                MasterResponse['data'] = masterSig
                return MasterResponse
            
        else:
            MasterResponse['Status'] = 'Failed'
            MasterResponse['data'] = 'Invalid CIN'
            return MasterResponse

    except Exception as e:
            MasterResponse['Status'] = 'Failed'
            MasterResponse['data'] = e
            return MasterResponse

def getCapImage():
    ImageData=getMCA_Captcha(session,False)
    return ImageData
    
