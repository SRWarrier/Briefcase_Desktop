import requests_html
import hashlib
from io import BytesIO
from PIL import Image
import pandas as pd
import pickle


def Login(username='SRWARRIER92', password='Letmein92@'):
    session = requests_html.HTMLSession()
    header = session.headers
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    loginValidationUrl = 'http://www.mca.gov.in/mcafoportal/js/loginValidations.js'
    Validationdata = session.get(loginValidationUrl,headers = header)
    ValidationKeyString = Validationdata.html.search('astring = "{}"')[0]
    retstr = ''
    for x in range(len(username)):
        aNum = ValidationKeyString.find(username[x:x+1])
        aNum ^= 0xf
        retstr = retstr + ValidationKeyString[aNum:aNum + 1]
    encodedUserName = retstr
    #Default Username= 9!@D!!Y:!S#
    #Def Pwenc = 65100be781516d0fb3571fc01c5c5e35203087c2
    sha = hashlib.sha1()
    sha.update(password.encode())
    EncodedPw = sha.hexdigest()
    loginPage = 'http://www.mca.gov.in/mcafoportal/logout.do'
    LoginPageData = session.get(loginPage,headers = header)
    AccessCode = LoginPageData.html.find('#login_accessCode')[0].attrs['value']
    CaptchaUrl = 'http://www.mca.gov.in/mcafoportal/getCapchaImage.do'
    header['Referer']='http://www.mca.gov.in/mcafoportal/logout.do'
    image_data = session.get(CaptchaUrl, headers=header).content
    img = BytesIO(image_data)
    Image.open(img).show()
    UserCaptcha = input("Enter Captcha: ")
    data = {"browserFlag":"false",
     "loginType":"pwdBasedLogin",
     "userName":"",
     "userNamedenc":encodedUserName,
     "__checkbox_dscBasedLoginFlag":"true",
     "password":"",
     "passwordenc":EncodedPw,
     "Cert":"",
     "strSignature":"",
     "certificateFlag":"",
     "accessCode":AccessCode,
     "displayCaptcha":"true",
     "userEnteredCaptcha":UserCaptcha,
     "operationName":"validateUser",
     "taskID":"",
     "requestedPage":""}
    loginPage = 'http://www.mca.gov.in/mcafoportal/loginValidateUser.do'
    LoginData = session.post(loginPage, headers=header,data = data)
    try:
        WelcomeMsg = LoginData.html.find('#welcomeMsg')[0].text
        if not 'guest' in WelcomeMsg.lower():
            print(LoginData.html.find('#welcomeMsg')[0].text)
            with open('../_temp/session', 'wb') as f:
                pickle.dump(session, f)
        else:
            print("Login Failed")
    except:
        print("Login Failed")
    

def getCompanies(DIN):
##    session = requests_html.HTMLSession()
##    header = session.headers
##    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    with open('../_temp/session', 'rb') as f:
        session = pickle.load(f)
    ValidationUrl = 'http://www.mca.gov.in/mcafoportal/findCompanyForDirector.do'
    data = {'dinNo': DIN}
    DirectorPage = session.post(ValidationUrl, headers=header,data =data)
    if 'errMsg' in DirectorPage.html.text.lower():
        print(DirectorPage.html.text)
    else:
        print(DirectorPage.html.text)
        CompanyPageUrl = 'http://www.mca.gov.in/mcafoportal/showCompanyResults.do'
        CompaniesPage = session.get(CompanyPageUrl,headers=header)
        htmlTables = CompaniesPage.html.find('table')
        DirectorsInterestTable=pd.read_html(htmlTables[4].html)[0]
        DirectorsInterestTable.columns = DirectorsInterestTable.iloc[0]
        DirectorsInterestTable = DirectorsInterestTable.drop(index=0)
        return DirectorsInterestTable
    
    

def logout():
    with open('../_temp/session', 'rb') as f:
        session = pickle.load(f)
    logoutUrl = 'http://www.mca.gov.in/mcafoportal/logout.do'
    session.get(logoutUrl)
    
    
        
