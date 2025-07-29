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
from unidecode import unidecode
from cryptography.hazmat.primitives import hmac, hashes
from cryptography.fernet import Fernet
from notification import show_notification # Import the function from notification.py


# -----------------------------
# Global Variables and Paths
# -----------------------------
drugs = []  # List to store medicine information for the current session
response = []
search_data = {}  # Global variable to store search data
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


def creator(table: str = "main"):
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

# ------------------
# Search Page Window
#-------------------

class SearchWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/gozaresh_search.ui', self)
        self.setWindowTitle("جستجو و مرور گزارشات")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/ravalogo.png"))
        self.setWindowIcon(icon)
        self.widgets()
        self.connectors()
    
    def widgets(self):
        """
        Finds and assigns all widgets from the UI to class attributes.
        """
        self.txt_code = self.findChild(QtWidgets.QLineEdit, "txt_code")
        self.txt_day = self.findChild(QtWidgets.QLineEdit, "txt_day")
        self.txt_month = self.findChild(QtWidgets.QLineEdit, "txt_month")
        self.txt_year = self.findChild(QtWidgets.QLineEdit, "txt_year")
        self.btn_sendsearch = self.findChild(QtWidgets.QPushButton, "btn_sendsearch")

    def connectors(self):
        self.btn_sendsearch.clicked.connect(self.send_search)

    def send_search(self):
        """
        Stores search data in global variable, closes the search window, and triggers checkread in parent.
        """
        global search_data
        search_data = {
            "code": unidecode(self.txt_code.text()),
            "day": unidecode(self.txt_day.text()),
            "month": unidecode(self.txt_month.text()),
            "year": unidecode(self.txt_year.text())
        }
        self.close()
        if self.parent():
            self.parent().checkread()

# -----------------------------
# Main Application Window Class
# -----------------------------

class Rava(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load UI and set fonts/icons
        uic.loadUi('ui/gozaresh.ui', self)
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/ravalogo.png"))
        self.setWindowIcon(icon)
        self.widgets()
        self.connectors()
        #self.txt_day.hide()
        #self.txt_month.hide()
        #self.txt_year.hide()
        self.lbl_pagemedicineX.hide()
        self.lbl_pagemedicine.hide()
        self.spb_numberpagemedicine.hide()
        self.btn_pagemedicine.hide()
        self.btn_pagereport.hide()
        self.btn_pagereport_2.hide()
        self.lbl_pagereport.hide()
        #self.spb_numberpagereport.hide()
        self.lbl_pagereportX.hide()
        #self.btn_checkread.hide()
        self.lbl_time.hide()
        self.lbl_reporter.hide()

    def widgets(self):
        """
        Finds and assigns all widgets from the UI to class attributes.
        """
        self.lbl_welcome = self.findChild(QtWidgets.QLabel, 'lbl_welcome')
        self.lbl_pagemedicine = self.findChild(
            QtWidgets.QLabel, "lbl_pagemedicine")
        self.lbl_pagemedicineX = self.findChild(
            QtWidgets.QLabel, "lbl_pagemedicineX")
        self.lbl_pagereport = self.findChild(
            QtWidgets.QLabel, 'lbl_pagereport')
        self.lbl_pagereportX = self.findChild(
            QtWidgets.QLabel, 'lbl_pagereportX')
        self.lbl_reporter = self.findChild(QtWidgets.QLabel, 'lbl_reporter')
        self.lbl_time = self.findChild(QtWidgets.QLabel, 'lbl_time')
        self.cbx_mood = self.findChild(QtWidgets.QComboBox, 'cbx_mood')
        self.cbx_Illusion = self.findChild(QtWidgets.QComboBox, 'cbx_Illusion')
        self.cbx_ratespeech = self.findChild(
            QtWidgets.QComboBox, 'cbx_ratespeech')
        self.cbx_speedspeech = self.findChild(
            QtWidgets.QComboBox, 'cbx_speedspeech')
        self.cbx_contentspeech = self.findChild(
            QtWidgets.QComboBox, 'cbx_contentspeech')
        self.cbx_tonespeech = self.findChild(
            QtWidgets.QComboBox, 'cbx_tonespeech')
        self.cbx_affection = self.findChild(
            QtWidgets.QComboBox, 'cbx_affection')
        self.cbx_psychomotor = self.findChild(
            QtWidgets.QComboBox, 'cbx_psychomotor')
        self.cbx_suicidalthoughts = self.findChild(
            QtWidgets.QComboBox, 'cbx_suicidalthoughts')
        self.cbx_eat = self.findChild(QtWidgets.QComboBox, 'cbx_eat')
        self.cbb_type = self.findChild(QtWidgets.QComboBox, 'cbb_type')

        self.txt_code = self.findChild(QtWidgets.QLineEdit, "txt_code")
        self.txt_delusion = self.findChild(QtWidgets.QLineEdit, 'txt_delusion')
        self.txt_medicinename = self.findChild(
            QtWidgets.QLineEdit, 'txt_medicinename')
        self.txt_weight = self.findChild(QtWidgets.QLineEdit, 'txt_weight')
        self.txt_height = self.findChild(QtWidgets.QLineEdit, 'txt_height')
        self.txt_bmi = self.findChild(QtWidgets.QLineEdit, 'txt_bmi')
        self.txt_diet = self.findChild(QtWidgets.QLineEdit, 'txt_diet')
        self.txt_bp = self.findChild(QtWidgets.QLineEdit, 'txt_bp')
        self.txt_p = self.findChild(QtWidgets.QLineEdit, 'txt_p')
        self.txt_r = self.findChild(QtWidgets.QLineEdit, 'txt_r')
        self.txt_spo2 = self.findChild(QtWidgets.QLineEdit, 'txt_spo2')
        self.txt_t = self.findChild(QtWidgets.QLineEdit, 'txt_t')

        self.txt_moredetails = self.findChild(
            QtWidgets.QTextEdit, 'txt_moredetails')

        self.spb_numbermedicine = self.findChild(
            QtWidgets.QSpinBox, 'spb_numbermedicine')
        self.spb_massmedicine = self.findChild(
            QtWidgets.QSpinBox, 'spb_massmedicine')
        self.txt_year = self.findChild(QtWidgets.QLineEdit, 'txt_year')
        self.txt_month = self.findChild(QtWidgets.QLineEdit, 'txt_month')
        self.txt_day = self.findChild(QtWidgets.QLineEdit, 'txt_day')
        self.spb_numberpagemedicine = self.findChild(
            QtWidgets.QSpinBox, 'spb_numberpagemedicine')
        self.spb_numberpagereport = self.findChild(
            QtWidgets.QSpinBox, 'spb_numberpagereport')
        self.time_medicinetime = self.findChild(
            QtWidgets.QTimeEdit, 'time_medicinetime')

        self.che_Illusion = self.findChild(QtWidgets.QCheckBox, 'che_Illusion')
        self.che_eyecontact = self.findChild(
            QtWidgets.QCheckBox, 'che_eyecontact')
        self.che_pain = self.findChild(QtWidgets.QCheckBox, 'che_pain')
        #self.che_read = self.findChild(QtWidgets.QCheckBox, 'che_read')

        self.btn_savemedicine = self.findChild(
            QtWidgets.QPushButton, 'btn_savemedicine')
        self.btn_save = self.findChild(QtWidgets.QPushButton, 'btn_save')
        self.btn_calculateBMI = self.findChild(
            QtWidgets.QPushButton, 'btn_calculateBMI')
        #self.btn_logout = self.findChild(QtWidgets.QPushButton, 'btn_logout')
        self.btn_pagemedicine = self.findChild(
            QtWidgets.QPushButton, 'btn_pagemedicine')
        self.btn_pagereport = self.findChild(
            QtWidgets.QPushButton, 'btn_pagereport')
        self.btn_pagereport_2 = self.findChild(
            QtWidgets.QPushButton, 'btn_pagereport_2')
        self.btn_checkread = self.findChild(
            QtWidgets.QPushButton, 'btn_checkread')
        self.btn_search = self.findChild(QtWidgets.QPushButton, 'btn_search')

    def connectors(self):
        """
        Connects button signals to their respective slot methods.
        """
        self.btn_save.clicked.connect(self.save)
        self.btn_savemedicine.clicked.connect(self.savemedicine)
        self.btn_calculateBMI.clicked.connect(self.calculateBMI)
        self.btn_search.clicked.connect(self.readmode)
        #self.btn_checkread.clicked.connect(self.checkread)
        self.btn_pagereport.clicked.connect(self.read)
        self.btn_pagereport_2.clicked.connect(self.read)
        self.btn_search.clicked.connect(self.open_search_window)

    def open_search_window(self):
        search_window = SearchWindow(self)
        search_window.show()

    def verify_get(self, time, date, drug):
        SUM = ("username" +
               str(unidecode(self.txt_code.text())) +
               str(time) +
               str(date) +
               self.cbx_mood.currentText() +
               self.cbx_Illusion.currentText() +
               self.txt_delusion.text() +
               self.cbx_suicidalthoughts.currentText() +
               self.cbx_psychomotor.currentText() +
               str(int(self.che_Illusion.isChecked())) +
               self.cbx_ratespeech.currentText() +
               self.cbx_speedspeech.currentText() +
               self.cbx_contentspeech.currentText() +
               self.cbx_tonespeech.currentText() +
               self.cbx_affection.currentText() +
               str(int(self.che_eyecontact.isChecked())) +
               str(drug) +
               str(int(self.che_pain.isChecked())) +
               self.txt_bp.text() +
               self.txt_p.text() +
               self.txt_r.text() +
               self.txt_spo2.text() +
               self.txt_t.text() +
               self.txt_weight.text() +
               self.txt_height.text() +
               self.txt_bmi.text() +
               self.cbx_eat.currentText() +
               self.txt_diet.text() +
               self.txt_moredetails.toPlainText())
        print(SUM)
        return verify_generator(SUM)

    def save(self):
        """
        Saves the form data to the database. Handles validation and error messages.
        """
        copy()
        creator()
        decrypt_database(filepath)
        q = """INSERT INTO main (
            username, code, time, date, mood, Illusion, delusion, suicidalthoughts, psychomotor, Illusion01, ratespeech,
            speedspeech, contentspeech, tonespeech, affection, eyecontact, medicine, pain, bp, p, r, spo2, t,
            weight, height, bmi, eat, diet, moredetails, verify
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        try:
            values = (
                "username",
                str(unidecode(self.txt_code.text())),
                get_shamsi_time_str(),
                get_shamsi_date_str(),
                self.cbx_mood.currentText(),
                self.cbx_Illusion.currentText(),
                self.txt_delusion.text(),
                self.cbx_suicidalthoughts.currentText(),
                self.cbx_psychomotor.currentText(),
                self.che_Illusion.isChecked(),
                self.cbx_ratespeech.currentText(),
                self.cbx_speedspeech.currentText(),
                self.cbx_contentspeech.currentText(),
                self.cbx_tonespeech.currentText(),
                self.cbx_affection.currentText(),
                self.che_eyecontact.isChecked(),
                str(drugs),
                self.che_pain.isChecked(),
                self.txt_bp.text(),
                self.txt_p.text(),
                self.txt_r.text(),
                self.txt_spo2.text(),
                self.txt_t.text(),
                self.txt_weight.text(),
                self.txt_height.text(),
                self.txt_bmi.text(),
                self.cbx_eat.currentText(),
                self.txt_diet.text(),
                self.txt_moredetails.toPlainText(),
                self.verify_get(get_shamsi_time_str(),
                                get_shamsi_date_str(), drugs)
            )
            cursor.execute(q, values)
            connection.commit()
            encrypt_database(filepath)
            copy()
            show_notification(None,"اطلاعات با موفقیت ذخیره شد")
        except ValueError:
            show_notification(None,"لطفا شماره پرونده بیمار را به عدد وارد کنید")
        # except:
        #     msg("خطای ورود داده", "W")

    def savemedicine(self):
        """
        Saves the current medicine entry to the drugs list and shows a confirmation message.
        """
        global drugs
        print('medicine saved!')
        name = self.txt_medicinename.text()
        number = self.spb_numbermedicine.value()
        mass = self.spb_massmedicine.value()
        type_medicine = self.cbb_type.currentText()
        time_medicine = unidecode(
            self.time_medicinetime.time().toString("hh:mm"))
        newmed = {
            "name": name,
            "number": number,
            "mass": mass,
            "type": type_medicine,
            "time": time_medicine
        }
        if name != '' and number != 0:
            drugs.append(newmed)
            show_notification(None,"داروی {} با موفقیت ذخیره شد".format(name))
        else:
            show_notification(None,"نام دارو را وارد کنید یا عدد دارو را غیر صفر بنویسید")

    def calculateBMI(self):
        """
        Calculates BMI from weight and height fields and updates the BMI field.
        Shows a warning if input is invalid.
        """
        try:
            w = int(unidecode(self.txt_weight.text()))
            h = int(unidecode(self.txt_height.text())) / 100
            if w < 10 or w > 300:
                show_notification(None,"لطفا وزن را به کیلوگرم وارد کنید ")
            if h < 0.9 or h > 3:
                show_notification(None,"لطفا قد را به سانتی متر وارد کنید",)
            else:
                BMI = w / (h) ** 2
                self.txt_bmi.setText(str(BMI))
        except:
            show_notification(None,"لطفا برای قد و وزن یک عدد انتخاب کنید")

    def readmode(self, state=2):
        """
        Toggles read-only mode for the application using whitelist/blacklist style for all widgets.
        """
        # Widget objectNames to show in read mode (whitelist)

        show_whitelist = {
            "txt_day", "txt_month", "txt_year",
            "btn_pagemedicine", "lbl_pagemedicine", "lbl_pagemedicineX",
            "spb_numberpagemedicine", "btn_pagereport","btn_pagereport_2", "lbl_pagereport",
            "spb_numberpagereport", "lbl_pagereportX", "btn_checkread"
        }
        # if state == 2:
        with open("ui/readonly.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        for child in self.findChildren(QtWidgets.QWidget):
            if child.objectName() in show_whitelist:
                child.show()
            elif child.objectName() == "btn_savemedicine" or child.objectName() == "btn_calculateBMI":
                child.hide()
            child.setEnabled(child.objectName() in show_whitelist or child.objectName() in {
                "txt_year", "txt_month", "txt_day", "lotmain_3", "centralwidget", "txt_code",
                "spb_numberpagemedicine", "btn_pagemedicine", "grp_medicine", "lot_medicine", "che_read","btn_search",
                "btn_pagereport","btn_pagereport_2", "lbl_pagereport", "spb_numberpagereport", "lbl_pagereportX", "btn_checkread", "btn_logout"
            })

        # elif state == 0:
        #     with open("ui/main.qss", encoding="utf-8") as f:
        #         self.setStyleSheet(f.read())
        #     for child in self.findChildren(QtWidgets.QWidget):
        #         if child.objectName() in show_whitelist:
        #             child.hide()
        #         elif child.objectName() == "btn_savemedicine" or child.objectName() == "btn_calculateBMI":
        #             child.show()
        #         self.lbl_time.hide()
        #         self.lbl_reporter.hide()
        #         # Enable all widgets except those in show_whitelist (if you want to disable them, otherwise keep enabled)
        #         child.setEnabled(child.objectName(
        #         ) not in show_whitelist or child.objectName() == "btn_savemedicine" or child.objectName() == "btn_calculateBMI")

    def checkread(self):
        global response, search_data
        code = search_data.get("code", "")
        day = search_data.get("day", "")
        month = search_data.get("month", "")
        year = search_data.get("year", "")
        if day != '' and month != '' and year != '':
            try:
                if int(day) > 31 or int(day) < 1:
                    show_notification(None,"روز را به درستی وارد کنید")
                elif int(month) < 1 or int(month) > 12:
                    show_notification(None,"ماه را به درستی وارد کنید")
                else:
                    if len(day) == 1:
                        day = "0"+day
                    if len(month) == 1:
                        month = "0"+month
                    date = year+"/"+month+"/"+day
                    q = "SELECT * FROM main WHERE code = ? and date = ?"
                    values = (code, date)
                    decrypt_database(filepath)
                    cursor.execute(q, values)
            except ValueError:
                show_notification(None,"روز ماه و سال را به عدد وارد کنید")
        else:
            try:
                intcode = int(code)
                q = "SELECT * FROM main WHERE code = ?"
                values = (code,)
                decrypt_database(filepath)
                cursor.execute(q, values)
            except ValueError:
                show_notification(None,"لطفا شماره پرونده بیمار را به عدد وارد نمایید")
            except:
                show_notification(None,"متاسفانه اطلاعاتی موجود نمی باید")
        connection.commit()
        response = cursor.fetchall()
        if len(response) == 0:
            show_notification(None,"متاسفانه گزارش پرستاری مورد نظر یافت نشد")
            #self.spb_numberpagereport.setMaximum(0)
            #self.spb_numberpagereport.setMinimum(0)

        else:
            n = str(len(response))
            self.lbl_pagereportX.setText("از {}".format(n))
            #self.spb_numberpagereport.setMaximum(len(response))
            #self.spb_numberpagereport.setMinimum(1)
            #self.spb_numberpagereport.setValue(len(response))
            show_notification(None,"به تعداد {} گزارش یافت شد".format(n))
            self.read()
        encrypt_database(filepath)

    def read(self):
        page = self.spb_numberpagereport.value()
        self.lbl_time.show()
        self.lbl_reporter.show()
        try:
            self.lbl_reporter.setText("نویسنده:{}".format(response[page-1][0]))
            self.lbl_time.setText("در تاریخ{}".format(
                response[page-1][2]+"  "+response[page-1][3]))
            self.cbx_mood.setCurrentText(response[page-1][4])
            self.cbx_Illusion.setCurrentText(response[page-1][5])
            self.txt_delusion.setText(response[page-1][6])
            self.cbx_suicidalthoughts.setCurrentText(response[page-1][7])
            self.cbx_psychomotor.setCurrentText(response[page-1][8])
            self.che_Illusion.setChecked(response[page-1][9])
            self.cbx_ratespeech.setCurrentText(response[page-1][10])
            self.cbx_speedspeech.setCurrentText(response[page-1][11])
            self.cbx_contentspeech.setCurrentText(response[page-1][12])
            self.cbx_tonespeech.setCurrentText(response[page-1][13])
            self.cbx_affection.setCurrentText(response[page-1][14])
            print(response[page-1][15])
            self.che_eyecontact.setChecked(response[page-1][15])
            drug = response[page-1][16]
            print(drug)
            self.che_pain.setChecked(response[page-1][17])
            self.txt_bp.setText(response[page-1][18])
            self.txt_p.setText(response[page-1][19])
            self.txt_r.setText(response[page-1][20])
            self.txt_spo2.setText(response[page-1][21])
            self.txt_t.setText(response[page-1][22])
            self.txt_weight.setText(response[page-1][23])
            self.txt_height.setText(response[page-1][24])
            self.txt_bmi.setText(response[page-1][25])
            self.cbx_eat.setCurrentText(response[page-1][26])
            self.txt_diet.setText(response[page-1][27])
            self.txt_moredetails.setText(response[page-1][28])
            if self.verify_get(response[page-1][2], response[page-1][3], drug) == response[page-1][29]:
                pass
            else:
                msg("اخطار جدی این گزارش اعتبار ندارد و تغییر کرده", "C")

        except ValueError:
            print('pass')


# -----------------------------
# Application Entry Point
# -----------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Rava()
    window.show()
    sys.exit(app.exec_())