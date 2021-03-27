import requests_html
import pickle
import os


def sessionLogout():
    if os.path.isfile('_temp/session'):
        with open('_temp/session', 'rb') as f:
            session = pickle.load(f)
        logoutUrl = 'http://www.mca.gov.in/mcafoportal/logout.do'
        LogOutPage = session.get(logoutUrl)
        WelcomeMsg = LogOutPage.html.find('#welcomeMsg')[0].text
        if 'guest' in WelcomeMsg.lower():
            #print("You have been successfully logged out")
            os.remove('_temp/session')
            return True
    else:
        if os.path.isfile('_temp/session'):
            os.remove('_temp/session')
        return False
    
            
