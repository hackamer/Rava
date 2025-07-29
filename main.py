import os
import sys
import shutil
import sqlite3
import uuid
import hashlib
import base64
from datetime import datetime
import jdatetime
from PyQt5 import uic, QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import (QFrame, QLabel, QHBoxLayout, QApplication)
from PyQt5.QtCore import (Qt, QPropertyAnimation, QTimer, 
                         QPoint, QEasingCurve, pyqtProperty)
from unidecode import unidecode
from cryptography.hazmat.primitives import hmac, hashes
from cryptography.fernet import Fernet
import ast
import bcrypt


# -----------------------------
# Global Variables and Paths
# -----------------------------
drugs = []  # List to store medicine information for the current session
medicine = []
response = []
search_data = {}  # Global variable to store search data
u = "NONE"
# Determine the folder path for storing config and data
folderpath = os.path.join(os.path.join(
    os.environ['USERPROFILE']), 'AppData', 'Local', 'Rava')
try:
    os.mkdir(folderpath)
except FileExistsError:
    # Folder already exists, nothing to do
    pass
except PermissionError:
    # Fallback in case of permission error
    folderpath = os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Rava')

# File paths for config and hidden backup
filepath = os.path.join(folderpath, "config.sys")
hidden_path = os.path.join(os.path.join(
    os.environ['USERPROFILE']), "AppData", "Local", "Microsoft", "Windows", "Explorer", "thumbs.db")

# SQLite connection setup
connection = sqlite3.connect(filepath)
cursor = connection.cursor()

# -----------------------------
# Utility Functions
# -----------------------------


def get_shamsi_date_str():
    """
    Returns the current date and time in Shamsi (Jalali) format as a string.
    """
    now = datetime.now()
    shamsi_now = jdatetime.datetime.fromgregorian(datetime=now)
    return f"{shamsi_now.year:04d}/{shamsi_now.month:02d}/{shamsi_now.day:02d}"


def get_shamsi_time_str():
    now = datetime.now()
    shamsi_now = jdatetime.datetime.fromgregorian(datetime=now)
    return f"{shamsi_now.hour:02d}:{shamsi_now.minute:02d}:{shamsi_now.second:02d}"


def copy():
    """
    Copies the config file to a hidden backup location.
    """
    shutil.copy2(filepath, hidden_path)


def msg(text: str, status: str):
    """
    Shows a message box with the given text and status.
    status: 'C' = Critical, 'W' = Warning, 'I' = Information
    """
    if status == "C":
        QtWidgets.QMessageBox.critical(None, "خطای نرم افزار راوا", text)
    elif status == "W":
        QtWidgets.QMessageBox.warning(None, "هشدار نرم افزار راوا", text)
    elif status == "I":
        QtWidgets.QMessageBox.information(None, "پیام نرم افزار راوا", text)


def get_machine_id():
    """
    Gets the MAC address of the machine as a unique identifier.
    """
    mac = uuid.getnode()
    mac_str = f"{mac:012x}"
    return mac_str


def get_stored_piece():
    """
    Reads the first 6 characters from the libs.dll file.
    """
    with open("libs.dll", "rb") as f:
        return f.read().decode()[:6]


def build_final_key():
    """
    Builds the final encryption key by combining machine ID and stored piece.
    """
    piece1 = get_machine_id()[:6]
    piece2 = get_stored_piece()
    combined = piece1 + piece2
    hash_val = hashlib.sha256(combined.encode()).digest()
    return base64.urlsafe_b64encode(hash_val)


def generate_key(key_file='libs.dll'):
    """
    Generate a key for encryption and save it to a file.
    """
    key = Fernet.generate_key()
    with open(key_file, 'wb') as file:
        file.write(key)
    return build_final_key()


def load_key(key_file='libs.dll'):
    """
    Load the encryption key from a file.
    """
    if not os.path.exists(key_file):
        raise FileNotFoundError(
            "Key file not found. Please ensure the key file exists.")
    with open(key_file, 'rb') as file:
        return build_final_key()


def encrypt_database(db_file, key_file='libs.dll'):
    """
    Encrypt the database file.
    Args:
        db_file (str): Path to the database file to encrypt.
        key_file (str): Path to the key file for encryption.
    Returns:
        str: Path to the encrypted file.
    """
    # Generate or load key
    if not os.path.exists(key_file):
        key = generate_key(key_file)
    else:
        key = load_key(key_file)

    fernet = Fernet(key)

    # Read the database file
    if not os.path.exists(db_file):
        raise FileNotFoundError(f"Database file {db_file} not found.")
    with open(db_file, 'rb') as file:
        data = file.read()

    # Encrypt the data
    encrypted_data = fernet.encrypt(data)

    # Save encrypted data to a new file
    encrypted_file = db_file
    with open(encrypted_file, 'wb') as file:
        file.write(encrypted_data)
    copy()
    return encrypted_file


def decrypt_database(encrypted_file, key_file='libs.dll'):
    """
    Decrypt the database file.
    Args:
        encrypted_file (str): Path to the encrypted database file.
        key_file (str): Path to the key file for decryption.
    Returns:
        str: Path to the decrypted file.
    """
    # Load key
    key = load_key(key_file)
    fernet = Fernet(key)

    # Read the encrypted file
    if not os.path.exists(encrypted_file):
        raise FileNotFoundError(f"Encrypted file {encrypted_file} not found.")
    with open(encrypted_file, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data)

    # Save decrypted data to a new file
    decrypted_file = encrypted_file.replace('', '')
    with open(decrypted_file, 'wb') as file:
        file.write(decrypted_data)
    copy()
    return decrypted_file


def verify_generator(data: str) -> str:
    """
    Generates a verification hash for the given data using hardware ID.
    """
    hardware_id = get_machine_id().encode()
    key = hashlib.sha256(hardware_id).digest()
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data.encode())
    tag = h.finalize()
    return base64.urlsafe_b64encode(tag).decode()


def main_creator(table: str = "main"):
    """
    Creates the main table in the database if it does not exist.
    """
    try:
        decrypt_database(filepath)
    except:
        pass
    q = (
        "CREATE TABLE IF NOT EXISTS {} ("
        "username TEXT,code TEXT,time TEXT,date TEXT, mood TEXT,Illusion TEXT,"
        "delusion TEXT,suicidalthoughts TEXT,psychomotor TEXT,Illusion01 BINARY,ratespeech TEXT,"
        "speedspeech TEXT,contentspeech TEXT,tonespeech TEXT,affection TEXT,eyecontact BINARY,"
        "medicine TEXT,pain BINARY,bp TEXT,p TEXT,r TEXT,spo2 TEXT,t TEXT,"
        "weight TEXT,height TEXT,bmi TEXT,eat TEXT,diet TEXT,moredetails TEXT,verify TEXT)"
    ).format(table)
    cursor.execute(q)
    connection.commit()
    encrypt_database(filepath)
    copy()




# Login funtions
folderpath = os.path.join(os.path.join(
    os.environ['USERPROFILE']), 'AppData', 'Local', 'Rava')
try:
    os.mkdir(folderpath)
except FileExistsError:
    print()
except PermissionError:
    folderpath = os.path.join(os.path.join(
        os.environ['USERPROFILE']), 'Rava')


filepath = os.path.join(folderpath, "config.sys")
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
    global login_msg
    qsalt = "SELECT salt FROM login_data WHERE username = ?"
    decrypt_database(filepath)
    cursor.execute(qsalt, (username,))
    connection.commit()
    salt = cursor.fetchall()
    encrypt_database(filepath)
    if salt:
        salt = salt[0][0]
        q = "SELECT * FROM login_data WHERE username = ? AND password = ?"
        decrypt_database(filepath)
        cursor.execute(q, (username, crypting(
            password, salt.encode('utf-8'))))
        connection.commit()
        result = cursor.fetchall()
        encrypt_database(filepath)
        if result:
            login_msg = "ورود با موفقیت آمیز انجام شد"
            print("login OK")
            return True
        else:
            login_msg = "نام کاربری یا رمز عبور اشتباه است"
            return False
    else:
        login_msg = "نام کاربری یا رمز عبور اشتباه است"
        return False

def creator(table: str = "login_data"):
    try:
        decrypt_database(filepath)
    except:
        pass
    q = "CREATE TABLE IF NOT EXISTS {} (username TEXT, password TEXT,salt TEXT)".format(
        table)
    cursor.execute(q)
    connection.commit()
    encrypt_database(filepath)


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
    decrypt_database(filepath)
    cursor.execute(q, (username, crypting(
        password, salt), salt.decode()))
    connection.commit()
    encrypt_database(filepath)
    signup_status = "I"
    signup_msg = "نام کاربری با موفقیت وارد شد"
    return True


def remover(username: str, table="rava_login") -> str:
    creator()
    decrypt_database(filepath)
    q = "DELETE FROM {} WHERE username = ?".format(table)
    cursor.execute(q, (username,))
    result = cursor.fetchall()
    connection.commit()
    encrypt_database(filepath)
    if result:
        return "OK"
    else:
        return "NO"


def selector(username: str, table="rava_login"):
    decrypt_database(filepath)
    q = "SELECT username FROM {} WHERE username = ?".format(table)
    cursor.execute(q, (username,))
    result = cursor.fetchall()
    connection.commit()
    encrypt_database(filepath)
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
        self.btn_delete = self.findChild(QtWidgets.QPushButton,'btn_delete')

    def connectors(self):
        self.btn_sendsignup.clicked.connect(self.sendsignup)
        self.btn_delete.clicked.connect(self.delete)
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
            show_notification(None,"خطای خالی بودن نام کاربری یا رمز عبور")
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
        elif password != passwordrep:
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            show_notification(None,"رمز عبور تکراری مطابقت ندارد")
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
        if u.startswith("admin"):
            if insertor(username, password):
                self.btn_sendsignup.setEnabled(True)
                self.btn_sendsignup.setText("ثبت نام")
                self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
                show_notification(None,signup_msg)
                self.returnlogin()
            else:
                self.btn_sendsignup.setEnabled(True)
                self.btn_sendsignup.setText("ثبت نام")
                self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
                show_notification(None,signup_msg)
                self.btn_sendsignup.setEnabled(True)
                self.btn_sendsignup.setText("ثبت نام")
        else:
            show_notification(None,"لطفا با یوزر ادمین وارد شوید")
    def delete(self):
        if self.txt_username.text() != "admin" and u == "admin":
            if remover(self.txt_username.text()) == "OK":
                show_notification(None,"با موفقیت حذف شد")
            else:show_notification(None,"خطا در حذف نام کاربری")

        elif self.txt_username.text().startswith("admin") and u.startswith("admin"):
            show_notification(None,"یک ادمین ادمین دیگری را نمیتواند حذف کند")
        elif self.txt_username.text().startswith("admin") and not u.startswith("admin"):
            if remover(self.txt_username.text()) == "OK":
                show_notification(None,"با موفقیت حذف شد")
            else:show_notification(None,"خطا در حذف نام کاربری")
        self.returnlogin()
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
        self.lnk_signup.setEnabled(False)

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
        global u
        creator()
        username = self.txt_username.text()
        password = self.txt_password.text()
        if username == '' or password == '':
            show_notification(None,"خطای خالی بودن ")

        self.btn_sendlogin.setEnabled(False)
        self.btn_sendlogin.setText("درحال ورود")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
        try:
            logincheck = Login(username, password)
        except:
            show_notification(None,"خطای غیر قابل پیش بینی نرم افزار")
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            exit()
        if logincheck:
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            u = self.txt_username.text()
            if username.startswith("admin"):
                self.lnk_signup.setEnabled(True)
                show_notification(None,"یوزر ادمین خوش آمدی!!")
            
            show_notification(None,login_msg)
            print('hi there')
            self.main = Main()
            self.main.show()
            self.main.showMinimized()
            # self.close()
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            show_notification(None,login_msg)
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")

creator()
insertor("admin","P@ssw0rd")
class Notification(QFrame):
    def __init__(self, parent=None, message="ثبت شد ✓"):
        super().__init__(parent)
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        self._is_hiding = False
        self.message = message
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumWidth(500)  
        self.setMaximumWidth(600)  
        self.setMinimumHeight(80)
        self.setStyleSheet('''
            font-family: IRANYekanXFaNum ExtraBold;
            font-size: 18px;
            background-color: rgba(76, 175, 80, 0.85);
            border-radius: 12px;
            padding: 20px;
            margin: 10px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
        ''')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.0)

        self.label = QLabel(self.message)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(False)  
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)  
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showEvent(self, event):
        self.adjustSize()
        self.start_show_animation()
        QTimer.singleShot(2000, self.start_hide_animation)

    def start_show_animation(self):
        parent_rect = self.parent().geometry() if self.parent() else self.screen().geometry()
        start_y = parent_rect.height() + 100
        end_y = parent_rect.height() // 2 - self.height() // 4
        x_pos = (parent_rect.width() - self.width()) // 2

        self.move(QPoint(x_pos, start_y))
        
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(1000)
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)
        self.pos_anim.setStartValue(QPoint(x_pos, start_y))
        self.pos_anim.setEndValue(QPoint(x_pos, end_y))

        self.opacity_anim = QPropertyAnimation(self, b"opacity")
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)

        self.pos_anim.start()
        self.opacity_anim.start()

    def start_hide_animation(self):
        if self._is_hiding:
            return
            
        self._is_hiding = True
        self.opacity_anim = QPropertyAnimation(self, b"opacity")
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.finished.connect(self.close_notification)
        self.opacity_anim.start()

    def close_notification(self):
        self.close()
        self.deleteLater()

    def get_opacity(self):
        return self.windowOpacity()

    def set_opacity(self, value):
        self.setWindowOpacity(value)

    opacity = pyqtProperty(float, get_opacity, set_opacity)

def show_notification(parent=None, message="در حال پردازش"):
    notification = Notification(parent, message)
    notification.show()
    return notification

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Login_UI()
    window.show()
    sys.exit(app.exec_())
