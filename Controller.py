from PySide2 import QtWidgets
import os
import Login
import Setup
import sys
import logging

app = QtWidgets.QApplication(sys.argv)

if os.path.isfile('Config'):
    Widget = Login.Ui()
else:
    print("setup")
    Widget = Setup.Ui()
    Widget.show()
logging.raiseExceptions = False
sys.exit(app.exec_())
