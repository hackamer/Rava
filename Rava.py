import os
import sys
import shutil
import sqlite3
from datetime import datetime
import jdatetime
from PyQt5 import uic, QtGui, QtWidgets, QtCore
from unidecode import unidecode

# -----------------------------
# Global Variables and Paths
# -----------------------------
drugs = []  # List to store medicine information for the current session

# Determine the folder path for storing config and data
folderpath = os.path.join(os.path.join(
    os.environ['USERPROFILE']), 'AppData', 'Local', 'Rava')
try:
    os.mkdir(folderpath)
except FileExistsError:
    # Folder already exists, nothing to do
    print()
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


def get_shamsi_datetime_str():
    """
    Returns the current date and time in Shamsi (Jalali) format as a string.
    """
    now = datetime.now()
    shamsi_now = jdatetime.datetime.fromgregorian(datetime=now)
    return f"{shamsi_now.year:04d}/{shamsi_now.month:02d}/{shamsi_now.day:02d} - {shamsi_now.hour:02d}:{shamsi_now.minute:02d}:{shamsi_now.second:02d}"


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


def creator(table: str = "main"):
    """
    Creates the main table in the database if it does not exist.
    """
    q = (
        "CREATE TABLE IF NOT EXISTS {} ("
        "username TEXT,code Integer,time TEXT, mood TEXT,Illusion TEXT,"
        "delusion TEXT,suicidalthoughts TEXT,psychomotor TEXT,Illusion01 Binary,ratespeech TEXT,"
        "speedspeech TEXT,contentspeech TEXT,tonespeech TEXT,affection TEXT,eyecontact TEXT,"
        "medicine TEXT,pain Binary,bp TEXT,p TEXT,r TEXT,spo2 TEXT,t TEXT,"
        "weight Integer,height Integer,bmi Integer,eat TEXT,diet TEXT,moredetails TEXT)"
    ).format(table)
    cursor.execute(q)
    connection.commit()
    copy()

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

    def widgets(self):
        """
        Finds and assigns all widgets from the UI to class attributes.
        """
        self.lbl_welcome = self.findChild(QtWidgets.QLabel, "lbl_welcome")
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

        self.time_medicinetime = self.findChild(
            QtWidgets.QTimeEdit, 'time_medicinetime')

        self.che_Illusion = self.findChild(QtWidgets.QCheckBox, 'che_Illusion')
        self.che_eyecontact = self.findChild(
            QtWidgets.QCheckBox, 'che_eyecontact')
        self.che_pain = self.findChild(QtWidgets.QCheckBox, 'che_pain')

        self.btn_savemedicine = self.findChild(
            QtWidgets.QPushButton, 'btn_savemedicine')
        self.btn_save = self.findChild(QtWidgets.QPushButton, 'btn_save')
        self.btn_calculateBMI = self.findChild(
            QtWidgets.QPushButton, 'btn_calculateBMI')
        self.btn_logout = self.findChild(QtWidgets.QPushButton, 'btn_logout')

    def connectors(self):
        """
        Connects button signals to their respective slot methods.
        """
        self.btn_save.clicked.connect(self.save)
        self.btn_savemedicine.clicked.connect(self.savemedicine)
        self.btn_calculateBMI.clicked.connect(self.calculateBMI)

    def save(self):
        """
        Saves the form data to the database. Handles validation and error messages.
        """
        print("workiiiiiing")
        copy()
        creator()
        q = """INSERT INTO main (
            username, code, time, mood, Illusion, delusion, suicidalthoughts, psychomotor, Illusion01, ratespeech,
            speedspeech, contentspeech, tonespeech, affection, eyecontact, medicine, pain, bp, p, r, spo2, t,
            weight, height, bmi, eat, diet, moredetails
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        try:
            values = (
                "username",
                int(unidecode(self.txt_code.text())),
                get_shamsi_datetime_str(),
                self.cbx_mood.currentText(),
                self.cbx_Illusion.currentText(),
                self.txt_delusion.text(),
                self.cbx_suicidalthoughts.currentText(),
                self.cbx_psychomotor.currentText(),
                int(self.che_Illusion.isChecked()),
                self.cbx_ratespeech.currentText(),
                self.cbx_speedspeech.currentText(),
                self.cbx_contentspeech.currentText(),
                self.cbx_tonespeech.currentText(),
                self.cbx_affection.currentText(),
                int(self.che_eyecontact.isChecked()),
                str(drugs),
                int(self.che_pain.isChecked()),
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
                self.txt_moredetails.toPlainText()
            )
            cursor.execute(q, values)
            connection.commit()
            copy()
            msg("اطلاعات با موفقیت ذخیره شد", "I")
        except ValueError:
            msg("لطفا شماره پرونده بیمار را به عدد وارد کنید", "W")
        except:
            msg("خطای ورود داده", "W")

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
        drugs.append(newmed)
        msg("داروی {} با موفقیت ذخیره شد".format(name), "I")

    def calculateBMI(self):
        """
        Calculates BMI from weight and height fields and updates the BMI field.
        Shows a warning if input is invalid.
        """
        try:
            BMI = int(unidecode(self.txt_weight.text())) / \
                (int(unidecode(self.txt_height.text())) / 100) ** 2
            self.txt_bmi.setText(str(BMI))
        except:
            msg("لطفا برای قد و وزن یک عدد انتخاب کنید", "W")


# -----------------------------
# Application Entry Point
# -----------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Rava()
    window.show()
    sys.exit(app.exec_())
