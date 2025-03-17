import time
from hashlib import sha512
import bcrypt
from supabase import create_client, Client
import json

# timing
start_time = time.time()
with open('config.json') as config_file:
    config = json.load(config_file)
url = config['API_URL']
key = config['API_KEY']

print("API URL:", url)
print("API Key:", key)

supabase: Client = create_client(str(url), str(key))
table = "rava_login"


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def Hashing(text: str) -> str:
    text += "M<Ng8EmHU}?*k$~v-u)nz(&Jsr:>L3wa4edq;t_xZ/'!D{AK5G"
    m = sha512()
    m.update(text.encode())
    return m.hexdigest()


def crypting(text: str, salt: bytes) -> bytes:
    text += "T2/)$gmx*ju8_&<}.>r94=`]@y7;AY(#G3SvV?B!EdC'FpXh6D"
    text_bytes = text.encode('utf-8')
    hashed_password = bcrypt.hashpw(text_bytes, salt)
    return hashed_password


def Login(username: str, password: str):
    salt_response = supabase.table(table).select(
        "salt").eq('username', Hashing(username)).execute()
    try:
        salt = salt_response.data[0]['salt']
    except:
        print("The Username Not True Login Failed")
        return False
    username = Hashing(username)
    password = crypting(password, salt.encode()).decode()
    response = supabase.table(table).select(
        "*").eq('username', username).eq('password', password).execute()
    if response.data:
        print("login OK")

    else:
        print("password has wrong or connection is broken")


# dbmanager


def remover(username: str, file: str = "Login.db") -> bool:

    response = (
        supabase.table(table)
        .delete().eq("username", Hashing(username))
        .execute()
    )
    if response.data:
        print("remove successful")
        return True
    else:
        print("problem in remove")
        return False


def insertor(username: str, password: str) -> bool:
    salt = generate_salt().decode()
    username = Hashing(username)
    password = crypting(password, salt.encode()).decode()
    if username == selector(username):
        print("username exist")
        return False
    if selector(username) == False:
        print("Problem in Connection")
        return False
    response = (supabase.table(table).insert(
        {"username": username, "password": password, "salt": salt})).execute()
    if response.data:
        print("insert successful")
        return True
    else:
        print("problem in insert")
        return False


def selector(username: str):
    try:
        response = supabase.table(table).select(
            "username").eq("username", username).execute()
    except:
        return False
    if response.data:
        return response.data[0]['username']
    else:
        return True


# funtions
insertor("Hossein", "P@ssw0rd")
Login("Hossein", "P@ssw0rd")
# timing
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
