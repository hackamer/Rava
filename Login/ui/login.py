import sys
from PyQt6 import QtCore, QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow

# test


def asasi(text):
    if text == "H":
        return True


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(193, 206)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 90, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.toolButton = QtWidgets.QToolButton(parent=self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(110, 110, 25, 19))
        self.toolButton.setObjectName("toolButton")
        self.radioButton = QtWidgets.QRadioButton(parent=self.centralwidget)
        self.radioButton.setGeometry(QtCore.QRect(110, 80, 82, 17))
        self.radioButton.setObjectName("radioButton")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 193, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.toolButton.setText(_translate("MainWindow", "..."))
        self.radioButton.setText(_translate("MainWindow", "RadioButton"))
# test finish


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(400, 250)
        Login.setMinimumSize(QtCore.QSize(400, 259))
        Login.setMaximumSize(QtCore.QSize(438, 259))
        Login.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        with open('login_style.txt') as stylefile:
            style = stylefile.read()
        Login.setStyleSheet(style)
        self.iranyekan = QtGui.QFontDatabase.addApplicationFont(
            "fonts/IRANYekanX_Regular.ttf")
        self.centralwidget = QtWidgets.QWidget(parent=Login)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setContentsMargins(-1, -1, -1, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gl_login = QtWidgets.QGridLayout()
        self.gl_login.setObjectName("gl_login")
        self.lnk_signup = QtWidgets.QCommandLinkButton(
            parent=self.centralwidget)
        self.lnk_signup.setLayoutDirection(
            QtCore.Qt.LayoutDirection.RightToLeft)
        self.lnk_signup.setAutoDefault(False)
        self.lnk_signup.setDefault(False)
        self.lnk_signup.setDescription("")
        self.lnk_signup.setObjectName("lnk_signup")
        self.gl_login.addWidget(self.lnk_signup, 5, 1, 1, 1)
        self.btn_sendlogin = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_sendlogin.setStyleSheet("QPushButton {\n"
                                         "  background-color: rgb(255, 179, 0);\n"
                                         "  color: #fff;\n"
                                         "  font-weight: 600;\n"
                                         "  border-radius: 8px;\n"
                                         "  border: 1px solid rgb(255, 179, 0);\n"
                                         "  padding: 5px 15px;\n"
                                         "  margin-top: 0px;\n"
                                         "  margin-bottom: 0px;\n"
                                         "  outline: 0px;\n"
                                         "  font: 10pt ;\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:hover{\n"
                                         "  background-color: rgb(236, 118, 0);\n"
                                         "}\n"
                                         "\n"
                                         "QPushButton:pressed{\n"
                                         "  background-color: rgb(255, 227, 82);\n"
                                         "  border-color:;\n"
                                         "  font-weight: 600;\n"
                                         "  border-radius: 8px;\n"
                                         "  border: 3px solid rgb(255, 170, 0);\n"
                                         "  padding: 5px 15px;\n"
                                         "  margin-top: 0px;\n"
                                         "  outline: 0px;\n"
                                         "  color: rgb(255, 170, 0);\n"
                                         "}")
        self.btn_sendlogin.setObjectName("btn_sendlogin")
        self.gl_login.addWidget(self.btn_sendlogin, 4, 0, 1, 3)
        self.txt_password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txt_password.setObjectName("txt_password")
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.gl_login.addWidget(self.txt_password, 3, 0, 1, 3)
        self.txt_username = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txt_username.setObjectName("txt_username")
        self.gl_login.addWidget(self.txt_username, 2, 0, 1, 3)
        self.lbl_login = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("IRANYekanX")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_login.setFont(font)
        self.lbl_login.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.lbl_login.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_login.setObjectName("lbl_login")
        self.gl_login.addWidget(self.lbl_login, 1, 0, 1, 3)
        self.gridLayout_2.addLayout(self.gl_login, 0, 0, 1, 1)
        Login.setCentralWidget(self.centralwidget)

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)
        Login.setTabOrder(self.txt_username, self.txt_password)
        Login.setTabOrder(self.txt_password, self.btn_sendlogin)
        Login.setTabOrder(self.btn_sendlogin, self.lnk_signup)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "صفحه ورود"))
        self.lnk_signup.setText(_translate("Login", "ثبت کاربر جدید"))
        self.btn_sendlogin.setText(_translate("Login", "ورود"))
        self.txt_password.setPlaceholderText(_translate("Login", "رمز عبور"))
        self.txt_username.setPlaceholderText(_translate("Login", "نام کاربری"))
        self.lbl_login.setText(_translate("Login", "صفحه ورود"))


class Ui_SignUp(object):
    def setupUi(self, SignUp):
        SignUp.setObjectName("SignUp")
        SignUp.resize(400, 250)
        SignUp.setMinimumSize(QtCore.QSize(400, 250))
        SignUp.setMaximumSize(QtCore.QSize(400, 250))
        with open('signup_style.txt') as stylefile:
            style = stylefile.read()
        SignUp.setStyleSheet(style)
        self.iranyekan = QtGui.QFontDatabase.addApplicationFont(
            "fonts/IRANYekanX_Regular.ttf")
        self.centralwidget = QtWidgets.QWidget(parent=SignUp)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gl_signup = QtWidgets.QGridLayout()
        self.gl_signup.setObjectName("gl_signup")
        self.txt_username = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txt_username.setObjectName("txt_username")
        self.gl_signup.addWidget(self.txt_username, 2, 0, 1, 1)
        self.txt_password = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txt_password.setObjectName("txt_password")
        self.txt_password.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.gl_signup.addWidget(self.txt_password, 3, 0, 1, 1)
        self.btn_sendsignup = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btn_sendsignup.setObjectName("btn_sendsignup")
        self.gl_signup.addWidget(self.btn_sendsignup, 5, 0, 1, 1)
        self.lbl_signup = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("IRANYekanX")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.lbl_signup.setFont(font)
        self.lbl_signup.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.lbl_signup.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lbl_signup.setObjectName("lbl_signup")
        self.gl_signup.addWidget(self.lbl_signup, 1, 0, 1, 1)
        self.txt_repeatpassword = QtWidgets.QLineEdit(
            parent=self.centralwidget)
        self.txt_repeatpassword.setObjectName("txt_repeatpassword")
        self.txt_repeatpassword.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password)

        self.gl_signup.addWidget(self.txt_repeatpassword, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gl_signup, 0, 0, 1, 1)
        SignUp.setCentralWidget(self.centralwidget)
        self.retranslateUi(SignUp)
        QtCore.QMetaObject.connectSlotsByName(SignUp)
        SignUp.setTabOrder(self.txt_username, self.txt_password)
        SignUp.setTabOrder(self.txt_password, self.txt_repeatpassword)
        SignUp.setTabOrder(self.txt_repeatpassword, self.btn_sendsignup)

    def retranslateUi(self, SignUp):
        _translate = QtCore.QCoreApplication.translate
        SignUp.setWindowTitle(_translate("SignUp", "ثبت کاربر جدید"))
        self.txt_username.setPlaceholderText(
            _translate("SignUp", "نام کاربری"))
        self.txt_password.setPlaceholderText(_translate("SignUp", "رمز عبور"))
        self.btn_sendsignup.setText(_translate("SignUp", "ثبت"))
        self.lbl_signup.setText(_translate("SignUp", "ثبت کاربر جدید"))
        self.txt_repeatpassword.setPlaceholderText(
            _translate("SignUp", "تکرار رمز عبور"))


class Login(QMainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lnk_signup.clicked.connect(self.opensignup)
        self.btn_sendlogin.clicked.connect(self.login)

    def login(self):
        if asasi(self.txt_username.text()):
            self.main = Main()
            self.main.setupUi(self)
            self.main.show()
            self.close()
        else:
            self.btn_sendlogin.setEnabled(False)

    def opensignup(self):
        self.signup = SignUp()
        self.signup.show()
        self.close()


class SignUp(QMainWindow, Ui_SignUp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_sendsignup.clicked.connect(self.returnlogin)

    def returnlogin(self):
        self.login = Login()
        self.login.show()
        self.close()


class Main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec())
