import requests_html
import hashlib
from io import BytesIO
import pickle


def Login(AccessCode, session = requests_html.HTMLSession(), username='SRWARRIER92', password='Letmein92@', captcha=''):
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
     "userEnteredCaptcha":captcha,
     "operationName":"validateUser",
     "taskID":"",
     "requestedPage":""}
    loginPage = 'http://www.mca.gov.in/mcafoportal/loginValidateUser.do'
    header['Referer']='http://www.mca.gov.in/mcafoportal/login.do'
    LoginData = session.post(loginPage,headers = header, data = data)
    try:
        WelcomeMsg = LoginData.html.find('#welcomeMsg')[0].text
        print(WelcomeMsg)
        if not 'guest' in WelcomeMsg.lower():
            with open('_temp/session', 'wb') as f:
                pickle.dump(session, f)
            return True
        else:
            return False
    except:
        return False
    

    
    
        
