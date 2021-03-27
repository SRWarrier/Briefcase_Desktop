import os


def convertui(uifile,pyfilename):
    os.system(f'python -m PyQt5.uic.pyuic {os.path.join(os.getcwd(),uifile)} -o {os.path.join(os.getcwd(),pyfilename)}.py -x')
