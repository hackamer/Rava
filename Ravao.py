import sys
from PyQt5 import uic, QtGui, QtWidgets, QtCore
import sqlite3
import os


class Rava(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/gozaresh_search.ui', self)
        self.fontregular = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_Regular.ttf")
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Rava()
    window.show()
    sys.exit(app.exec_())
