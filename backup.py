"""
Backup Management Module

This module provides comprehensive backup functionality for the Rava application,
including file hashing, change detection, automatic backup creation, and
archive management to prevent storage overflow.

Features:
- SHA256 file hashing for change detection
- Timestamped backup creation
- Automatic archive compression when backup count exceeds limit
- Smart backup system that only creates backups when files have changed
"""

from imports import *
from config import *


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
# MODULE PROTECTION
# =============================================================================

if __name__ == "__main__":
    raise RavaAppError("Please don't run this file directly. Run main.py instead.")

