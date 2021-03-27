from io import BytesIO
import requests_html
from PIL import Image


def getMCA_Captcha(session='',view = False):
    header = session.headers
    header['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'
    loginPage = 'http://www.mca.gov.in/mcafoportal/logout.do'
    LoginPageData = session.get(loginPage, headers = header)
    AccessCode = LoginPageData.html.find('#login_accessCode')[0].attrs['value']
    header['Referer']='http://www.mca.gov.in/mcafoportal/logout.do'
    CaptchaUrl = 'http://www.mca.gov.in/mcafoportal/getCapchaImage.do'
    image_data = session.get(CaptchaUrl, headers=header).content
    if view:
        img = BytesIO(image_data)
        Image.open(img).show()
    else:
        return image_data, AccessCode
