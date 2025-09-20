"""
بسم الله الرحمن الرحیم.
"""
"""
In the name of Allah, the Most Gracious, the Most Merciful.
"""
"""
full.py - Main application module.
This module implements the main application window and search functionality.
"""

import os
import sys
import shutil
import sqlite3
import platform
import hashlib
import base64
from datetime import datetime
import jdatetime
from PyQt5 import uic, QtGui, QtWidgets, QtCore
from unidecode import unidecode
from cryptography.hazmat.primitives import hmac, hashes
from cryptography.fernet import Fernet
from PyQt5.QtCore import (QPropertyAnimation, QTimer,
                          QPoint, QEasingCurve, pyqtProperty)  # type: ignore
import ast
import bcrypt
import zipfile


# =============================================================================
# GLOBAL DATA STRUCTURES
# =============================================================================

# Session-based data storage
drugs = []          # Current session's medicine list
medicine = []       # Medicine data for report display
response = []       # Database query results
search_data = {}    # Search criteria and filters


# =============================================================================
# APPLICATION PATHS AND DIRECTORIES
# =============================================================================

# Primary application data directory
folderpath = os.path.join(
    os.environ['USERPROFILE'],
    'AppData',
    'Local',
    'Rava'
)

# Application library file
dllpath = os.path.join(folderpath, 'libs.dll')

# Main database file
filepath = os.path.join(folderpath, "config.sys")

# Hidden backup directories (disguised as system folders)
hidden_path = os.path.join(
    os.environ['USERPROFILE'],
    "AppData",
    "Local",
    "Microsoft",
    "Windows",
    "Explorer",
    "thumbs.db"
)

hidden_path_2 = os.path.join(
    os.environ['USERPROFILE'],
    "AppData",
    "Local",
    "Microsoft",
    "Windows",
    "SystemSecurity"
)


# =============================================================================
# DIRECTORY INITIALIZATION
# =============================================================================


"""
Create necessary application directories with fallback handling.

Attempts to create the main application directory and backup directories.
Provides fallback path if permission errors occur during creation.
"""
# Create main application directory
try:
    os.mkdir(folderpath)
except FileExistsError:
    # Directory already exists - no action needed
    pass
except PermissionError:
    # Fallback to user's home directory if AppData access denied
    folderpath = os.path.join(os.environ['USERPROFILE'], 'Rava')
    filepath = os.path.join(folderpath, "config.sys")
    dllpath = os.path.join(folderpath, 'libs.dll')
    os.mkdir(folderpath)

# Create hidden backup directory
try:
    os.mkdir(hidden_path_2)
except FileExistsError:
    # Directory already exists - no action needed
    pass


# =============================================================================
# DATABASE CONNECTION
# =============================================================================

# Initialize SQLite database connection
connection = sqlite3.connect(filepath)
cursor = connection.cursor()


def get_file_hash(file_path):
    """
    Compute SHA256 hash of the entire file for change detection.
    
    This function reads the entire file into memory and computes its SHA256 hash.
    Suitable for small to medium files due to memory usage considerations.
    
    Args:
        file_path (str): Path to the file to hash
        
    Returns:
        str: Hexadecimal representation of the SHA256 hash
    """
    hash_algorithm = hashlib.sha256()
    with open(file_path, "rb") as file:
        hash_algorithm.update(file.read())
    return hash_algorithm.hexdigest()


def new_file_checker(source_path, target_path):
    """
    Determine if a file has been modified by comparing SHA256 hashes.
    
    Compares the hash of the source file with the target file to detect
    any changes. Returns True if files are different, False if identical.
    
    Args:
        source_path (str): Path to the source file
        target_path (str): Path to the target file for comparison
        
    Returns:
        bool: True if files are different, False if identical
    """
    return get_file_hash(source_path) != get_file_hash(target_path)


def backup(file_path):
    """
    Create a timestamped backup of the specified file.
    
    Creates a backup copy of the file in the backup directory with
    a timestamp prefix to ensure uniqueness and chronological ordering.
    
    Args:
        file_path (str): Path to the file to backup
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"{timestamp}_{os.path.basename(file_path)}"
    backup_path = os.path.join(hidden_path_2, backup_filename)
    shutil.copy2(file_path, backup_path)


def get_last_file(file_extension):
    """
    Retrieve the most recent file of a specific extension from backup directory.
    
    Scans the backup directory for files with the specified extension and
    returns the most recent one. If more than 20 files exist, they are
    automatically compressed into a ZIP archive.
    
    Args:
        file_extension (str): File extension to search for (e.g., '.db', '.dll')
        
    Returns:
        str or False: Path to the most recent file, or False if no files found
    """
    # Get all files with the specified extension
    backup_files = [
        os.path.join(hidden_path_2, filename) 
        for filename in os.listdir(hidden_path_2) 
        if (os.path.isfile(os.path.join(hidden_path_2, filename)) and 
            filename.lower().endswith(file_extension))
    ]
    
    # Sort files by modification time (most recent first)
    backup_files.sort(key=os.path.getmtime, reverse=True)
    
    # If too many files, compress them
    if len(backup_files) >= 20:
        zip_files(backup_files)
        return False
    elif len(backup_files) > 0:
        return backup_files[0]  # Most recent file
    else:
        return False


def smart_backup(file_path):
    """
    Intelligently create backup only if the file has changed.
    
    This function implements smart backup logic that:
    1. Checks if a previous backup exists for this file type
    2. Compares the current file with the last backup
    3. Creates a new backup only if changes are detected
    
    Args:
        file_path (str): Path to the file to potentially backup
    """
    file_extension = os.path.splitext(file_path)[1]
    last_backup = get_last_file(file_extension)
    
    # Create backup if no previous backup exists or file has changed
    if last_backup is False:
        backup(file_path)
    elif new_file_checker(file_path, last_backup):
        backup(file_path)


def zip_files(file_list):
    """
    Compress multiple files into a single ZIP archive and remove originals.
    
    Creates a timestamped ZIP archive containing all specified files and
    removes the original files to save disk space. Used when backup count
    exceeds the maximum threshold.
    
    Args:
        file_list (list): List of file paths to compress
    """
    timestamp = datetime.now().strftime("%Y%m-%d_%H-%M-%S")
    zip_filename = f"{timestamp}.zip"
    zip_path = os.path.join(hidden_path_2, zip_filename)
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_path in file_list:
            if os.path.isfile(file_path):
                # Add file to archive using only the filename (no path)
                zip_file.write(file_path, arcname=os.path.basename(file_path))
                # Remove original file after successful compression
                os.remove(file_path)


# =============================================================================
# BACKUP AND FILE MANAGEMENT
# =============================================================================

def copy():
    """
    Create secure backup copies of critical application files.
    
    Copies the main database file to a hidden backup location and triggers
    smart backup operations for both the database and library files.
    """
    shutil.copy2(filepath, hidden_path)
    smart_backup(dllpath)
    smart_backup(filepath)


# =============================================================================
# HARDWARE-BASED IDENTIFICATION
# =============================================================================

def get_machine_id():
    """
    Generate a hardware-based identifier for key derivation.
    
    Uses the processor information as a hardware identifier to create
    machine-specific encryption keys that cannot be easily replicated
    on different systems.
    
    Returns:
        str: Hardware identifier string
    """
    return platform.processor()


def get_stored_piece():
    """
    Retrieve the stored key piece from the library file.
    
    Reads the first 6 characters from the key file to use as part
    of the key derivation process.
    
    Returns:
        str: First 6 characters from the key file
    """
    with open(dllpath, "rb") as key_file:
        return key_file.read().decode()[:6]


# =============================================================================
# KEY GENERATION AND MANAGEMENT
# =============================================================================

def build_final_key():
    """
    Construct a deterministic Fernet key from hardware ID and stored piece.
    
    Combines hardware-specific information with a stored key piece to create
    a unique encryption key that is bound to the specific machine. This ensures
    that encrypted data cannot be decrypted on different systems.
    
    Returns:
        bytes: Base64-encoded Fernet key
    """
    # Get hardware identifier (first 6 characters)
    hardware_piece = get_machine_id()[:6]
    
    # Get stored key piece
    stored_piece = get_stored_piece()
    
    # Combine pieces and create deterministic hash
    combined_key = hardware_piece + stored_piece
    key_hash = hashlib.sha256(combined_key.encode()).digest()
    
    # Return base64-encoded key suitable for Fernet
    return base64.urlsafe_b64encode(key_hash)


def generate_key(key_file: str = dllpath):
    """
    Generate a new random key and store it for future use.
    
    Creates a new random Fernet key, stores it in the specified file,
    and returns the final derived key based on hardware and stored pieces.
    
    Args:
        key_file (str): Path to the key storage file
        
    Returns:
        bytes: Derived Fernet key for encryption/decryption
    """
    # Generate a new random key
    random_key = Fernet.generate_key()
    
    # Store the key in the specified file
    with open(key_file, 'wb') as file:
        file.write(random_key)
    
    # Return the final derived key
    return build_final_key()


def load_key(key_file: str = dllpath):
    """
    Load the stored key and derive the final encryption key.
    
    Reads the stored key file and uses it along with hardware information
    to derive the final encryption key.
    
    Args:
        key_file (str): Path to the key storage file
        
    Returns:
        bytes: Derived Fernet key for encryption/decryption
        
    Raises:
        FileNotFoundError: If the key file does not exist
    """
    if not os.path.exists(key_file):
        raise FileNotFoundError(
            "Key file not found. Please ensure the key file exists.")
    
    # Return the derived key (stored key is used in build_final_key)
    return build_final_key()


# =============================================================================
# DATABASE ENCRYPTION OPERATIONS
# =============================================================================

def encrypt_database(db_file: str, key_file: str = dllpath) -> str:
    """
    Encrypt the SQLite database file using Fernet encryption.
    
    Encrypts the specified database file in place using a hardware-bound
    encryption key. Ensures the database is decrypted before encryption
    to handle any existing encrypted state.
    
    Args:
        db_file (str): Path to the database file to encrypt
        key_file (str): Path to the key storage file
        
    Returns:
        str: Path to the encrypted database file
        
    Raises:
        FileNotFoundError: If the database file does not exist
    """
    # Ensure database is decrypted before encryption
    try:
        while True:
            decrypt_database(filepath, key_file)
    except BaseException:
        # Database might not be encrypted or other error - continue
        pass
    
    # Generate or load encryption key
    if not os.path.exists(key_file):
        key = generate_key(key_file)
    else:
        key = load_key(key_file)
    
    # Initialize Fernet cipher
    fernet = Fernet(key)
    
    # Verify database file exists
    if not os.path.exists(db_file):
        raise FileNotFoundError(f"Database file {db_file} not found.")
    
    # Read database file
    with open(db_file, 'rb') as file:
        database_data = file.read()
    
    # Encrypt the database data
    encrypted_data = fernet.encrypt(database_data)
    
    # Write encrypted data back to the same file
    with open(db_file, 'wb') as file:
        file.write(encrypted_data)
    
    # Create backup of encrypted file
    copy()
    return db_file


def decrypt_database(encrypted_file: str, key_file: str = dllpath) -> str:
    """
    Decrypt the encrypted database file using Fernet decryption.
    
    Decrypts the specified encrypted database file in place using the
    hardware-bound decryption key. The decrypted data is written back
    to the same file location.
    
    Args:
        encrypted_file (str): Path to the encrypted database file
        key_file (str): Path to the key storage file
        
    Returns:
        str: Path to the decrypted database file
        
    Raises:
        FileNotFoundError: If the encrypted file does not exist
    """
    # Load decryption key
    key = load_key(key_file)
    fernet = Fernet(key)
    
    # Verify encrypted file exists
    if not os.path.exists(encrypted_file):
        raise FileNotFoundError(f"Encrypted file {encrypted_file} not found.")
    
    # Read encrypted file
    with open(encrypted_file, 'rb') as file:
        encrypted_data = file.read()
    
    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data)
    
    # Write decrypted data back to the same file
    with open(encrypted_file, 'wb') as file:
        file.write(decrypted_data)
    
    # Create backup of decrypted file
    copy()
    return encrypted_file


# =============================================================================
# DATA INTEGRITY VERIFICATION
# =============================================================================

def verify_generator(data: str) -> str:
    """
    Generate a hardware-bound verification tag using HMAC-SHA256.
    
    Creates a cryptographic verification tag that is bound to the specific
    hardware, ensuring data integrity and preventing tampering. The tag
    can only be verified on the same machine that generated it.
    
    Args:
        data (str): Data string to generate verification tag for
        
    Returns:
        str: Base64-encoded HMAC-SHA256 verification tag
    """
    # Get hardware identifier for key generation
    hardware_id = get_machine_id().encode()
    
    # Create key from hardware ID
    verification_key = hashlib.sha256(hardware_id).digest()
    
    # Generate HMAC-SHA256 tag
    hmac_calculator = hmac.HMAC(verification_key, hashes.SHA256())
    hmac_calculator.update(data.encode())
    verification_tag = hmac_calculator.finalize()
    
    # Return base64-encoded tag
    return base64.urlsafe_b64encode(verification_tag).decode()



# =============================================================================
# GLOBAL MESSAGE VARIABLES
# =============================================================================

login_msg = ""   # Global variable for login status messages
signup_msg = ""  # Global variable for signup status messages


# =============================================================================
# TABLE CREATION FUNCTIONS
# =============================================================================

def main_creator(table: str = "main"):
    """
    Create the main medical reports table with comprehensive schema.
    
    Creates the primary table for storing medical reports with all necessary
    fields for patient data, medical assessments, and verification.
    
    Args:
        table (str): Name of the table to create (default: "main")
    """
    try:
        decrypt_database(filepath)
    except BaseException:
        # Database might not exist yet - continue with creation
        pass
    
    # Define comprehensive medical report schema
    create_table_query = (
        "CREATE TABLE IF NOT EXISTS {} ("
        "username TEXT, code TEXT, time TEXT, date TEXT, mood TEXT, Illusion TEXT, "
        "delusion TEXT, suicidalthoughts TEXT, psychomotor TEXT, Illusion01 BINARY, "
        "ratespeech TEXT, speedspeech TEXT, contentspeech TEXT, tonespeech TEXT, "
        "affection TEXT, eyecontact BINARY, medicine TEXT, pain BINARY, bp TEXT, "
        "p TEXT, r TEXT, spo2 TEXT, t TEXT, weight TEXT, height TEXT, bmi TEXT, "
        "eat TEXT, diet TEXT, moredetails TEXT, verify TEXT)"
    ).format(table)
    
    cursor.execute(create_table_query)
    connection.commit()
    encrypt_database(filepath)
    copy()


def creator(table: str = "login_data"):
    """
    Create the user authentication table with security fields.
    
    Creates a table for storing user credentials with salted password hashes
    for secure authentication.
    
    Args:
        table (str): Name of the table to create (default: "login_data")
    """
    try:
        decrypt_database(filepath)
    except BaseException:
        # Database might not exist yet - continue with creation
        pass
    
    create_table_query = (
        f"CREATE TABLE IF NOT EXISTS {table} "
        "(username TEXT, password TEXT, salt TEXT)"
    )
    cursor.execute(create_table_query)
    connection.commit()
    encrypt_database(filepath)


# =============================================================================
# PASSWORD SECURITY FUNCTIONS
# =============================================================================

def generate_salt() -> bytes:
    """
    Generate a cryptographically secure random salt for password hashing.
    
    Returns:
        bytes: Random salt for use with bcrypt password hashing
    """
    return bcrypt.gensalt()


def crypting(password: str, salt: bytes) -> bytes:
    """
    Hash password with salt using bcrypt for secure storage.
    
    Appends a custom pepper string to the password before hashing
    to provide additional security against rainbow table attacks.
    
    Args:
        password (str): Plain text password to hash
        salt (bytes): Random salt for hashing
        
    Returns:
        bytes: Hashed password ready for storage
    """
    # Add custom pepper for additional security
    password_with_pepper = password + "b:2S]3zeFU_E>WNq!rPs^[5Rn)CZw(LtYK`hV;8/"
    password_bytes = password_with_pepper.encode('utf-8')
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password


# =============================================================================
# USER AUTHENTICATION FUNCTIONS
# =============================================================================

def Login(username: str, password: str) -> bool:
    """
    Authenticate user credentials against stored database records.
    
    Performs secure password verification using bcrypt with stored salt.
    Updates global login_msg variable with authentication result.
    
    Args:
        username (str): Username to authenticate
        password (str): Plain text password to verify
        
    Returns:
        bool: True if authentication successful, False otherwise
    """
    global login_msg
    
    # Retrieve salt for the username
    salt_query = "SELECT salt FROM login_data WHERE username = ?"
    decrypt_database(filepath)
    cursor.execute(salt_query, (username,))
    connection.commit()
    salt_result = cursor.fetchall()
    encrypt_database(filepath)
    
    if salt_result:
        # Extract salt and verify password
        salt = salt_result[0][0]
        verification_query = "SELECT * FROM login_data WHERE username = ? AND password = ?"
        decrypt_database(filepath)
        cursor.execute(verification_query, (username, crypting(password, salt.encode('utf-8'))))
        connection.commit()
        auth_result = cursor.fetchall()
        encrypt_database(filepath)
        
        if auth_result:
            login_msg = "ورود با موفقیت انجام شد"
            return True
        else:
            login_msg = "نام کاربری یا رمز عبور اشتباه است"
            return False
    else:
        login_msg = "نام کاربری یا رمز عبور اشتباه است"
        return False


def insertor(username: str, password: str, table: str = "login_data") -> bool:
    """
    Register a new user with secure password hashing.
    
    Creates a new user account with bcrypt-hashed password and random salt.
    Checks for existing usernames to prevent duplicates.
    
    Args:
        username (str): Username for the new account
        password (str): Plain text password to hash and store
        table (str): Database table name (default: "login_data")
        
    Returns:
        bool: True if registration successful, False if username exists
    """
    global signup_msg
    
    # Ensure table exists
    creator()
    # Check if username already exists
    if username == selector(username, table):
        signup_msg = "نام کاربری تکراری است"
        return False
    
    # Generate salt and hash password
    salt = generate_salt()
    hashed_password = crypting(password, salt)
    
    # Insert new user record
    insert_query = f"INSERT INTO {table} (username, password, salt) VALUES (?, ?, ?)"
    decrypt_database(filepath)
    cursor.execute(insert_query, (username, hashed_password, salt.decode()))
    connection.commit()
    encrypt_database(filepath)
    
    signup_msg = "نام کاربری با موفقیت ثبت شد"
    return True


def remover(username: str, table: str = "login_data") -> str:
    """
    Remove a user account from the database.
    
    Deletes the specified user from the authentication table and returns
    status indicating success or failure.
    
    Args:
        username (str): Username to remove
        table (str): Database table name (default: "login_data")
        
    Returns:
        str: "OK" if deletion successful, "NO" if user not found
    """
    # Ensure table exists
    creator()
    
    # Delete user record
    decrypt_database(filepath)
    delete_query = f"DELETE FROM {table} WHERE username = ?"
    cursor.execute(delete_query, (username,))
    deleted_rows = cursor.rowcount
    connection.commit()
    encrypt_database(filepath)
    
    if deleted_rows > 0:
        print("OK")
        return "OK"
    else:
        print("NO")
        return "NO"


def selector(username: str, table: str = "login_data"):
    """
    Check if a username exists in the database.
    
    Searches for the specified username in the authentication table
    and returns the username if found, False otherwise.
    
    Args:
        username (str): Username to search for
        table (str): Database table name (default: "login_data")
        
    Returns:
        str or False: Username if found, False if not found
    """
    decrypt_database(filepath)
    select_query = f"SELECT username FROM {table} WHERE username = ?"
    cursor.execute(select_query, (username,))
    result = cursor.fetchall()
    connection.commit()
    encrypt_database(filepath)
    
    if result:
        return result[0][0]
    else:
        return False


# =============================================================================
# MESSAGE RETRIEVAL FUNCTIONS
# =============================================================================

def get_login_msg() -> str:
    """
    Retrieve the current login status message.
    
    Returns:
        str: Current login message (success or error)
    """
    return login_msg


def get_signup_msg() -> str:
    """
    Retrieve the current signup status message.
    
    Returns:
        str: Current signup message (success or error)
    """
    return signup_msg

# =============================================================================
# PERSIAN CALENDAR DATE FUNCTIONS
# =============================================================================

def get_shamsi_date_str():
    """
    Get the current date in Persian (Shamsi/Jalali) calendar format.
    
    Converts the current Gregorian date to Persian calendar and returns
    it in a standardized YYYY/MM/DD format suitable for medical reports.
    
    Returns:
        str: Current date in Persian calendar format (YYYY/MM/DD)
        
    Example:
        >>> get_shamsi_date_str()
        '1403/09/15'
    """
    # Get current Gregorian date and time
    current_datetime = datetime.now()
    
    # Convert to Persian (Shamsi) calendar
    persian_datetime = jdatetime.datetime.fromgregorian(datetime=current_datetime)
    
    # Format as YYYY/MM/DD with zero-padding
    return f"{persian_datetime.year:04d}/{persian_datetime.month:02d}/{persian_datetime.day:02d}"


def get_shamsi_time_str():
    """
    Get the current time in Persian calendar context.
    
    Returns the current time in HH:MM:SS format, maintaining consistency
    with the Persian calendar system used throughout the application.
    
    Returns:
        str: Current time in HH:MM:SS format
        
    Example:
        >>> get_shamsi_time_str()
        '14:30:25'
    """
    # Get current Gregorian date and time
    current_datetime = datetime.now()
    
    # Convert to Persian (Shamsi) calendar
    persian_datetime = jdatetime.datetime.fromgregorian(datetime=current_datetime)
    
    # Format as HH:MM:SS with zero-padding
    return f"{persian_datetime.hour:02d}:{persian_datetime.minute:02d}:{persian_datetime.second:02d}"


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
        """
        Initialize and bind UI widgets to class attributes.
        """
        self.txt_code = self.findChild(QtWidgets.QLineEdit, "txt_code")
        self.txt_day = self.findChild(QtWidgets.QLineEdit, "txt_day")
        self.txt_month = self.findChild(QtWidgets.QLineEdit, "txt_month")
        self.txt_year = self.findChild(QtWidgets.QLineEdit, "txt_year")
        self.btn_sendsearch = self.findChild(QtWidgets.QPushButton, "btn_sendsearch")

    def connectors(self):
        """
        Connect UI signals to their respective slot methods.
        """
        self.btn_sendsearch.clicked.connect(self.send_search)

    def send_search(self):
        """
        Process search form data and trigger report retrieval.

        Collects search criteria (patient code, date) and initiates the search process
        in the parent window.
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

    Handles report creation, editing, searching, and medicine tracking with
    comprehensive data validation and encryption.
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
        self.menu_logout = self.findChild(QtWidgets.QMenu, 'menu_logout')
        self.menu_signup = self.findChild(QtWidgets.QMenu, 'menu_signup')

    def connectors(self):
        """
        Connect UI signals to their respective slot methods.

        Establishes event handlers for all interactive elements including buttons, form
        submissions, and navigation controls.
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
        
        # Menus connectors
        self.menu.setTitle(f"خوش آمدی {u}")
        self.menu_signup.hide()
        self.menu_logout.aboutToShow.connect(self.logout)
        self.menu_signup.aboutToShow.connect(self.goto_signup)
        if u.startswith("admin"):
            self.menu_signup.show()
        else:
            self.menu_signup.deleteLater()

    def logout(self):
        self.newwindow = Login_UI()
        self.newwindow.show()
        self.close()

    def goto_signup(self):
        if u.startswith("admin"):
            self.newwindow = Signup_UI()
            self.newwindow.show()
            self.close()
    def open_search_window(self):
        """
        Open the search window for report queries.

        Creates and displays a new SearchWindow instance for querying medical reports by
        patient code and date.
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

        Performs data validation, encryption handling, and database insertion with
        proper error handling and user feedback.
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

        Validates medicine data and adds it to the in-memory drugs list for inclusion in
        the medical report.
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

        Applies read-only styling and enables only navigation and search widgets. Hides
        editing controls and shows pagination elements for report browsing.
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

        Clears form data, applies main stylesheet, and re-enables all editing controls
        while hiding read-only navigation elements.
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

        Searches for medical reports based on patient code and optional date. Validates
        date inputs and sets up pagination controls for results.
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

        Resets medicine name, quantity, mass, type, and time fields to their initial
        state for new medicine entry.
        """
        self.txt_medicinename.clear()
        self.spb_numbermedicine.setValue(0)
        self.spb_massmedicine.setValue(0)
        self.cbb_type.setCurrentText("po")
        self.time_medicinetime.setTime(QtCore.QTime.fromString("00:00", "hh:mm"))

    def cleardata(self):
        """
        Clear all form fields to their default state.

        Uses a dictionary-based approach to reset different widget types to their
        appropriate default values efficiently.
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

    Handles new user creation and user deletion with proper validation and permission
    checking.
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
        """
        Initialize and bind signup form widgets.
        """
        self.txt_username = self.findChild(QtWidgets.QLineEdit, 'txt_username')
        self.txt_password = self.findChild(QtWidgets.QLineEdit, 'txt_password')
        self.txt_repeatpassword = self.findChild(QtWidgets.QLineEdit, 'txt_repeatpassword')
        self.btn_sendsignup = self.findChild(QtWidgets.QPushButton, 'btn_sendsignup')
        self.btn_delete = self.findChild(QtWidgets.QPushButton, 'btn_delete')

    def connectors(self):
        """
        Connect signup form actions to their handlers.
        """
        self.btn_sendsignup.clicked.connect(self.sendsignup)
        self.btn_delete.clicked.connect(self.delete)

    def sendsignup(self):
        """
        Process user registration with comprehensive validation.

        Validates form inputs, checks admin permissions, and creates new user accounts
        with proper error handling and user feedback.
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
        """
        Reset signup button to normal state.
        """
        self.btn_sendsignup.setEnabled(True)
        self.btn_sendsignup.setText("ثبت نام")
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))

    def delete(self):
        """
        Delete user account with proper permission validation.

        Ensures only authorized users can delete accounts and prevents admin users from
        deleting other admin accounts.
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

    Handles user login with credential validation and provides access to the main
    application upon successful authentication.
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
        

    def widgets(self):
        """
        Initialize and bind login form widgets.
        """
        self.btn_sendlogin = self.findChild(QtWidgets.QPushButton, 'btn_sendlogin')
        self.txt_username = self.findChild(QtWidgets.QLineEdit, 'txt_username')
        self.txt_password = self.findChild(QtWidgets.QLineEdit, 'txt_password')

    def connectors(self):
        """
        Connect login form actions to their handlers.
        """
        self.btn_sendlogin.clicked.connect(self.sendlogin)

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

        Validates credentials, handles admin privileges, and launches the main
        application window upon successful authentication.
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
                    
                    show_notification(None, "یوزر ادمین خوش آمدی!!")
                
                # Show login success message
                show_notification(None, get_login_msg())
                
                # Launch main application
                self.main = Rava()
                self.main.show()
                self.main.showNormal()
                self.close()
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


# =============================================================================
# ANIMATED NOTIFICATION WIDGET
# =============================================================================

class Notification(QtWidgets.QFrame):
    """
    Custom animated notification widget for displaying user feedback.
    
    Creates a modern, animated toast notification that slides in from the bottom
    of the screen with fade effects. Automatically disappears after a set duration.
    """
    
    def __init__(self, parent=None, message="ثبت شد ✓"):
        """
        Initialize the notification widget.
        
        Args:
            parent: Parent widget (optional)
            message (str): Message text to display in the notification
        """
        super().__init__(parent)
        
        # Load Persian font for proper text rendering
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        
        # Initialize state variables
        self._is_hiding = False
        self.message = message
        
        # Set up the user interface
        self.setup_ui()

    def setup_ui(self):
        """
        Configure the notification widget appearance and layout.
        
        Sets up styling, positioning, and layout for the notification widget
        with modern design elements and Persian font support.
        """
        # Set size constraints
        self.setMinimumWidth(500)
        self.setMaximumWidth(600)
        self.setMinimumHeight(80)
        
        # Apply modern styling with green success theme
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
        
        # Configure window properties for overlay behavior
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint) #type: ignore
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) #type: ignore
        self.setWindowOpacity(0.0)

        # Create and configure message label
        self.label = QtWidgets.QLabel(self.message)
        self.label.setAlignment(QtCore.Qt.AlignCenter) #type: ignore
        self.label.setWordWrap(False)
        
        # Set up layout with proper margins
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showEvent(self, a0):
        """
        Handle the show event to trigger animations.
        
        Automatically starts the show animation and sets up the auto-hide timer
        when the notification becomes visible.
        """
        self.adjustSize()
        self.start_show_animation()
        # Auto-hide after 2 seconds
        QTimer.singleShot(2000, self.start_hide_animation)

    def start_show_animation(self):
        """
        Create and execute the slide-in animation with fade effect.
        
        Animates the notification sliding up from the bottom of the screen
        with a smooth easing curve and simultaneous opacity fade-in.
        """
        # Calculate positioning relative to parent or screen
        if self.parent():
            parent_rect = self.parent().geometry() #type: ignore
        else:
            parent_rect = self.screen().geometry() #type: ignore
        
        # Define animation start and end positions
        start_y = parent_rect.height() + 100  # Start below screen
        end_y = parent_rect.height() // 2 - self.height() // 4  # Center vertically
        x_pos = (parent_rect.width() - self.width()) // 2  # Center horizontally

        # Position widget at start location
        self.move(QPoint(x_pos, start_y))

        # Create position animation (slide up)
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(1000)
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)  # Bouncy effect
        self.pos_anim.setStartValue(QPoint(x_pos, start_y))
        self.pos_anim.setEndValue(QPoint(x_pos, end_y))

        # Create opacity animation (fade in)
        self.opacity_anim = QPropertyAnimation(self, b"opacity")
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)

        # Start both animations simultaneously
        self.pos_anim.start()
        self.opacity_anim.start()

    def start_hide_animation(self):
        """
        Create and execute the fade-out animation.
        
        Prevents multiple hide animations and creates a smooth fade-out effect
        that triggers cleanup when complete.
        """
        # Prevent multiple hide animations
        if self._is_hiding:
            return

        self._is_hiding = True
        
        # Create fade-out animation
        self.opacity_anim = QPropertyAnimation(self, b"opacity")
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.finished.connect(self.close_notification)
        self.opacity_anim.start()

    def close_notification(self):
        """
        Clean up the notification widget after animation completes.
        
        Closes the widget and schedules it for deletion to free memory.
        """
        self.close()
        self.deleteLater()

    def get_opacity(self):
        """
        Get the current window opacity value.
        
        Returns:
            float: Current opacity value (0.0 to 1.0)
        """
        return self.windowOpacity()

    def set_opacity(self, value):
        """
        Set the window opacity value for animation purposes.
        
        Args:
            value (float): Opacity value (0.0 to 1.0)
        """
        self.setWindowOpacity(value)

    # Property for Qt animation system
    opacity = pyqtProperty(float, get_opacity, set_opacity)


# =============================================================================
# NOTIFICATION DISPLAY FUNCTIONS
# =============================================================================

def show_notification(parent=None, message="در حال پردازش"):
    """
    Display an animated notification with the specified message.
    
    Creates and shows a new notification widget with the given message.
    The notification will automatically animate in and disappear after 2 seconds.
    
    Args:
        parent: Parent widget for the notification (optional)
        message (str): Message text to display
        
    Returns:
        Notification: The created notification widget instance
    """
    notification = Notification(parent, message)
    notification.show()
    return notification


def msg(text: str, status: str):
    """
    Display a modal message dialog based on the specified status.
    
    Shows different types of message boxes (critical, warning, information)
    based on the status code provided.
    
    Args:
        text (str): Message text to display
        status (str): Status code determining dialog type
                     'C' = Critical error dialog
                     'W' = Warning dialog  
                     'I' = Information dialog
    """
    if status == "C":
        QtWidgets.QMessageBox.critical(None, "خطای نرم افزار راوا", text)
    elif status == "W":
        QtWidgets.QMessageBox.warning(None, "هشدار نرم افزار راوا", text)
    elif status == "I":
        QtWidgets.QMessageBox.information(None, "پیام نرم افزار راوا", text)

if __name__ == "__main__":
    # Create and run the application
    app = QtWidgets.QApplication(sys.argv)
    window = Login_UI()
    window.show()
    sys.exit(app.exec_())

