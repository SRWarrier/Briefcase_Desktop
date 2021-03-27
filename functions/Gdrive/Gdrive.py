from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import mimetypes
import os
import json
import webbrowser



def Authenticate():
    gauth = GoogleAuth()
    if not os.path.isfile('client_secrets.json') or not os.path.isfile('settings.yaml'):
        webbrowser.open('https://console.developers.google.com')
        while True:
            if not os.path.isfile('client_secrets.json'):
                continue
            else:
                break
        with open('client_secrets.json','r') as f:
            JsonFile = f.read()
            JsonRead = json.loads(JsonFile)
            client_id= JsonRead['web']['client_id']
            client_secret= JsonRead['web']['client_secret']
            f.close()
        baseFile = '''
    client_config_backend: settings
    client_config:
      client_id: %s
      client_secret: %s

    save_credentials: True
    save_credentials_backend: file
    save_credentials_file: credentials.json

    get_refresh_token: True

    oauth_scope:
      - https://www.googleapis.com/auth/drive.file
      - https://www.googleapis.com/auth/drive.install
    '''
        with open('settings.yaml','w') as f:
            f.write(baseFile%(client_id,client_secret))
            f.close()           
    gauth.LocalWebserverAuth() 
    drive = GoogleDrive(gauth)
    return drive
    


def createFolder(drive,foldername,needID=False):
    fileID=''
    fileList = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
    for file in fileList:
      if(file['title'] == foldername):
          fileID = file['id']
          return fileID
    if not fileID:
        folder_metadata = {'title' : foldername, 'mimeType' : 'application/vnd.google-apps.folder'}
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        if needID:
            return folder['id']


def createFile(drive,file,folder=None):
    MimeTuple =  mimetypes.guess_type(file)
    MIME = MimeTuple[0] if MimeTuple[0]!=None else "application/octet-stream"
    folderID = createFolder(drive,folder,True)
    gfile = drive.CreateFile({"mimeType": MIME, "parents": [{"kind": "drive#fileLink", "id": folderID}]})
    gfile.SetContentFile(file)
    filename = os.path.split(file)[-1]
    gfile['title'] = filename
    gfile.Upload()


def updateFile(drive,file,folder=None):
    if folder!=None:
        folder = createFolder(drive,folder,True)
    else:
        folder = 'root'
        
    file_list = drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()
    filefound = False
    for gfile in file_list:
        if gfile['title'] == os.path.split(file)[-1]:
            filefound = True
            break
    if filefound:
        gfile.SetContentFile(file)
        gfile.Upload()
    else:
        return "File Not Found"

def openFile(drive,file,folder=None,toprint = False):
    fileID =''
    fileList = drive.ListFile({'q': "'{}' in parents and trashed=false".format(createFolder(drive,folder,True))}).GetList()
    filename = os.path.split(file)[-1]
    for gfile in fileList:
        if gfile['title']==filename:
            fileID = gfile['id']
    if not fileID:
        return 'No File Found'
    else:
        document = drive.CreateFile({'id': fileID})
        if not toprint:
            document.GetContentFile(file)
        else:
            return document.GetContentString()
