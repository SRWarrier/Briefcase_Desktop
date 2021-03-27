import requests_html


session = requests_html.HTMLSession()
def getDIN(director_name='', father_name = '', dob = ''):
    DinQuery={}
    try:
        header = session.headers
        header['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
        header['Referer'] = 'http://www.mca.gov.in/mcafoportal/viewDirectorMasterData.do'
        url = 'http://www.mca.gov.in/mcafoportal/dinLookup.do'
        data = {
            'directorName': director_name,
            'fatherLastName': father_name,
            'dob': dob
        }
            
        output = session.post(url, data=data, headers=header)
        if output.json()['success']=='true':
            Directors = {}
            loop_count = 1
            for x in range(len(output.json()['directorList'][:10])):
                tempDict = {}
                for key in list(output.json()['directorList'][x].keys()):
                        if key == 'din':
                                tempDict['DIN']=output.json()['directorList'][x][key]
                        elif key == 'fatherLastName':
                                tempDict['FATHER NAME']=output.json()['directorList'][x][key]
                        elif key == 'dob':
                                tempDict['DOB']=output.json()['directorList'][x][key]
                        elif key == 'directorName':
                                tempDict['NAME']=output.json()['directorList'][x][key]
                Directors[loop_count]=tempDict
                loop_count+=1
            if 20>len(Directors) > 1:
               DinQuery['Status'] = 'Selection'
               DinQuery['data'] = Directors
               return DinQuery
            elif len(Directors)==1:
               DinQuery['Status'] = 'Success'
               DinQuery['data'] = Directors
               return DinQuery
        else:
            DinQuery['Status']='Failed'
            DinQuery['data']='Query return Null'
            return DinQuery
    except:
        DinQuery['Status']='Failed'
        DinQuery['data']='Query Failed'
        return DinQuery
