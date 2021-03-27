import sqlite3 as lite
import sys
import datetime
import sys, os

def createDBFile(Path):
    con = lite.connect(os.path.join(Path,'C3_DataBase.db'))
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Masterdata('company_cin' TEXT UNIQUE, 'company_name' TEXT, 'company_roc' TEXT,\
                'company_registration_number' TEXT, 'company_category' TEXT, 'company_subcategory' TEXT,\
                'company_class' TEXT, 'company_authorized_capital' TEXT, 'company_paidup_capital' TEXT,\
                'company_date_of_incorporation' TEXT, 'company_registered_address' TEXT,\
                'company_email_id' TEXT, 'company_listed' TEXT,\
                'company_pan' TEXT,'company_gstin' TEXT, 'company_phone' TEXT , 'company_refer' TEXT, 'filehash' TEXT, 'company_last_update' DATE)" )
    cur.execute("CREATE TABLE IF NOT EXISTS basicInfo('NAME' TEXT, 'ADDRESS' TEXT, 'PAN' TEXT,'GSTIN' TEXT, 'BANK' TEXT,'BRANCH' TEXT, 'ACCOUNTNO' TEXT,'IFSC' TEXT,'MICR' TEXT)" )
    cur.execute("CREATE TABLE IF NOT EXISTS Contacts('company_cin' TEXT, 'contact_person_name' TEXT, 'contact_person_designation' TEXT,\
                'contact_person_mobile' TEXT, 'contact_person_email_id' TEXT, unique (company_cin, 'contact_person_name','contact_person_designation'))" )
    cur.execute("CREATE TABLE IF NOT EXISTS HoldingCompanies('company_cin' TEXT, 'entity_name' TEXT, 'entity_type' TEXT,\
                'holding' TEXT, 'country_of_origin' TEXT, unique (company_cin, 'entity_name'))" )
    cur.execute("CREATE TABLE IF NOT EXISTS SubsidiaryCompanies('company_cin' TEXT, 'entity_name' TEXT, 'entity_type' TEXT,\
                'investment' TEXT, 'country_of_origin' TEXT, unique (company_cin, 'entity_name'))" )
    cur.execute("CREATE TABLE IF NOT EXISTS AssociateCompanies('company_cin' TEXT, 'entity_name' TEXT, 'entity_type' TEXT,\
                'holding' TEXT, 'country_of_origin' TEXT, unique (company_cin, 'entity_name'))" )
    cur.execute("CREATE TABLE IF NOT EXISTS documents('company_cin' TEXT, 'document_name' TEXT, 'document_location' TEXT,unique (company_cin, 'document_location'))" )
    cur.execute("CREATE TABLE IF NOT EXISTS Shareholders('company_cin' TEXT, 'name' TEXT, 'fathers name' TEXT,\
                'address' TEXT,'nationality' TEXT, 'shares' TEXT,'type of share' TEXT, 'file' TEXT, unique (company_cin, 'name', 'type of share'))" )
    cur.execute("CREATE TABLE IF NOT EXISTS Signatories('company_cin' TEXT,'director_din'  TEXT, 'director_name' TEXT, 'director_address' TEXT, 'Designation' TEXT,'director_date_of_appointment' TEXT,'director_dsc_registered' TEXT, 'director_dsc_expiry_date' DATE,'director_first_name' TEXT, 'director_middle_name' TEXT,'director_family_name' TEXT, director_gender TEXT, 'director_fathers_first_name' TEXT, 'director_fathers_middle_name' TEXT, 'director_fathers_last_name' TEXT, 'director_present_address' TEXT, 'director_permanent_address' TEXT, director_mobile_number TEXT, director_email_id TEXT, director_nationality TEXT, 'director_place_of_birth' TEXT, 'director_occupation' TEXT, 'director_date_of_birth' DATE, director_age TEXT, 'director_educational_qualification' TEXT, director_aadhar TEXT, director_pan TEXT, director_passport TEXT, 'director_otherID' TEXT,Alias TEXT,unique (company_cin, 'director_din'))")
    cur.close()
    con.commit()
    con.close()
    con = lite.connect(os.path.join(Path,'chat.db'))
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS chat('USER' TEXT, 'MESSAGE' TEXT, 'ATTACHMENT' TEXT, 'TIME' TEXT)" )
    cur.close()
    con.commit()
    con.close()
    
def updateMasterdata(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS Masterdata('company_cin' TEXT UNIQUE, 'company_name' TEXT, 'company_roc' TEXT,\
                'company_registration_number' TEXT, 'company_category' TEXT, 'company_subcategory' TEXT,\
                'company_class' TEXT, 'company_authorized_capital' TEXT, 'company_paidup_capital' TEXT,\
                'company_date_of_incorporation' TEXT, 'company_registered_address' TEXT,\
                'company_email_id' TEXT, 'company_listed' TEXT,\
                'company_pan' TEXT,'company_gstin' TEXT, 'company_phone' TEXT , 'company_refer' TEXT, 'filehash' TEXT, 'company_last_update' DATE)" )
    
    #Masterdata
    infoDict.append(datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S'))
    Masterdatatuple =tuple(infoDict)


    #UPSERT
    cur.execute("INSERT OR REPLACE INTO Masterdata VALUES"+str(Masterdatatuple))
    cur.close()
    con.commit()
    con.close()


def basicInfo(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS basicInfo('NAME' TEXT, 'ADDRESS' TEXT, 'PAN' TEXT,'GSTIN' TEXT, 'BANK' TEXT,'BRANCH' TEXT, 'ACCOUNTNO' TEXT,'IFSC' TEXT,'MICR' TEXT)" )
    
    #UPSERT
    datatuple =tuple(infoDict)


    #UPSERT
    cur.execute("REPLACE INTO basicInfo VALUES"+str(datatuple))
    cur.close()
    con.commit()
    con.close()

def chathistory(infoDict):
    con = lite.connect('Database/chat.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS chat('USER' TEXT, 'MESSAGE' TEXT, 'ATTACHMENT' TEXT, 'TIME' TEXT)" )
    
    #UPSERT
    datatuple =tuple(infoDict)
    cur.execute("INSERT OR REPLACE INTO chat VALUES"+str(datatuple))
    cur.close()
    con.commit()
    con.close()

def updateContacts(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS Contacts('company_cin' TEXT, 'contact_person_name' TEXT, 'contact_person_designation' TEXT,\
                'contact_person_mobile' TEXT, 'contact_person_email_id' TEXT, unique (company_cin, 'contact_person_name','contact_person_designation'))" )
    
    #UPSERT
    for contact in infoDict:
        cur.execute("INSERT OR REPLACE INTO Contacts VALUES"+str(contact))
    cur.close()
    con.commit()
    con.close()


def updateHolding(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS HoldingCompanies('company_cin' TEXT, 'entity_name' TEXT, 'entity_type' TEXT,\
                'holding' TEXT, 'country_of_origin' TEXT, unique (company_cin, 'entity_name'))" )
    
    #UPSERT
    for entity in infoDict:
        cur.execute("INSERT OR REPLACE INTO HoldingCompanies VALUES"+str(entity))
    cur.close()
    con.commit()
    con.close()

def updateSubsidiary(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS SubsidiaryCompanies('company_cin' TEXT, 'entity_name' TEXT, 'entity_type' TEXT,\
                'investment' TEXT, 'country_of_origin' TEXT, unique (company_cin, 'entity_name'))" )
    
    #UPSERT
    for entity in infoDict:
        cur.execute("INSERT OR REPLACE INTO SubsidiaryCompanies VALUES"+str(entity))
    cur.close()
    con.commit()
    con.close()

def updateAssociate(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS AssociateCompanies('company_cin' TEXT, 'entity_name' TEXT, 'entity_type' TEXT,\
                'holding' TEXT, 'country_of_origin' TEXT, unique (company_cin, 'entity_name'))" )
    
    #UPSERT
    for entity in infoDict:
        cur.execute("INSERT OR REPLACE INTO AssociateCompanies VALUES"+str(entity))
    cur.close()
    con.commit()
    con.close()

def updateDocuments(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS documents('company_cin' TEXT, 'document_name' TEXT, 'document_location' TEXT,unique (company_cin, 'document_location'))" )
    
    #UPSERT
    for document in infoDict:
        cur.execute("INSERT OR REPLACE INTO documents VALUES"+str(document))
    cur.close()
    con.commit()
    con.close()

def updateShareholders(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS Shareholders('company_cin' TEXT, 'name' TEXT, 'fathers name' TEXT,\
                'address' TEXT,'nationality' TEXT, 'shares' TEXT,'type of share' TEXT, 'file' TEXT, unique (company_cin, 'name', 'type of share'))" )
    
    #UPSERT
    for holder in infoDict:
        cur.execute("INSERT OR REPLACE INTO Shareholders VALUES"+str(holder))
    cur.close()
    con.commit()
    con.close()
    
    

def updateSignatories(infoDict):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS Signatories('company_cin' TEXT,'director_din'  TEXT, 'director_name' TEXT, 'director_address' TEXT, 'Designation' TEXT,'director_date_of_appointment' TEXT,'director_dsc_registered' TEXT, 'director_dsc_expiry_date' DATE,'director_first_name' TEXT, 'director_middle_name' TEXT,'director_family_name' TEXT, director_gender TEXT, 'director_fathers_first_name' TEXT, 'director_fathers_middle_name' TEXT, 'director_fathers_last_name' TEXT, 'director_present_address' TEXT, 'director_permanent_address' TEXT, director_mobile_number TEXT, director_email_id TEXT, director_nationality TEXT, 'director_place_of_birth' TEXT, 'director_occupation' TEXT, 'director_date_of_birth' DATE, director_age TEXT, 'director_educational_qualification' TEXT, director_aadhar TEXT, director_pan TEXT, director_passport TEXT, 'director_otherID' TEXT,Alias TEXT,unique (company_cin, 'director_din'))")
    #UPSERT
    for Signatories in infoDict:
        cur.execute("INSERT OR REPLACE INTO Signatories VALUES"+str(Signatories))
    cur.close()
    con.commit()
    con.close()



def UpdateCell(Table, Column, ColValue, Row, RowValue):
    con = lite.connect('Database/C3_DataBase.db')
    Column = Column if Column.find(' ')==-1 else repr(Column)
    Row =  Row if Row.find(' ')==-1 else repr(Row)
    cur = con.cursor()
    cur.execute(f'UPDATE {Table} SET {Column} = {repr(ColValue)} WHERE {Row} = {repr(RowValue)}')
    cur.close()
    con.commit()
    con.close()


def AddUser(UserDict):
    userkeys = tuple(UserDict.keys())
    uservalues = tuple(UserDict.values())                
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS Users(ID INTEGER PRIMARY KEY NOT NULL,USERNAME TEXT,PASSWORD TEXT, ROLE TEXT,NAME TEXT,LASTLOGIN DATE,UNIQUE(USERNAME))")
        cur.execute(f"INSERT INTO Users "+str(userkeys)+" VALUES"+str(uservalues))
        cur.close()
        con.commit()
        con.close()
        return 'Success'
    except lite.IntegrityError:
        return 'Duplicate'


def UpdateUser(Column, ColValue, Row, RowValue):
    con = lite.connect('Database/C3_DataBase.db')
    Column = Column if Column.find(' ')==-1 else repr(Column)
    Row =  Row if Row.find(' ')==-1 else repr(Row)
    cur = con.cursor()
    cur.execute(f'UPDATE Users SET {Column} = {repr(ColValue)} WHERE {Row} = {repr(RowValue)}')
    cur.close()
    con.commit()
    con.close()

    

    
def addTemplate(table,description,template):
    data = (description,template)
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()
    cur.execute(f"CREATE TABLE IF NOT EXISTS {table} (Description TEXT,Template BLOB)")
    cur.execute(f"INSERT INTO {table} (Description,Template) VALUES"+str(data))
    cur.close()
    con.commit()
    con.close()
    
    
    
def AddResolution(ResolutionDict):
    ResoluKeys = tuple(ResolutionDict.keys())
    ResoluValues = tuple(ResolutionDict.values())                
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Resolutions(ID INTEGER PRIMARY KEY NOT NULL,DESCRIPTION TEXT,TITLE TEXT, SUMMARY TEXT, NARRATION TEXT,RESOLUTION TEXT,FIELDS BLOB,UNIQUE(DESCRIPTION))")
    try:
        cur.execute(f"INSERT INTO Resolutions "+str(ResoluKeys)+" VALUES"+str(ResoluValues))
        cur.close()
        con.commit()
        con.close()
        return 'Success'
    except lite.IntegrityError:
        return 'Duplicate'


def AddAgenda(AgendaDict):
    AgendaKeys = tuple(AgendaDict.keys())
    AgendaValues = tuple(AgendaDict.values())                
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Agenda(AGENDA TEXT,EXPLANATION TEXT, UNIQUE(AGENDA))")
    try:
        cur.execute(f"INSERT INTO Agenda "+str(AgendaKeys)+" VALUES"+str(AgendaValues))
        cur.close()
        con.commit()
        con.close()
        return 'Success'
    except lite.IntegrityError:
        return 'Duplicate'


def Bills(BillsList):
    con = lite.connect('Database/C3_DataBase.db')
    cur = con.cursor()    
    cur.execute("CREATE TABLE IF NOT EXISTS Bills('BILLNO' TEXT, 'DATE' DATE, 'CLIENT' TEXT,'AMOUNT' TEXT, 'TYPE' TEXT, 'FILEPATH' TEXT, UNIQUE(BILLNO))" )
    
    #UPSERT
    datatuple =tuple(BillsList)


    #UPSERT
    cur.execute("INSERT OR REPLACE INTO Bills VALUES"+str(datatuple))
    cur.close()
    con.commit()
    con.close()
    
    


	
