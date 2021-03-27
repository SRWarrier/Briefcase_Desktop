import requests
from bs4 import BeautifulSoup as bs
import datetime


def getCharge(ChargeID):#10493127
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
                    <callID>INPUT</callID>
                    <chargeId>"""+str(ChargeID)+"""</chargeId>
                    <formID>ZCH4</formID>
                    <sid>NCA</sid>
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
        if not tag.text=='':
            tagDict[tag.name]=tag.text
    if 'messagetext'in tagDict.keys():
        return tagDict['messagetext']
    else:
        ChDetails={}
        ChDetails['charge_cin']=tagDict['personname']
        ChDetails['charge_chargeholder_name']=tagDict['namechrgholder']
        ChDetails['charge_chargeholder_address']=tagDict['companyaddress'].replace('$',',')
        ChDetails['charge_Amount']=float(tagDict['paddresslineone'].strip())
        ChDetails['charge_chargeholder_email']=tagDict['email']
        CreationDate = datetime.datetime.strptime(tagDict['creationdate'],'%Y-%m-%dT00:00:00+05:30')
        ChDetails['charge_creation_date']= datetime.datetime.strftime(CreationDate,'%d %B,%Y')
        ModificationDate = datetime.datetime.strptime(tagDict['modifydate'],'%Y-%m-%dT00:00:00+05:30')
        ChDetails['charge_modification_date']= datetime.datetime.strftime(ModificationDate,'%d %B,%Y') if ModificationDate>=CreationDate else "No Modifications"
        SatisfactionDate = datetime.datetime.strptime(tagDict['satisfydate'],'%Y-%m-%dT00:00:00+05:30')
        ChDetails['charge_satisfaction_date']= datetime.datetime.strftime(SatisfactionDate,'%d %B,%Y') if SatisfactionDate>=CreationDate else "No Satisfaction"
        return ChDetails     
