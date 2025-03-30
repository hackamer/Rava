import sys
from PyQt5 import QtCore, QtWidgets, QtGui
import bcrypt
from supabase import create_client, Client
import json
import threading
# thread funtion


def run_in_thread(fun, arg1, arg2):
    lock = [True]
    retu = [None]

    def make_lock():
        x = fun(arg1, arg2)
        retu[0] = x
        lock[0] = False

    thr = threading.Thread(None, make_lock)
    thr.start()
    while lock[0]:
        app.processEvents()
    return (retu[0])
# end thread funtion

# MessageBox funtion


def msg(text: str, status: str):
    if status == "C":
        QtWidgets.QMessageBox.critical(None, "خطای نرم افزار راوا", text)
    elif status == "W":
        QtWidgets.QMessageBox.warning(None, "هشدار نرم افزار راوا", text)
    elif status == "I":
        QtWidgets.QMessageBox.information(
            None, "پیام نرم افزار راوا", text)


# Login funtions
with open('config.json') as config_file:
    config = json.load(config_file)
url = config['API_URL']
key = config['API_KEY']
hash_salt = config['SALT_HASH']
crypt_salt = config['SALT_CRYPT']
supabase: Client = create_client(str(url), str(key))
table = "rava_login"


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def crypting(text: str, salt: bytes) -> bytes:
    text += crypt_salt
    text_bytes = text.encode('utf-8')
    hashed_password = bcrypt.hashpw(text_bytes, salt)
    return hashed_password


def Login(username: str, password: str) -> bool:
    global login_status
    global login_msg
    try:
        salt_response = supabase.table(table).select(
            "salt").eq('username', username).execute()
    except:
        login_status = "C"
        login_msg = "مشکل در اتصال به اینترنت لطفا از اتصال به وب مطمئن شوید"
        return False
    try:
        salt = salt_response.data[0]['salt']
    except:
        login_status = "C"
        login_msg = "نام کاربری اشتباه است"
        return False
    username = username
    password = crypting(password, salt.encode()).decode()
    response = supabase.table(table).select(
        "*").eq('username', username).eq('password', password).execute()
    if response.data:
        login_status = "I"
        login_msg = "ورود با موفقیت آمیز انجام شد"
        return True

    else:
        login_status = "C"
        login_msg = "رمز عبور اشتباه است"
        return False


# dbmanager


def remover(username: str) -> bool:

    response = (
        supabase.table(table)
        .delete().eq("username", username)
        .execute()
    )
    if response.data:
        print("remove successful")
        return True
    else:
        print("problem in remove")
        return False


def insertor(username: str, password: str) -> bool:
    global signup_status
    global signup_msg
    salt = generate_salt().decode()
    password = crypting(password, salt.encode()).decode()
    if username == selector(username):
        signup_status = "C"
        signup_msg = "نام کاربری از قبل تعریف شده"
        return False
    if selector(username) == False:
        signup_status = "C"
        signup_msg = "مشکل در اتصال به اینترنت"
        return False
    try:
        response = (supabase.table(table).insert(
            {"username": username, "password": password, "salt": salt})).execute()
    except:
        signup_status = "C"
        signup_msg = "مشکل در اتصال به اینترنت"
        return False
    if response.data:
        signup_status = "I"
        signup_msg = "نام کاربری با موفقیت وارد شد"
        return True
    else:
        signup_status = "C"
        signup_msg = "مشکل غیر قابل پیش بینی"
        return False


def selector(username: str):
    try:
        response = supabase.table(table).select(
            "username").eq("username", username).execute()
    except:
        return False
    if response.data:
        return response.data[0]['username']
    else:
        return True


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(193, 206)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/ravalogo.png"))
        MainWindow.setWindowIcon(icon)
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/ravalogo.png"))
        Login.setWindowIcon(icon)
        with open('ui/styles/login_style.txt') as stylefile:
            style = stylefile.read()
        Login.setStyleSheet(style)
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
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
                                         "  font: 10pt ;\n"
                                         "  background-color: rgb(255, 227, 82);\n"
                                         "  border-color:;\n"
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
        self.txt_password.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password)
        self.gl_login.addWidget(self.txt_password, 3, 0, 1, 3)
        self.txt_username = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.txt_username.setObjectName("txt_username")
        self.gl_login.addWidget(self.txt_username, 2, 0, 1, 3)
        self.lbl_login = QtWidgets.QLabel(parent=self.centralwidget)
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
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/images/ravalogo.png"))
        SignUp.setWindowIcon(icon)
        with open('ui/styles/signup_style.txt') as stylefile:
            style = stylefile.read()
        SignUp.setStyleSheet(style)
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
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


class login(QtWidgets.QMainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.lnk_signup.clicked.connect(self.opensignup)
        self.btn_sendlogin.clicked.connect(self.login)

    def login(self) -> bool:
        username = self.txt_username.text()
        password = self.txt_password.text()
        if username == '' or password == '':
            msg("خطای خالی بودن نام کاربری ", "W")
            return False
        self.lnk_signup.setEnabled(False)
        self.btn_sendlogin.setEnabled(False)
        self.btn_sendlogin.setText("درحال ورود")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
        try:
            logincheck = run_in_thread(Login, username, password)
        except:
            msg("خطای غیر قابل پیش بینی نرم افزار", "C")
            self.lnk_signup.setEnabled(True)
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            return False
        if logincheck:
            self.lnk_signup.setEnabled(True)
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg(login_msg, login_status)
            self.main = Main()
            self.main.setupUi(self)
            self.main.show()
            self.close()
            return True
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg(login_msg, login_status)
            self.lnk_signup.setEnabled(True)
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")
            return False

    def opensignup(self):
        self.signup = SignUp()
        self.signup.show()
        self.close()


class SignUp(QtWidgets.QMainWindow, Ui_SignUp):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.btn_sendsignup.clicked.connect(self.signup)

    def signup(self):
        username = self.txt_username.text()
        password = self.txt_password.text()
        self.btn_sendsignup.setEnabled(False)
        self.btn_sendsignup.setText("درحال ثبت نام")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
        passwordrep = self.txt_repeatpassword.text()
        if username == '' or password == '':
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg("خطای خالی بودن نام کاربری یا رمز عبور", "W")
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            return False
        elif password != passwordrep:
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg("رمز عبور تکراری مطابقت ندارد", "W")
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            return False

        elif run_in_thread(insertor, username, password):
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg(signup_msg, signup_status)
            self.returnlogin()
            return True
        else:
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg(signup_msg, signup_status)
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            return False

    def returnlogin(self):
        self.login = login()
        self.login.show()
        self.close()


class Main(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = login()
    window.show()
    sys.exit(app.exec())
