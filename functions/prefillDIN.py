import requests
from bs4 import BeautifulSoup as bs
import datetime


def prefillDIN(din_):
    if len(din_)==8 and din_.isnumeric():
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
                        <callID>DIN</callID>
                        <chargeId/>
                        <din>"""+str(din_)+"""</din>
                        <formID>ZI29</formID>
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
            tagDict[tag.name]=tag.text
        if 'messagetext'in tagDict.keys():
            return tagDict['messagetext']
        else:
            DirDetails={}
            DirDetails['director_first_name']=tagDict['firstname']
            DirDetails['director_middle_name']=tagDict['middlename']
            DirDetails['director_family_name']=tagDict['familyname']
            DirDetails['director_gender']=tagDict['rbgender']
            DirDetails['director_fathers_first_name']=tagDict['fatherfirstname']
            DirDetails['director_fathers_middle_name']=tagDict['fathermiddlename']
            DirDetails['director_fathers_last_name']=tagDict['fatherlastname']
            DirDetails['director_present_address']=tagDict['companyaddress'].replace('$',' ').title()
            DirDetails['director_permanent_address']=tagDict['paddresslineone']+' '+tagDict['paddresslinetwo']+' '+tagDict['cityone']+'-'+tagDict['postcodeone']+' '+tagDict['state1']
            DirDetails['director_mobile_number']=tagDict['pmobile']
            DirDetails['director_email_id']=tagDict['email']
            DirDetails['director_nationality']=tagDict['nationality']
            DirDetails['director_place_of_birth']=tagDict['placeofbirth'].title()
            DirDetails['director_occupation']=tagDict['areaofoccu']
            DirDetails['director_date_of_birth']=datetime.datetime.strftime(datetime.datetime.strptime(tagDict['dateofbirth'], "%Y-%m-%dT%H:%M:%S%z"),"%d-%m-%Y")
            if DirDetails['director_date_of_birth']!='':
                Birday=datetime.datetime.strptime(tagDict['dateofbirth'], "%Y-%m-%dT%H:%M:%S%z")
                Byear=Birday.year
                Bmonth=Birday.month
                Bday=Birday.day
                today=datetime.datetime.now()
                age = today.year - Byear - ((today.month, today.day) < (Bmonth, Bday))
                DirDetails['director_age'] = age
            DirDetails['director_educational_qualification']=tagDict['pastate']
            DirDetails['director_aadhar']=tagDict['adhaar']
            DirDetails['director_pan']=tagDict['pan']
            DirDetails['director_passport']=tagDict['passport']
            DirDetails['director_voters_id']=tagDict['voteridcrd']
            return DirDetails
