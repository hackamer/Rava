"""
Rava desktop application (PyQt5).

This module implements login, signup, reporting, and data encryption utilities. All
comments and docstrings are standardized in English.
"""
# -----------------------------
# Imports
# -----------------------------
from imports import *
# import my modules
from config import *
from timing import *
from notification import msg,show_notification
from database import *
from encryption import *

# ------------------
# Search Page Window
# -------------------

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
        self.btn_sendsearch = self.findChild(
            QtWidgets.QPushButton, "btn_sendsearch")

    def connectors(self):
        """
        Connect UI signals to slots.
        """
        self.btn_sendsearch.clicked.connect(self.send_search)

    def send_search(self):
        """
        Persist search fields and trigger parent's read action.
        """
        global search_data
        search_data = {
            "code": unidecode(self.txt_code.text()),
            "day": unidecode(self.txt_day.text()),
            "month": unidecode(self.txt_month.text()),
            "year": unidecode(self.txt_year.text())
        }
        parent = self.parent()
        if isinstance(parent, Rava):
            parent.checkread()
            self.close()

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
        self.lbl_pagemedicineX.hide()
        self.lbl_pagemedicine.hide()
        self.spb_numberpagemedicine.hide()
        self.btn_pagemedicine.hide()
        self.btn_pagereport.hide()
        self.lbl_pagereport.hide()
        self.spb_numberpagereport.hide()
        self.lbl_pagereportX.hide()
        self.btn_back.hide()
        self.lbl_time.hide()
        self.lbl_reporter.hide()

    def widgets(self):
        """
        Finds and assigns all widgets from the UI to class attributes.
        """
        self.button = QtWidgets.QPushButton("hi there")
        self.button.hide()
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

        self.btn_savemedicine = self.findChild(
            QtWidgets.QPushButton, 'btn_savemedicine')
        self.btn_save = self.findChild(QtWidgets.QPushButton, 'btn_save')
        self.btn_calculateBMI = self.findChild(
            QtWidgets.QPushButton, 'btn_calculateBMI')
        self.btn_pagemedicine = self.findChild(
            QtWidgets.QPushButton, 'btn_pagemedicine')
        self.btn_pagereport = self.findChild(
            QtWidgets.QPushButton, 'btn_pagereport')
        self.btn_checkread = self.findChild(
            QtWidgets.QPushButton, 'btn_checkread')
        self.btn_search = self.findChild(QtWidgets.QPushButton, 'btn_search')
        self.btn_back = self.findChild(QtWidgets.QPushButton, 'btn_back')
        self.menu = self.findChild(QtWidgets.QMenu, 'menu_2')

    def connectors(self):
        """
        Connect button signals to their respective slot methods.
        """
        self.btn_save.clicked.connect(self.save)
        self.btn_savemedicine.clicked.connect(self.savemedicine)
        self.btn_calculateBMI.clicked.connect(self.calculateBMI)
        self.btn_search.clicked.connect(self.readmode)
        self.btn_back.clicked.connect(self.back)
        self.btn_pagereport.clicked.connect(self.read)
        self.btn_search.clicked.connect(self.open_search_window)
        self.btn_pagemedicine.clicked.connect(self.readdrug)
        self.menu.setTitle(f"خوش آمدی {u}")

    def open_search_window(self):
        """
        Open the search window for report queries.
        """
        search_window = SearchWindow(self)
        search_window.show()

    def verify_get(self, time, date, drug, code, username):
        """
        Compute verification tag for a report entry payload.
        """
        SUM = (username +
               unidecode(code) +
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
        return verify_generator(SUM)

    def save(self):
        """
        Save form data to the database with validation and messages.
        """
        copy()
        main_creator()
        decrypt_database(filepath)
        q = """INSERT INTO main (
            username, code, time, date, mood, Illusion, delusion, suicidalthoughts, psychomotor, Illusion01, ratespeech,
            speedspeech, contentspeech, tonespeech, affection, eyecontact, medicine, pain, bp, p, r, spo2, t,
            weight, height, bmi, eat, diet, moredetails, verify
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        if self.txt_code.text() == '':
            show_notification(
                None, "لطفا در لطفا شماره پرونده بیمار را وارد کنید!")
        else:
            try:
                x = int(unidecode(self.txt_code.text()))
                values = (
                    u,
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
                                    get_shamsi_date_str(), drugs, self.txt_code.text(), u)
                )
                cursor.execute(q, values)
                connection.commit()
                encrypt_database(filepath)
                copy()
                show_notification(None, "اطلاعات با موفقیت ذخیره شد")
            except ValueError:
                show_notification(
                    None, "لطفا شماره پرونده بیمار را به عدد وارد کنید")
            except BaseException:
                show_notification(None, "خطای ورود داده")

    def savemedicine(self):
        """
        Append current medicine entry to the in-memory list and notify.
        """
        global drugs
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
            show_notification(None, "داروی {} با موفقیت ذخیره شد".format(name))
        else:
            show_notification(
                None, "نام دارو را وارد کنید یا عدد دارو را غیر صفر بنویسید")

    def calculateBMI(self):
        """
        Calculate BMI from weight/height and update the BMI field.
        """
        try:
            w = int(unidecode(self.txt_weight.text()))
            h = int(unidecode(self.txt_height.text())) / 100
            if w < 10 or w > 300:
                show_notification(None, "لطفا وزن را به کیلوگرم وارد کنید ")
            if h < 0.9 or h > 3:
                show_notification(None, "لطفا قد را به سانتی متر وارد کنید",)
            else:
                BMI = w / (h) ** 2
                self.txt_bmi.setText(str(BMI))
        except BaseException:
            show_notification(None, "لطفا برای قد و وزن یک عدد انتخاب کنید")

    def readmode(self):
        """
        Enable read-only mode using a widget whitelist approach.
        """
        # Widget objectNames to show in read mode (whitelist)

        show_whitelist = {
            "txt_day",
            "txt_month",
            "txt_year",
            "btn_pagemedicine",
            "lbl_pagemedicine",
            "lbl_pagemedicineX",
            "spb_numberpagemedicine",
            "btn_pagereport",
            "lbl_pagereport",
            "spb_numberpagereport",
            "lbl_pagereportX",
            "btn_checkread",
            "btn_back"}
        with open("ui/readonly.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        for child in self.findChildren(QtWidgets.QWidget):
            if child.objectName() in show_whitelist:
                child.show()
            elif child.objectName() == "btn_savemedicine" or child.objectName() == "btn_calculateBMI":
                child.hide()
            child.setEnabled(
                child.objectName() in show_whitelist or child.objectName() in {
                    "txt_year",
                    "txt_month",
                    "txt_day",
                    "lotmain_3",
                    "centralwidget",
                    "spb_numberpagemedicine",
                    "btn_pagemedicine",
                    "grp_medicine",
                    "lot_medicine",
                    "che_read",
                    "btn_search",
                    "btn_pagereport",
                    "lbl_pagereport",
                    "spb_numberpagereport",
                    "lbl_pagereportX",
                    "btn_checkread"})

    def back(self):
        """
        Exit read-only mode and restore primary UI state.
        """
        show_whitelist = {
            "txt_day",
            "txt_month",
            "txt_year",
            "btn_pagemedicine",
            "lbl_pagemedicine",
            "lbl_pagemedicineX",
            "spb_numberpagemedicine",
            "btn_pagereport",
            "lbl_pagereport",
            "spb_numberpagereport",
            "lbl_pagereportX",
            "btn_checkread",
            "btn_back"}
        with open("ui/main.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        for child in self.findChildren(QtWidgets.QWidget):
            if child.objectName() in show_whitelist:
                child.hide()
            elif child.objectName() == "btn_savemedicine" or child.objectName() == "btn_calculateBMI" or child.objectName() == "btn_back":
                child.show()
            self.lbl_time.hide()
            self.lbl_reporter.hide()
            # Enable all widgets except those in show_whitelist (if you want to
            # disable them, otherwise keep enabled)
            child.setEnabled(child.objectName() not in show_whitelist or child.objectName(
            ) == "btn_savemedicine" or child.objectName() == "btn_calculateBMI" or child.objectName() == "btn_back")

    def checkread(self):
        """
        Execute a search query on saved reports and prepare pagination.
        """
        global response, search_data
        code = search_data.get("code", "")
        day = search_data.get("day", "")
        month = search_data.get("month", "")
        year = search_data.get("year", "")
        if day != '' and month != '' and year != '':
            try:
                if int(day) > 31 or int(day) < 1:
                    show_notification(None, "روز را به درستی وارد کنید")
                elif int(month) < 1 or int(month) > 12:
                    show_notification(None, "ماه را به درستی وارد کنید")
                else:
                    if len(day) == 1:
                        day = "0" + day
                    if len(month) == 1:
                        month = "0" + month
                    date = year + "/" + month + "/" + day
                    q = "SELECT * FROM main WHERE code = ? and date = ?"
                    values = (code, date)
                    decrypt_database(filepath)
                    cursor.execute(q, values)
            except ValueError:
                show_notification(None, "روز ماه و سال را به عدد وارد کنید")
        else:
            try:
                intcode = int(code)
                q = "SELECT * FROM main WHERE code = ?"
                values = (code,)
                decrypt_database(filepath)
                cursor.execute(q, values)
            except ValueError:
                show_notification(
                    None, "لطفا شماره پرونده بیمار را به عدد وارد نمایید")
            except BaseException:
                show_notification(None, "متاسفانه اطلاعاتی موجود نمی باید")
        connection.commit()
        response = cursor.fetchall()
        if len(response) == 0:
            self.spb_numberpagereport.setMaximum(0)
            self.spb_numberpagereport.setMinimum(0)
            show_notification(None, "متاسفانه گزارش پرستاری مورد نظر یافت نشد")

        else:
            n = str(len(response))
            self.lbl_pagereportX.setText("از {}".format(n))
            self.spb_numberpagereport.setMaximum(len(response))
            self.spb_numberpagereport.setMinimum(1)
            self.spb_numberpagereport.setValue(len(response))
            show_notification(None, "به تعداد {} گزارش یافت شد".format(n))
            self.read()
        encrypt_database(filepath)

    def read(self):
        """
        Load a selected report page into UI widgets.
        """
        global medicine
        page = self.spb_numberpagereport.value()
        self.lbl_time.show()
        self.lbl_reporter.show()
        try:
            self.lbl_reporter.setText(
                "نویسنده:{}".format(response[page - 1][0]))
            self.txt_code.setText(response[page - 1][1])
            self.lbl_time.setText("در تاریخ{}".format(
                response[page - 1][2] + "  " + response[page - 1][3]))
            self.cbx_mood.setCurrentText(response[page - 1][4])
            self.cbx_Illusion.setCurrentText(response[page - 1][5])
            self.txt_delusion.setText(response[page - 1][6])
            self.cbx_suicidalthoughts.setCurrentText(response[page - 1][7])
            self.cbx_psychomotor.setCurrentText(response[page - 1][8])
            self.che_Illusion.setChecked(response[page - 1][9])
            self.cbx_ratespeech.setCurrentText(response[page - 1][10])
            self.cbx_speedspeech.setCurrentText(response[page - 1][11])
            self.cbx_contentspeech.setCurrentText(response[page - 1][12])
            self.cbx_tonespeech.setCurrentText(response[page - 1][13])
            self.cbx_affection.setCurrentText(response[page - 1][14])
            self.che_eyecontact.setChecked(response[page - 1][15])
            medicine_raw = response[page - 1][16]
            medicine = ast.literal_eval(medicine_raw)
            self.lbl_pagemedicineX.setText("از {}".format(len(medicine)))
            self.spb_numberpagemedicine.setMaximum(len(medicine))
            if len(medicine) == 0:
                self.spb_numberpagemedicine.setMinimum(len(medicine))
                self.spb_numberpagemedicine.setValue(0)
            else:
                self.spb_numberpagemedicine.setValue(1)
                self.readdrug()
            self.che_pain.setChecked(response[page - 1][17])
            self.txt_bp.setText(response[page - 1][18])
            self.txt_p.setText(response[page - 1][19])
            self.txt_r.setText(response[page - 1][20])
            self.txt_spo2.setText(response[page - 1][21])
            self.txt_t.setText(response[page - 1][22])
            self.txt_weight.setText(response[page - 1][23])
            self.txt_height.setText(response[page - 1][24])
            self.txt_bmi.setText(response[page - 1][25])
            self.cbx_eat.setCurrentText(response[page - 1][26])
            self.txt_diet.setText(response[page - 1][27])
            self.txt_moredetails.setText(response[page - 1][28])
            if self.verify_get(response[page - 1][2],
                               response[page - 1][3],
                               medicine,
                               search_data.get("code"),
                               response[page - 1][0]) == response[page - 1][29]:
                pass
            else:
                msg("اخطار جدی این گزارش اعتبار ندارد و تغییر کرده", "C")

        except ValueError:
            pass
        except BaseException:
            show_notification(None, "متاسفانه گزارشی یافت نشد")

    def readdrug(self):
        """
        Load a selected medicine entry into UI widgets.
        """
        n = len(medicine)
        if n == 0:
            show_notification(None, "دارویی وجود ندارد")
        else:
            l = self.spb_numberpagemedicine.value()
            self.txt_medicinename.setText(medicine[l - 1].get("name"))
            self.spb_numbermedicine.setValue(medicine[l - 1].get("number"))
            self.spb_massmedicine.setValue(medicine[l - 1].get("mass"))
            self.cbb_type.setCurrentText(medicine[l - 1].get("type"))
            time_str = medicine[l - 1].get("time")
            self.time_medicinetime.setTime(
                QtCore.QTime.fromString(time_str, "hh:mm"))


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
        """
        Bind and cache widget references from the signup UI.
        """
        self.txt_username = self.findChild(QtWidgets.QLineEdit, 'txt_username')
        self.txt_password = self.findChild(QtWidgets.QLineEdit, 'txt_password')
        self.btn_sendsignup = self.findChild(
            QtWidgets.QPushButton, 'btn_sendsignup')
        self.btn_delete = self.findChild(QtWidgets.QPushButton, 'btn_delete')

    def connectors(self):
        """
        Connect signup UI actions.
        """
        self.btn_sendsignup.clicked.connect(self.sendsignup)
        self.btn_delete.clicked.connect(self.delete)

    def sendsignup(self):
        """
        Handle signup form submission with validations and status messages.
        """
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
            show_notification(None, "خطای خالی بودن نام کاربری یا رمز عبور")
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
        elif password != passwordrep:
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            show_notification(None, "رمز عبور تکراری مطابقت ندارد")
            self.btn_sendsignup.setEnabled(True)
            self.btn_sendsignup.setText("ثبت نام")
        if u.startswith("admin"):
            if insertor(username, password):
                self.btn_sendsignup.setEnabled(True)
                self.btn_sendsignup.setText("ثبت نام")
                self.setCursor(QtGui.QCursor(
                    QtCore.Qt.CursorShape.ArrowCursor))
                show_notification(None, get_signup_msg())
                self.returnlogin()
            else:
                self.btn_sendsignup.setEnabled(True)
                self.btn_sendsignup.setText("ثبت نام")
                self.setCursor(QtGui.QCursor(
                    QtCore.Qt.CursorShape.ArrowCursor))
                show_notification(None, get_signup_msg())
                self.btn_sendsignup.setEnabled(True)
                self.btn_sendsignup.setText("ثبت نام")
        else:
            show_notification(None, "لطفا با یوزر ادمین وارد شوید")

    def delete(self):
        """
        Delete a user based on current permissions and inputs.
        """
        if self.txt_username.text() != "admin" and u == "admin":
            if remover(self.txt_username.text()) == "OK":
                show_notification(None, "با موفقیت حذف شد")
            else:
                show_notification(None, "خطا در حذف نام کاربری")

        elif self.txt_username.text().startswith("admin") and u.startswith("admin"):
            show_notification(None, "یک ادمین ادمین دیگری را نمیتواند حذف کند")
        elif self.txt_username.text().startswith("admin") and not u.startswith("admin"):
            if remover(self.txt_username.text()) == "OK":
                show_notification(None, "با موفقیت حذف شد")
            else:
                show_notification(None, "خطا در حذف نام کاربری")
        self.returnlogin()

    def returnlogin(self):
        """
        Return to the login window.
        """
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
        """
        Bind and cache widget references from the login UI.
        """
        self.btn_sendlogin = self.findChild(
            QtWidgets.QPushButton, 'btn_sendlogin')
        self.lnk_signup = self.findChild(
            QtWidgets.QCommandLinkButton, 'lnk_signup')
        self.txt_username = self.findChild(QtWidgets.QLineEdit, 'txt_username')
        self.txt_password = self.findChild(QtWidgets.QLineEdit, 'txt_password')

    def connectors(self):
        """
        Connect login UI actions.
        """
        self.btn_sendlogin.clicked.connect(self.sendlogin)
        self.lnk_signup.clicked.connect(self.opensignup)

    def opensignup(self):
        """
        Open the signup window and close the current login window.
        """
        self.signup = Signup_UI()
        self.signup.show()
        self.close()

    def sendlogin(self):
        """
        Handle login flow and open main window upon success.
        """
        global u
        creator()
        username = self.txt_username.text()
        password = self.txt_password.text()
        if username == '' or password == '':
            show_notification(None, "خطای خالی بودن ")
        else:
            self.btn_sendlogin.setEnabled(False)
            self.btn_sendlogin.setText("درحال ورود")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
            try:
                logincheck = Login(username, password)
            except BaseException:
                show_notification(None, "خطای غیر قابل پیش بینی نرم افزار")
                self.btn_sendlogin.setEnabled(True)
                self.btn_sendlogin.setText("ورود")
                self.setCursor(QtGui.QCursor(
                    QtCore.Qt.CursorShape.ArrowCursor))
                exit()
            if logincheck:
                self.btn_sendlogin.setEnabled(True)
                self.btn_sendlogin.setText("ورود")
                self.setCursor(QtGui.QCursor(
                    QtCore.Qt.CursorShape.ArrowCursor))
                u = self.txt_username.text()
                if username.startswith("admin"):
                    self.lnk_signup.setEnabled(True)
                    show_notification(None, "یوزر ادمین خوش آمدی!!")

                show_notification(None, get_login_msg())
                self.main = Rava()
                self.main.show()
                # self.main.showMinimized()
                self.main.showMaximized()
                self.showMinimized()
            else:
                self.setCursor(QtGui.QCursor(
                    QtCore.Qt.CursorShape.ArrowCursor))
                show_notification(None, get_login_msg())
                self.btn_sendlogin.setEnabled(True)
                self.btn_sendlogin.setText("ورود")


insertor("admin", "P@ssw0rd")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Login_UI()
    window.show()
    sys.exit(app.exec_())
