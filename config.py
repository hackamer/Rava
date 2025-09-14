"""
Configuration and Global Variables Module

This module defines global variables, file paths, and database connections
for the Rava medical reporting application. It handles directory creation,
path management, and initializes the SQLite database connection.

Key Components:
- Global data structures for session management
- Application directory and file path configuration
- Database connection initialization
- Error handling for directory creation
"""

from imports import *


# =============================================================================
# GLOBAL DATA STRUCTURES
# =============================================================================

# Session-based data storage
drugs = []          # Current session's medicine list
medicine = []       # Medicine data for report display
response = []       # Database query results
search_data = {}    # Search criteria and filters


# =============================================================================
# APPLICATION PATHS AND DIRECTORIES
# =============================================================================

# Primary application data directory
folderpath = os.path.join(
    os.environ['USERPROFILE'],
    'AppData',
    'Local',
    'Rava'
)

# Application library file
dllpath = os.path.join(folderpath, 'libs.dll')

# Main database file
filepath = os.path.join(folderpath, "config.sys")

# Hidden backup directories (disguised as system folders)
hidden_path = os.path.join(
    os.environ['USERPROFILE'],
    "AppData",
    "Local",
    "Microsoft",
    "Windows",
    "Explorer",
    "thumbs.db"
)

hidden_path_2 = os.path.join(
    os.environ['USERPROFILE'],
    "AppData",
    "Local",
    "Microsoft",
    "Windows",
    "SystemSecurity"
)


# =============================================================================
# DIRECTORY INITIALIZATION
# =============================================================================


"""
Create necessary application directories with fallback handling.

Attempts to create the main application directory and backup directories.
Provides fallback path if permission errors occur during creation.
"""
# Create main application directory
try:
    os.mkdir(folderpath)
except FileExistsError:
    # Directory already exists - no action needed
    pass
except PermissionError:
    # Fallback to user's home directory if AppData access denied
    folderpath = os.path.join(os.environ['USERPROFILE'], 'Rava')
    filepath = os.path.join(folderpath, "config.sys")
    dllpath = os.path.join(folderpath, 'libs.dll')
    os.mkdir(folderpath)

# Create hidden backup directory
try:
    os.mkdir(hidden_path_2)
except FileExistsError:
    # Directory already exists - no action needed
    pass


# =============================================================================
# DATABASE CONNECTION
# =============================================================================

# Initialize SQLite database connection
connection = sqlite3.connect(filepath)
cursor = connection.cursor()


# =============================================================================
# MODULE PROTECTION
# =============================================================================

if __name__ == "__main__":
    raise RavaAppError("Please don't run this file directly. Run main.py instead.")
