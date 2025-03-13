import sqlite3
import bcrypt
import os
from hashlib import sha512
salt = bcrypt.gensalt()


def Hashing(text: str) -> str:
    text += "SlMdlasdmij|||q&&$14kadnzxc$$@#9ads"
    m = sha512()
    m.update(text.encode())
    return m.hexdigest()


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def crypting(text: str, salt: bytes) -> bytes:
    text += "SlFz_Hp2madmnvnduarhf73298rfafa|&@#"
    text_bytes = text.encode('utf-8')
    hashed_password = bcrypt.hashpw(text_bytes, salt)
    return hashed_password


def Login(username, password):
    connection = sqlite3.connect("Login.db")
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
            # print(result)

        else:
            print("Failed in LogIn")
    else:
        print("The Username Not True Login Failed")

# dbmanager


def creator(file="Login.db", table="login_data"):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    q = "CREATE TABLE IF NOT EXISTS {} (username TEXT, password TEXT,salt TEXT)".format(
        table)
    cursor.execute(q)
    connection.commit()
    connection.close()


def insertor(username, password, file="Login.db", table="login_data"):
    creator()
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    salt = generate_salt().decode()
    q = "INSERT INTO {} (username, password, salt) VALUES (?, ?, ?)".format(
        table)
    cursor.execute(q, (Hashing(username), crypting(
        password, salt.encode('utf-8')), salt))
    connection.commit()
    connection.close()


def selector(file="Login.db", table="login_data"):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    q = "SELECT * FROM {} ".format(table)
    cursor.execute(q)
    result = cursor.fetchall()
    connection.commit()
    connection.close()
    return result


def reset(file="Login.db"):
    if os.path.exists(file):
        os.remove(file)
    else:
        print("The file does not exist")


# reset()
Login("Hossein", "P@ssw0rd")
Login("Alieh", "33129545")
