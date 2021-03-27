from functions import getDIN, getDirDetails, getDirName, prefillDIN

def profileDirector(DIN=False, Name=False):
    Master = {}
    ispass = False    
    if Name and not DIN:
        Namesplit = Name.split(',')
        name = Namesplit[0]
        fathersname=''
        dob = ''
        if len(Namesplit)>1:
            if Namesplit[1].replace(' ','').isalpha():
                fathersname = Namesplit[1].strip()
            else:
                dob = Namesplit[1].strip()
            if len(Namesplit)>2:
                fathersname = Namesplit[1].strip()
                dob = Namesplit[2].strip()
        result=getDIN.getDIN(name,fathersname,dob)
        print(result)
        if result['Status']=='Success':
            DIN=result['data'][1]['DIN']
            Name=result['data'][1]['NAME']
            DOB=result['data'][1]['DOB']
            Dinstatus=getDirName.getDirName(DIN)
            if isinstance(Dinstatus,str):
                return Dinstatus
            elif Dinstatus['data']['DIN Status']=='Lapsed' or Dinstatus['data']['DIN Status']=='Disabled' or Dinstatus['data']['DIN Status']=='Deactivated due to non-filing of DIR-3 KYC':
                Master['Status'] = 'Failed'
                Master['Personal'] = f"DIN {DIN} (Name: {Dinstatus['Director Name']}) is {Dinstatus['data']['DIN Status']}."
                return Master
            else:
                Name = Dinstatus['data']['Director Name']
                DINInfo=prefillDIN.prefillDIN(DIN)
        elif result['Status']=='Selection':
            return result
        else:
            Master['Status'] = 'Failed'
            return Master
    elif DIN and not Name:
        Dinstatus=getDirName.getDirName(DIN)
        if isinstance(Dinstatus,str):
            return Dinstatus
        elif Dinstatus['data']['DIN Status']=='Lapsed' or Dinstatus['data']['DIN Status']=='Disabled' or Dinstatus['data']['DIN Status']=='Deactivated due to non-filing of DIR-3 KYC':
            Master['Status'] = 'Failed'
            Master['Personal'] = f"DIN {DIN} (Name: {Dinstatus['data']['Director Name']}) is {Dinstatus['data']['DIN Status']}."
            return Master
        else:
            Name = Dinstatus['data']['Director Name']
            DINInfo=prefillDIN.prefillDIN(DIN)
            
    if isinstance(DINInfo,str):
        return DINInfo
    compDetails=getDirDetails.getDirdetails(DIN)
    Master['Status'] = 'Success'
    DINInfo = {**{'director_name':Name},**DINInfo}
    filterDINinfo = {}
    for key in DINInfo.keys():
        if DINInfo[key]!='':
            filterDINinfo[key] = DINInfo[key]
    Master['Personal'] = filterDINinfo
    if compDetails['Status'] =='Success':
        Master['Companies'] = compDetails['data']
    return Master
    
                  
        
