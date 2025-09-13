from imports import *
from config import *

def copy():
    """
    Copy the config database file to the hidden backup location.
    """
    shutil.copy2(filepath, hidden_path)


def get_machine_id():
    """
    Return a hardware-based identifier (processor string).
    """
    mac = platform.processor()
    return mac


def get_stored_piece():
    """
    Read and return the first 6 characters from the key file.
    """
    with open(dllpath, "rb") as f:
        return f.read().decode()[:6]


def build_final_key():
    """
    Build a deterministic Fernet key from hardware ID and stored piece.
    """
    piece1 = get_machine_id()[:6]
    piece2 = get_stored_piece()
    combined = piece1 + piece2
    hash_val = hashlib.sha256(combined.encode()).digest()
    return base64.urlsafe_b64encode(hash_val)


def generate_key(key_file=dllpath):
    """
    Generate and persist a random key; return final derived Fernet key.
    """
    key = Fernet.generate_key()
    with open(key_file, 'wb') as file:
        file.write(key)
    return build_final_key()


def load_key(key_file=dllpath):
    """
    Load and return the derived Fernet key built from persisted piece.
    """
    if not os.path.exists(key_file):
        raise FileNotFoundError(
            "Key file not found. Please ensure the key file exists.")
    with open(key_file, 'rb') as file:
        return build_final_key()


def encrypt_database(db_file, key_file=dllpath):
    """
    Encrypt the SQLite database file in place and back it up.

    Args:
        db_file: Path to database file.
        key_file: Path to key piece file.
    Returns:
        Path to the encrypted database file.
    """
    try:
        while True:
            decrypt_database(filepath, key_file)
    except BaseException:
        pass
    # Generate or load key
    if not os.path.exists(key_file):
        key = generate_key(key_file)
    else:
        key = load_key(key_file)

    fernet = Fernet(key)

    # Read the database file
    if not os.path.exists(db_file):
        raise FileNotFoundError(f"Database file {db_file} not found.")
    with open(db_file, 'rb') as file:
        data = file.read()

    # Encrypt the data
    encrypted_data = fernet.encrypt(data)

    # Save encrypted data to a new file
    encrypted_file = db_file
    with open(encrypted_file, 'wb') as file:
        file.write(encrypted_data)
    copy()
    return encrypted_file


def decrypt_database(encrypted_file, key_file=dllpath):
    """
    Decrypt the database file in place and back it up.

    Args:
        encrypted_file: Path to encrypted database file.
        key_file: Path to key piece file.
    Returns:
        Path to the decrypted database file.
    """
    # Load key
    key = load_key(key_file)
    fernet = Fernet(key)

    # Read the encrypted file
    if not os.path.exists(encrypted_file):
        raise FileNotFoundError(f"Encrypted file {encrypted_file} not found.")
    with open(encrypted_file, 'rb') as file:
        encrypted_data = file.read()

    # Decrypt the data
    decrypted_data = fernet.decrypt(encrypted_data)

    # Save decrypted data to a new file
    decrypted_file = encrypted_file.replace('', '')
    with open(decrypted_file, 'wb') as file:
        file.write(decrypted_data)
    copy()
    return decrypted_file


def verify_generator(data: str) -> str:
    """
    Generate a verification tag (HMAC-SHA256) bound to hardware ID.
    """
    hardware_id = get_machine_id().encode()
    key = hashlib.sha256(hardware_id).digest()
    h = hmac.HMAC(key, hashes.SHA256())
    h.update(data.encode())
    tag = h.finalize()
    return base64.urlsafe_b64encode(tag).decode()


if __name__ == "__main__":
    raise RavaAppError("Please Dont run this file run main.py file")
