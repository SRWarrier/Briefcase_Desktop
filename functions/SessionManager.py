import requests_html
import pickle



def getSession():
    session = requests_html.HTMLSession()
    header = session.headers
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    with open('../_temp/cookies', 'wb') as f:
        pickle.dump(session.cookies, f)
    return session
