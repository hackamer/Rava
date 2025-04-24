import os
import bcrypt
import sqlite3

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


#  run funtions
insertor("hackamer", "P@ssw0rd")
insertor("Hossein", "SlFz")
insertor("Alieh", "5764")
Login("hackamer", "P@ssw0rd")
Login("Hossein", "SlFz")
Login("Alieh", "5764")
