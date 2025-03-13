import os
import sqlite3
from prompt import Hashing


def creator(file="Login.db", table="login_data"):
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    q = "CREATE TABLE IF NOT EXISTS {} (username TEXT, password TEXT,salt TEXT)".format(
        table)
    cursor.execute(q)
    connection.commit()
    connection.close()


def insertor(username, password, file="Login.db", table="login_data"):
    salt = password.split("||;;::")[1]
    print(salt)
    password = password.split("||;;::")[0]
    username = username.split("||;;::")[0]
    connection = sqlite3.connect(file)
    cursor = connection.cursor()
    q = "INSERT INTO {} (username, password,salt) VALUES (?, ?, ?)".format(
        table)
    cursor.execute(q, (Hashing(username), Hashing(password), salt))
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
