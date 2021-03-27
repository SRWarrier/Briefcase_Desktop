from io import BytesIO
import requests_html
from PIL import Image


def getMCA_Captcha(session='',view = False):
    header = session.headers
    header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
    header['Referer']='http://www.mca.gov.in/mcafoportal/viewSignatoryDetails.do'
    CaptchaUrl = 'http://www.mca.gov.in/mcafoportal/getCapchaImage.do'
    image_data = session.get(CaptchaUrl, headers=header).content
    if view:
        img = BytesIO(image_data)
        Image.open(img).show()
    else:
        return image_data
