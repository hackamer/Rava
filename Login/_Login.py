import sys
from PyQt5 import uic, QtGui, QtWidgets, QtCore
import threading
import bcrypt
import json
from supabase import create_client, Client


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


class Main(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)


class Signup_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/add_user_page.ui', self)
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/images/ravalogo.png"))
        self.setWindowIcon(icon)
        self.widgets()
        self.connectors()

    def widgets(self):
        self.txt_username = self.findChild(QtWidgets.QLineEdit, 'txt_username')
        self.txt_password = self.findChild(QtWidgets.QLineEdit, 'txt_password')
        self.btn_sendsignup = self.findChild(
            QtWidgets.QPushButton, 'btn_sendsignup')

    def connectors(self):
        self.btn_sendsignup.clicked.connect(self.sendsignup)

    def sendsignup(self):
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
        elif password != passwordrep:
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg("رمز عبور تکراری مطابقت ندارد", "W")
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")

        elif run_in_thread(insertor, username, password):
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg(signup_msg, signup_status)
            self.returnlogin()
        else:
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg(signup_msg, signup_status)
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")

    def returnlogin(self):
        self.login = Login_UI()
        self.login.show()
        self.close()


class Login_UI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/login_page.ui', self)
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        self.widgets()
        self.connectors()
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/images/ravalogo.png"))
        self.setWindowIcon(icon)

    def widgets(self):
        self.btn_sendlogin = self.findChild(
            QtWidgets.QPushButton, 'btn_sendlogin')
        self.lnk_signup = self.findChild(
            QtWidgets.QCommandLinkButton, 'lnk_signup')
        self.txt_username = self.findChild(QtWidgets.QLineEdit, 'txt_username')
        self.txt_password = self.findChild(QtWidgets.QLineEdit, 'txt_password')

    def connectors(self):
        self.btn_sendlogin.clicked.connect(self.sendlogin)
        self.lnk_signup.clicked.connect(self.opensignup)

    def on_submit(self):
        print("دکمه کلیک شد!")

    def opensignup(self):
        self.signup = Signup_UI()
        self.signup.show()
        self.close()

    def sendlogin(self):
        username = self.txt_username.text()
        password = self.txt_password.text()
        if username == '' or password == '':
            msg("خطای خالی بودن نام کاربری ", "W")
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
            exit()
        if logincheck:
            self.lnk_signup.setEnabled(True)
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg(login_msg, login_status)
            print('hi there')
            self.main = Main()
            self.main.show()
            self.close()
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            msg(login_msg, login_status)
            self.lnk_signup.setEnabled(True)
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Login_UI()
    window.show()
    sys.exit(app.exec_())
