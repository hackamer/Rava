import os
import sys
import shutil
import sqlite3
import platform
import hashlib
import base64
from datetime import datetime
import jdatetime
from PyQt5 import uic, QtGui, QtWidgets, QtCore
from unidecode import unidecode
from cryptography.hazmat.primitives import hmac, hashes
from cryptography.fernet import Fernet
from PyQt5.QtWidgets import (QFrame, QLabel, QHBoxLayout, QApplication)
from PyQt5.QtCore import (Qt, QPropertyAnimation, QTimer,
                          QPoint, QEasingCurve, pyqtProperty)  # type: ignore
import ast
import bcrypt
import zipfile


class RavaAppError(Exception):
    pass

if __name__ == "__main__":
    raise RavaAppError("Please Dont run this file run main.py file")
