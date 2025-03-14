import time
from hashlib import sha512
import os
import bcrypt
import sqlite3
import wget
import tempfile
# timing
start_time = time.time()


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def Hashing(text: str) -> str:
    text += "SlMdlasdmij|||q&&$14kadnzxc$$@#9ads"
    m = sha512()
    m.update(text.encode())
    return m.hexdigest()


def crypting(text: str, salt: bytes) -> bytes:
    text += "SlFz_Hp2madmnvnduarhf73298rfafa|&@#"
    text_bytes = text.encode('utf-8')
    hashed_password = bcrypt.hashpw(text_bytes, salt)
    return hashed_password


def Login(username: str, password: str):
    URL = 'https://github.com/hackamer/Rava/releases/download/data/Login.db'
    file = tempfile.gettempdir()+"\Login.db"  # type: ignore
    try:
        os.remove(file)
    except:
        pass
    try:
        wget.download(URL, file)
    except:
        print("connection Error")
        return False
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    qsalt = "SELECT salt FROM login_data WHERE username = ?"
    cursor.execute(qsalt, (Hashing(username),))
    connection.commit()
    salt = cursor.fetchall()
    if salt:
        salt = salt[0][0]
        q = "SELECT * FROM login_data WHERE username = ? AND password = ?"
        cursor.execute(q, (Hashing(username), crypting(
            password, salt.encode('utf-8'))))
        connection.commit()
        result = cursor.fetchall()
        if result:
            print("login OK")

        else:
            print("Failed in LogIn")
    else:
        print("The Username Not True Login Failed")

# dbmanager


def reset(file: str = "Login.db"):
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist")


def creator(file: str = "Login.db", table: str = "login_data"):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    q = "CREATE TABLE IF NOT EXISTS {} (username TEXT, password TEXT,salt TEXT)".format(
        table)
    cursor.execute(q)
    connection.commit()
    connection.close()


def insertor(username: str, password: str, file: str = "Login.db", table: str = "login_data"):
    creator()
    if Hashing(username) == selector(username, file, table):
        print('Exist Username')
        return False
    salt = generate_salt()
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    q = "INSERT INTO {} (username, password,salt) VALUES (?, ?, ?)".format(
        table)
    cursor.execute(q, (Hashing(username), crypting(
        password, salt), salt.decode()))
    connection.commit()
    connection.close()


def remover(username: str, file="Login.db", table="login_data") -> str:
    creator()
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    q = "DELETE FROM {} WHERE username = ?".format(table)
    cursor.execute(q, (Hashing(username),))
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    if result:
        return "OK"
    else:
        return "NO"


def selector(username: str, file="Login.db", table="login_data"):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    q = "SELECT username FROM {} WHERE username = ?".format(table)
    cursor.execute(q, (Hashing(username),))
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    if result:
        return result[0][0]
    else:
        return False


# funtions

Login("Hossein", "P@ssw0rd")
Login("Alieh", "33129545")
# timing
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
