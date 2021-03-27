import requests
from bs4 import BeautifulSoup as bs
import datetime


def prefillName(SRN):
    url="http://www.mca.gov.in/FOServicesWeb/NCAPrefillService"
    #headers = {'content-type': 'application/soap+xml'}
    headers = {'content-type': 'text/xml'}
    headers['User-Agent']='Mozilla/3.0 (compatible; Spider 1.0; Windows)'
    headers['Host']='www.mca.gov.in'
    body = """<?xml version="1.0" encoding="UTF-8"?>
    <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
        <soap:Body>
            <tns:getNCAPrefillDetails xmlns:tns="http://ncaprifill.org/wsdl">
                <NCAPrefillProcessorDTO>
                    <callID>SRN</callID>
                    <formID>ZN29</formID>
                    <sid>NCA</sid>
                    <srn>"""+SRN+"""</srn>
                </NCAPrefillProcessorDTO>
            </tns:getNCAPrefillDetails>
        </soap:Body>
    </soap:Envelope>"""
    response = requests.post(url,data=body,headers=headers)
    soup=bs(response.text,'lxml')
    respons_data=soup.find('return')
    All_tags=respons_data.find_all()
    tagDict={}
    for tag in All_tags:
        if tag.text!='':
            tagDict[tag.name]=tag.text
    if 'messagetext'in tagDict.keys():
        return tagDict['messagetext']
    else:
        NameDetails={}
        NameDetails['Company Name']=tagDict['companyorg1']
        NameDetails['Type']=tagDict['nameperson']
        return NameDetails     
