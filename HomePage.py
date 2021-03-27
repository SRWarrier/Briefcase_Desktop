from PySide2 import QtWidgets, QtCore, QtGui
import os
import pickle
from functions import pyside_dynamic, SessionLogout
from ADMIN import AddResolution, AddUser, AddBasicInfo, EditResolution,ResolutionsManager, UserManager
from COMPANIES import AddCompany, CompaniesAct2013Qref, QuickResolution
from COMPANIES import FormFiller, Notice, Minutes
from COMPANIES import EditMasterdata, EditSignatory, editContact
from COMPANIES import deleteCompany, viewCompany, masterdata, DirectorProfile
from COMPANIES import masterdata_toolbar
from COMPANIES import MGT1, generateMBP1, ClientManager, Incorporation
from DASHBOARD import Chat, news
from ACCOUNTS import InvoiceManager
from TOOLS import ImageCompressor, ImageResize, ImagetoScan


class Ui(QtWidgets.QWidget):
    def __init__(self):
        super(Ui, self).__init__()
        pyside_dynamic.loadUi('Resources/ui/new/dashboard_3.ui', self)
        self.setWindowState(QtCore.Qt.WindowState.WindowMaximized)
        self.setWindowTitle('Corporate Compliance Companion')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/logo.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        with open('_temp/_currentuser', 'rb') as currentUser:
            self.Userdata = pickle.loads(currentUser.read())
            currentUser.close()
        self.lastMenu = None
        self.lastTool = None
        self.CurrentUserName = self.Userdata['CurrentUser']
        self.CurrentUserRole = self.Userdata['Role']

        # MenuButton
        self.menuButton.clicked.connect(self.showMenu)
        self.menuButton.setIconSize(self.menuButton.size())
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/menu-inactive.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.menuButton.setIcon(icon)
        self.MasterData.clicked.connect(self.Toolbar)
        self.MenuBar.setHidden(False)
        self.RightBar.setHidden(not self.RightBar.isHidden())
        self.toasts.setHidden(not self.toasts.isHidden())
        self.Displaylayout = QtWidgets.QGridLayout()
        self.MainWindow.setLayout(self.Displaylayout)
        self.Widgetlayout = QtWidgets.QGridLayout()
        self.Widgetlayout.setContentsMargins(0, 0, 0, 0)
        self.WidgetWindow.setLayout(self.Widgetlayout)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/settings.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings.setIcon(icon)
        self.avatar.setPixmap(QtGui.QPixmap(
                QtGui.QImage("Resources/Icon/avatar.png")))
        self.Name.setText(str(self.Userdata['CurrentUser']))
        #self.lastlogin.setText(str(self.Userdata['LastLogin']))
        self.role.setText(str(self.Userdata['Role']))
        self.logoutBtn.clicked.connect(self.confirmlogout)
        self.MCALogout.clicked.connect(self.logoutMCA)
##        self.DASHBOARD = self.findChild(QtWidgets.QPushButton, 'DASHBOARD')
        self.DASHBOARD = self.findChild(QtWidgets.QToolButton, 'DASHBOARD')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/dashboard.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftBar.setItemIcon(0, icon)
##        self.DASHBOARD.setIcon(icon)
        self.COMPANIES = self.findChild(QtWidgets.QToolButton, 'SECRETARIAL')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/company.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftBar.setItemIcon(1, icon)
        self.ACCOUNTS = self.findChild(QtWidgets.QToolButton, 'ACCOUNTS')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/accounting.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftBar.setItemIcon(2, icon)
        # self.ACCOUNTS.clicked.connect(self.AddHomePageButtons)
        self.LEGAL = self.findChild(QtWidgets.QToolButton, 'LEGAL')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/law.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftBar.setItemIcon(3, icon)
        # self.ADMIN.clicked.connect(self.AddHomePageButtons)
        self.TOOLS = self.findChild(QtWidgets.QToolButton, 'TOOLS')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/tools.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftBar.setItemIcon(4, icon)
        self.leftBar.currentChanged.connect(self.AddHomePageButtons)
        # self.TOOLS.clicked.connect(self.AddHomePageButtons)
        self.ADMIN = self.findChild(QtWidgets.QToolButton, 'ADMIN')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/admin.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.leftBar.setItemIcon(5, icon)
        self.ExtendedMenu = QtWidgets.QWidget()
        self.extendedMenuLayout = QtWidgets.QVBoxLayout(self.ExtendedMenu)
        self.extendedMenuLayout.setObjectName("extendedMenuLayout")

        # Toolbar Buttons
        # CloseRightBar
        self.closeRightBar.clicked.connect(self.hideRightBar)

        # =>QuickRef
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/Qref.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Quickref.setIcon(icon)
        self.Quickref.clicked.connect(self.Toolbar)

        # =>Masterdata
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/masterdata.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.MasterData.setIcon(icon)
        self.MasterData.clicked.connect(self.Toolbar)

        # =>Chat
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/chat.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Chat.setIcon(icon)
        self.Chat.clicked.connect(self.Toolbar)

        # =>News
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/news.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.News.setIcon(icon)
        self.News.clicked.connect(self.Toolbar)

        # =>Logout
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
            "Resources/Icon/logout.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Logout.setIcon(icon)
        self.Logout.clicked.connect(self.Toolbar)
        # <Hide Tabs>
        if self.CurrentUserRole == 'Secretary':
            self.leftBar.widget(5).setParent(None)
            self.leftBar.widget(2).setParent(None)
        elif self.CurrentUserRole == 'Accounts':
            self.leftBar.widget(5).setParent(None)
            self.leftBar.widget(1).setParent(None)
            self.MCALogout.setParent(None)
        # </Hide Tabs>
        print(self.leftBar.count())
        self.AddHomePageButtons(self.leftBar.currentIndex())
        self.show()

    def showMenu(self):
        self.MasterData.clicked.connect(self.Toolbar)
        self.MenuBar.setHidden(not self.MenuBar.isHidden())

    def handleButtonClicked(self):
        sender = (self.sender())
        self.lastMenu = False
        self.MenuBar.setHidden(True)
        page = sender.objectName()
        self.WidgetTitleText.setText(page.upper())
        if 'delete' in page.lower():
            self.WidgetTitleText.setStyleSheet(
                "background-color: rgb(244,10,10); color: rgb(255,255,255)")
        elif 'add' in page.lower():
            self.WidgetTitleText.setStyleSheet(
                "background-color: rgb(0,230,45); color: rgb(255,255,255)")
        elif 'edit' in page.lower():
            self.WidgetTitleText.setStyleSheet(
                "background-color: rgb(0,45,230); color: rgb(255,255,255)")
        else:
            self.WidgetTitleText.setStyleSheet(
                "background-color: rgb(117,134,166); color: rgb(255,255,255)")
        if page not in ('Edit Company', 'Add User'):
            clearLayout(self.Displaylayout)
        if page == 'Client Manager':
            self.CurrentWidget = ClientManager.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Companies Act':
            self.CurrentWidget = CompaniesAct2013Qref.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Add Resolution':
            self.CurrentWidget = AddResolution.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Edit Resolution':
            self.CurrentWidget = EditResolution.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Compress Image':
            self.CurrentWidget = ImageCompressor.Ui_Form()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Resize Image':
            self.CurrentWidget = ImageResize.Ui_Form()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Image to Scan':
            self.CurrentWidget = ImagetoScan.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Quick Resolution':
            self.CurrentWidget = QuickResolution.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Add Company':
            self.CurrentWidget = AddCompany.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Form Filler':
            self.CurrentWidget = FormFiller.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Edit Company':
            self.EditCompanyWidget = QtWidgets.QWidget()
            self.EditCompanyWidget.setWindowTitle('Select Edit')
            pyside_dynamic.loadUi(
                'Resources/ui/EditCompanies.ui', self.EditCompanyWidget)
            editMasterdata = self.EditCompanyWidget.findChild(
                QtWidgets.QPushButton, 'editMasterdata')
            editMasterdata.clicked.connect(self.handleButtonClicked)
            Icon1 = self.EditCompanyWidget.findChild(QtWidgets.QLabel, 'Icon1')
            Icon1.setPixmap(QtGui.QPixmap(
                QtGui.QImage("Resources/Icon/company.png")))
            EditContacts = self.EditCompanyWidget.findChild(
                QtWidgets.QPushButton, 'EditContacts')
            EditContacts.clicked.connect(self.handleButtonClicked)
            Icon2 = self.EditCompanyWidget.findChild(QtWidgets.QLabel, 'Icon2')
            Icon2.setPixmap(QtGui.QPixmap(
                QtGui.QImage("Resources/Icon/company.png")))
            EditSignatories = self.EditCompanyWidget.findChild(
                QtWidgets.QPushButton, 'EditSignatories')
            EditSignatories.clicked.connect(self.handleButtonClicked)
            Icon3 = self.EditCompanyWidget.findChild(QtWidgets.QLabel, 'Icon3')
            Icon3.setPixmap(QtGui.QPixmap(
                QtGui.QImage("Resources/Icon/company.png")))
            self.EditCompanyWidget.show()
        elif page == 'editMasterdata':
            self.EditCompanyWidget.close()
            self.CurrentWidget = EditMasterdata.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'EditSignatories':
            self.EditCompanyWidget.close()
            self.CurrentWidget = EditSignatory.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'EditContacts':
            self.EditCompanyWidget.close()
            self.CurrentWidget = editContact.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Delete Company':
            self.CurrentWidget = deleteCompany.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'View Company':
            self.CurrentWidget = viewCompany.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Master Data':
            self.CurrentWidget = masterdata.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Register Manager':
            clearLayout(self.Displaylayout)
            CorporateActions = {'MGT-1': 'register.png', 'DIR_12': 'register.png', 'Rights Issue': 'register.png', 'Increase in Authorized Capital': 'register.png',
                                'Bonus Issue': 'register.png', 'MBP_1': 'register.png'}
            tlayout = 2
            positions = [(i, j) for i in range(int(len(CorporateActions)+1))
                         for j in range(tlayout)]
            for x in CorporateActions.keys():
                for position, name in zip(positions, CorporateActions.keys()):
                    self.ButtonPanel = QtWidgets.QWidget(self.MainWindow)
                    self.ButtonPanel.setGeometry(QtCore.QRect(50, 90, 321, 81))
                    self.ButtonPanel.setStyleSheet("border-radius:10;\n"
                                                   "background-color: rgb(3,169,244);")
                    self.ButtonPanel.setObjectName("ButtonPanel")
                    self.BTgridLayout = QtWidgets.QGridLayout(self.ButtonPanel)
                    self.BTgridLayout.setContentsMargins(0, 0, 0, 0)
                    self.BTgridLayout.setObjectName("BTgridLayout")
                    Icon = QtWidgets.QLabel(self.ButtonPanel)
                    sizePolicy = QtWidgets.QSizePolicy(
                        QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(
                        Icon.sizePolicy().hasHeightForWidth())
                    Icon.setSizePolicy(sizePolicy)
                    Icon.setMaximumSize(QtCore.QSize(100, 16777215))
                    if 'add' in name.lower():
                        Icon.setStyleSheet(
                            "background-color: rgb(129,199,132);")
                    elif 'delete' in name.lower():
                        Icon.setStyleSheet("background-color: rgb(244,81,30);")
                    elif 'edit' in name.lower():
                        Icon.setStyleSheet(
                            "background-color: rgb(186,104,200);")
                    else:
                        Icon.setStyleSheet(
                            "background-color: rgb(255, 255, 0);")
                    Icon.setText("")
                    Icon.setPixmap(QtGui.QPixmap(QtGui.QImage(
                        "Resources/Icon/"+CorporateActions[name])))
                    Icon.setAlignment(QtCore.Qt.AlignCenter)
                    Icon.setObjectName("Icon")
                    self.BTgridLayout.addWidget(Icon, 0, 0, 1, 1)
                    self.Button = QtWidgets.QPushButton(self.ButtonPanel)
                    sizePolicy = QtWidgets.QSizePolicy(
                        QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(
                        self.Button.sizePolicy().hasHeightForWidth())
                    self.Button.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setFamily("Open Sans")
                    font.setPointSize(11)
                    font.setBold(True)
                    font.setWeight(75)
                    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
                    self.Button.setFont(font)
                    self.Button.setStyleSheet("color: rgb(255, 255, 255);")
                    self.Button.setFlat(True)
                    self.Button.setObjectName(name)
                    self.Button.setText(name)
                    self.BTgridLayout.addWidget(self.Button, 0, 1, 1, 1)
                    self.Displaylayout.addWidget(
                        self.ButtonPanel, *position)
                    self.Button.clicked.connect(self.handleButtonClicked)
        elif page == 'MGT-1':
            self.CurrentWidget = MGT1.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Profile Director':
            self.CurrentWidget = DirectorProfile.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Notice/Agenda':
            self.CurrentWidget = Notice.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Minutes Manager':
            self.CurrentWidget = Minutes.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Corporate Actions':
            clearLayout(self.Displaylayout)
            CorporateActions = {'MBP_1': 'register.png', 'DIR_12': 'register.png', 'Rights Issue': 'register.png', 'Increase in Authorized Capital': 'register.png',
                                'Bonus Issue': 'register.png', 'MBP_1': 'register.png', 'Incorporation': 'register.png'}
            tlayout = 2
            positions = [(i, j) for i in range(int(len(CorporateActions)+1))
                         for j in range(tlayout)]
            for x in CorporateActions.keys():
                for position, name in zip(positions, CorporateActions.keys()):
                    self.ButtonPanel = QtWidgets.QWidget(self.MainWindow)
                    self.ButtonPanel.setGeometry(QtCore.QRect(50, 90, 321, 81))
                    self.ButtonPanel.setStyleSheet("border-radius:10;\n"
                                                   "background-color: rgb(3,169,244);")
                    self.ButtonPanel.setObjectName("ButtonPanel")
                    self.BTgridLayout = QtWidgets.QGridLayout(self.ButtonPanel)
                    self.BTgridLayout.setContentsMargins(0, 0, 0, 0)
                    self.BTgridLayout.setObjectName("BTgridLayout")
                    Icon = QtWidgets.QLabel(self.ButtonPanel)
                    sizePolicy = QtWidgets.QSizePolicy(
                        QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(
                        Icon.sizePolicy().hasHeightForWidth())
                    Icon.setSizePolicy(sizePolicy)
                    Icon.setMaximumSize(QtCore.QSize(100, 16777215))
                    if 'add' in name.lower():
                        Icon.setStyleSheet(
                            "background-color: rgb(129,199,132);")
                    elif 'delete' in name.lower():
                        Icon.setStyleSheet("background-color: rgb(244,81,30);")
                    elif 'edit' in name.lower():
                        Icon.setStyleSheet(
                            "background-color: rgb(186,104,200);")
                    else:
                        Icon.setStyleSheet(
                            "background-color: rgb(255, 255, 0);")
                    Icon.setText("")
                    Icon.setPixmap(QtGui.QPixmap(QtGui.QImage(
                        "Resources/Icon/"+CorporateActions[name])))
                    Icon.setAlignment(QtCore.Qt.AlignCenter)
                    Icon.setObjectName("Icon")
                    self.BTgridLayout.addWidget(Icon, 0, 0, 1, 1)
                    self.Button = QtWidgets.QPushButton(self.ButtonPanel)
                    sizePolicy = QtWidgets.QSizePolicy(
                        QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
                    sizePolicy.setHorizontalStretch(0)
                    sizePolicy.setVerticalStretch(0)
                    sizePolicy.setHeightForWidth(
                        self.Button.sizePolicy().hasHeightForWidth())
                    self.Button.setSizePolicy(sizePolicy)
                    font = QtGui.QFont()
                    font.setFamily("Open Sans")
                    font.setPointSize(11)
                    font.setBold(True)
                    font.setWeight(75)
                    font.setStyleStrategy(QtGui.QFont.PreferAntialias)
                    self.Button.setFont(font)
                    self.Button.setStyleSheet("color: rgb(255, 255, 255);")
                    self.Button.setFlat(True)
                    self.Button.setObjectName(name)
                    self.Button.setText(name)
                    self.BTgridLayout.addWidget(self.Button, 0, 1, 1, 1)
                    self.Displaylayout.addWidget(self.ButtonPanel, *position)
                    self.Button.clicked.connect(self.handleButtonClicked)
        elif page == 'MBP_1':
            self.CurrentWidget = generateMBP1.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Incorporation':
            self.CurrentWidget = Incorporation.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Add User':
            self.CurrentWidget = AddUser.Ui()
            self.CurrentWidget.isProgrammer(False)
            self.CurrentWidget.show()
        elif page == 'User Manager':
            self.CurrentWidget = UserManager.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        # elif page == 'Add Invoice':
        #     self.CurrentWidget = AddInvoice.Ui()
        #     self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Invoice Manager':
            self.CurrentWidget = InvoiceManager.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Add Basic data':
            self.CurrentWidget = AddBasicInfo.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        elif page == 'Resolutions Manager':
            self.CurrentWidget = ResolutionsManager.Ui()
            self.Displaylayout.addWidget(self.CurrentWidget, *(0, 0))
        else:
            print(page)
        self.MainWindow.setLayout(self.Displaylayout)

    def AddHomePageButtons(self, index):
        ActiveWidget = self.leftBar.widget(index)
        Activelayout = ActiveWidget.layout()
        clearLayout(self.extendedMenuLayout)
        page = self.leftBar.itemText(index).upper()
        # self.MenuTitle.setText(page)


        DASHBOARD = {'Secretarial': 'company.png', 'Accounts': 'bill.png', 'Legal': 'law.svg'}

        
        SECRETARIAL = {'Client Manager': 'company.png', 'Master Data': 'masterdata.png', 'Profile Director': 'ProfileDirector.png',
                     'Register Manager': 'register.png', #'Notice/Agenda': 'notice.png', 'Minutes Manager': 'minutes.png',
                     'Quick Resolution': 'quickres.png', 'Corporate Actions': 'suitcase.png', 'CheckList': 'checklist.png',
                     'Companies Act': 'lawbook2.png', 'XBRL': 'xbrl.png', 'Form Filler': 'form.png'}  # 'Add Company':'company.png', 'Edit Company':'company.png', 'Delete Company':'company.png','View Company':'company.png'
        LLP = {'Add LLP': 'LLP.png', 'Edit LLP': 'LLP.png', 'Delete LLP': 'LLP.png',
               'View LLP': 'LLP.png', 'Master Data': 'masterdata.png', 'Profile Director': 'ProfileDirector.png',
##               'Register Manager': 'register.png', 'Notice/Agenda': 'notice.png', 'Minutes Manager': 'minutes.png',
               'Quick Resolution': 'quickres.png', 'Corporate Actions': 'suitcase.png', 'CheckList': 'checklist.png',
               'LLP Act': 'lawbook2.png', 'XBRL': 'xbrl.png', 'Form Filler': 'form.png'}

        # ACCOUNTS = {'Add Invoice': 'bill.png', 'Edit Invoice': 'bill.png', 'Delete Invoice': 'bill.png',
        #             'View Invoice': 'bill.png', 'Generate Report': 'report.png'}

        ACCOUNTS = {'Invoice Manager': 'bill.png', 'Generate Report': 'report.png'}

        ADMIN = {'Add User': 'adduser.png', 'Reset User Password': 'edituser.png', 'Delete User': 'deleteuser.png',
                 'Resolutions Manager':'resolution.png','User Manager':'adduser.png',
                 'Add Minutes Layout': 'editresolution.png', 'Edit Minutes Layout': 'editresolution.png', 'Delete Minutes Layout': 'editresolution.png',
                 'Add Basic data': 'agenda.png', 'View Basic Data': 'agenda.png', 'Delete Basic Data': 'agenda.png', 'View Activities': 'activities.png', 'Generate Reports': 'report.png'}

        TOOLS = {'Compress Image': 'compress.png', 'Resize Image': 'resize.png', 'Image to Scan': 'scanner.png', 'Image to PDF': 'imagetopdf.png',
                 'Compress PDF': 'compress.png', 'Split PDF': 'splitFile.png', 'Merge PDF': 'merge.png', 'PDF to Image': 'converttoImage.png', 'Extract Text': 'toText.png', 'Encrpyt': 'encrypt.png', 'Decrypt': 'decrypt.png', 'Digital Signature': 'Digital Signature'}

        for x in (eval(page).keys()):
            menuItem = QtWidgets.QPushButton(self)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(QtGui.QImage(
                "Resources/Icon/"+eval(page)[x])), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            sizePolicy = QtWidgets.QSizePolicy(
                        QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            menuItem.setSizePolicy(sizePolicy)
            menuItem.setStyleSheet(
                "QPushButton{border: 0px;background:rgb(253, 255, 252); color: rgb(15,15,15);text-align: left;} QPushButton:hover{background:rgb(240, 240, 240)}")
            menuItem.setIcon(icon)
            font = QtGui.QFont()
            font.setFamily("Open Sans")
            font.setPointSize(10)
            font.setStyleStrategy(QtGui.QFont.PreferAntialias)
            menuItem.setFont(font)
            menuItem.setIconSize(QtCore.QSize(24, 24))
            menuItem.setObjectName("menuItem")
            menuItem.setText('\t'+x)
            menuItem.setObjectName(x)
            menuItem.clicked.connect(self.handleButtonClicked)
            self.extendedMenuLayout.addWidget(menuItem)
            Activelayout.addWidget(self.ExtendedMenu, *(0, 0))

    def confirmlogout(self):
        buttonReply = QtWidgets.QMessageBox.question(self, 'Logout?', "Do you want to Logout?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if buttonReply == QtWidgets.QMessageBox.Yes:
            self.logout()
        else:
            pass
        
    def logout(self):
        os.remove('_temp/_currentuser')
        self.close()

    def Toolbar(self):
        clearLayout(self.Widgetlayout)
        sender = (self.sender())
        tool = sender.objectName()
        self.WidgetTitle.setText(tool.upper())
        print(tool)
        if tool == 'Quickref':
            if self.RightBar.isHidden():
                self.RightBar.setHidden(False)
            self.CurrentTool = CompaniesAct2013Qref.Ui(isSidebar=True)
            self.Widgetlayout.addWidget(self.CurrentTool, *(0, 0))
            self.lastTool = 'Quickref'
        elif tool == 'MasterData':
            if self.RightBar.isHidden():
                self.RightBar.setHidden(False)
            self.CurrentTool = masterdata_toolbar.Ui()
            self.Widgetlayout.addWidget(self.CurrentTool, *(0, 0))
        elif tool == 'Chat':
            if self.RightBar.isHidden():
                self.RightBar.setHidden(False)

            self.CurrentTool = Chat.Ui()
            self.Widgetlayout.addWidget(self.CurrentTool, *(0, 0))
        elif tool == 'News':
            if self.RightBar.isHidden():
                self.RightBar.setHidden(False)
            self.CurrentTool = news.Ui()
            self.Widgetlayout.addWidget(self.CurrentTool, *(0, 0))
        elif tool == 'Logout':
            if self.RightBar.isHidden():
                self.RightBar.setHidden(False)
            self.CurrentTool = QtWidgets.QWidget()
            pyside_dynamic.loadUi(
                'Resources/ui/UserSidebar.ui', self.CurrentTool)
            
            self.Widgetlayout.addWidget(self.CurrentTool, *(0, 0))

    def hideRightBar(self):
        self.RightBar.setHidden(not self.RightBar.isHidden())

    def logoutMCA(self):
        LogoutStat = SessionLogout.sessionLogout()
        Message = QtWidgets.QMessageBox(self)
        Message.setWindowTitle("Information")
        if LogoutStat:
            Message.setText('All active Login Session has been terminated')
        else:
            Message.setText('No Active Sessions Found')
        Message.setModal(False)
        self.AddSignatoriesButtion = QtWidgets.QPushButton()
        self.AddSignatoriesButtion.setText('Done')
        Message.addButton(self.AddSignatoriesButtion,
                          QtWidgets.QMessageBox.YesRole)
        Message.show()


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        if child.widget() is not None:
            child.widget().deleteLater()
        elif child.layout() is not None:
            clearLayout(child.layout())
