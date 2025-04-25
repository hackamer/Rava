import sys
from PyQt5 import uic, QtGui, QtWidgets, QtCore
import bcrypt
import sqlite3
import os


def msg(text: str, status: str):
    if status == "C":
        QtWidgets.QMessageBox.critical(None, "خطای نرم افزار راوا", text)
    elif status == "W":
        QtWidgets.QMessageBox.warning(None, "هشدار نرم افزار راوا", text)
    elif status == "I":
        QtWidgets.QMessageBox.information(
            None, "پیام نرم افزار راوا", text)


# Login funtions
folderpath = os.path.join(os.path.join(
    os.environ['USERPROFILE']), 'Documents', 'Rava')

try:
    os.mkdir(folderpath)
except FileExistsError:
    print()
except PermissionError:
    folderpath = os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Rava')


filepath = os.path.join(folderpath, "Rava.db")
connection = sqlite3.connect(filepath)
cursor = connection.cursor()


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def Hashing(text: str) -> str:
    return text


def crypting(text: str, salt: bytes) -> bytes:
    text += "b:2S]3zeFU_E>WNq!rPs^[5Rn)CZw(LtYK`hV;8/"
    text_bytes = text.encode('utf-8')
    hashed_password = bcrypt.hashpw(text_bytes, salt)
    return hashed_password


def Login(username: str, password: str) -> bool:
    global login_msg, login_status
    qsalt = "SELECT salt FROM login_data WHERE username = ?"
    cursor.execute(qsalt, (username,))
    connection.commit()
    salt = cursor.fetchall()
    if salt:
        salt = salt[0][0]
        q = "SELECT * FROM login_data WHERE username = ? AND password = ?"
        cursor.execute(q, (username, crypting(
            password, salt.encode('utf-8'))))
        connection.commit()
        result = cursor.fetchall()
        if result:
            login_status = "I"
            login_msg = "ورود با موفقیت آمیز انجام شد"
            print("login OK")
            return True
        else:
            login_status = "C"
            login_msg = "نام کاربری یا رمز عبور اشتباه است"
            return False
    else:
        login_status = "C"
        login_msg = "نام کاربری یا رمز عبور اشتباه است"
        return False


def reset(file):
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist")


def creator(table: str = "login_data"):
    q = "CREATE TABLE IF NOT EXISTS {} (username TEXT, password TEXT,salt TEXT)".format(
        table)
    cursor.execute(q)
    connection.commit()


def insertor(username: str, password: str, table: str = "login_data") -> bool:
    global signup_status, signup_msg
    creator()
    if username == selector(username, table):
        signup_status = "C"
        signup_msg = "نام کاربری از قبل تعریف شده"
        return False
    salt = generate_salt()
    q = "INSERT INTO {} (username, password,salt) VALUES (?, ?, ?)".format(
        table)
    cursor.execute(q, (username, crypting(
        password, salt), salt.decode()))
    connection.commit()
    signup_status = "I"
    signup_msg = "نام کاربری با موفقیت وارد شد"
    return True


def remover(username: str, table="rava_login") -> str:
    creator()
    q = "DELETE FROM {} WHERE username = ?".format(table)
    cursor.execute(q, (username,))
    result = cursor.fetchall()
    connection.commit()
    if result:
        return "OK"
    else:
        return "NO"


def selector(username: str, table="rava_login"):
    q = "SELECT username FROM {} WHERE username = ?".format(table)
    cursor.execute(q, (username,))
    result = cursor.fetchall()
    connection.commit()
    if result:
        return result[0][0]
    else:
        return False


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

        elif insertor(username, password):
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
            logincheck = Login(username, password)
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
            # self.close()
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
