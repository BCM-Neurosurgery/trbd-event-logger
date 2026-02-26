"""
Styling constants and functions for TRBD Event Logger
Contains all QSS stylesheets and styling utilities
"""

# Main window stylesheet
MAIN_WINDOW_STYLE = """
    QMainWindow {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f8f9fa, stop:1 #e9ecef);
    }
    QPushButton {
        font-size: 13px;
        font-weight: 600;
        padding: 15px;
        border-radius: 12px;
        border: none;
        min-height: 25px;
    }
"""

# Project ID label style
PROJECT_ID_STYLE = """
    QLabel { 
        color: #2c3e50; 
        padding: 12px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #e8f4f8, stop:1 #d5e9f2);
        border-radius: 8px;
        border: 1px solid #b8d4e0;
    }
"""

# Status label style
STATUS_LABEL_STYLE = """
    QLabel {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #ffffff, stop:1 #f5f7fa);
        color: #34495e;
        border: 2px solid #d5dce3;
        border-radius: 12px;
        padding: 20px;
        min-height: 30px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
"""

# Event button styles
EVENT_BUTTON_NORMAL_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #4a90e2, stop:1 #357abd);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 18px;
        text-align: left;
        font-size: 13px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #5ca3f5, stop:1 #4a90e2);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #357abd, stop:1 #2868a8);
    }
"""

EVENT_BUTTON_ACTIVE_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2ecc71, stop:1 #27ae60) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 18px !important;
        text-align: left !important;
        font-size: 13px !important;
        font-weight: bold !important;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #58d68d, stop:1 #2ecc71) !important;
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #27ae60, stop:1 #229954) !important;
    }
"""

EVENT_BUTTON_DISABLED_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #bdc3c7, stop:1 #95a5a6);
        color: #7f8c8d;
        border: none;
        border-radius: 12px;
        padding: 18px;
    }
"""

# Control frame style
CONTROLS_FRAME_STYLE = """
    QFrame {
        background: white;
        border-radius: 15px;
        border: 1px solid #dfe4ea;
    }
"""

# Notes input style
NOTES_INPUT_STYLE = """
    QLineEdit {
        padding: 12px;
        border: 2px solid #e1e8ed;
        border-radius: 8px;
        font-size: 12px;
        background-color: #f8f9fa;
    }
    QLineEdit:focus {
        border-color: #4a90e2;
        background-color: white;
    }
"""

# Abort button style
ABORT_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #e74c3c, stop:1 #c0392b);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        padding: 15px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #ec7063, stop:1 #e74c3c);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #c0392b, stop:1 #a93226);
    }
"""

# Missing events button style
MISSING_EVENTS_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #4a90e2, stop:1 #357abd);
        color: white;
        border: none;
        border-radius: 10px;
        font-size: 13px;
        padding: 15px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #5ca3f5, stop:1 #4a90e2);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #357abd, stop:1 #2868a8);
    }
"""

# End session button style
END_SESSION_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #8e44ad, stop:1 #71368a);
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 15px;
        padding: 18px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #a569bd, stop:1 #8e44ad);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #71368a, stop:1 #5b2c6f);
    }
"""

# Dialog background style
DIALOG_BACKGROUND_STYLE = """
    QDialog {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #f8f9fa, stop:1 #e9ecef);
    }
"""

# Startup dialog button styles
STARTUP_RECORD_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2ecc71, stop:1 #27ae60);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 18px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #58d68d, stop:1 #2ecc71);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #27ae60, stop:1 #229954);
    }
"""

STARTUP_SKIP_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #bdc3c7, stop:1 #95a5a6);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 18px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #d5dbdb, stop:1 #bdc3c7);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #95a5a6, stop:1 #7f8c8d);
    }
"""

# Missing event dialog input styles
MISSING_EVENT_INPUT_STYLE = """
    padding: 10px;
    border: 2px solid #d5dce3;
    border-radius: 8px;
    background-color: white;
    color: #2c3e50;
"""

MISSING_EVENT_COMBOBOX_STYLE = f"""
    QComboBox {{
        {MISSING_EVENT_INPUT_STYLE}
    }}
    QComboBox:focus {{
        border-color: #4a90e2;
    }}
    QComboBox::drop-down {{
        border: none;
    }}
    QComboBox QAbstractItemView {{
        background-color: white;
        color: #2c3e50;
        selection-background-color: #4a90e2;
        selection-color: white;
    }}
"""

MISSING_EVENT_TIMEEDIT_STYLE = f"""
    QTimeEdit {{
        {MISSING_EVENT_INPUT_STYLE}
    }}
    QTimeEdit:focus {{
        border-color: #4a90e2;
    }}
"""

MISSING_EVENT_LINEEDIT_STYLE = f"""
    QLineEdit {{
        {MISSING_EVENT_INPUT_STYLE}
    }}
    QLineEdit:focus {{
        border-color: #4a90e2;
    }}
"""

# Missing event dialog button styles
MISSING_EVENT_SUBMIT_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2ecc71, stop:1 #27ae60);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #58d68d, stop:1 #2ecc71);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #27ae60, stop:1 #229954);
    }
"""

MISSING_EVENT_CANCEL_BUTTON_STYLE = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #bdc3c7, stop:1 #95a5a6);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
    }
    QPushButton:hover {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #d5dbdb, stop:1 #bdc3c7);
    }
    QPushButton:pressed {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #95a5a6, stop:1 #7f8c8d);
    }
"""

# Message box styles
def get_message_box_style(button_color="#4a90e2", button_hover="#5ca3f5"):
    """Generate message box stylesheet with custom button colors"""
    return f"""
        QMessageBox {{
            background-color: white;
        }}
        QMessageBox QLabel {{
            color: #2c3e50;
            font-size: 12px;
        }}
        QPushButton {{
            background-color: {button_color};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            min-width: 80px;
        }}
        QPushButton:hover {{
            background-color: {button_hover};
        }}
    """

# Predefined message box styles
MESSAGE_BOX_INFO_STYLE = get_message_box_style("#4a90e2", "#5ca3f5")
MESSAGE_BOX_SUCCESS_STYLE = get_message_box_style("#2ecc71", "#58d68d")
MESSAGE_BOX_WARNING_STYLE = get_message_box_style("#e74c3c", "#ec7063")
MESSAGE_BOX_QUESTION_STYLE = get_message_box_style("#4a90e2", "#5ca3f5")

# Dialog title styles
DIALOG_TITLE_STYLE = """
    QLabel {
        color: #2c3e50;
        padding: 12px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #e8f4f8, stop:1 #d5e9f2);
        border-radius: 8px;
    }
"""

DIALOG_SUBTITLE_STYLE = "QLabel { color: #34495e; }"

STARTUP_TITLE_STYLE = """
    QLabel { 
        color: #2c3e50; 
        padding: 15px;
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
            stop:0 #e8f4f8, stop:1 #d5e9f2);
        border-radius: 10px;
    }
"""
