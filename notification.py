from PyQt5.QtWidgets import (QFrame, QLabel, QHBoxLayout)
from PyQt5.QtCore import (Qt, QPropertyAnimation, QTimer, 
                         QPoint, QEasingCurve, pyqtProperty)
from PyQt5.QtGui import QColor

class Notification(QFrame):
    def __init__(self, parent=None, message="ثبت شد ✓"):
        super().__init__(parent)
        self._is_hiding = False
        self.message = message
        self.setup_ui()

    def setup_ui(self):
        self.setMinimumWidth(500)  
        self.setMaximumWidth(600)  
        self.setMinimumHeight(80)
        self.setStyleSheet('''
            background-color: rgba(76, 175, 80, 0.85);
            border-radius: 12px;
            padding: 20px;
            margin: 10px;
            border: 2px solid rgba(255, 255, 255, 0.3);
            color: white;
        ''')
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(0.0)

        self.label = QLabel(self.message)
        #self.label.setStyleSheet('''
         #   color: white;
          #  font-size: 17px;  
           # font-weight: bold;
            #margin: 5px;
        #''')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(False)  
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)  
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showEvent(self, event):
        self.adjustSize()
        self.start_show_animation()
        QTimer.singleShot(2000, self.start_hide_animation)

    def start_show_animation(self):
        parent_rect = self.parent().geometry()
        start_y = parent_rect.height() + 100
        end_y = parent_rect.height() // 2 - self.height() // 4
        x_pos = (parent_rect.width() - self.width()) // 2

        self.move(QPoint(x_pos, start_y))
        
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(1000)
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)
        self.pos_anim.setStartValue(QPoint(x_pos, start_y))
        self.pos_anim.setEndValue(QPoint(x_pos, end_y))

        self.opacity_anim = QPropertyAnimation(self, b"opacity")
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)

        self.pos_anim.start()
        self.opacity_anim.start()

    def start_hide_animation(self):
        if self._is_hiding:
            return
            
        self._is_hiding = True
        self.opacity_anim = QPropertyAnimation(self, b"opacity")
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

    opacity = pyqtProperty(float, get_opacity, set_opacity)

def show_notification(parent, message="در حال پردازش"):
    #تابع برای نمایش نوتیفیکیشن
    notification = Notification(parent, message)
    notification.show()
    return notification