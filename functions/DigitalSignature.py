from PyQt5 import QtWidgets, uic
import sys
import HomePage
import os
import uuid
from OpenSSL import crypto, SSL



class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('../Resources/ui/DigitalSignature.ui', self)
        self.CertifierName = self.findChild(QtWidgets.QLineEdit, 'CertifierName')
        self.CertifierUnit = self.findChild(QtWidgets.QLineEdit, 'CertifierUnit')
        self.CommonName = self.findChild(QtWidgets.QLineEdit, 'UserName')
        self.ContryCode = self.findChild(QtWidgets.QComboBox, 'ContryCode')
        self.Email = self.findChild(QtWidgets.QLineEdit, 'Email')
        self.Password_2 = self.findChild(QtWidgets.QLineEdit, 'Password_2')
        self.City = self.findChild(QtWidgets.QLineEdit, 'City')
        self.State = self.findChild(QtWidgets.QComboBox, 'State')
        self.State.setCurrentIndex(10)
        self.validityPeriodGroup = self.findChild(QtWidgets.QGroupBox, 'validityPeriodGroup')
        self.FiveYears = self.findChild(QtWidgets.QRadioButton, 'FiveYears')
        self.OneYear = self.findChild(QtWidgets.QRadioButton, 'OneYear')
        self.OneYear.setChecked(True)
        self.TwoYears = self.findChild(QtWidgets.QRadioButton, 'TwoYears')


        self.GenerateDSC = self.findChild(QtWidgets.QPushButton, 'GenerateDSC')
        self.GenerateDSC.clicked.connect(self.generate_keys)
        
        self.backtohome = self.findChild(QtWidgets.QPushButton, 'Bactohome')
        self.backtohome.clicked.connect(self.GobackToHomePage)
        
        self.show()


    def GobackToHomePage(self):
        self.hide()
        self.ui = HomePage.Ui()


    def generate_keys(self):
        Encr_bits=2048
        Key = crypto.PKey()
        Key.generate_key(crypto.TYPE_RSA, Encr_bits)
        publicKey=crypto.dump_publickey(crypto.FILETYPE_PEM, Key)
        if self.Password_2.text()=='':
            password = b'12345678'
        else:
            password = bytes(self.Password_2.text().encode('utf-8'))
        privateKey=crypto.dump_privatekey(crypto.FILETYPE_PEM, Key,passphrase=password)

        #CERTIFICATE
        C=self.ContryCode.currentText()
        ST=self.State.currentText().upper()
        L='BENGALURU' if self.City.text()=='' else self.City.text().upper()
        O='Self Signed Certificates' if self.CertifierName.text()=='' else self.CertifierName.text()
        OU='Self Signed Certificates' if self.CertifierUnit.text()=='' else self.CertifierUnit.text()
        CN=self.CommonName.text().upper()
        if self.Email.text()!='':
            EM=self.Email.text()
        cert = crypto.X509()
        cert.get_subject().C = C
        cert.get_subject().ST = ST
        cert.get_subject().L = L
        cert.get_subject().O = O
        cert.get_subject().OU = OU
        cert.get_subject().CN = CN
        if self.Email.text()!='':
            cert.get_subject().emailAddress=EM
        cert.set_serial_number(int(str(uuid.uuid4().int>>64)[0:16]))
        cert.gmtime_adj_notBefore(0)
        if self.FiveYears.isChecked():
            year = 5
        elif self.OneYear.isChecked():
            year = 1
        elif self.TwoYears.isChecked():
            year = 2
        cert.gmtime_adj_notAfter(year*365*24*60*60) 
        cert.set_issuer(cert.get_subject())
        key_public=crypto.load_publickey(crypto.FILETYPE_PEM,publicKey)
        cert.set_pubkey(key_public)
        key_private=crypto.load_privatekey(crypto.FILETYPE_PEM,privateKey)
        cert.sign(key_private, 'sha256')

        #PFX
        pfx = crypto.PKCS12()
        pfx.set_privatekey(key_private)
        pfx.set_certificate(cert)
        pfxdata = pfx.export(password)
        fileName, filetype = QtWidgets.QFileDialog.getSaveFileName(self,"Save file", "","Pfx File (*.pfx)")   
        with open(os.path.splitext(fileName)[0]+'.pfx', 'wb') as pfxfile:
                pfxfile.write(pfxdata)


    


