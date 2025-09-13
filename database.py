from imports import *
from config import *
from encryption import decrypt_database,encrypt_database,copy
# -----------------------------
# Login and User Management Functions
# -----------------------------

def main_creator(table: str = "main"):
    """
    Create the main table if it does not already exist.
    """
    try:
        decrypt_database(filepath)
    except BaseException:
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


def generate_salt() -> bytes:
    """
    Generate a random salt for password hashing.
    """
    return bcrypt.gensalt()


def Hashing(text: str) -> str:
    """
    Placeholder hashing function (currently returns input).
    """
    return text


def crypting(text: str, salt: bytes) -> bytes:
    """
    Hash the password with a salt using bcrypt.
    """
    text += "b:2S]3zeFU_E>WNq!rPs^[5Rn)CZw(LtYK`hV;8/"
    text_bytes = text.encode('utf-8')
    hashed_password = bcrypt.hashpw(text_bytes, salt)
    return hashed_password


def Login(username: str, password: str) -> bool:
    """
    Validate username and password against stored credentials.
    """
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
        cursor.execute(q, (username, crypting(password, salt.encode('utf-8'))))
        connection.commit()
        result = cursor.fetchall()
        encrypt_database(filepath)
        if result:
            login_msg = "Login successful."
            return True
        else:
            login_msg = "Username or password is incorrect."
            return False
    else:
        login_msg = "Username or password is incorrect."
        return False


def creator(table: str = "login_data"):
    """
    Create the login_data table if it does not already exist.
    """
    try:
        decrypt_database(filepath)
    except BaseException:
        pass
    q = f"CREATE TABLE IF NOT EXISTS {table} (username TEXT, password TEXT, salt TEXT)"
    cursor.execute(q)
    connection.commit()
    encrypt_database(filepath)


def insertor(username: str, password: str, table: str = "login_data") -> bool:
    """
    Insert a new user into the login_data table with salted hash.
    """
    global signup_msg
    creator()
    if username == selector(username, table):
        signup_msg = "Username already exists."
        return False
    salt = generate_salt()
    q = f"INSERT INTO {table} (username, password, salt) VALUES (?, ?, ?)"
    decrypt_database(filepath)
    cursor.execute(q, (username, crypting(password, salt), salt.decode()))
    connection.commit()
    encrypt_database(filepath)
    signup_msg = "User registered successfully."
    return True


def remover(username: str, table="login_data") -> str:
    """
    Remove a user from the specified table and return status.
    """
    creator()
    decrypt_database(filepath)
    q = f"DELETE FROM {table} WHERE username = ?"
    cursor.execute(q, (username,))
    result = cursor.rowcount
    connection.commit()
    encrypt_database(filepath)
    if result >0:
        print("OK")
        return "OK"
    else:
        print("NO")
        return "NO"


def selector(username: str, table="login_data"):
    """
    Return the username if found in the specified table; otherwise False.
    """
    decrypt_database(filepath)
    q = f"SELECT username FROM {table} WHERE username = ?"
    cursor.execute(q, (username,))
    result = cursor.fetchall()
    connection.commit()
    encrypt_database(filepath)
    if result:
        return result[0][0]
    else:
        return False

def get_login_msg():
    return login_msg
def get_signup_msg() -> str:
    return signup_msg

if __name__ == "__main__":
    raise RavaAppError("Please Dont run this file run main.py file")

