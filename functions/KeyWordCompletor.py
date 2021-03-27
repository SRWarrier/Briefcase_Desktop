from PySide2 import QtGui,QtCore, QtWidgets
from functions.AutoComplete import KeywordCompletor

class KeywordComplete(QtWidgets.QTextEdit):
    def __init__(self,*args):
        #*args to set parent
        QtWidgets.QTextEdit.__init__(self,*args)
        font=QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)
        self.completer = KeywordCompletor()


    def setCompleter(self, completer):
        if self.completer:
            self.disconnect(self.completer, 0, self, 0)
        if not completer:
            return

        completer.setWidget(self)
        completer.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.completer = completer
        self.completer.insertText.connect(self.insertCompletion)

    def insertCompletion(self, completion):
        tc = self.textCursor()
        extra = (len(completion) -
            len(self.completer.completionPrefix()))
        tc.movePosition(QtGui.QTextCursor.Left)
        tc.movePosition(QtGui.QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def textUnderCursor(self):
        tc = self.textCursor()
        tc.select(QtGui.QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def focusInEvent(self, event):
        if self.completer:
            self.completer.setWidget(self);
        QtWidgets.QTextEdit.focusInEvent(self, event)

    def keyPressEvent(self, event):
        if self.completer and self.completer.popup() and self.completer.popup().isVisible():
            if event.key() in (
            QtCore.Qt.Key_Enter,
            QtCore.Qt.Key_Return,
            QtCore.Qt.Key_Escape,
            QtCore.Qt.Key_Tab,
            QtCore.Qt.Key_Backtab):
                event.ignore()
                return 
        isShortcut = (event.modifiers() == QtCore.Qt.ControlModifier and\
                      event.key() == QtCore.Qt.Key_Space)

        if (not self.completer or not isShortcut):
            pass
            QtWidgets.QTextEdit.keyPressEvent(self, event)
            
        ctrlOrShift = event.modifiers() in (QtCore.Qt.ControlModifier ,\
                QtCore.Qt.ShiftModifier)
        if ctrlOrShift and event.text()== '':
            return
        eow = "~!@#$%^&*+{}|:\"<>?,./;'[]\\-=" #end of word


        completionPrefix = self.textUnderCursor()

        if not isShortcut :
            if self.completer.popup():
                self.completer.popup().hide()
            return

        self.completer.setCompletionPrefix(completionPrefix)
        popup = self.completer.popup()
        popup.setCurrentIndex(
            self.completer.completionModel().index(0,0))
        cr = self.cursorRect()
        cr.setWidth(self.completer.popup().sizeHintForColumn(0)
            + self.completer.popup().verticalScrollBar().sizeHint().width())
        self.completer.complete(cr) ## popup it up!

