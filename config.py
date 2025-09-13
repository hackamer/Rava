from imports import *


# -----------------------------

# -----------------------------
# Global variables and paths
# -----------------------------
drugs = []  # لیست داروهای ثبت شده در این جلسه
medicine = []
response = []
search_data = {}  # متغیر سراسری برای داده‌های جستجو

# Set base folder for settings and data storage
folderpath = os.path.join(
    os.path.join(
        os.environ['USERPROFILE']),
    'AppData',
    'Local',
    'Rava')
dllpath = os.path.join(folderpath, 'libs.dll')
try:
    os.mkdir(folderpath)
except FileExistsError:
    # Folder already exists; nothing to do
    pass
except PermissionError:
    # Fallback path on permission error
    folderpath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Rava')

# Paths for config file and hidden backup
filepath = os.path.join(folderpath, "config.sys")
hidden_path = os.path.join(
    os.path.join(
        os.environ['USERPROFILE']),
    "AppData",
    "Local",
    "Microsoft",
    "Windows",
    "Explorer",
    "thumbs.db")

# Initialize SQLite connection
connection = sqlite3.connect(filepath)
cursor = connection.cursor()

if __name__ == "__main__":
    raise RavaAppError("Please Dont run this file run main.py file")
