"""بسم الله الرحمن الرحیم"""
"""In the name of Allah, the Most Gracious, the Most Merciful."""
"""
main.py - Main application module.
This module implements the main application window and search functionality.
"""
"""
Rava Desktop Application (PyQt5)

A comprehensive medical reporting system with user authentication, 
data encryption, and report management capabilities.

This module implements:
- User login and signup functionality
- Medical report creation and management
- Data encryption and security
- Search and pagination features
- Medicine tracking system
"""

from imports import *
from config import *
from timing import *
from notification import msg, show_notification
from database import *
from encryption import *

class SearchWindow(QtWidgets.QMainWindow):
    """
    Search window for querying medical reports by patient code and date.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('ui/gozaresh_search.ui', self)
        self.setWindowTitle("جستجو و مرور گزارشات")
        
        # Set application icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/ravalogo.png"))
        self.setWindowIcon(icon)
        
        self.widgets()
        self.connectors()

    def widgets(self):
        """Initialize and bind UI widgets to class attributes."""
        self.txt_code = self.findChild(QtWidgets.QLineEdit, "txt_code")
        self.txt_day = self.findChild(QtWidgets.QLineEdit, "txt_day")
        self.txt_month = self.findChild(QtWidgets.QLineEdit, "txt_month")
        self.txt_year = self.findChild(QtWidgets.QLineEdit, "txt_year")
        self.btn_sendsearch = self.findChild(QtWidgets.QPushButton, "btn_sendsearch")

    def connectors(self):
        """Connect UI signals to their respective slot methods."""
        self.btn_sendsearch.clicked.connect(self.send_search)

    def send_search(self):
        """
        Process search form data and trigger report retrieval.
        
        Collects search criteria (patient code, date) and initiates
        the search process in the parent window.
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
            parent.cleardata()
            parent.checkread()
            self.close()

class Rava(QtWidgets.QMainWindow):
    """
    Main application window for medical report management.
    
    Handles report creation, editing, searching, and medicine tracking
    with comprehensive data validation and encryption.
    """
    
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/gozaresh.ui', self)
        
        # Load Persian fonts for proper text rendering
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        
        # Set application icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/ravalogo.png"))
        self.setWindowIcon(icon)
        
        self.widgets()
        self.connectors()
        
        # Hide pagination and read-only mode widgets initially
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
        Initialize and bind all UI widgets to class attributes.
        
        Organizes widgets by category for better maintainability:
        - Labels for display and pagination
        - ComboBoxes for selection fields
        - LineEdits for text input
        - TextEdit for detailed notes
        - SpinBoxes for numeric input
        - TimeEdit for time selection
        - CheckBoxes for boolean options
        - PushButtons for actions
        - Menu for user options
        """
        # Hidden test button (legacy)
        self.button = QtWidgets.QPushButton("hi there")
        self.button.hide()
        
        # Labels
        self.lbl_welcome = self.findChild(QtWidgets.QLabel, 'lbl_welcome')
        self.lbl_pagemedicine = self.findChild(QtWidgets.QLabel, "lbl_pagemedicine")
        self.lbl_pagemedicineX = self.findChild(QtWidgets.QLabel, "lbl_pagemedicineX")
        self.lbl_pagereport = self.findChild(QtWidgets.QLabel, 'lbl_pagereport')
        self.lbl_pagereportX = self.findChild(QtWidgets.QLabel, 'lbl_pagereportX')
        self.lbl_reporter = self.findChild(QtWidgets.QLabel, 'lbl_reporter')
        self.lbl_time = self.findChild(QtWidgets.QLabel, 'lbl_time')
        
        # ComboBoxes for medical assessment fields
        self.cbx_mood = self.findChild(QtWidgets.QComboBox, 'cbx_mood')
        self.cbx_Illusion = self.findChild(QtWidgets.QComboBox, 'cbx_Illusion')
        self.cbx_ratespeech = self.findChild(QtWidgets.QComboBox, 'cbx_ratespeech')
        self.cbx_speedspeech = self.findChild(QtWidgets.QComboBox, 'cbx_speedspeech')
        self.cbx_contentspeech = self.findChild(QtWidgets.QComboBox, 'cbx_contentspeech')
        self.cbx_tonespeech = self.findChild(QtWidgets.QComboBox, 'cbx_tonespeech')
        self.cbx_affection = self.findChild(QtWidgets.QComboBox, 'cbx_affection')
        self.cbx_psychomotor = self.findChild(QtWidgets.QComboBox, 'cbx_psychomotor')
        self.cbx_suicidalthoughts = self.findChild(QtWidgets.QComboBox, 'cbx_suicidalthoughts')
        self.cbx_eat = self.findChild(QtWidgets.QComboBox, 'cbx_eat')
        self.cbb_type = self.findChild(QtWidgets.QComboBox, 'cbb_type')

        # LineEdits for text input
        self.txt_code = self.findChild(QtWidgets.QLineEdit, "txt_code")
        self.txt_delusion = self.findChild(QtWidgets.QLineEdit, 'txt_delusion')
        self.txt_medicinename = self.findChild(QtWidgets.QLineEdit, 'txt_medicinename')
        self.txt_weight = self.findChild(QtWidgets.QLineEdit, 'txt_weight')
        self.txt_height = self.findChild(QtWidgets.QLineEdit, 'txt_height')
        self.txt_bmi = self.findChild(QtWidgets.QLineEdit, 'txt_bmi')
        self.txt_diet = self.findChild(QtWidgets.QLineEdit, 'txt_diet')
        self.txt_bp = self.findChild(QtWidgets.QLineEdit, 'txt_bp')
        self.txt_p = self.findChild(QtWidgets.QLineEdit, 'txt_p')
        self.txt_r = self.findChild(QtWidgets.QLineEdit, 'txt_r')
        self.txt_spo2 = self.findChild(QtWidgets.QLineEdit, 'txt_spo2')
        self.txt_t = self.findChild(QtWidgets.QLineEdit, 'txt_t')
        self.txt_year = self.findChild(QtWidgets.QLineEdit, 'txt_year')
        self.txt_month = self.findChild(QtWidgets.QLineEdit, 'txt_month')
        self.txt_day = self.findChild(QtWidgets.QLineEdit, 'txt_day')

        # TextEdit for detailed notes
        self.txt_moredetails = self.findChild(QtWidgets.QTextEdit, 'txt_moredetails')

        # SpinBoxes for numeric input
        self.spb_numbermedicine = self.findChild(QtWidgets.QSpinBox, 'spb_numbermedicine')
        self.spb_massmedicine = self.findChild(QtWidgets.QSpinBox, 'spb_massmedicine')
        self.spb_numberpagemedicine = self.findChild(QtWidgets.QSpinBox, 'spb_numberpagemedicine')
        self.spb_numberpagereport = self.findChild(QtWidgets.QSpinBox, 'spb_numberpagereport')
        
        # TimeEdit for medicine timing
        self.time_medicinetime = self.findChild(QtWidgets.QTimeEdit, 'time_medicinetime')

        # CheckBoxes for boolean options
        self.che_Illusion = self.findChild(QtWidgets.QCheckBox, 'che_Illusion')
        self.che_eyecontact = self.findChild(QtWidgets.QCheckBox, 'che_eyecontact')
        self.che_pain = self.findChild(QtWidgets.QCheckBox, 'che_pain')

        # PushButtons for actions
        self.btn_savemedicine = self.findChild(QtWidgets.QPushButton, 'btn_savemedicine')
        self.btn_save = self.findChild(QtWidgets.QPushButton, 'btn_save')
        self.btn_calculateBMI = self.findChild(QtWidgets.QPushButton, 'btn_calculateBMI')
        self.btn_pagemedicine = self.findChild(QtWidgets.QPushButton, 'btn_pagemedicine')
        self.btn_pagereport = self.findChild(QtWidgets.QPushButton, 'btn_pagereport')
        self.btn_checkread = self.findChild(QtWidgets.QPushButton, 'btn_checkread')
        self.btn_search = self.findChild(QtWidgets.QPushButton, 'btn_search')
        self.btn_back = self.findChild(QtWidgets.QPushButton, 'btn_back')
        
        # Menu for user options
        self.menu = self.findChild(QtWidgets.QMenu, 'menu_2')

    def connectors(self):
        """
        Connect UI signals to their respective slot methods.
        
        Establishes event handlers for all interactive elements
        including buttons, form submissions, and navigation controls.
        """
        # Form action buttons
        self.btn_save.clicked.connect(self.save)
        self.btn_savemedicine.clicked.connect(self.savemedicine)
        self.btn_calculateBMI.clicked.connect(self.calculateBMI)
        
        # Navigation and search buttons
        self.btn_search.clicked.connect(self.readmode)
        self.btn_search.clicked.connect(self.open_search_window)
        self.btn_back.clicked.connect(self.back)
        self.btn_pagereport.clicked.connect(self.read)
        self.btn_pagemedicine.clicked.connect(self.readdrug)
        
        # Set welcome message in menu
        self.menu.setTitle(f"خوش آمدی {u}")

    def open_search_window(self):
        """
        Open the search window for report queries.
        
        Creates and displays a new SearchWindow instance
        for querying medical reports by patient code and date.
        """
        search_window = SearchWindow(self)
        search_window.show()

    def verify_get(self, time, date, drug, code, username):
        """
        Generate verification hash for data integrity validation.
        
        Creates a comprehensive hash from all form fields to ensure
        data integrity and detect unauthorized modifications.
        
        Args:
            time (str): Report timestamp
            date (str): Report date
            drug (list): Medicine data
            code (str): Patient code
            username (str): Reporter username
            
        Returns:
            str: Verification hash for data integrity check
        """
        # Concatenate all form data for hash generation
        data_string = (username +
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
        
        return verify_generator(data_string)

    def save(self):
        """
        Save medical report data to the database with comprehensive validation.
        
        Performs data validation, encryption handling, and database insertion
        with proper error handling and user feedback.
        """
        global drugs
        
        # Prepare database and decrypt for writing
        copy()
        main_creator()
        decrypt_database(filepath)
        
        # SQL query for inserting medical report data
        insert_query = """INSERT INTO main (
            username, code, time, date, mood, Illusion, delusion, suicidalthoughts, 
            psychomotor, Illusion01, ratespeech, speedspeech, contentspeech, 
            tonespeech, affection, eyecontact, medicine, pain, bp, p, r, spo2, t,
            weight, height, bmi, eat, diet, moredetails, verify
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        
        # Validate required patient code field
        if self.txt_code.text() == '':
            show_notification(None, "لطفا در لطفا شماره پرونده بیمار را وارد کنید!")
            return
        
        try:
            # Validate patient code is numeric
            patient_code = int(unidecode(self.txt_code.text()))
            
            # Prepare data tuple for database insertion
            values = (
                u,  # Username
                str(unidecode(self.txt_code.text())),  # Patient code
                get_shamsi_time_str(),  # Current time
                get_shamsi_date_str(),  # Current date
                self.cbx_mood.currentText(),  # Mood assessment
                self.cbx_Illusion.currentText(),  # Illusion status
                self.txt_delusion.text(),  # Delusion details
                self.cbx_suicidalthoughts.currentText(),  # Suicidal thoughts
                self.cbx_psychomotor.currentText(),  # Psychomotor activity
                self.che_Illusion.isChecked(),  # Illusion checkbox
                self.cbx_ratespeech.currentText(),  # Speech rate
                self.cbx_speedspeech.currentText(),  # Speech speed
                self.cbx_contentspeech.currentText(),  # Speech content
                self.cbx_tonespeech.currentText(),  # Speech tone
                self.cbx_affection.currentText(),  # Affection level
                self.che_eyecontact.isChecked(),  # Eye contact
                str(drugs),  # Medicine data
                self.che_pain.isChecked(),  # Pain status
                self.txt_bp.text(),  # Blood pressure
                self.txt_p.text(),  # Pulse
                self.txt_r.text(),  # Respiration
                self.txt_spo2.text(),  # Oxygen saturation
                self.txt_t.text(),  # Temperature
                self.txt_weight.text(),  # Weight
                self.txt_height.text(),  # Height
                self.txt_bmi.text(),  # BMI
                self.cbx_eat.currentText(),  # Eating status
                self.txt_diet.text(),  # Diet details
                self.txt_moredetails.toPlainText(),  # Additional notes
                self.verify_get(get_shamsi_time_str(), get_shamsi_date_str(), 
                               drugs, self.txt_code.text(), u)  # Verification hash
            )
            
            # Execute database insertion
            cursor.execute(insert_query, values)
            connection.commit()
            
            # Re-encrypt database and create backup
            encrypt_database(filepath)
            copy()
            
            # Show success notification and clear medicine list
            show_notification(None, "اطلاعات با موفقیت ذخیره شد")
            drugs = []

        except ValueError:
            show_notification(None, "لطفا شماره پرونده بیمار را به عدد وارد کنید")
        except BaseException:
            show_notification(None, "خطای ورود داده")

    def savemedicine(self):
        """
        Add medicine entry to the current report's medicine list.
        
        Validates medicine data and adds it to the in-memory drugs list
        for inclusion in the medical report.
        """
        global drugs
        
        # Extract medicine data from form fields
        name = self.txt_medicinename.text()
        number = self.spb_numbermedicine.value()
        mass = self.spb_massmedicine.value()
        type_medicine = self.cbb_type.currentText()
        time_medicine = unidecode(self.time_medicinetime.time().toString("hh:mm"))
        
        # Create medicine dictionary
        medicine_entry = {
            "name": name,
            "number": number,
            "mass": mass,
            "type": type_medicine,
            "time": time_medicine
        }
        
        # Validate required fields before adding
        if name != '' and number != 0:
            drugs.append(medicine_entry)
            show_notification(None, "داروی {} با موفقیت ذخیره شد".format(name))
        else:
            show_notification(None, "نام دارو را وارد کنید یا عدد دارو را غیر صفر بنویسید")

    def calculateBMI(self):
        """
        Calculate Body Mass Index (BMI) from weight and height inputs.
        
        Validates input ranges and calculates BMI using the standard formula:
        BMI = weight(kg) / height(m)²
        """
        try:
            # Extract and convert weight (kg) and height (cm)
            weight = int(unidecode(self.txt_weight.text()))
            height = int(unidecode(self.txt_height.text())) / 100  # Convert cm to meters
            
            # Validate weight range (10-300 kg)
            if weight < 10 or weight > 300:
                show_notification(None, "لطفا وزن را به کیلوگرم وارد کنید")
                return
            
            # Validate height range (0.9-3.0 meters)
            if height < 0.9 or height > 3.0:
                show_notification(None, "لطفا قد را به سانتی متر وارد کنید")
                return
            
            # Calculate BMI and update field
            bmi = weight / (height ** 2)
            self.txt_bmi.setText(str(bmi))
            
        except (ValueError, TypeError):
            show_notification(None, "لطفا برای قد و وزن یک عدد انتخاب کنید")

    def readmode(self):
        """
        Switch to read-only mode for viewing existing reports.
        
        Applies read-only styling and enables only navigation and search widgets.
        Hides editing controls and shows pagination elements for report browsing.
        """
        self.cleardrug()
        
        # Define widgets that should be visible in read mode
        read_mode_widgets = {
            "txt_day", "txt_month", "txt_year",
            "btn_pagemedicine", "lbl_pagemedicine", "lbl_pagemedicineX",
            "spb_numberpagemedicine", "btn_pagereport", "lbl_pagereport",
            "spb_numberpagereport", "lbl_pagereportX", "btn_checkread", "btn_back"
        }
        
        # Apply read-only stylesheet
        with open("ui/readonly.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        
        # Configure widget visibility and state
        for child in self.findChildren(QtWidgets.QWidget):
            if child.objectName() in read_mode_widgets:
                child.show()
            elif child.objectName() in ("btn_savemedicine", "btn_calculateBMI"):
                child.hide()
            
            # Enable only navigation and search widgets
            enabled_widgets = read_mode_widgets | {
                "txt_year", "txt_month", "txt_day", "lotmain_3", "centralwidget",
                "spb_numberpagemedicine", "btn_pagemedicine", "grp_medicine",
                "lot_medicine", "che_read", "btn_search", "btn_pagereport",
                "lbl_pagereport", "spb_numberpagereport", "lbl_pagereportX", "btn_checkread"
            }
            child.setEnabled(child.objectName() in enabled_widgets)

    def back(self):
        """
        Exit read-only mode and restore primary editing interface.
        
        Clears form data, applies main stylesheet, and re-enables
        all editing controls while hiding read-only navigation elements.
        """
        self.cleardrug()
        self.cleardata()
        
        # Widgets to hide when returning to edit mode
        read_mode_widgets = {
            "txt_day", "txt_month", "txt_year",
            "btn_pagemedicine", "lbl_pagemedicine", "lbl_pagemedicineX",
            "spb_numberpagemedicine", "btn_pagereport", "lbl_pagereport",
            "spb_numberpagereport", "lbl_pagereportX", "btn_checkread", "btn_back"
        }
        
        # Apply main stylesheet
        with open("ui/main.qss", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        
        # Configure widget visibility and state
        for child in self.findChildren(QtWidgets.QWidget):
            if child.objectName() in read_mode_widgets:
                child.hide()
            elif child.objectName() in ("btn_savemedicine", "btn_calculateBMI", "btn_back"):
                child.show()
            
            # Hide read-only mode labels
            self.lbl_time.hide()
            self.lbl_reporter.hide()
            
            # Enable editing widgets, disable read-only widgets
            editing_widgets = {"btn_savemedicine", "btn_calculateBMI", "btn_back"}
            child.setEnabled(
                child.objectName() not in read_mode_widgets or 
                child.objectName() in editing_widgets
            )

    def checkread(self):
        """
        Execute search query and prepare pagination for report results.
        
        Searches for medical reports based on patient code and optional date.
        Validates date inputs and sets up pagination controls for results.
        """
        global response, search_data
        
        # Extract search criteria
        code = search_data.get("code", "")
        day = search_data.get("day", "")
        month = search_data.get("month", "")
        year = search_data.get("year", "")
        
        # Search by code and date if all date fields provided
        if day != '' and month != '' and year != '':
            try:
                # Validate day range (1-31)
                if int(day) > 31 or int(day) < 1:
                    show_notification(None, "روز را به درستی وارد کنید")
                    return
                
                # Validate month range (1-12)
                if int(month) < 1 or int(month) > 12:
                    show_notification(None, "ماه را به درستی وارد کنید")
                    return
                
                # Format date with leading zeros
                if len(day) == 1:
                    day = "0" + day
                if len(month) == 1:
                    month = "0" + month
                
                date = f"{year}/{month}/{day}"
                query = "SELECT * FROM main WHERE code = ? and date = ?"
                values = (code, date)
                
            except ValueError:
                show_notification(None, "روز ماه و سال را به عدد وارد کنید")
                return
        else:
            # Search by code only
            try:
                int(code)  # Validate code is numeric
                query = "SELECT * FROM main WHERE code = ?"
                values = (code,)
            except ValueError:
                show_notification(None, "لطفا شماره پرونده بیمار را به عدد وارد نمایید")
                return
            except BaseException:
                show_notification(None, "متاسفانه اطلاعاتی موجود نمی باید")
                return
        
        # Execute database query
        decrypt_database(filepath)
        cursor.execute(query, values)
        connection.commit()
        response = cursor.fetchall()
        
        # Handle search results
        if len(response) == 0:
            self.spb_numberpagereport.setMaximum(0)
            self.spb_numberpagereport.setMinimum(0)
            show_notification(None, "متاسفانه گزارش پرستاری مورد نظر یافت نشد")
        else:
            # Set up pagination for results
            result_count = str(len(response))
            self.lbl_pagereportX.setText("از {}".format(result_count))
            self.spb_numberpagereport.setMaximum(len(response))
            self.spb_numberpagereport.setMinimum(1)
            self.spb_numberpagereport.setValue(len(response))
            show_notification(None, "به تعداد {} گزارش یافت شد".format(result_count))
            self.read()
        
        # Re-encrypt database
        encrypt_database(filepath)

    def read(self):
        """
        Load a selected report page into UI widgets.
        """
        global medicine
        self.cleardrug()
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
        self.cleardrug()
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
    
    def cleardrug(self):
        """
        Clear all medicine-related form fields to default values.
        
        Resets medicine name, quantity, mass, type, and time fields
        to their initial state for new medicine entry.
        """
        self.txt_medicinename.clear()
        self.spb_numbermedicine.setValue(0)
        self.spb_massmedicine.setValue(0)
        self.cbb_type.setCurrentText("po")
        self.time_medicinetime.setTime(QtCore.QTime.fromString("00:00", "hh:mm"))

    def cleardata(self):
        """
        Clear all form fields to their default state.
        
        Uses a dictionary-based approach to reset different widget types
        to their appropriate default values efficiently.
        """
        # Define clearing actions for each widget type
        clear_actions = {
            QtWidgets.QLineEdit: lambda w: w.clear(),
            QtWidgets.QTextEdit: lambda w: w.clear(),
            QtWidgets.QCheckBox: lambda w: w.setChecked(False),
            QtWidgets.QComboBox: lambda w: w.setCurrentIndex(0),
            QtWidgets.QSpinBox: lambda w: w.setValue(0),
            QtWidgets.QTimeEdit: lambda w: w.setTime(QtCore.QTime.fromString("00:00", "hh:mm"))
        }
        
        # Apply appropriate clearing action to each widget
        for widget in self.findChildren(QtWidgets.QWidget):
            for widget_type, action in clear_actions.items():
                if isinstance(widget, widget_type):
                    action(widget)
                    break

class Signup_UI(QtWidgets.QMainWindow):
    """
    User registration and management interface.
    
    Handles new user creation and user deletion with proper
    validation and permission checking.
    """
    
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/add_user_page.ui', self)
        
        # Load Persian fonts
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        
        # Set application icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/images/ravalogo.png"))
        self.setWindowIcon(icon)
        
        self.widgets()
        self.connectors()

    def widgets(self):
        """Initialize and bind signup form widgets."""
        self.txt_username = self.findChild(QtWidgets.QLineEdit, 'txt_username')
        self.txt_password = self.findChild(QtWidgets.QLineEdit, 'txt_password')
        self.txt_repeatpassword = self.findChild(QtWidgets.QLineEdit, 'txt_repeatpassword')
        self.btn_sendsignup = self.findChild(QtWidgets.QPushButton, 'btn_sendsignup')
        self.btn_delete = self.findChild(QtWidgets.QPushButton, 'btn_delete')

    def connectors(self):
        """Connect signup form actions to their handlers."""
        self.btn_sendsignup.clicked.connect(self.sendsignup)
        self.btn_delete.clicked.connect(self.delete)

    def sendsignup(self):
        """
        Process user registration with comprehensive validation.
        
        Validates form inputs, checks admin permissions, and creates
        new user accounts with proper error handling and user feedback.
        """
        username = self.txt_username.text()
        password = self.txt_password.text()
        password_confirm = self.txt_repeatpassword.text()
        
        # Set loading state
        self.btn_sendsignup.setEnabled(False)
        self.btn_sendsignup.setText("درحال ثبت نام")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
        
        # Validate required fields
        if username == '' or password == '':
            self._reset_signup_button()
            show_notification(None, "خطای خالی بودن نام کاربری یا رمز عبور")
            return
        
        # Validate password confirmation
        if password != password_confirm:
            self._reset_signup_button()
            show_notification(None, "رمز عبور تکراری مطابقت ندارد")
            return
        
        # Check admin permissions
        if not u.startswith("admin"):
            show_notification(None, "لطفا با یوزر ادمین وارد شوید")
            self._reset_signup_button()
            return
        
        # Attempt user creation
        try:
            if insertor(username, password):
                show_notification(None, get_signup_msg())
                self.returnlogin()
            else:
                show_notification(None, get_signup_msg())
        finally:
            self._reset_signup_button()
    
    def _reset_signup_button(self):
        """Reset signup button to normal state."""
        self.btn_sendsignup.setEnabled(True)
        self.btn_sendsignup.setText("ثبت نام")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))

    def delete(self):
        """
        Delete user account with proper permission validation.
        
        Ensures only authorized users can delete accounts and prevents
        admin users from deleting other admin accounts.
        """
        username_to_delete = self.txt_username.text()
        
        # Regular admin can delete non-admin users
        if username_to_delete != "admin" and u == "admin":
            if remover(username_to_delete) == "OK":
                show_notification(None, "با موفقیت حذف شد")
            else:
                show_notification(None, "خطا در حذف نام کاربری")
        
        # Prevent admin from deleting other admins
        elif username_to_delete.startswith("admin") and u.startswith("admin"):
            show_notification(None, "یک ادمین ادمین دیگری را نمیتواند حذف کند")
        
        # Non-admin trying to delete admin (should not happen)
        elif username_to_delete.startswith("admin") and not u.startswith("admin"):
            if remover(username_to_delete) == "OK":
                show_notification(None, "با موفقیت حذف شد")
            else:
                show_notification(None, "خطا در حذف نام کاربری")
        
        self.returnlogin()

    def returnlogin(self):
        """
        Navigate back to the login window.
        
        Creates a new login window instance and closes the current signup window.
        """
        self.login = Login_UI()
        self.login.show()
        self.close()


class Login_UI(QtWidgets.QMainWindow):
    """
    User authentication interface.
    
    Handles user login with credential validation and provides
    access to the main application upon successful authentication.
    """
    
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/login_page.ui', self)
        
        # Load Persian fonts
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        
        self.widgets()
        self.connectors()
        
        # Set application icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ui/images/ravalogo.png"))
        self.setWindowIcon(icon)
        
        # Disable signup link initially (enabled after admin login)
        self.lnk_signup.setEnabled(False)

    def widgets(self):
        """Initialize and bind login form widgets."""
        self.btn_sendlogin = self.findChild(QtWidgets.QPushButton, 'btn_sendlogin')
        self.lnk_signup = self.findChild(QtWidgets.QCommandLinkButton, 'lnk_signup')
        self.txt_username = self.findChild(QtWidgets.QLineEdit, 'txt_username')
        self.txt_password = self.findChild(QtWidgets.QLineEdit, 'txt_password')

    def connectors(self):
        """Connect login form actions to their handlers."""
        self.btn_sendlogin.clicked.connect(self.sendlogin)
        self.lnk_signup.clicked.connect(self.opensignup)

    def opensignup(self):
        """
        Navigate to the signup window.
        
        Creates a new signup window instance and closes the current login window.
        """
        self.signup = Signup_UI()
        self.signup.show()
        self.close()

    def sendlogin(self):
        """
        Process user login with authentication and session management.
        
        Validates credentials, handles admin privileges, and launches
        the main application window upon successful authentication.
        """
        global u
        
        # Initialize database
        creator()
        
        username = self.txt_username.text()
        password = self.txt_password.text()
        
        # Validate required fields
        if username == '' or password == '':
            show_notification(None, "خطای خالی بودن")
            return
        
        # Set loading state
        self.btn_sendlogin.setEnabled(False)
        self.btn_sendlogin.setText("درحال ورود")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
        
        try:
            # Attempt authentication
            login_success = Login(username, password)
            
            if login_success:
                # Set global user variable
                u = username
                
                # Enable signup for admin users
                if username.startswith("admin"):
                    self.lnk_signup.setEnabled(True)
                    show_notification(None, "یوزر ادمین خوش آمدی!!")
                
                # Show login success message
                show_notification(None, get_login_msg())
                
                # Launch main application
                self.main = Rava()
                self.main.show()
                self.main.showMaximized()
                self.showMinimized()
            else:
                # Show login failure message
                show_notification(None, get_login_msg())
                
        except BaseException:
            show_notification(None, "خطای غیر قابل پیش بینی نرم افزار")
            exit()
        finally:
            # Reset button state
            self.btn_sendlogin.setEnabled(True)
            self.btn_sendlogin.setText("ورود")
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))


# Initialize default admin user
insertor("admin", "P@ssw0rd")

if __name__ == "__main__":
    # Create and run the application
    app = QtWidgets.QApplication(sys.argv)
    window = Login_UI()
    window.show()
    sys.exit(app.exec_())
