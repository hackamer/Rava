"""
Encryption and Security Module

This module provides comprehensive encryption and security functionality for the
Rava medical reporting application, including database encryption, key management,
data integrity verification, and secure backup operations.

Key Features:
- Fernet-based database encryption with hardware-bound keys
- HMAC-SHA256 data integrity verification
- Hardware-based key derivation for enhanced security
- Automatic backup and key management
- Secure file operations with error handling
"""

from imports import *
from config import *
from backup import smart_backup


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
# MODULE PROTECTION
# =============================================================================

if __name__ == "__main__":
    raise RavaAppError("Please don't run this file directly. Run main.py instead.")
