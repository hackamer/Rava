"""
Database Management Module

This module provides comprehensive database operations for the Rava medical
reporting application, including user authentication, medical report storage,
and secure data management with encryption.

Key Features:
- User authentication with bcrypt password hashing
- Medical report data storage and retrieval
- Database encryption and security
- Table creation and management
- User registration and deletion
"""

from imports import *
from config import *
from encryption import decrypt_database, encrypt_database, copy


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
# MODULE PROTECTION
# =============================================================================

if __name__ == "__main__":
    raise RavaAppError("Please don't run this file directly. Run main.py instead.")

