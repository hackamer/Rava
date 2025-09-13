from imports import *



class Notification(QtWidgets.QFrame):
    def __init__(self, parent=None, message="ثبت شد ✓"):
        super().__init__(parent)
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        self._is_hiding = False
        self.message = message
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumWidth(500)
        self.setMaximumWidth(600)
        self.setMinimumHeight(80)
        self.setStyleSheet('''
            font-family: IRANYekanXFaNum ExtraBold;
            font-size: 18px;
            background-color: rgba(76, 175, 80, 0.85);
            border-radius: 12px;
            padding: 20px;
            margin: 10px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
        ''')
        self.setWindowFlags(Qt.FramelessWindowHint |  # type: ignore
                            Qt.WindowStaysOnTopHint)  # type: ignore
        self.setAttribute(Qt.WA_TranslucentBackground)  # type: ignore
        self.setWindowOpacity(0.0)

        self.label = QtWidgets.QLabel(self.message)
        self.label.setAlignment(Qt.AlignCenter)  # type: ignore
        self.label.setWordWrap(False)
        layout = QtWidgets.QHBoxLayout(self)  # type: ignore
        layout.setContentsMargins(20, 15, 20, 15)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showEvent(self, event):  # type: ignore
        self.adjustSize()
        self.start_show_animation()
        QTimer.singleShot(2000, self.start_hide_animation)  # type: ignore

    def start_show_animation(self):
        parent_rect = self.parent().geometry() if self.parent(  # type: ignore
        ) else self.screen().geometry()  # type: ignore
        start_y = parent_rect.height() + 100
        end_y = parent_rect.height() // 2 - self.height() // 4
        x_pos = (parent_rect.width() - self.width()) // 2

        self.move(QPoint(x_pos, start_y))  # type: ignore

        self.pos_anim = QPropertyAnimation(self, b"pos")  # type: ignore
        self.pos_anim.setDuration(1000)
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)  # type: ignore
        self.pos_anim.setStartValue(QPoint(x_pos, start_y))  # type: ignore
        self.pos_anim.setEndValue(QPoint(x_pos, end_y))  # type: ignore

        self.opacity_anim = QPropertyAnimation(
            self, b"opacity")  # type: ignore
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)

        self.pos_anim.start()
        self.opacity_anim.start()

    def start_hide_animation(self):
        if self._is_hiding:
            return

        self._is_hiding = True
        self.opacity_anim = QPropertyAnimation(
            self, b"opacity")  # type: ignore
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.finished.connect(self.close_notification)
        self.opacity_anim.start()

    def close_notification(self):
        self.close()
        self.deleteLater()

    def get_opacity(self):
        return self.windowOpacity()

    def set_opacity(self, value):
        self.setWindowOpacity(value)

    opacity = pyqtProperty(float, get_opacity, set_opacity)  # type: ignore


def show_notification(parent=None, message="در حال پردازش"):
    notification = Notification(parent, message)
    notification.show()
    return notification

def msg(text: str, status: str):
    """
    Show a message box based on status.

    Status codes: 'C' = Critical, 'W' = Warning, 'I' = Information.
    """
    if status == "C":
        QtWidgets.QMessageBox.critical(None, "خطای نرم افزار راوا", text)
    elif status == "W":
        QtWidgets.QMessageBox.warning(None, "هشدار نرم افزار راوا", text)
    elif status == "I":
        QtWidgets.QMessageBox.information(None, "پیام نرم افزار راوا", text)

if __name__ == "__main__":
    raise RavaAppError("Please Dont run this file run main.py file")
