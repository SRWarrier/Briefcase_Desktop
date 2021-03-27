from PySide2 import QtGui, QtCore,QtWidgets

class KeywordCompletor(QtWidgets.QCompleter):
    insertText = QtCore.Signal(str)
    def __init__(self, myKeywords=None,parent=None):
        myKeywords =['{director_first_name}', '{director_middle_name}',
                     '{director_gender}', '{director_fathers_first_name}',
                     '{director_fathers_middle_name}', '{director_fathers_last_name}',
                     '{director_family_name}', '{director_present_address}',
                     '{director_permanent_address}', '{director_mobile_number}',
                     '{director_email_id}', '{director_nationality}',
                     '{director_place_of_birth}', '{director_occupation}',
                     '{director_date_of_birth}', '{director_age}',
                     '{director_educational_qualification}', '{director_aadhar}',
                     '{director_pan}', '{director_passport}', '{director_voters_id}']
        QtWidgets.QCompleter.__init__(self, myKeywords, parent)
        self.connect(self,
            QtCore.SIGNAL("activated(const QString&)"), self.changeCompletion)

    def changeCompletion(self, completion):
        if completion.find("(") != -1:
            completion = completion[:completion.find("(")]
        print(completion)
        self.insertText.emit(completion)
