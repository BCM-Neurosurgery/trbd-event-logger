"""
Dialog classes for TRBD Event Logger
Contains ConfigSelectionDialog, StartupDialog and MissingEventDialog
"""

from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTimeEdit,
    QLineEdit,
    QMessageBox,
)
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QFont

from constants import DEFAULT_FONT_FAMILY
from styles import (
    DIALOG_BACKGROUND_STYLE,
    STARTUP_TITLE_STYLE,
    DIALOG_SUBTITLE_STYLE,
    STARTUP_RECORD_BUTTON_STYLE,
    STARTUP_SKIP_BUTTON_STYLE,
    DIALOG_TITLE_STYLE,
    CONFIG_SELECTION_COMBOBOX_STYLE,
    MISSING_EVENT_COMBOBOX_STYLE,
    MISSING_EVENT_TIMEEDIT_STYLE,
    MISSING_EVENT_LINEEDIT_STYLE,
    MISSING_EVENT_SUBMIT_BUTTON_STYLE,
    MISSING_EVENT_CANCEL_BUTTON_STYLE,
    MESSAGE_BOX_WARNING_STYLE,
    MESSAGE_BOX_SUCCESS_STYLE,
)


class ConfigSelectionDialog(QDialog):
    """Dialog for selecting configuration profile (Jamail or NBU)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_config = "NBU"  # Default
        self.init_ui()

    def init_ui(self):
        """Initialize the configuration selection dialog UI"""
        self.setWindowTitle("Event Logger - Configuration")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)

        layout = QVBoxLayout(self)
        layout.setSpacing(25)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel("⚙️ Select Configuration")
        title_label.setFont(QFont(DEFAULT_FONT_FAMILY, 22, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(STARTUP_TITLE_STYLE)
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Choose your deployment environment:")
        subtitle_label.setFont(QFont(DEFAULT_FONT_FAMILY, 13))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet(DIALOG_SUBTITLE_STYLE + " padding: 10px;")
        layout.addWidget(subtitle_label)

        # Configuration dropdown
        config_label = QLabel("🖥️ Environment:")
        config_label.setFont(QFont(DEFAULT_FONT_FAMILY, 12, QFont.Weight.DemiBold))
        config_label.setStyleSheet(DIALOG_SUBTITLE_STYLE)
        layout.addWidget(config_label)

        self.config_combo = QComboBox()
        self.config_combo.addItems(["NBU", "Jamail"])
        self.config_combo.setFont(QFont(DEFAULT_FONT_FAMILY, 12))
        self.config_combo.setStyleSheet(CONFIG_SELECTION_COMBOBOX_STYLE)
        self.config_combo.setCurrentIndex(0)  # Default to NBU
        layout.addWidget(self.config_combo)

        # Info label
        info_label = QLabel(
            "1. NBU \n"
            "2. Jamail"
        )
        info_label.setFont(QFont(DEFAULT_FONT_FAMILY, 10))
        info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_label.setStyleSheet("QLabel { color: #7f8c8d; padding: 10px; }")
        layout.addWidget(info_label)

        # Spacer
        layout.addStretch()

        # Continue button
        continue_button = QPushButton("✅ Continue")
        continue_button.setFont(QFont(DEFAULT_FONT_FAMILY, 13, QFont.Weight.Bold))
        continue_button.setMinimumHeight(60)
        continue_button.setStyleSheet(STARTUP_RECORD_BUTTON_STYLE)
        continue_button.clicked.connect(self.on_continue)
        layout.addWidget(continue_button)

        # Apply general styling
        self.setStyleSheet(DIALOG_BACKGROUND_STYLE)

    def on_continue(self):
        """Handle continue button click"""
        selected_text = self.config_combo.currentText()
        if "Jamail" in selected_text:
            self.selected_config = "Jamail"
        else:
            self.selected_config = "NBU"
        self.accept()


class StartupDialog(QDialog):
    """Startup dialog for session initialization"""
    
    def __init__(self, parent=None, app_name="Event Logger"):
        super().__init__(parent)
        self.app_name = app_name
        self.record_start = False
        self.init_ui()

    def init_ui(self):
        """Initialize the startup dialog UI"""
        self.setWindowTitle(f"{self.app_name} - Session Start")
        self.setModal(True)
        self.setMinimumWidth(600)
        self.setMinimumHeight(350)

        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        layout.setContentsMargins(40, 40, 40, 40)

        # Title
        title_label = QLabel(f"🏥 Welcome to {self.app_name}")
        title_label.setFont(QFont(DEFAULT_FONT_FAMILY, 20, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(STARTUP_TITLE_STYLE)
        layout.addWidget(title_label)

        # Subtitle
        subtitle_label = QLabel("Do you want to record the session start time?")
        subtitle_label.setFont(QFont(DEFAULT_FONT_FAMILY, 14))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle_label.setStyleSheet(DIALOG_SUBTITLE_STYLE + " padding: 15px;")
        layout.addWidget(subtitle_label)

        # Spacer
        layout.addStretch()

        # Buttons layout
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(20)

        # Record Session Start button
        record_button = QPushButton("✅ Record Session Start")
        record_button.setFont(QFont(DEFAULT_FONT_FAMILY, 14, QFont.Weight.Bold))
        record_button.setMinimumHeight(70)
        record_button.setStyleSheet(STARTUP_RECORD_BUTTON_STYLE)
        record_button.clicked.connect(self.record_and_continue)
        buttons_layout.addWidget(record_button)

        # Skip button
        skip_button = QPushButton("⏭️ Skip")
        skip_button.setFont(QFont(DEFAULT_FONT_FAMILY, 14, QFont.Weight.Bold))
        skip_button.setMinimumHeight(70)
        skip_button.setStyleSheet(STARTUP_SKIP_BUTTON_STYLE)
        skip_button.clicked.connect(self.skip_and_continue)
        buttons_layout.addWidget(skip_button)

        layout.addLayout(buttons_layout)
        layout.addStretch()

        # Apply general styling
        self.setStyleSheet(DIALOG_BACKGROUND_STYLE)

    def record_and_continue(self):
        """Record session start and continue to main window"""
        self.record_start = True
        self.accept()

    def skip_and_continue(self):
        """Skip recording and continue to main window"""
        self.record_start = False
        self.accept()


class MissingEventDialog(QDialog):
    """Dialog for entering missing events retroactively"""
    
    def __init__(self, parent=None, submit_callback=None, event_options=None):
        super().__init__(parent)
        self.submit_callback = submit_callback
        self.event_options = event_options or []
        self.init_ui()

    def init_ui(self):
        """Initialize the missing event dialog UI"""
        self.setWindowTitle("⏰ Add Missing Event")
        self.setModal(True)
        self.setMinimumWidth(500)
        self.setStyleSheet(DIALOG_BACKGROUND_STYLE)

        layout = QVBoxLayout(self)
        layout.setSpacing(18)
        layout.setContentsMargins(25, 25, 25, 25)

        # Title
        title_label = QLabel("📋 Enter Missing Event Details")
        title_label.setFont(QFont(DEFAULT_FONT_FAMILY, 15, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet(DIALOG_TITLE_STYLE)
        layout.addWidget(title_label)

        # Event selection
        event_label = QLabel("📌 Select Event:")
        event_label.setFont(QFont(DEFAULT_FONT_FAMILY, 11, QFont.Weight.DemiBold))
        event_label.setStyleSheet(DIALOG_SUBTITLE_STYLE)
        layout.addWidget(event_label)

        self.event_combo = QComboBox()
        self.event_combo.addItems(self.event_options)
        self.event_combo.setFont(QFont(DEFAULT_FONT_FAMILY, 11))
        self.event_combo.setStyleSheet(MISSING_EVENT_COMBOBOX_STYLE)
        layout.addWidget(self.event_combo)

        # Start time
        start_label = QLabel("🕐 Start Time:")
        start_label.setFont(QFont(DEFAULT_FONT_FAMILY, 11, QFont.Weight.DemiBold))
        start_label.setStyleSheet(DIALOG_SUBTITLE_STYLE)
        layout.addWidget(start_label)

        self.start_time_edit = QTimeEdit()
        self.start_time_edit.setDisplayFormat("HH:mm:ss")
        self.start_time_edit.setTime(QTime.currentTime())
        self.start_time_edit.setFont(QFont(DEFAULT_FONT_FAMILY, 11))
        self.start_time_edit.setStyleSheet(MISSING_EVENT_TIMEEDIT_STYLE)
        layout.addWidget(self.start_time_edit)

        # End time
        end_label = QLabel("🕑 End Time:")
        end_label.setFont(QFont(DEFAULT_FONT_FAMILY, 11, QFont.Weight.DemiBold))
        end_label.setStyleSheet(DIALOG_SUBTITLE_STYLE)
        layout.addWidget(end_label)

        self.end_time_edit = QTimeEdit()
        self.end_time_edit.setDisplayFormat("HH:mm:ss")
        self.end_time_edit.setTime(QTime.currentTime())
        self.end_time_edit.setFont(QFont(DEFAULT_FONT_FAMILY, 11))
        self.end_time_edit.setStyleSheet(MISSING_EVENT_TIMEEDIT_STYLE)
        layout.addWidget(self.end_time_edit)

        # Optional notes
        notes_label = QLabel("📝 Optional Notes:")
        notes_label.setFont(QFont(DEFAULT_FONT_FAMILY, 11, QFont.Weight.DemiBold))
        notes_label.setStyleSheet(DIALOG_SUBTITLE_STYLE)
        layout.addWidget(notes_label)

        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Enter optional notes...")
        self.notes_input.setFont(QFont(DEFAULT_FONT_FAMILY, 11))
        self.notes_input.setStyleSheet(MISSING_EVENT_LINEEDIT_STYLE)
        layout.addWidget(self.notes_input)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)

        submit_button = QPushButton("✅ Submit")
        submit_button.setFont(QFont(DEFAULT_FONT_FAMILY, 12, QFont.Weight.Bold))
        submit_button.setStyleSheet(MISSING_EVENT_SUBMIT_BUTTON_STYLE)
        submit_button.clicked.connect(self.handle_submit)
        button_layout.addWidget(submit_button)

        cancel_button = QPushButton("❌ Cancel")
        cancel_button.setFont(QFont(DEFAULT_FONT_FAMILY, 12, QFont.Weight.Bold))
        cancel_button.setStyleSheet(MISSING_EVENT_CANCEL_BUTTON_STYLE)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        layout.addLayout(button_layout)

    def handle_submit(self):
        """Handle submit button click with validation"""
        # Get event name without emoji
        event_text = self.event_combo.currentText()
        event_name = event_text.split(" ", 1)[1] if " " in event_text else event_text
        
        start_qtime = self.start_time_edit.time()
        end_qtime = self.end_time_edit.time()
        user_notes = self.notes_input.text()

        # Validate that end time is after start time
        if end_qtime <= start_qtime:
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setWindowTitle("Invalid Time Range")
            msg_box.setText("End time must be after start time.")
            msg_box.setStyleSheet(MESSAGE_BOX_WARNING_STYLE)
            msg_box.exec()
            return

        # Call the submit callback if provided
        if self.submit_callback:
            success = self.submit_callback(event_name, start_qtime, end_qtime, user_notes)
            
            if success:
                # Show confirmation
                msg_box = QMessageBox(self)
                msg_box.setIcon(QMessageBox.Icon.Information)
                msg_box.setWindowTitle("Success")
                msg_box.setText(f"Missing event '{event_name}' has been logged successfully.")
                msg_box.setStyleSheet(MESSAGE_BOX_SUCCESS_STYLE)
                msg_box.exec()
                
                # Close dialog
                self.accept()

    def get_values(self):
        """Get the values from the dialog (alternative to callback)"""
        event_text = self.event_combo.currentText()
        event_name = event_text.split(" ", 1)[1] if " " in event_text else event_text
        
        return {
            'event_name': event_name,
            'start_time': self.start_time_edit.time(),
            'end_time': self.end_time_edit.time(),
            'notes': self.notes_input.text()
        }
