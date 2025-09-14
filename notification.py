"""
Notification and User Interface Module

This module provides comprehensive notification and messaging functionality for the
Rava medical reporting application, including animated toast notifications and
modal message dialogs for user feedback.

Key Features:
- Animated toast notifications with smooth transitions
- Persian font support for proper text rendering
- Modal message dialogs for critical information
- Customizable notification styling and positioning
- Automatic notification lifecycle management
"""

from imports import *


# =============================================================================
# ANIMATED NOTIFICATION WIDGET
# =============================================================================

class Notification(QtWidgets.QFrame):
    """
    Custom animated notification widget for displaying user feedback.
    
    Creates a modern, animated toast notification that slides in from the bottom
    of the screen with fade effects. Automatically disappears after a set duration.
    """
    
    def __init__(self, parent=None, message="ثبت شد ✓"):
        """
        Initialize the notification widget.
        
        Args:
            parent: Parent widget (optional)
            message (str): Message text to display in the notification
        """
        super().__init__(parent)
        
        # Load Persian font for proper text rendering
        self.fontebold = QtGui.QFontDatabase.addApplicationFont(
            "ui/fonts/IRANYekanXFaNum_ExtraBold.ttf")
        
        # Initialize state variables
        self._is_hiding = False
        self.message = message
        
        # Set up the user interface
        self.setup_ui()

    def setup_ui(self):
        """
        Configure the notification widget appearance and layout.
        
        Sets up styling, positioning, and layout for the notification widget
        with modern design elements and Persian font support.
        """
        # Set size constraints
        self.setMinimumWidth(500)
        self.setMaximumWidth(600)
        self.setMinimumHeight(80)
        
        # Apply modern styling with green success theme
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
        
        # Configure window properties for overlay behavior
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint) #type: ignore
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) #type: ignore
        self.setWindowOpacity(0.0)

        # Create and configure message label
        self.label = QtWidgets.QLabel(self.message)
        self.label.setAlignment(QtCore.Qt.AlignCenter) #type: ignore
        self.label.setWordWrap(False)
        
        # Set up layout with proper margins
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(20, 15, 20, 15)
        layout.addWidget(self.label)
        self.setLayout(layout)

    def showEvent(self, a0):
        """
        Handle the show event to trigger animations.
        
        Automatically starts the show animation and sets up the auto-hide timer
        when the notification becomes visible.
        """
        self.adjustSize()
        self.start_show_animation()
        # Auto-hide after 2 seconds
        QTimer.singleShot(2000, self.start_hide_animation)

    def start_show_animation(self):
        """
        Create and execute the slide-in animation with fade effect.
        
        Animates the notification sliding up from the bottom of the screen
        with a smooth easing curve and simultaneous opacity fade-in.
        """
        # Calculate positioning relative to parent or screen
        if self.parent():
            parent_rect = self.parent().geometry() #type: ignore
        else:
            parent_rect = self.screen().geometry() #type: ignore
        
        # Define animation start and end positions
        start_y = parent_rect.height() + 100  # Start below screen
        end_y = parent_rect.height() // 2 - self.height() // 4  # Center vertically
        x_pos = (parent_rect.width() - self.width()) // 2  # Center horizontally

        # Position widget at start location
        self.move(QPoint(x_pos, start_y))

        # Create position animation (slide up)
        self.pos_anim = QPropertyAnimation(self, b"pos")
        self.pos_anim.setDuration(1000)
        self.pos_anim.setEasingCurve(QEasingCurve.OutBack)  # Bouncy effect
        self.pos_anim.setStartValue(QPoint(x_pos, start_y))
        self.pos_anim.setEndValue(QPoint(x_pos, end_y))

        # Create opacity animation (fade in)
        self.opacity_anim = QPropertyAnimation(self, b"opacity")
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(0.0)
        self.opacity_anim.setEndValue(1.0)

        # Start both animations simultaneously
        self.pos_anim.start()
        self.opacity_anim.start()

    def start_hide_animation(self):
        """
        Create and execute the fade-out animation.
        
        Prevents multiple hide animations and creates a smooth fade-out effect
        that triggers cleanup when complete.
        """
        # Prevent multiple hide animations
        if self._is_hiding:
            return

        self._is_hiding = True
        
        # Create fade-out animation
        self.opacity_anim = QPropertyAnimation(self, b"opacity")
        self.opacity_anim.setDuration(800)
        self.opacity_anim.setStartValue(1.0)
        self.opacity_anim.setEndValue(0.0)
        self.opacity_anim.finished.connect(self.close_notification)
        self.opacity_anim.start()

    def close_notification(self):
        """
        Clean up the notification widget after animation completes.
        
        Closes the widget and schedules it for deletion to free memory.
        """
        self.close()
        self.deleteLater()

    def get_opacity(self):
        """
        Get the current window opacity value.
        
        Returns:
            float: Current opacity value (0.0 to 1.0)
        """
        return self.windowOpacity()

    def set_opacity(self, value):
        """
        Set the window opacity value for animation purposes.
        
        Args:
            value (float): Opacity value (0.0 to 1.0)
        """
        self.setWindowOpacity(value)

    # Property for Qt animation system
    opacity = pyqtProperty(float, get_opacity, set_opacity)


# =============================================================================
# NOTIFICATION DISPLAY FUNCTIONS
# =============================================================================

def show_notification(parent=None, message="در حال پردازش"):
    """
    Display an animated notification with the specified message.
    
    Creates and shows a new notification widget with the given message.
    The notification will automatically animate in and disappear after 2 seconds.
    
    Args:
        parent: Parent widget for the notification (optional)
        message (str): Message text to display
        
    Returns:
        Notification: The created notification widget instance
    """
    notification = Notification(parent, message)
    notification.show()
    return notification


def msg(text: str, status: str):
    """
    Display a modal message dialog based on the specified status.
    
    Shows different types of message boxes (critical, warning, information)
    based on the status code provided.
    
    Args:
        text (str): Message text to display
        status (str): Status code determining dialog type
                     'C' = Critical error dialog
                     'W' = Warning dialog  
                     'I' = Information dialog
    """
    if status == "C":
        QtWidgets.QMessageBox.critical(None, "خطای نرم افزار راوا", text)
    elif status == "W":
        QtWidgets.QMessageBox.warning(None, "هشدار نرم افزار راوا", text)
    elif status == "I":
        QtWidgets.QMessageBox.information(None, "پیام نرم افزار راوا", text)


# =============================================================================
# MODULE PROTECTION
# =============================================================================

if __name__ == "__main__":
    raise RavaAppError("Please don't run this file directly. Run main.py instead.")
