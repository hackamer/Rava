# Form implementation generated from reading ui file 'add_user_page.ui'
#
# Created by: PyQt6 UI code generator 6.8.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


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


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SignUp = QtWidgets.QMainWindow()
    ui = Ui_SignUp()
    ui.setupUi(SignUp)
    SignUp.show()
    sys.exit(app.exec())
